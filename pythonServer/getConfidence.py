from Blackbox_classifier_FCN.functionBased.Train_model import load_model
import numpy as np


def get_confidence(ts,dataset):
    model = load_model(dataset)
    confidence = np.max(model.predict(ts.reshape(1, -1, 1)))
    return confidence

