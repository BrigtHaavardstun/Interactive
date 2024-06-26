import random

from sklearn_extra.cluster import KMedoids
from tensorflow import keras
import numpy as np

from utils.load_data import load_dataset
import pandas as pd
import matplotlib.pyplot as plt

from Blackbox_classifier_FCN.LITE.predict import predict_lite


def showPlot(data):
    plt.style.use("classic")
    colors = [
        '#08F7FE',  # teal/cyan
        '#FE53BB',  # pink
        '#F5D300',  # yellow
        '#00ff41',  # matrix green
        '#FF0000',  # red
        '#0000FF',  # Blue
        '#00FF00',  # Green

    ]
    df = pd.DataFrame({key : value for key,value in data.items()})
    fig, ax = plt.subplots(figsize=(10,5))
    df.plot(marker='.', color=colors, ax=ax)
    # Redraw the data with low alpha and slighty increased linewidth:
    n_shades = 10
    diff_linewidth = 1.05
    alpha_value = 0.3 / n_shades
    for n in range(1, n_shades+1):
        df.plot(marker='.',
                linewidth=2+(diff_linewidth*n),
                alpha=alpha_value,
                legend=False,
                ax=ax,
                color=colors)

    ax.grid(color='#2A3459')
    plt.xlabel('Time', fontweight = 'bold', fontsize='large')
    plt.ylabel('Value', fontweight = 'bold', fontsize='large')
    #plt.savefig('../Images/Initial_Example_Neon.pdf')
    plt.show()

def load_model(dataset):
    model = keras.models.load_model('Blackbox_classifier_FCN/' + str(dataset) + '_best_model.hdf5')
    return model

def get_clusters(x_data):
    seed = 42
    kmedoids = KMedoids(n_clusters=3, random_state=seed)
    kmedoids.fit(x_data)
    return kmedoids.cluster_centers_

def get_index_in_train(cluster,x_data):
    for i,entry in enumerate(x_data):
        if np.array_equal(entry.flatten(), cluster.flatten()):
            return i
    raise Exception ("could find match for", cluster, "in x_data")

def generate_prototypes(dataset,cf_mode,displayPlot=True):
    seed = 42

    X_train, y_train, X_test, y_test = load_dataset(dataset)
    print(dataset)
    #print(X_train, y_train, X_test, y_test)
    X_joint = np.concatenate([X_train, X_test])
    y_pred = [np.argmax(predict_lite(dataset,x)) for x in X_joint]
    cz_x_joint = [X_joint[i].flatten() for i in range(len(X_joint)) if y_pred[i] == 0]  # Class zero x train
    co_x_joint = [X_joint[i].flatten() for i in range(len(X_joint)) if y_pred[i] == 1]  # Class one x train


    medoids_zero = get_clusters(cz_x_joint)
    medoids_one = get_clusters(co_x_joint)

    idx_cz = [get_index_in_train(mediod, X_joint) for mediod in medoids_zero]
    idx_co = [get_index_in_train(mediod, X_joint) for mediod in medoids_one]

    # Visual
    data_dict_zero = {"z_" + str(i): val.flatten() for i, val in enumerate(medoids_zero)}
    data_dict_one_dw = {"o_" + str(i): val.flatten() for i, val in enumerate(medoids_one)}

    if displayPlot:
        showPlot(data_dict_zero)
        showPlot(data_dict_one_dw)
    
    host = "158.42.185.235"
    port = "8766"

    url = f"http://{host}:{port}?domain=" + str(dataset) + f"&cf_mode={cf_mode}&mode=train" + "&instance="
    all_data = idx_cz + idx_co
    random.seed(seed)
    random.shuffle(all_data)
    for i, test_instance in enumerate(all_data):
        print(f"{i}:", url + str(test_instance))

    with open(f"prototypes/{dataset}_train_URLs.txt", "w") as f:
        for i, test_instance in enumerate(all_data):
            f.write(f"{i}:" + " " + url + str(test_instance)+"\n")


if __name__ == "__main__":
    datasets = ["ItalyPowerDemand", "Chinatown","Charging"]
    cf_modes = ["native", "artificial"]
    cf_mode = cf_modes[1]
    for dataset in datasets:
        generate_prototypes(dataset, cf_mode=cf_mode, displayPlot=True)


