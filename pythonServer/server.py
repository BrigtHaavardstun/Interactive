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
        timeSeries = request.args.get('time_series')  # Get the 'ys' parameter value
        dataSet = request.args.get('data_set')
        if timeSeries is not None:
            timeSeries = json.loads(timeSeries)  # Parse 'ys' as JSON
            if timeSeries == [0,0]:
                return 0
            timeSeries = [float(y) for y in timeSeries]
            #timeSeries = from_display_to_org(timeSeries,dataSet)
            timeSeries = np.array(timeSeries)

            if len(timeSeries) <= 10:
                return "Too few data", 400
            class_of_ts = str(_classify(timeSeries,dataSet))
            print("Class:",class_of_ts)
            return_val = jsonify(class_of_ts), 200
            print("Classification:", return_val)
            return return_val

    except Exception as e:
        print(str(e))
        return e, 400




@app.route('/getTS', methods=['GET'])
def get_ts():
    try:
        dataSet = request.args.get('data_set')
        index = int(request.args.get('index'))
        time_series = get_time_series(dataSet,index).flatten().tolist()
        #time_series = from_org_to_display(time_series)
        print("TIME_SERIES_", time_series)
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

        dataSet = request.args.get('data_set')

        cf_mode = request.args.get('cf_mode')

        ts = json.loads(ts)
        if ts == [0,0]:
            return ts
        print("CF-TS pre:",ts,"ORG-TAG:",ts_org)
        #ts = from_display_to_org(ts, dataSet)
        print("CF-TS post:",ts,"ORG-TAG:",ts_org)
        ts = np.asarray(ts)





        if ts is None:  # or index is None:
            return "You have to provide a 'dataSet' parameter and a 'index' parameter.", 400
        else:
            if cf_mode == "native" or cf_mode.startswith("nat"):
                cf = generate_native_cf(ts,dataSet).tolist()
            elif cf_mode == "artificial" or cf_mode.startswith("art"):
                cf = generate_cf(ts, dataSet).tolist()

            else:
                print(f"Invalid CF mode wrong cf mode {cf_mode}")
                return f"Invalid CF mode {cf_mode}",500
            return jsonify(cf), 200

    except Exception as e:
        print("We got an error", e)
        return "Something  went wrong", 500



if __name__ == '__main__':
    app.run(port=8765)  # Start the server
    # test()
