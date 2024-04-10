from NativeGuide.find_native_guide import find_native_cf



def generate_native_cf(ts,dataset):
    cf = find_native_cf(ts,dataset)
    return cf