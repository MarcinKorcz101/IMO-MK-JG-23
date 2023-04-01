from utils import read_file, read_best_solutions
from algorithm_utils import *

def greedy_local_search():
    instance = 'kroa100.tsp'
    distance_matrix, nodes = read_file(instance)
    random_first_cycle, random_second_cycle = make_random_solution(nodes)
    regret_solutions = read_best_solutions('best_solutions.json')
    cycles = [regret_solutions[instance]['first_cycle'], regret_solutions[instance]['second_cycle']]
    running = True

    while running:
        running = False
        new_cycles = inside_cycle_node_exchange(cycles, distance_matrix)

        if new_cycles == cycles:
            # no imporvement
            new_cycles = inside_cycle_edge_exchange(cycles, distance_matrix)
            if new_cycles == cycles: break