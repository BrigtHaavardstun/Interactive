import json
from tqdm import tqdm
import numpy as np
from tslearn.datasets import UCR_UEA_datasets
def searchForBest():
    datasets = UCR_UEA_datasets().list_datasets()

    all_data = {}
    for dataset in tqdm(datasets):
        print(dataset)
        if dataset in ["EigenWorms","AtrialFibrillation","CharacterTrajectories","DuckDuckGeese"]:
            break
        X_train, y_train, X_test, y_test = UCR_UEA_datasets().load_dataset(dataset)


        time_series_length = len(X_train[0].flatten())
        classes = len(set(np.concatenate(([y_test, y_train]))))
        all_data[dataset] = {"length": time_series_length, "classes": classes}

    keys = list(all_data.keys())
    keys =  sorted(keys, key=lambda key: all_data[key]["classes"])

    keys = sorted(keys, key=lambda key: all_data[key]["length"])
    print(keys[:5])

    with open("bestUCR.json", "w") as outfile:
        outfile.write(json.dumps(all_data,indent=2))



if __name__ == "__main__":
    searchForBest()




