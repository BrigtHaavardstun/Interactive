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
    host = "158.42.185.235"
    port = "8766"
    url = f"http://{host}:{port}?domain=" + str(dataset) + "&mode=test" + "&instance="
    for test_instance in X_test_instances:
        print(f"{test_instance}:", url + str(test_instance))

    with open(f"test_instances/{dataset}_TestInstance.json", "w") as f:
        questions = {f'{test_instance}': url + str(test_instance) for test_instance in X_test_instances}
        f.write(json.dumps(questions,indent=2))

import json
def convert_to_html_format(dataset):
    file_path = f"test_instances/{dataset}_TestInstance.json"
    json_obj = None
    with open(file_path) as user_file:
        parsed_json = json.load(user_file)
        print(type(parsed_json))
        json_obj = parsed_json
    all_html_code = {}
    for idx,key in enumerate(json_obj.keys()):
        html_code = f'<center><h1> Test {idx+1}. What do you think the AI classified this as?</h1><img alt="" src="/files/XAIBergen/{dataset}/Test/{key}.png" style="width: 100%; height: auto;"/></center>'
        all_html_code[key]= html_code
    
    file_path = f"test_instances/{dataset}_TestInstanceHTML.json"
    json_string = json.dumps(all_html_code, indent=4)
    with open(file_path, "w") as json_file:
        for key in all_html_code.keys():
            json_file.write(f"{all_html_code[key]}\n")
        #json_file.write(json_string)
    
    for key in all_html_code.keys():
        print(f"{key}:  {all_html_code[key]}")

if __name__ == "__main__":
    datasets = ["ItalyPowerDemand","Chinatown", "Charging"]
    for dataset in datasets:
        generate_test_instance([], dataset)
        convert_to_html_format(dataset)








