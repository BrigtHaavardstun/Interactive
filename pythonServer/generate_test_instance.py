import json

import numpy as np
from tslearn.datasets import UCR_UEA_datasets
from tensorflow import keras
import random
from utils.load_data import load_dataset


def load_model(dataset):
    model = keras.models.load_model('../pythonServer/Blackbox_classifier_FCN/' + str(dataset) + '_best_model.hdf5')
    return model


def generate_test_instance(train_examples,dataset):
        X_train, y_train, X_test, y_test = load_dataset(dataset)
        X_all = np.concatenate((X_train, X_test), axis=0)
        model = load_model(dataset)
        Y_all_pred = [np.argmax(instance) for instance in model.predict(X_all)]


        X_idx_all = list(range(len(X_all)))
        X_idx_all = np.asarray(X_idx_all)

        X_idx_zero = list(filter(lambda idx: Y_all_pred[idx] == 0, X_idx_all))
        X_idx_one = list(filter(lambda idx: Y_all_pred[idx]==1, X_idx_all))

        seed = 42
        random.seed(seed)
        zero_class = random.sample(X_idx_zero, 10)
        one_class = random.sample(X_idx_one, 10)

        X_test_instances = np.concatenate([zero_class,one_class])
        random.shuffle(X_test_instances)
        correct_ans_list = [0 if idx in zero_class else 1 for idx in X_test_instances ]

        with open(f"test_instances/{dataset}_CorrectAnswer.json", "w") as f:
            ans_dict = {idx.item():ans for idx,ans in zip(X_test_instances,correct_ans_list)}
            f.write(json.dumps(ans_dict,indent=2))

        url = "http://localhost:3000?domain=" + str(dataset) + "&mode=test" + "&instance="
        for i,test_instance in enumerate(X_test_instances):
            print(f"{i}:", url + str(test_instance))

        with open(f"test_instances/{dataset}_TestInstance.json", "w") as f:
            questions = {f'{i}': url + str(test_instance) for i, test_instance in enumerate(X_test_instances)}
            f.write(json.dumps(questions,indent=2))


if __name__ == "__main__":
    datasets = ["ECGFiveDays", "ItalyPowerDemand", "GunPoint", "ArrowHead","ECGFiveDays", "DistalPhalanxOutlineCorrect"]
    for dataset in datasets:
        generate_test_instance([], dataset)







