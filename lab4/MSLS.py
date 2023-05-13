from lab4.utils import *
from lab4.candidates_rework import *
from tqdm import tqdm

def make_random_solution(n):
    nodes = np.arange(n)
    # print(len(nodes))
    nodes = np.random.permutation(nodes).tolist()
    half = len(nodes) // 2
    return [nodes[:half], nodes[half:]]

def MSLS(distance_matrix):
    max_iter = 10
    best_solution = None
    best_cost = float('inf')
    for i in tqdm(range(max_iter)):
        # print(i)
        cycles = make_random_solution(len(distance_matrix))
        solution = candidates_moves_reworked(cycles, distance_matrix)
        print(solution)
        cost = calc_cycles_length(distance_matrix, solution)
        if cost < best_cost:
            best_solution = solution
            best_cost = cost
    return best_solution