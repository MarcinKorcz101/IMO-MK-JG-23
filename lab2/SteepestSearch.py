from utils import read_file, read_best_solutions
from algorithm_utils import *

def steepest_local_search():
    instance = 'kroa100.tsp'
    distance_matrix, nodes = read_file(instance)
    random_first_cycle, random_second_cycle = make_random_solution(nodes)
    regret_solutions = read_best_solutions('best_solutions.json')
    cycles = [regret_solutions[instance]['first_cycle'], regret_solutions[instance]['second_cycle']]
    
    print("before greedy 1", calc_cycle_length(distance_matrix, cycles[0]))
    print("before greedy 2", calc_cycle_length(distance_matrix, cycles[1]))

    greedy_one_epoch(cycles, distance_matrix, )

    print("after greedy 1", calc_cycle_length(distance_matrix, cycles[0]))
    print("adter greedy 2", calc_cycle_length(distance_matrix, cycles[1]))

if __name__ == '__main__':
    steepest_local_search()