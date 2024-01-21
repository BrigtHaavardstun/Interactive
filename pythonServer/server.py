from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


def _find_mean_array(ds):
    mean_array = [0]*len(ds[0])
    for i in range(0, len(ds[0])):
        curr_sum = 0
        for j in range(0, len(ds)):
            curr_sum += ds[j][i]
        mean_array[i] = curr_sum/len(ds)


TARGET_DIFF_VALUE = 50


def _evaluate(ds):
    diff = [0]*len(ds[0])
    for i in range(0, len(ds[0])):
        min_curr = min([ds[j][i] for j in range(0, len(ds))])
        max_curr = max([ds[j][i] for j in range(0, len(ds))])

        diff[i] = abs(max_curr - min_curr)

    diff_sum = sum(diff)
    small_error = 3
    return diff_sum <= (TARGET_DIFF_VALUE + small_error)


@app.route('/getCol', methods=['GET'])
def get_random():
    ds = request.args.get('dataSet')  # Get the 'ys' parameter value
    if ds is not None:
        ds = json.loads(ds)  # Parse 'ys' as JSON
        if _evaluate(ds):
            returnVal = jsonify(1), 200
        else:
            returnVal = jsonify(0), 200
        print(returnVal)
        return returnVal
    else:
        return "No 'ys' parameter provided.", 400  # Bad request


@app.route('/', methods=['GET'])
def get_ys():
    ys = request.args.get('ys')  # Get the 'ys' parameter value
    if ys is not None:
        ys = json.loads(ys)  # Parse 'ys' as JSON
        return jsonify(ys), 200  # Return 'ys' as a JSON response
    else:
        return "No 'ys' parameter provided.", 400  # Bad request


def get_cf_func(ds):
    print("Does orginal work?", _evaluate(ds))
    new_time_series = [[yVal for yVal in timeSeries] for timeSeries in ds]

    diff_per_time_steps = [0]*len(new_time_series[0])
    median = [0]*len(new_time_series[0])

    for timeStep in range(len(new_time_series[0])):  # for each timeStep
        minVal = float("inf")

        maxVal = float("-inf")
        for timeSeries in new_time_series:
            currYVal = timeSeries[timeStep]

            if currYVal < minVal:
                minVal = currYVal

            if currYVal > maxVal:
                maxVal = currYVal

        diff = abs(maxVal - minVal)
        diff_per_time_steps[timeStep] = diff
        median[timeStep] = (maxVal + minVal) / 2

    total_diff = sum(diff_per_time_steps)
    # How much we should move depending on the difference
    scale = TARGET_DIFF_VALUE / total_diff
    print("scale:", scale)
    print("median", median)

    updated_time_series = [[yVal for yVal in timeSeries]
                           for timeSeries in new_time_series]
    for idTStep in range(len(new_time_series[0])):  # for each timeStep
        currMedian = median[idTStep]
        for idTSeries, timeSeries in enumerate(new_time_series):
            currYVal = timeSeries[idTStep]
            distToMed = abs(currMedian-currYVal)
            moveFromMid = distToMed*scale
            if currYVal > currMedian:
                updated_time_series[idTSeries][idTStep] = currMedian + moveFromMid
            else:
                updated_time_series[idTSeries][idTStep] = currMedian - moveFromMid

    print("Worked?", _evaluate(updated_time_series))
    return updated_time_series


@app.route('/cf', methods=['GET'])
def get_cf():
    """
    we want to find a counterfactual of the index item to make it positive
    @return A counterfactual time series. For now we only change one time series
    """
    ds = request.args.get('dataSet')  # List of time series
    # index = request.get("index")
    if ds is None:  # or index is None:
        return "You have to provide a 'dataSet' parameter and a 'index' parameter.", 400
    else:
        ds = json.loads(ds)  # Parse 'ys' as JSON
        if _evaluate(ds):
            return jsonify(ds), 200

        cf = get_cf_func(ds)

        return jsonify(cf), 200


def test():
    ds = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
          [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
          [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]]
    print(list([round(val, 3) for val in row] for row in ds))
    new_ds = get_cf_func(ds)
    print(list([round(val, 3) for val in row] for row in new_ds))


if __name__ == '__main__':
    app.run(port=8765)  # Start the server
    # test()
