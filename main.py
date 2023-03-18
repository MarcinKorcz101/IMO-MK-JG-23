from lab1.greedy_nn import greedy_nn
from utils import read_TSP, calc_distance_matrix, get_start_nodes
from plot_results import plot_results
import numpy as np

if __name__ == '__main__':
    coords = read_TSP('kroa100.tsp')
    distance_matrix = calc_distance_matrix(coords)
    routes = greedy_nn(distance_matrix)
    # print(coords)

    plot_results(coords, routes)
