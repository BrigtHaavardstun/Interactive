import numpy as np
from fastapi import FastAPI, Query, UploadFile, File
from getConfidence import get_confidence
from classifyTimeSeries import _classify
from getTimeSeries import get_time_series
from generateCF import generate_native_cf
from fastapi.middleware.cors import CORSMiddleware
import shutil


from typing import Any

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


def convert_time_series_str_list_float(time_series: str) -> np.ndarray[Any, np.dtype[np.float64]]:
    print("CONVERT STARTING...")
    if time_series is None:
        return np.array([], dtype=float)
    time_series = time_series.replace("[", "").replace("]", "")
    time_series_array = time_series.split(",")
    time_series_array = [float(val) for val in time_series_array]
    time_series_array = np.array(time_series_array)
    print("CONVERT FINISHED!")
    return time_series_array


# Security improvments. DO NOT MAKE A FILE BASED ON THE ENTERED NAME!!!
# instead make a map between model name and some basic numbering system.
@ app.post("/reciveDataset")
async def reciveData(file: UploadFile):
    with open(f"utils/csvData/{file.filename}", "wb") as f:
        contents = await file.read()  # read the file
        f.write(contents)

    return {"filename": file.filename}


@ app.post("/reciveModel")
async def reciveModel(file: UploadFile):
    print("FILE!!:", file.filename)
    with open(f"KerasModels/models/{file.filename}", "wb") as f:
        contents = await file.read()  # read the file
        f.write(contents)

    return {"filename": file.filename}


@ app.get('/confidence')
async def confidence(time_series: str = Query(None, description=''), data_set_name: str = Query(None, description=''), model_name: str = Query(None, description='')):
    print("Confidence", time_series)
    time_series_array = convert_time_series_str_list_float(time_series)
    print("Confidence2", time_series_array)
    model_confidence = get_confidence(time_series_array, model_name)
    return str(model_confidence)


@ app.get('/getClass')
async def get_class(time_series: str = Query(None, description=''), data_set_name: str = Query(None, description=''), model_name: str = Query(None, description='')):
    if time_series == "[0,0]":
        return 0
    time_series_array = convert_time_series_str_list_float(time_series)
    class_of_ts = _classify(model_name=model_name,
                            time_series=time_series_array)
    return class_of_ts


@ app.get('/getTS')
async def get_ts(data_set_name: str = Query(None, description='Name of domain'), model_name: str = Query(None, description=''), index: int = Query(None, description='Index of entry in train data')):
    time_series = get_time_series(data_set_name, index).flatten().tolist()
    return time_series


@ app.get('/cf')
async def get_cf(cf_mode: str = Query(None, description=''), time_series: str = Query(None, description=''), data_set_name: str = Query(None, description=''), model_name: str = Query(None, description='')):
    """
    we want to find a counterfactual of the index item to make it positive
    @return A counterfactual time series. For now we only change one time series
    """
    time_series_array = convert_time_series_str_list_float(time_series)
    # if cf_mode =="Nearest-Neighbour":
    cf = generate_native_cf(ts=time_series_array, data_set_name=data_set_name,
                            model_name=model_name).flatten().tolist()
    # else:
    #    cf = generate
    return cf


@ app.get("/")
async def welcome():
    return "Welcom home", 200
