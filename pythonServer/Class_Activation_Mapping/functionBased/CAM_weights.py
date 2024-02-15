### Training Weights

from Class_Activation_Mapping.functionBased.counterfactual_utils import label_encoder, ucr_data_loader
from tensorflow import keras
import numpy as np
def training_weights_cam(dataset, save_weights=True):
    X_train, y_train, X_test, y_test = ucr_data_loader(str(dataset))
    y_train, y_test = label_encoder(y_train, y_test)

    model = keras.models.load_model("Blackbox_classifier_FCN/"+str(dataset) + '_best_model.hdf5')

    w_k_c = model.layers[-1].get_weights()[0]

    new_input_layer = model.inputs
    # output is both the original as well as the before last layer
    new_output_layer = [model.layers[-3].output, model.layers[-1].output]

    new_feed_forward = keras.backend.function(new_input_layer, new_output_layer)

    weights = []
    for i, ts in enumerate(X_train):
        ts = ts.reshape(1, -1, 1)
        [conv_out, predicted] = new_feed_forward([ts])
        pred_label = np.argmax(predicted)

        cas = np.zeros(dtype=float, shape=(conv_out.shape[1]))
        for k, w in enumerate(w_k_c[:, pred_label]):
            cas += w * conv_out[0, :, k]
        weights.append(cas)
    weights = np.array(weights)

    if save_weights == True:
        np.save("Class_Activation_Mapping/"+str(dataset) + '_cam_train_weights.npy', weights)
        print("Saving:", str(dataset) + '_cam_train_weights.npy')

    return weights


def test_weights_cam(dataset, save_weights=True):
    X_train, y_train, X_test, y_test = ucr_data_loader(str(dataset))
    y_train, y_test = label_encoder(y_train, y_test)

    model = keras.models.load_model("Blackbox_classifier_FCN/"+str(dataset) + '_best_model.hdf5')

    w_k_c = model.layers[-1].get_weights()[0]

    new_input_layer = model.inputs
    # output is both the original as well as the before last layer
    new_output_layer = [model.layers[-3].output, model.layers[-1].output]

    new_feed_forward = keras.backend.function(new_input_layer, new_output_layer)

    weights = []
    for i, ts in enumerate(X_test):
        ts = ts.reshape(1, -1, 1)
        [conv_out, predicted] = new_feed_forward([ts])
        pred_label = np.argmax(predicted)

        cas = np.zeros(dtype=float, shape=(conv_out.shape[1]))
        for k, w in enumerate(w_k_c[:, pred_label]):
            cas += w * conv_out[0, :, k]
        weights.append(cas)
    weights = np.array(weights)

    if save_weights == True:
        np.save("Class_Activation_Mapping/"+str(dataset) + '_cam_test_weights.npy', weights)
        print("Saving:", str(dataset) + '_cam_test_weights.npy')

    return weights


