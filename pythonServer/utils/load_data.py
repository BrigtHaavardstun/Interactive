import numpy as np
from utils.dataConverter import from_org_to_display, DISPLAY_NUM_POINTS
import pandas as pd

from tslearn.datasets import UCR_UEA_datasets
from sklearn.preprocessing import LabelEncoder,StandardScaler, Normalizer, RobustScaler
from sklearn.model_selection import train_test_split


def convert_sep_files(file, sep):

    df = pd.read_csv(file, sep=sep, header=None)

    # Write the DataFrame to a CSV file with a custom separator (e.g., ':::')
    custom_separator = ','
    output_file = file[:-4] + ".csv"

    df.to_csv(output_file, sep=custom_separator, index=False, header=False)



def normalize_data(dataset_name):
    filepath_train = f"utils/datasets/{dataset_name}/{dataset_name}_TRAIN.csv"
    pd_data_train = pd.read_csv(filepath_train, sep=",", header=None)
    filepath_test = f"utils/datasets/{dataset_name}/{dataset_name}_TEST.csv"
    pd_data_test = pd.read_csv(filepath_test, sep=",", header=None)



    # Extract the first column (y_train)
    y_train = pd_data_train.iloc[:, 0]
    y_test = pd_data_test.iloc[:,0]

  
    # Extract values excluding the first column (x_train)
    x_train = pd_data_train.iloc[:, 1:].values  
    x_test = pd_data_test.iloc[:,1:].values

    # numpy arrays
    x_train = np.array(x_train)
    x_test = np.array(x_test)

    normalizer = RobustScaler()
    x_comb = np.concatenate([x_train,x_test])
    normalizer.fit(x_comb)
    x_train_fitted = normalizer.transform(x_train)
    x_train = x_train_fitted.reshape(x_train.shape)

    x_test_fitted = normalizer.transform(x_test)
    x_test = x_test_fitted.reshape(x_test.shape)
    #x_test = x_test.reshape((x_test_shape[0], x_test_shape[1], 1))


    y_train = np.array(y_train)
    y_test = np.array(y_test)
    le = LabelEncoder()
    le.fit(np.concatenate([y_train, y_test]))
    y_train = le.transform(y_train)
    y_test  = le.transform(y_test)


    #x_test = x_test.reshape((x_test_shape[0], x_test_shape[1]))
    #x_train = x_train.reshape((x_test_shape[0], x_test_shape[1]))
    with open(filepath_train, "w") as f:
        for y, row in zip(y_train, x_train):
            f.write(f"{y},{','.join([str(x) for x in row])}\n")

    with open(filepath_test, "w") as f:
        for y, row in zip(y_test, x_test):
            f.write(f"{y},{','.join([str(x) for x in row])}\n")
     

    #return x_train, y_train, x_test, y_test


def train_test_split_both(dataset_name):
    filepath_both = f"utils/datasets/{dataset_name}/{dataset_name}_BOTH.csv"
    pd_data_both = pd.read_csv(filepath_both, sep=",", header=None)



    # Extract the first column (y_train)
    y_both = pd_data_both.iloc[:, 0]
  
    # Extract values excluding the first column (x_train)
    x_both = pd_data_both.iloc[:, 1:].values  

    X_train, X_test, y_train, y_test = train_test_split(x_both,y_both)

    train_file = f"utils/datasets/{dataset_name}/{dataset_name}_TRAIN.csv"
    with open(train_file, "w") as f:
        for y, row in zip(y_train, X_train):
            f.write(f"{y},{','.join([str(x) for x in row])}\n")
    
    test_file = f"utils/datasets/{dataset_name}/{dataset_name}_TEST.csv"
    with open(test_file, "w") as f:
        for y, row in zip(y_train, X_test):
            f.write(f"{y},{','.join([str(x) for x in row])}\n")
        


    



def load_dataset(dataset_name):
    filepath_train = f"utils/datasets/{dataset_name}/{dataset_name}_TRAIN.csv"
    pd_data_train = pd.read_csv(filepath_train, sep=",", header=None)
    filepath_test = f"utils/datasets/{dataset_name}/{dataset_name}_TEST.csv"
    pd_data_test = pd.read_csv(filepath_test, sep=",", header=None)



    # Extract the first column (y_train)
    y_train = pd_data_train.iloc[:, 0]
    y_test = pd_data_test.iloc[:,0]

  
    # Extract values excluding the first column (x_train)
    x_train = pd_data_train.iloc[:, 1:].values  
    x_test = pd_data_test.iloc[:,1:].values

    # numpy arrays
    x_train = np.array(x_train)
    x_test = np.array(x_test)

    #normalizer = StandardScaler()
    #x_train = normalizer.fit_transform(x_train)
    x_train_shape = x_train.shape
    x_train = x_train.reshape((x_train_shape[0], x_train_shape[1], 1))
    #x_test = normalizer.transform(x_test)
    x_test_shape = x_test.shape
    x_test = x_test.reshape((x_test_shape[0], x_test_shape[1], 1))


    y_train = np.array(y_train)
    y_test = np.array(y_test)
    #le = LabelEncoder()
    #le.fit(np.concatenate([y_train, y_test]))
    #y_train = le.transform(y_train)
    #y_test  = le.transform(y_test)

     

    return x_train, y_train, x_test, y_test





DATA_DICT = {}
def load_dataset_UCR(dataset):
    global DATA_DICT
    if dataset not in DATA_DICT:
        X_train, y_train, X_test, y_test = UCR_UEA_datasets().load_dataset(dataset)
        #instace_shape = X_train[0].shape
        #X_train = [np.array(from_org_to_display(instance.flatten()),dtype=np.float32).reshape((DISPLAY_NUM_POINTS,instace_shape[1])) for instance in X_train]
        #X_test = [np.array(from_org_to_display(instance.flatten()),dtype=np.float32).reshape((DISPLAY_NUM_POINTS,instace_shape[1]))  for instance in X_test]
        #X_train = np.array(X_train)
        #X_test = np.array(X_test)
        DATA_DICT[dataset] = [X_train, y_train, X_test, y_test]
    return DATA_DICT[dataset]


if __name__ == "__main__":
    
    load_dataset("Chinatown")