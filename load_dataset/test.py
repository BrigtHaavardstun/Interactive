from tslearn.datasets import UCR_UEA_datasets
import os
import shutil


def delete_if_exists(dataset):
    folder_path = "/Users/brigt/.tslearn/datasets/UCR_UEA/" + dataset
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Remove the folder and all its contents
        shutil.rmtree(folder_path)

def load_dataset_UCR(dataset_name):
    ucr = UCR_UEA_datasets(use_cache=True)
    if dataset_name in ucr.list_datasets():
        #delete_if_exists(dataset_name)
        X_train, y_train, X_test, y_test = ucr.load_dataset(dataset_name=dataset_name, )
        return  X_train, y_train, X_test, y_test
    return None, None, None, None

def main():
    # Load the first three dataset
    count = 10
    ucr = UCR_UEA_datasets()
    datasets = ucr.list_datasets()[:count]

    for dataset in datasets:
        print("Loading...", dataset)
        load_dataset_UCR(dataset_name=dataset)


if __name__ == "__main__":
    main()
