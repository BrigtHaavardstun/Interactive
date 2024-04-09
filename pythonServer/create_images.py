



import matplotlib.pyplot as plt
import numpy as np

def make_image(dataset,name, time_series,color_ts,label_ts="Test",counter_factual=None, color_cf=None):
    """
    Create a matplotlib plot of the data in `time_series` with a blue line if `label == 0`,
    otherwise a pink line. Optionally, plot `counter_factual` on the same plot.

    Store the created image in 'Images/name.png'.
    """
    # Generate some sample data (you can replace this with your actual data)
    x_values = np.arange(len(time_series))
    y_values = np.array(time_series)

    # Create a new figure and axis
    screen_width = 1920
    screen_height = 1185  # Close to the golden ratio (16:10)   
    fig, ax = plt.subplots(figsize=(screen_width / 100, screen_height / 100))  # Convert pixels to inches

    # Plot the time series data
    ax.plot(x_values, y_values, color=color_ts, label=label_ts)
    
    # Optionally, plot the counterfactual data
    if counter_factual is not None:
        ax.plot(x_values, counter_factual, color=color_cf, linestyle='--', label='Counterfactual')

    # Customize the plot (add labels, title, legend, etc.)
    ax.set_xlabel('Hours')
    ax.legend()
    ax.set_ylim(-2, 4)  
    ax.set_xlim(0,23)
   

    # Save the plot as a PNG file
    plt.savefig(f"Images/{dataset}/{name}.png",bbox_inches="tight")

    # Show the plot (optional)
    plt.show()



def create_images_for_test_data(dataset):
    import json
    from getTimeSeries import get_time_series
    file_path = f"test_instances/{dataset}_TestInstance.json"
    keys = []
    with open(file_path) as f:
        json_dict = json.load(f)
        print(json.dumps(json_dict, indent=2))
        keys = json_dict.keys()
    
    all_time_series = [get_time_series(dataset,int(key)).flatten() for key in keys]
    
    for key,time_series in zip(keys, all_time_series):
        make_image(dataset=dataset,name=key, time_series=time_series,color_ts="grey",label_ts="Test")

    

    
# Example usage:
if __name__ == "__main__":
    datasets = ["ItalyPowerDemand", "Chinatown", "Charging"]
    for dataset in datasets:
        create_images_for_test_data(dataset)
