
import tensorflow as tf
tf.get_logger().setLevel(40) # suppress deprecation messages
tf.compat.v1.disable_v2_behavior() # disable TF2 behaviour as alibi code still relies on TF1 constructs
from tensorflow.keras.utils import to_categorical
from tensorflow import keras

import numpy as np
import os



from Blackbox_classifier_FCN.functionBased.counterfactual_utils import label_encoder, ucr_data_loader
from Blackbox_classifier_FCN.functionBased.FCN_model import Classifier_FCN

def load_model(dataset):
    model = keras.models.load_model('Blackbox_classifier_FCN/' + str(dataset) + '_best_model.hdf5')
    return model
def train_model(dataset,epochs=500,verbose=True):
    X_train, y_train, X_test, y_test = ucr_data_loader(str(dataset))
    y_train, y_test = label_encoder(y_train, y_test)

    input_shape = X_train.shape[1:]
    nb_classes = len(np.unique(np.concatenate([y_train, y_test])))
    one_hot = to_categorical(y_train)
    dataset_name = str(dataset)

    fcn = Classifier_FCN(output_directory=os.getcwd(), input_shape=input_shape, nb_classes=nb_classes,
                         dataset_name=dataset_name, verbose=verbose,epochs=epochs)
    fcn.build_model(input_shape=input_shape, nb_classes=nb_classes)
    fcn.fit(X_train, to_categorical(y_train))
    fcn.predict(X_test)
