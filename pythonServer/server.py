from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import numpy as np

from classifyTimeSeries import _classify
from generateCF import generate_cf
from getTimeSeries import get_time_series
from getConfidence import get_confidence

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

dataSet = "GunPoint"


@app.route('/confidence', methods=['GET'])
def confidence():
    try:
        time_series = request.args.get('timeSeries')  # Get the 'ys' parameter value
        data_set = request.args.get('dataSet')

        time_series = json.loads(time_series)  # Parse 'ys' as JSON
        time_series = [float(y) for y in time_series]
        time_series = np.array(time_series)

        model_confidence = get_confidence(time_series, data_set)
        return jsonify(model_confidence.item()), 200
    except Exception as e:
        print("COFIDENCE EROOR",e)
        return jsonify(e), 400


@app.route('/getClass', methods=['GET'])
def get_class():

    timeSeries = request.args.get('timeSeries')  # Get the 'ys' parameter value
    dataSet = request.args.get('dataSet')
    if timeSeries is not None:
        timeSeries = json.loads(timeSeries)  # Parse 'ys' as JSON
        timeSeries = [float(y) for y in timeSeries]
        timeSeries = np.array(timeSeries)

        if len(timeSeries) <= 10:
            return "Too few data", 400
        try:
            class_of_ts = str(_classify(timeSeries,dataSet))
            print("Class:",class_of_ts)
            return_val = jsonify(class_of_ts), 200
            print("Classification:", return_val)
            return return_val

        except Exception as e:
            print(e)
            return e, 400

        return return_val
    else:
        return "No 'ys' parameter provided.", 400  # Bad request


@app.route('/getTS', methods=['GET'])
def get_ts():
    try:
        dataSet = request.args.get('dataSet')
        index = int(request.args.get('index'))
        time_series = get_time_series(dataSet,index)
        return jsonify(time_series.flatten().tolist()), 200 # Convert from numpy to array
    except Exception as e:
        return jsonify({'error': e}), 400




@app.route('/cf', methods=['GET'])
def get_cf():

    """
    we want to find a counterfactual of the index item to make it positive
    @return A counterfactual time series. For now we only change one time series
    """
    try:
        ts = request.args.get('timeSeries')  # List of time series
        dataSet = request.args.get('dataSet')
        ts = json.loads(ts)
        ts = np.asarray(ts)





        if ts is None:  # or index is None:
            return "You have to provide a 'dataSet' parameter and a 'index' parameter.", 400
        else:

            cf = generate_cf(ts,dataSet)
            return jsonify(cf.tolist()), 200

    except Exception as e:
        print("We got an error", e)
        return "Something  went wrong", 500



if __name__ == '__main__':
    app.run(port=8765)  # Start the server
    # test()
