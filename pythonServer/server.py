from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import numpy as np

from classifyTimeSeries import _classify
from generateCF import generate_cf,generate_native_cf
from getTimeSeries import get_time_series
from getConfidence import get_confidence
app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/confidence', methods=['GET'])
def confidence():
    try:
        time_series = request.args.get('time_series')  # Get the 'ys' parameter value
        data_set = request.args.get('data_set')
        time_series = json.loads(time_series)  # Parse 'ys' as JSON
        if len(time_series) <= 11:
            return jsonify("1"), 200
        time_series = [float(y) for y in time_series]
        time_series = np.array(time_series)
        


        model_confidence = get_confidence(time_series, data_set)
        return jsonify(model_confidence), 200
    except Exception as e:
        print("COFIDENCE EROOR",str(e))
        return jsonify(str(e)), 400


@app.route('/getClass', methods=['GET'])
def get_class():
    try:
        time_series = request.args.get('time_series')  # Get the 'ys' parameter value
        if time_series == "[0,0]":
            return "0", 200
        data_set = request.args.get('data_set')
        if time_series is not None:
            time_series = json.loads(time_series)  # Parse 'ys' as JSON
            if time_series == [0,0]:
                return "0"
            time_series = [float(y) for y in time_series]
            #time_series = from_display_to_org(time_series,data_set)
            time_series = np.array(time_series)

            if len(time_series) <= 10:
                return "Too few data", 400
            class_of_ts = str(_classify(time_series,data_set))
            return_val = jsonify(class_of_ts), 200
            return return_val

    except Exception as e:
        print("ERROR IN CLASS", "ON ts:",request.args.get('time_series'), str(e))
        return e, 400




@app.route('/getTS', methods=['GET'])
def get_ts():
    try:
        data_set = request.args.get('data_set')
        index = int(request.args.get('index'))
        time_series = get_time_series(data_set,index).flatten().tolist()
        #time_series = from_org_to_display(time_series)
        return jsonify(time_series), 200 # Convert from numpy to array
    except Exception as e:
        return jsonify({'error': e}), 400




@app.route('/cf', methods=['GET'])
def get_cf():
    """
    we want to find a counterfactual of the index item to make it positive
    @return A counterfactual time series. For now we only change one time series
    """

    try:
        ts = request.args.get('time_series')  # List of time series
        ts_org = request.args.get('time_series')  # List of time series

        data_set = request.args.get('data_set')

        cf_mode = request.args.get('cf_mode')

        ts = json.loads(ts)

        if ts == [0,0]:
            return ts
        #ts = from_display_to_org(ts, data_set)
        ts = np.asarray(ts)





        if ts is None:  # or index is None:
            return "You have to provide a 'data_set' parameter and a 'index' parameter.", 400
        else:
            if cf_mode == "native" or cf_mode.startswith("nat"):
                cf = generate_native_cf(ts,data_set).flatten().tolist()
            elif cf_mode == "artificial" or cf_mode.startswith("art"):
                cf = generate_cf(ts, data_set).flatten().tolist()

            else:
                print(f"Invalid CF mode wrong cf mode {cf_mode}")
                return f"Invalid CF mode {cf_mode}",444
            return jsonify(cf), 200

    except Exception as e:
        print("We got an error", e)
        return "Something  went wrong", 444



if __name__ == '__main__':
    app.run(host="158.42.185.235",port=8765)  # Start the server
    # test()
