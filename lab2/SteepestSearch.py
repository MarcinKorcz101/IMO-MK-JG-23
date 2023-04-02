from utils import read_file, read_best_solutions
from algorithm_utils import *
from utils import plot_result

def steepest_local_search():
    instance = 'kroa100.tsp'
    distance_matrix, nodes = read_file(instance)
    regret_solutions = read_best_solutions('best_solutions.json')
    cycles = [regret_solutions[instance]['first_cycle'], regret_solutions[instance]['second_cycle']]
    # cycles = make_random_solution(len(nodes))
    # print(f"WAZNE!!! {cycles[0]}")
    print("before steepest 1", calc_cycle_length(distance_matrix, cycles[0]))
    print("before steepest 2", calc_cycle_length(distance_matrix, cycles[1]))
    print("before steepest BOTH", calc_cycles_length(distance_matrix, cycles))
    # plot_result("aa", cycles[0], cycles[1], nodes)
    for i in range(10):
        # cycles = steepest_one_epoch(cycles, distance_matrix, delta_inside_cycle_node_exchange)
        cycles = steepest_one_epoch(cycles, distance_matrix, delta_inside_cycle_edge_exchange)
        # if i%1 == 0:
        plot_result(f"step {i}", cycles[0], cycles[1], nodes)
        print(f"step {i}:", calc_cycles_length(distance_matrix, cycles))
    print(cycles)
    print("after steepest 1", calc_cycle_length(distance_matrix, cycles[0]))
    print("after steepest 2", calc_cycle_length(distance_matrix, cycles[1]))
    print("after steepest BOTH", calc_cycles_length(distance_matrix, cycles))

if __name__ == '__main__':
    steepest_local_search()