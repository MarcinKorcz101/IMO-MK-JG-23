from utils import read_file, read_best_solutions, plot_result
from algorithm_utils import *

def greedy_local_search():
    instance = 'kroa100.tsp'
    distance_matrix, nodes = read_file(instance)
    random_first_cycle, random_second_cycle = make_random_solution(nodes)
    regret_solutions = read_best_solutions('best_solutions.json')
    cycles = [regret_solutions[instance]['first_cycle'], regret_solutions[instance]['second_cycle']]
    # moves = [inside_cycle_node_exchange, between_cycle_node_exchange]
    # moves = [inside_cycle_edge_exchange, between_cycle_node_exchange]
    
    print("before greedy 1", calc_cycle_length(distance_matrix, cycles[0]))
    print("before greedy 2", calc_cycle_length(distance_matrix, cycles[1]))
    # plot_result("aa", cycles[0], cycles[1], nodes)
    for _ in range(100):
        greedy_one_epoch(cycles, distance_matrix, delta_inside_cycle_node_exchange)

    print("after greedy 1", calc_cycle_length(distance_matrix, cycles[0]))
    print("adter greedy 2", calc_cycle_length(distance_matrix, cycles[1]))
    # plot_result("bb", cycles[0], cycles[1], nodes)


if __name__ == '__main__':
    greedy_local_search()