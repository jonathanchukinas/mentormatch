import matplotlib.pyplot as plt
import numpy as np


def printchart(array, names, title):
    # https://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes

    fig, ax = plt.subplots()
    ax.imshow(array)

    x_labels = names['mentees']
    y_labels = names['mentors']

    x_len = len(x_labels)
    y_len = len(y_labels)

    # We want to show all ticks...
    ax.set_xticks(np.arange(x_len))
    ax.set_yticks(np.arange(y_len))
    # ... and label them with the respective list entries
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(y_labels)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over applicant dimensions and create text annotations.
    # for x in range(x_len):
    #     for y in range(y_len):
    #         ax.text(x, y, array[x, y],
    #                 ha="center", va="center", color="w")

    ax.set_title(title)
    fig.tight_layout()
    plt.show()
