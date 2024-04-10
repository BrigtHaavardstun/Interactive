#from Blackbox_classifier_FCN.LITE.predict import predict_lite
from KerasModels.load_keras_model import model_confidence
from utils.common import get_domains
import numpy as np
import tensorflow as tf
from keras import backend as K

import threading

# Thread-local storage for our TensorFlow model
#mode_ITALY = load_model("ItalyPowerDemand")


def get_confidence(time_series:np.ndarray, data_set:str) -> float:
    print("Dataset:",data_set, "Time_sereies:", time_series)
    confidence = None
    try:
        print("MODEL CONFIDENC!!")
        confidence = model_confidence(data_set, time_series)
        print("CONFS:", confidence)
        print("MODEL CONFIDENC DONE!")

    except Exception as e:
        print(e)
        print("Error!!!!")

    print("Confidence complited")
    print("CoNFS return", confidence)
    return confidence

