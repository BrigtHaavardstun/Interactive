from NativeGuide.FunctionBased.NativeGuideGeneration_CAM import find_cf,find_native_cf


def generate_cf(ts,dataset):
    cf = find_cf(ts,dataset)
    return cf

def generate_native_cf(ts,dataset):
    cf = find_native_cf(ts,dataset)
    return cf