import tensorflow as tf
import numpy as np
from utils.load_data import load_dataset

def load_keras_model(dataset):
    print("Loading Keras model...")
    print("Dataset:", dataset)
    keras_model = tf.keras.models.load_model(f"KerasModels/models/{dataset}.keras")
    print("Loaded Keras")
    return keras_model


def model_classify(dataset, timeseries):
    model = load_keras_model(dataset)
    input_shape = model.input_shape[1:] # Get Shape
    reshaped_input = timeseries.reshape(input_shape)
    timeseries = np.array([reshaped_input]) # (batchsize=1,(inputshape))
    predictions = model.predict(timeseries)
    class_pred = np.argmax(predictions, axis=1)[0] # Extract batch index 0
    return class_pred

PREDICTIONS = {}
def model_batch_classify(dataset, batch_of_timeseries):
    if dataset not in PREDICTIONS:
        model = load_keras_model(dataset)
        input_shape = model.input_shape[1:]  # Get Shape
        batch_of_timeseries = [timeseries.reshape(input_shape) for timeseries in batch_of_timeseries]
        batch_of_timeseries = np.array(batch_of_timeseries)
        print("DATASET shape:", batch_of_timeseries.shape)
        predictions = model.predict(batch_of_timeseries)
        print("PREDSHAPE:",predictions.shape)
        print("P")
        class_pred = [np.argmax(prediction) for prediction in predictions]
        PREDICTIONS[dataset] = class_pred
    return PREDICTIONS[dataset]



def model_confidence(dataset, timeseries):
    model = load_keras_model(dataset)
    input_shape = model.input_shape[1:]  # Get Shape
    reshaped_input = timeseries.reshape(input_shape)
    timeseries = np.array([reshaped_input])  # (batchsize=1,(inputshape))
    print("Timeseries_reshaped:", timeseries)
    predictions = model.predict(timeseries)
    print("Predictions:", predictions)
    confidence = np.max(predictions)
    return confidence
