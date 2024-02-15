
from Blackbox_classifier_FCN.functionBased.Train_model import load_model
import numpy as np

def _classify(ts,dataset):
    model = load_model(dataset)
    prediction = np.argmax(model.predict(ts.reshape(1,-1,1)))
    return prediction


