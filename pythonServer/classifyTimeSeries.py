
MAX_VAL = 50
MIN_VAL = -50


def _classify(ts):
    """
    @ts = Univariate Time Series
    @ return class of time series
    """
    global MAX_VAL, MIN_VAL
    max_curr = max(ts)
    min_curr = min(ts)
    if MIN_VAL <= min_curr and max_curr <= MAX_VAL:
        return 1
    else:
        return 2


