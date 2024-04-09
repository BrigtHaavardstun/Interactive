
from Blackbox_classifier_FCN.LITE.predict import predict_lite
import numpy as np




def _classify(ts,dataset):
    prediction = np.argmax(predict_lite(dataset,ts)[0]) # TODO: REDO
    prediction = prediction.item()
    return prediction



    