from typing import Annotated, Union
import numpy as np
from fastapi import FastAPI, Query
from getConfidence import get_confidence
from classifyTimeSeries import _classify
from getTimeSeries import get_time_series
from generateCF import generate_native_cf
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Where do we accept calls from
origins = [
    "",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def convert_time_series_str_list_float(time_series:str) -> np.ndarray[float]:
    print("CONVERT STARTING...")
    if time_series is None:
        return np.array([], dtype=float)
    time_series = time_series.replace("[","").replace("]", "")
    time_series = time_series.split(",")
    time_series = [float(val) for val in time_series]
    time_series = np.array(time_series)
    print("CONVERT FINISHED!")
    return time_series


@app.get('/confidence')
async def confidence(time_series : str = Query(None, description=''), data_set : str = Query(None, description='')):
    print("CONFIDENCE RUNNING!!!")
    #if True:
    #    return 1
    if time_series == "[0,0]":
        return 0
    time_series = convert_time_series_str_list_float(time_series)
    model_confidence = get_confidence(time_series, data_set)
    return str(model_confidence)


@app.get('/getClass')
async def get_class(time_series : str = Query(None, description=''), data_set : str = Query(None, description='')):
    if time_series == "[0,0]":
        return 0
    time_series = convert_time_series_str_list_float(time_series)
    class_of_ts = _classify(time_series, data_set)
    return class_of_ts


@app.get('/getTS')
async def get_ts(data_set : str = Query(None, description='Name of domain'), index: int = Query(None, description='Index of entry in train data')):
    time_series =  get_time_series(data_set, index).flatten().tolist()
    return time_series


@app.get('/cf')
async def get_cf(time_series : str = Query(None, description=''), data_set : str = Query(None, description=''), cf_mode : str = Query(None, description="Mode of cf")):
    """
    we want to find a counterfactual of the index item to make it positive
    @return A counterfactual time series. For now we only change one time series
    """
    print("TimerSeries recived", time_series)
    #if True:
    #    print(type(time_series), time_series)
    #    return convert_time_series_str_list_float(time_series).flatten().tolist()
    if time_series == "[0,0]":
        return 0
    time_series = convert_time_series_str_list_float(time_series)
    print("TS:",time_series)
    if cf_mode is None:
        raise ValueError("CF_mode not supported. CF_mode:", cf_mode)
    if cf_mode == "non":
        return time_series
    if cf_mode == "native" or cf_mode.startswith("nat"):
        cf = generate_native_cf(time_series, data_set).flatten().tolist()
    elif cf_mode == "artificial" or cf_mode.startswith("art"):
        print("ERROR: Only native guide supported.!!!")
    else:
        raise ValueError("CF_mode not supported. CF_mode:", cf_mode)

    return cf


