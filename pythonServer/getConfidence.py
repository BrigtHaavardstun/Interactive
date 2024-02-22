from Blackbox_classifier_FCN.functionBased.Train_model import load_model
import numpy as np


def get_confidence(ts,dataset):
    model = load_model(dataset)
    predictions =model.predict(ts.reshape(1, -1, 1))
    confidence = np.max(predictions[0])


    return confidence

