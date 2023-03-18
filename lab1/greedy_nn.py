import numpy as np

from utils import get_start_nodes

def get_nearest_neighbor(distance_matrix: np.ndarray,
                         visited: list[list[int]],
                         current_path: int) -> None:
    nodes_to_visit = [idx for idx in range(len(distance_matrix)) if idx not in visited[0] + visited[1]]
    last_element_idx = visited[current_path][-1]
    available_nodes = distance_matrix[last_element_idx, nodes_to_visit]

    best_idx = np.argmin(available_nodes)

    visited[current_path].append(nodes_to_visit[best_idx])



def greedy_nn(distance_matrix: np.ndarray) -> list[list[int]]:
    visited = get_start_nodes(distance_matrix)
    # print(distance_matrix)
    for i in range(2, len(distance_matrix)):
        current_path = i % 2
        get_nearest_neighbor(distance_matrix, visited, current_path)
    return visited

