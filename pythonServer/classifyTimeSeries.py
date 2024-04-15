
#from Blackbox_classifier_FCN.LITE.predict import predict_lite
from KerasModels.load_keras_model import model_classify
import numpy as np




#def _classify_old(ts,dataset):
#    prediction = np.argmax(predict_lite(dataset,ts)[0]) # TODO: REDO
#    prediction = prediction.item()
#    return prediction


def _classify(model_name, time_series):
    class_pred = model_classify(model_name=model_name,time_series=time_series)
    return int(class_pred)

    