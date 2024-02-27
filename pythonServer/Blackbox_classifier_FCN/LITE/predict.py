from flask import Flask, request, Response
import numpy as np
import tflite_runtime.interpreter as tflite
from utils.load_data import load_dataset
from Blackbox_classifier_FCN.functionBased.Train_model import load_model

def predict_lite(data_set,instance):
    interpreter = tflite.Interpreter(model_path="Blackbox_classifier_FCN/LITE/ItalyPowerDemand.tflite")
    interpreter.allocate_tensors()

    # Get input and output tensors
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()



    #input_arr = np.array([1,2,3,4,5,6,7,8,9,10,11,12.0], dtype=np.float32).reshape(1,12,1)
    
    input_arr = instance
    input_arr = np.array(input_arr, dtype=np.float32)
    input_arr = input_arr.reshape([1, input_arr.shape[0], 1])

    interpreter.set_tensor(input_details[0]['index'], input_arr)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])

    class_pred = output_data
    return class_pred