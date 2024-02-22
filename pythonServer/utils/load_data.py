import numpy as np
from tslearn.datasets import UCR_UEA_datasets
from utils.dataConverter import from_org_to_display, DISPLAY_NUM_POINTS
def load_dataset(dataset):
    X_train, y_train, X_test, y_test = UCR_UEA_datasets().load_dataset(dataset)
    print(X_train.shape)
    instace_shape = X_train[0].shape
    X_train_shape = X_train.shape
    X_test_shape = X_test.shape
    X_train = [np.asarray(from_org_to_display(instance.flatten())).reshape((DISPLAY_NUM_POINTS,instace_shape[1])) for instance in X_train]
    X_test = [np.asarray(from_org_to_display(instance.flatten())).reshape((DISPLAY_NUM_POINTS,instace_shape[1]))  for instance in X_test]
    X_train = np.asarray(X_train)
    print(X_train.shape)
    X_test = np.asarray(X_test)

    return X_train, y_train, X_test, y_test


if __name__ == "__main__":
    load_dataset("ItalyPowerDemand")