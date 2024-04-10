from tslearn.neighbors import KNeighborsTimeSeries
from KerasModels.load_keras_model import model_classify, model_batch_classify
import tensorflow as tf
from sklearn import preprocessing
from utils.load_data import load_dataset
import numpy as np
import pandas as pd
def label_encoder(training_labels, testing_labels):
    le = preprocessing.LabelEncoder()
    le.fit(np.concatenate((training_labels, testing_labels), axis=0))
    y_train = le.transform(training_labels)
    y_test = le.transform(testing_labels)
    return y_train, y_test

def native_guide_retrieval(query, predicted_label, distance, n_neighbors,data_set):
    X_train, y_train, X_test, y_test = load_dataset(data_set)
    y_train, y_test = label_encoder(y_train, y_test)
    print("THIS TAKES TIME...")
    y_pred = model_batch_classify(data_set, X_train)
    #y_pred = [model_classify(data_set,X_train[idx]) for idx in range(len(X_train))]
    print("OH BOI IT DOES...")
    print("unique?", np.unique(y_pred))

    df = pd.DataFrame(y_pred, columns=['label'])
    df.index.name = 'index'
    #df[df['label'] == 1].index.values, df[df['label'] != 1].index.values

    ts_length = X_train.shape[1]

    knn = KNeighborsTimeSeries(n_neighbors=n_neighbors, metric=distance)

    knn.fit(X_train[list(df[df['label'] != predicted_label].index.values)])

    dist, ind = knn.kneighbors(query.reshape(1, ts_length), return_distance=True)
    print(df[df['label'] != predicted_label].index[ind[0][:]])
    return df[df['label'] != predicted_label].index[ind[0][:]]

def find_native_cf(instance,data_set):
    # Get label
    pred_label = model_classify(data_set,instance)

    # Get NUN of instance
    nun_idx = native_guide_retrieval(instance, pred_label, 'euclidean', 1, data_set)[0]
    X_train, y_train, X_test, y_test = load_dataset(data_set)

    nun_cf =  X_train[nun_idx]
    nun_cf = [val[0] for val in nun_cf]
    nun_cf = np.asarray(nun_cf)
    return nun_cf