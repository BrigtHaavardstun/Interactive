import matplotlib.pyplot as plt


def show_examples(list_of_time_series: list[list[float]]):
    width = 2
    height = 3
    fig, axs = plt.subplots(width, height)

    counter = 0
    for x in range(width):
        for y in range(height):
            axs[x, y].plot(list_of_time_series[counter])
            counter += 1
    fig.show()

import random
if __name__ == "__main__":
    list_of_time_series = [[random.randint(-2,2) for i in range(12)] for j in range(6)]
    show_examples(list_of_time_series)
