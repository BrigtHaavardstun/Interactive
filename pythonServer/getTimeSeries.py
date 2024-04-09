
import numpy as np
from utils.load_data import load_dataset

def get_time_series(dataset,id):
    X_train, y_train, X_test, y_test = load_dataset(dataset)
    con_X = np.concatenate([X_train, X_test])
    return con_X[id]

