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

def get_clusters(x_train):
    seed = 42
    kmedoids = KMedoids(n_clusters=3, random_state=seed)
    kmedoids.fit(x_train)
    return kmedoids.cluster_centers_

def get_index_in_train(cluster,x_train):
    for i,entry in enumerate(x_train):
        if np.array_equal(entry.flatten(), cluster.flatten()):
            return i
    raise Exception ("could find match for", cluster, "in x_train")

def generate_prototypes():
    dataset = "ItalyPowerDemand"
    seed = 42

    X_train, X_test, y_train, y_test = UCR_UEA_datasets().load_dataset(dataset)
    ai_model = load_model(dataset)
    y_pred = ai_model.predict(X_train)
    y_pred = [np.argmax(y) for y in y_pred]
    print(y_pred)
    cz_x_train = [X_train[i].flatten() for i in range(len(X_train)) if y_pred[i] == 0]  # Class zero x train
    co_x_train = [X_train[i].flatten() for i in range(len(X_train)) if y_pred[i] == 1]  # Class one x train


    medoids_zero = get_clusters(cz_x_train)
    medoids_one = get_clusters(co_x_train)

    idx_cz = [get_index_in_train(mediod, X_train) for mediod in medoids_zero]
    print("prototypes zero",idx_cz)
    idx_co = [get_index_in_train(mediod, X_train) for mediod in medoids_one]
    print("prototypes one", idx_co)


    # Visual


    data_dict_zero = {"z_" + str(i): val.flatten() for i, val in enumerate(medoids_zero)}
    data_dict_one_dw = {"o_" + str(i): val.flatten() for i, val in enumerate(medoids_one)}

    showPlot(data_dict_zero)
    showPlot(data_dict_one_dw)


if __name__ == "__main__":
    generate_prototypes()


