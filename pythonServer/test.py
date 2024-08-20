from getTimeSeries import get_time_series
from classifyTimeSeries import model_classify


def test():
    dataset_name = "Chinatown.csv"
    model_name = "Chinatown.keras"

    time_series = get_time_series(data_set_name=dataset_name, index=1)
    print(model_classify(model_name=model_name, time_series=time_series))


if __name__ == "__main__":
    test()
