from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/random', methods=['GET'])
def get_random():
    ds = request.args.get('dataSet')  # Get the 'ys' parameter value
    if ds is not None:
        ds = json.loads(ds)  # Parse 'ys' as JSON
        print(ds)
        diff = 0
        for d1, d2 in zip(ds[0], ds[1]):
            diff += abs(d1-d2)
        print(diff)
        if diff <= 50:
            returnVal = jsonify(1), 200
        else:
            returnVal = jsonify(0), 200
        print(returnVal)
        return returnVal
        # return jsonify(ys), 200  # Return 'ys' as a JSON response
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


if __name__ == '__main__':
    app.run(port=8765)  # Start the server
