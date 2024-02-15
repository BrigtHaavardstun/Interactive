
from NativeGuide.FunctionBased.NativeGuideGeneration_CAM import find_cf

def generate_cf(ts,dataset):
    cf = find_cf(ts.reshape(1,-1,1),dataset)
    return cf