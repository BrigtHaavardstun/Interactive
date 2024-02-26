from Blackbox_classifier_FCN.functionBased.Train_model import load_model
from utils.common import get_domains
import numpy as np
import tensorflow as tf
from keras import backend as K

import threading

# Thread-local storage for our TensorFlow model
#mode_ITALY = load_model("ItalyPowerDemand")


def get_model(data_set):
    model = load_model(data_set)
    return model


def get_confidence(ts:np.ndarray, dataset:str) -> float:
    model = load_model(dataset)
    predictions = model.predict(ts.reshape(1, -1, 1))
    confidence = np.max(predictions[0])
    print("before_item")
    confidence = confidence.item()
    return confidence

