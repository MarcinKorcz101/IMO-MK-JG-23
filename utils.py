import random
import typing

import numpy as np


def read_TSP(path: str) -> np.ndarray:
    coords = []
    with open(path, "r") as file:
        for i, line in enumerate(file):
            if line == "EOF\n":
                break
            if i >= 6:
                _, x, y = line.split()
                coords.append((int(x), int(y)))
    return np.asarray(coords)


# https://stackoverflow.com/questions/1401712/how-can-the-euclidean-distance-be-calculated-with-numpy
def calc_distance_matrix(coords: np.ndarray) -> np.ndarray:
    distance_matrix = [[np.linalg.norm(coords[i] - coords[j]) for j in range(len(coords))] for i in range(len(coords))]
    return np.asarray(distance_matrix).astype(np.uint16)


def get_start_nodes(distance_matrix: np.ndarray) -> list[list[int]]:
    size = distance_matrix.shape[0]
    # print(size)
    start_node_1 = random.randint(0, size - 1)
    start_node_2 = np.argmax(distance_matrix[start_node_1])

    return [[start_node_1], [start_node_2]]
