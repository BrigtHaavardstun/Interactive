from getTimeSeries import get_time_series
from classifyTimeSeries import _classify
from generateCF import generate_cf
def test(dataset):
    x = get_time_series(dataset,0)
    print(x.shape)
    c = _classify(x,dataset)
    cf = generate_cf(x,dataset)


if __name__ == '__main__':
    dataset = "ItalyPowerDemand"
    test(dataset)