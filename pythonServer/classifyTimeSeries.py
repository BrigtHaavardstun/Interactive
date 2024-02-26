
from Blackbox_classifier_FCN.functionBased.Train_model import load_model
import numpy as np
import threading

# Thread-local storage for our TensorFlow model
model_ITALY = load_model("ItalyPowerDemand")
def get_model(dataset):
    global model_ITALY
    return model_ITALY
def _classify(ts,dataset):
    model = get_model(dataset)
    prediction = np.argmax(model.predict(ts.reshape(1,-1,1))) # TODO: REDO
    prediction = prediction.item()
    return prediction


