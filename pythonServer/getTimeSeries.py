
from tslearn.datasets import UCR_UEA_datasets
import numpy as np
def ucr_data_loader(dataset):
    X_train, y_train, X_test, y_test = UCR_UEA_datasets().load_dataset(dataset)

    return X_train, y_train, X_test, y_test

def get_time_series(dataset,id):
    X_train, y_train, X_test, y_test = ucr_data_loader(dataset)
    con_X = np.concatenate([X_train, X_test])
    return con_X[id]


