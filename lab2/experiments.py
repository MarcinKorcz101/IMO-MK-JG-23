from utils import read_file, read_best_solutions
from algorithm_utils import *
from utils import plot_result

def run_experiments(N=100):
    instances = ['kroa100.tsp', 'krob100.tsp']
    methods = [delta_inside_cycle_edge_exchange, delta_inside_cycle_node_exchange]
    algorithms = [greedy_one_epoch, steepest_one_epoch]
    # TODO
    # starting_points = [make_random_solution, make_regret_solution]
    starting_points = [make_random_solution]
    for starting_point in starting_points:
        for algoritm in algorithms:
            for method in methods:
                for instance in instances:
                    distance_matrix, nodes = read_file(instance)
                    regret_solutions = read_best_solutions('best_solutions.json')
                    cycles = [regret_solutions[instance]['first_cycle'], regret_solutions[instance]['second_cycle']]
                    
                    print("before steepest 1", calc_cycle_length(distance_matrix, cycles[0]))
                    print("before steepest 2", calc_cycle_length(distance_matrix, cycles[1]))
                    print("before steepest BOTH", calc_cycles_length(distance_matrix, cycles))
                    
                    # TODO change N to other stop condition and run this N times
                    for i in range(N):
                        # cycles = steepest_one_epoch(cycles, distance_matrix, delta_inside_cycle_node_exchange)
                        cycles = algoritm(cycles, distance_matrix, method)
                        # if i%1 == 0:
                        # plot_result(f"step {i}", cycles[0], cycles[1], nodes)
                        print(f"step {i}:", calc_cycles_length(distance_matrix, cycles))
                    print(cycles)
                    print("after steepest 1", calc_cycle_length(distance_matrix, cycles[0]))
                    print("after steepest 2", calc_cycle_length(distance_matrix, cycles[1]))
                    print("after steepest BOTH", calc_cycles_length(distance_matrix, cycles))

    for instance in instances:
        distance_matrix, nodes = read_file(instance)
        regret_solutions = read_best_solutions('best_solutions.json')
        cycles = [regret_solutions[instance]['first_cycle'], regret_solutions[instance]['second_cycle']]
        
        print("before steepest 1", calc_cycle_length(distance_matrix, cycles[0]))
        print("before steepest 2", calc_cycle_length(distance_matrix, cycles[1]))
        print("before steepest BOTH", calc_cycles_length(distance_matrix, cycles))
        
        for i in range(10):
            
            cycles = steepest_one_epoch(cycles, distance_matrix, delta_inside_cycle_edge_exchange)
            
            print(f"step {i}:", calc_cycles_length(distance_matrix, cycles))
        print(cycles)
        print("after steepest 1", calc_cycle_length(distance_matrix, cycles[0]))
        print("after steepest 2", calc_cycle_length(distance_matrix, cycles[1]))
        print("after steepest BOTH", calc_cycles_length(distance_matrix, cycles))

if __name__ == '__main__':
    run_experiments()