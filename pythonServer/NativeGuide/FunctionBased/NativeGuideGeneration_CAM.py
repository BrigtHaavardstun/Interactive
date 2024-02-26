import numpy as np
import pandas as pd

from tslearn.neighbors import KNeighborsTimeSeries

import tensorflow as tf
from sklearn import preprocessing

from NativeGuide.FunctionBased.showPlot import showPlot
from Blackbox_classifier_FCN.functionBased.Train_model import load_model
from utils.load_data import load_dataset





def label_encoder(training_labels, testing_labels):
    le = preprocessing.LabelEncoder()
    le.fit(np.concatenate((training_labels, testing_labels), axis=0))
    y_train = le.transform(training_labels)
    y_test = le.transform(testing_labels)
    return y_train, y_test


def native_guide_retrieval(query, predicted_label, distance, n_neighbors,dataset):
    X_train, y_train, X_test, y_test = load_dataset(dataset)
    y_train, y_test = label_encoder(y_train, y_test)
    df = pd.DataFrame(y_train, columns=['label'])
    df.index.name = 'index'
    #df[df['label'] == 1].index.values, df[df['label'] != 1].index.values

    ts_length = X_train.shape[1]

    knn = KNeighborsTimeSeries(n_neighbors=n_neighbors, metric=distance)

    knn.fit(X_train[list(df[df['label'] != predicted_label].index.values)])

    dist, ind = knn.kneighbors(query.reshape(1, ts_length), return_distance=True)
    return dist[0], df[df['label'] != predicted_label].index[ind[0][:]]


def findSubarray(a, k):  # used to find the maximum contigious subarray of length k in the explanation weight vector

    n = len(a)

    vec = []

    # Iterate to find all the sub-arrays
    for i in range(n - k + 1):
        temp = []

        # Store the sub-array elements in the array
        for j in range(i, i + k):
            temp.append(a[j])

            # Push the vector in the container
        vec.append(temp)

    sum_arr = []
    for v in vec:
        sum_arr.append(np.sum(v))

    return (vec[np.argmax(sum_arr)])


def load_weights(dataset):
    training_weights = np.load('Class_Activation_Mapping/' + str(dataset) + '_cam_train_weights.npy')
    test_weights = np.load('Class_Activation_Mapping/' + str(dataset) + '_cam_test_weights.npy')
    joint_weights = np.load('Class_Activation_Mapping/' + str(dataset) + '_cam_joint_weights.npy')

    return training_weights,test_weights,joint_weights





def counterfactual_generator_swap(instance, nun_idx, subarray_length,dataset):
    X_train, y_train, X_test, y_test = load_dataset(dataset)
    y_train,y_test = label_encoder(y_train,y_test)
    _, _, joint_weights = load_weights(dataset)

    model = get_model(dataset)

    model_preds = model.predict(X_train[nun_idx].reshape(1, -1, 1))[0]
    y_target = np.argmax(model_preds)
    prob_max = model_preds[y_target]/sum(model_preds)


    most_influencial_array = findSubarray((joint_weights[nun_idx]), subarray_length)

    starting_point = np.where(joint_weights[nun_idx] == most_influencial_array[0])[0][0]

    X_example = np.concatenate((instance.flatten()[:starting_point],
                                (X_train[nun_idx].flatten()[starting_point:subarray_length + starting_point]),
                                instance.flatten()[subarray_length + starting_point:]))

    prob_target = model.predict(X_example.reshape(1, -1, 1))[0][y_target]

    prob_goal = 0.51 # How far over the line do we want to go?
    while prob_target < min(prob_goal,prob_max):

        subarray_length += 1
        if subarray_length == len(X_example):
            break

        most_influencial_array = findSubarray((joint_weights[nun_idx]), subarray_length)
        starting_point = np.where(joint_weights[nun_idx] == most_influencial_array[0])[0][0]
        X_example = np.concatenate((instance.flatten()[:starting_point],
                                    (X_train[nun_idx].flatten()[starting_point:subarray_length + starting_point]),
                                    instance.flatten()[subarray_length + starting_point:]))
        prob_target = model.predict(X_example.reshape(1, -1, 1))[0][y_target]

    return X_example


def get_model(data_set):
    model = load_model(data_set)
    return model

def find_cf(instance,dataset):
    # Get label
    model = get_model(dataset)
    pred_label = np.argmax(model.predict(instance))

    # Get NUN of instance
    nun_idx = native_guide_retrieval(instance, pred_label,'euclidean',1,dataset)[1][0]

    cf = counterfactual_generator_swap(instance, nun_idx,1,dataset)
    return cf





def find_native_cf(instance,dataset):
    # Get label
    model = get_model(dataset)
    pred_label = np.argmax(model.predict(instance))

    # Get NUN of instance
    nun_idx = native_guide_retrieval(instance, pred_label, 'euclidean', 1, dataset)[1][0]
    X_train, y_train, X_test, y_test = load_dataset(dataset)
    nun_cf =  X_train[nun_idx]
    nun_cf = [val[0] for val in nun_cf]
    nun_cf = np.asarray(nun_cf)
    return nun_cf


def test():
    dataset =  "ItalyPowerDemand"
    X_train, X_test, y_train, y_test = load_dataset(dataset)
    random_instance = X_train[19]
    random_instance = random_instance.reshape(1,-1,1)
    cf = find_cf(random_instance,dataset)
    showPlot(random_instance,cf)

    return cf


