
from Train_model import train_model as train_and_save

def generate_model():
    datasets = ["ItalyPowerDemand"]
    for dataset in datasets:
        train_and_save(dataset)

if __name__ == "__main__":
    generate_model()