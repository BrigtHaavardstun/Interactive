from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random

from classifyTimeSeries import _classify
from generateCF import generate_cf
app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/getClass', methods=['GET'])
def get_class():
    ds = request.args.get('dataSet')  # Get the 'ys' parameter value
    if ds is not None:
        ds = json.loads(ds)  # Parse 'ys' as JSON
        ds = [float(y) for y in ds]
        try:
            return_val = jsonify(_classify(ds)), 200
        except Exception as e:
            return_val = e, 400

        return return_val
    else:
        return "No 'ys' parameter provided.", 400  # Bad request


@app.route('/getTS', methods=['GET'])
def get_ys():
    max_val = 100
    min_val = -100
    length = 10
    try:
        time_series = [random.randint(min_val, max_val) for _ in range(length)]
        return jsonify(time_series), 200  # Return 'ys' as a JSON response
    except Exception as e:
        return jsonify({'error': e}), 400




@app.route('/cf', methods=['GET'])
def get_cf():
    """
    we want to find a counterfactual of the index item to make it positive
    @return A counterfactual time series. For now we only change one time series
    """
    try:
        ds = request.args.get('dataSet')  # List of time series
        ds = json.loads(ds)

        target = request.args.get('targetClass')
        target = json.loads(target)



        if ds is None:  # or index is None:
            return "You have to provide a 'dataSet' parameter and a 'index' parameter.", 400
        else:
            if _classify(ds)==target:
                print("Target IS same")
                return jsonify(ds), 200

            cf = generate_cf(ds)

            return jsonify(cf), 200

    except Exception as e:
        print("We got an error", e)
        return "Something  went wrong", 500



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
