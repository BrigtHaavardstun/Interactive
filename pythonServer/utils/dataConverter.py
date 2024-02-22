
from tslearn.datasets import UCR_UEA_datasets

DISPLAY_NUM_POINTS = 12

def select_elemnts(array, k):
    if k > len(array):
        return "Error: k cannot be greater than the length of the array"
    step = (len(array) - 1) / (k - 1)
    return [array[int(round(step * i))] for i in range(k)]


def from_org_to_display(ts):
    global DISPLAY_NUM_POINTS
    indexes_to_pick = select_elemnts(list(range(len(ts))), DISPLAY_NUM_POINTS)
    return [ts[idx] for idx in indexes_to_pick]




SIZE_OF_DATASET = {}
def from_display_to_org(ts,dataset):
    global SIZE_OF_DATASET
    if dataset not in SIZE_OF_DATASET:
        X_train,_,_,_= UCR_UEA_datasets().load_dataset(dataset)
        SIZE_OF_DATASET[dataset] = len(X_train[0].flatten())

    size_for_data_set = SIZE_OF_DATASET[dataset]

    final_array = [0]*size_for_data_set
    org_index = select_elemnts(list(range(size_for_data_set)),len(ts))
    for i,idx in enumerate(org_index):
        final_array[idx] = ts[i]

    not_in_ts = [i for i in range(size_for_data_set) if i not in org_index]
    for idx in not_in_ts:

        # Find closest above
        idx_org_above = 0
        while org_index[idx_org_above] < idx:
            idx_org_above += 1

        idx_org_below = idx_org_above -1

        # How close to top compared to bottom
        percentage = (idx-org_index[idx_org_below])/(org_index[idx_org_above]-org_index[idx_org_below])
        final_array[idx] = (1-percentage)*ts[idx_org_below] + percentage*ts[idx_org_above]

    return final_array



if __name__ == "__main__":
    fake_italy_power = [0.52937307,-0.18254244,-0.40159337,-1.0587462,-1.1135089,-1.1135089,-0.94922068,-1.5516108,-0.78493248,0.20079669,0.80318673,0.80318673,0.63889853,0.14603395,-0.29206791,-0.23730517,-0.51111883,-0.56588155,-0.67540702,-0.18254244,0.74842399,1.5,1.8,1.4055768]
    for i in range(2,24):
        DISPLAY_NUM_POINTS = i
        print("#"*5,i,"#"*5)
        display_italy = from_org_to_display(fake_italy_power)
        real_italy = from_display_to_org(display_italy, "ItalyPowerDemand")

        print(fake_italy_power)
        print(display_italy)
        print(real_italy)




