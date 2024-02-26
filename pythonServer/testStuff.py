from flask import Flask, request, Response
import numpy as np
import tflite_runtime.interpreter as tflite
from utils.load_data import load_dataset
from Blackbox_classifier_FCN.functionBased.Train_model import load_model

def test_pred_new(data_set,instance):
    #app = Flask(__name__)
    interpreter = tflite.Interpreter(model_path="Blackbox_classifier_FCN/LITE/ItalyPowerDemand.tflite")
    interpreter.allocate_tensors()

    # Get input and output tensors
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # print(input_details)
    # print(output_details)



    #input_arr = np.array([1,2,3,4,5,6,7,8,9,10,11,12.0], dtype=np.float32).reshape(1,12,1)
    input_arr = instance
    input_arr = input_arr.reshape(1,12,1)


    interpreter.set_tensor(input_details[0]['index'], input_arr)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])

    class_pred = output_data
    return class_pred
    


def org_way(data_set, instance):
    model = load_model(data_set)
    preds = model.predict(instance.reshape(1,12,1))
    return preds
   

def test():
    data_set = "ItalyPowerDemand"
    x_train,y_train, x_test, y_train = load_dataset(data_set)
    x_instance = x_train[0]
    import time
    start_time = time.time()
    preds_org = org_way(data_set, x_instance)
    end_time = time.time()
    print("--- %s seconds ---" % (end_time - start_time))
    start_time = time.time()
    preds_new = test_pred_new(data_set, x_instance)
    end_time = time.time()
    print("--- %s seconds ---" % (end_time - start_time))
    print("ORG pred:", preds_org)
    print("NEW pred:", preds_new)


if __name__ == "__main__":
    test()