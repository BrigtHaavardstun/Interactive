import numpy as np
from fastapi import FastAPI, Query, UploadFile, File
from classifyTimeSeries import _classify
from getTimeSeries import get_time_series
from fastapi.middleware.cors import CORSMiddleware
from getConfidence import get_confidence
from simplification import get_simplification as simplify
from generateCF import generate_native_cf, generate_subseq_cf
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
    if time_series is None:
        return np.array([], dtype=float)
    time_series = time_series.replace("[", "").replace("]", "")
    time_series_array = time_series.split(",")
    time_series_array = [float(val) for val in time_series_array]
    time_series_array = np.array(time_series_array)
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
    with open(f"KerasModels/models/{file.filename}", "wb") as f:
        contents = await file.read()  # read the file
        f.write(contents)

    return {"filename": file.filename}

@ app.get('/simplification')
async def get_simplification(simp_algo: str, time_series: str, alpha: float):
    if alpha < 0:
        time_series_array = convert_time_series_str_list_float(time_series)
        return time_series_array
    """
    we want to find a counterfactual of the index item to make it positive
    @return A counterfactual time series. For now we only change one time series
    """
    time_series_array = convert_time_series_str_list_float(time_series)

    if simp_algo == "RDP":
        time_series_array = simplify(time_series_array,alpha=alpha)
    return time_series_array

@ app.get('/confidence')
async def confidence(time_series: str = Query(None, description=''), data_set_name: str = Query(None, description=''), model_name: str = Query(None, description='')):
    time_series_array = convert_time_series_str_list_float(time_series)
    model_confidence = get_confidence(time_series_array, model_name)
    return str(model_confidence)

@ app.get('/getClass')
async def get_class(time_series: str = Query(None, description=''), model_name: str = Query(None, description='')):
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

@ app.get("/")
async def welcome():
    return "Welcom home", 200
