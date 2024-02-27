#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tensorflow as tf

import numpy as np
from tslearn.neighbors import KNeighborsTimeSeries
from utils.load_data import load_dataset
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
print('TF version: ', tf.__version__)
print('Eager execution enabled counterfact utils: ', tf.executing_eagerly()) # False


# In[2]:


from tensorflow import keras
import time


# In[3]:





# In[4]:


def label_encoder(training_labels, testing_labels):
    print(training_labels, testing_labels)
    le = preprocessing.LabelEncoder()
    le.fit(np.concatenate((training_labels, testing_labels), axis=0))
    y_train = le.transform(training_labels)
    y_test = le.transform(testing_labels)
    
    return y_train, y_test


def native_guide_retrieval(query, predicted_label, distance, n_neighbors,X_train,df,ts_length):
    knn = KNeighborsTimeSeries(n_neighbors=n_neighbors, metric = distance)
    knn.fit(X_train[list(df[df['label'] != predicted_label].index.values)])
    dist,ind = knn.kneighbors(query.reshape(1,ts_length), return_distance=True)
    return dist[0], df[df['label'] != predicted_label].index[ind[0][:]]
    
    

