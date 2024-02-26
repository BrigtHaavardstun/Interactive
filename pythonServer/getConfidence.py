from Blackbox_classifier_FCN.LITE.predict import predict_lite
from utils.common import get_domains
import numpy as np
import tensorflow as tf
from keras import backend as K

import threading

# Thread-local storage for our TensorFlow model
#mode_ITALY = load_model("ItalyPowerDemand")


def get_confidence(time_series:np.ndarray, data_set:str) -> float:
    predictions = predict_lite(data_set, time_series)
    confidence = np.max(predictions[0])
    confidence = confidence.item()
    return confidence

