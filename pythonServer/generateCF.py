from NativeGuide.find_native_guide import find_native_cf



def generate_native_cf(ts,data_set_name, model_name):
    cf = find_native_cf(ts,data_set_name,model_name)
    return cf