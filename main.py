from utils import readTSP, calcDistanceMatrix
from plot_results import plotResults
import numpy as np

if __name__ == '__main__':
    coords = readTSP('kroa100.tsp')
    distance_matrix = calcDistanceMatrix(coords)




    # plotResults(coords)
