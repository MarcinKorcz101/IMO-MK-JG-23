import numpy as np


def readTSP(path: str) -> np.ndarray:
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
def calcDistanceMatrix(coords: np.ndarray) -> np.ndarray:
    distance_matrix = [[np.linalg.norm(coords[i]-coords[j]) for j in range(len(coords))]for i in range(len(coords))]
    return np.asarray(distance_matrix).astype(np.uint16)


