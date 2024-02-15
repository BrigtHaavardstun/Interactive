
from tslearn.datasets import UCR_UEA_datasets

def ucr_data_loader(dataset):
    X_train, y_train, X_test, y_test = UCR_UEA_datasets().load_dataset(dataset)

    return X_train, y_train, X_test, y_test

def get_time_series(dataset,id):
    X_train, y_train, X_test, y_test = ucr_data_loader(dataset)
    return X_train[id]


