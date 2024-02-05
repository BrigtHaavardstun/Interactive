
from classifyTimeSeries import MIN_VAL, MAX_VAL


def generate_cf(ds):
    global MAX_VAL, MIN_VAL
    new_cf = [y for y in ds]
    for i, e in enumerate(new_cf):
        if e > MAX_VAL:
            new_cf[i] = MAX_VAL
        if e < MIN_VAL:
            new_cf[i] = MIN_VAL
        print(e)
    print("Correct CF:",new_cf)
    return new_cf