import numpy as np
from tslearn.datasets import UCR_UEA_datasets
from utils.dataConverter import from_org_to_display, DISPLAY_NUM_POINTS

DATA_DICT = {}
def load_dataset(dataset):
    global DATA_DICT
    if dataset not in DATA_DICT:
        X_train, y_train, X_test, y_test = UCR_UEA_datasets().load_dataset(dataset)
        instace_shape = X_train[0].shape
        X_train = [np.asarray(from_org_to_display(instance.flatten())).reshape((DISPLAY_NUM_POINTS,instace_shape[1])) for instance in X_train]
        X_test = [np.asarray(from_org_to_display(instance.flatten())).reshape((DISPLAY_NUM_POINTS,instace_shape[1]))  for instance in X_test]
        X_train = np.asarray(X_train)
        X_test = np.asarray(X_test)
        DATA_DICT[dataset] = [X_train, y_train, X_test, y_test]
    return DATA_DICT[dataset]


if __name__ == "__main__":
    load_dataset("ItalyPowerDemand")