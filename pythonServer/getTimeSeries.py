
import numpy as np
from utils.load_data import load_dataset as old_load_dataset
from utils.load_csv import load_dataset

def get_time_series(data_set_name,index):
    x = load_dataset(data_set_name)
    return x[index]

