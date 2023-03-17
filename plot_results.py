import matplotlib.pyplot as plt
import numpy as np


def plotResults(coords):
    x, y = coords[:,0], coords[:,1]


    fig, ax = plt.subplots()

    ax.scatter(x, y)

    plt.show()