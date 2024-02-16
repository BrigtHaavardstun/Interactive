from sklearn_extra.cluster import KMedoids
import numpy as np
from tslearn.datasets import UCR_UEA_datasets
from tensorflow import keras
import numpy as np

import pandas as pd
import matplotlib.pyplot as plt


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
    model = keras.models.load_model('../pythonServer/Blackbox_classifier_FCN/' + str(dataset) + '_best_model.hdf5')
    return model

def get_clusters(x_data):
    seed = 42
    kmedoids = KMedoids(n_clusters=2, random_state=seed)
    kmedoids.fit(x_data)
    return kmedoids.cluster_centers_

def get_index_in_train(cluster,x_data):
    for i,entry in enumerate(x_data):
        if np.array_equal(entry.flatten(), cluster.flatten()):
            return i
    raise Exception ("could find match for", cluster, "in x_data")

def generate_prototypes(dataset):
    seed = 42

    X_train, y_train, X_test, y_test = UCR_UEA_datasets().load_dataset(dataset)
    X_joint = np.concatenate([X_train, X_test])
    print("Lengths:",len(X_train), len(X_test), len(y_train), len(y_test))
    ai_model = load_model(dataset)
    y_pred = ai_model.predict(X_joint)
    y_pred = [np.argmax(y) for y in y_pred]
    print(y_pred)
    cz_x_joint = [X_joint[i].flatten() for i in range(len(X_joint)) if y_pred[i] == 0]  # Class zero x train
    co_x_joint = [X_joint[i].flatten() for i in range(len(X_joint)) if y_pred[i] == 1]  # Class one x train


    medoids_zero = get_clusters(cz_x_joint)
    medoids_one = get_clusters(co_x_joint)

    idx_cz = [get_index_in_train(mediod, X_joint) for mediod in medoids_zero]
    print("prototypes zero",idx_cz)
    idx_co = [get_index_in_train(mediod, X_joint) for mediod in medoids_one]
    print("prototypes one", idx_co)


    # Visual


    data_dict_zero = {"z_" + str(i): val.flatten() for i, val in enumerate(medoids_zero)}
    data_dict_one_dw = {"o_" + str(i): val.flatten() for i, val in enumerate(medoids_one)}

    showPlot(data_dict_zero)
    showPlot(data_dict_one_dw)


if __name__ == "__main__":
    datasets = ["GunPoint", "ItalyPowerDemand"]
    for dataset in datasets:
        generate_prototypes(dataset)


