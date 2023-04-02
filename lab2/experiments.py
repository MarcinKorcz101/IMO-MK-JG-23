from utils import read_file, read_best_solutions
from algorithm_utils import *
from utils import plot_result, save_result
from tqdm import tqdm

def run_experiments(N=100):
    instances = ['kroa100.tsp', 'krob100.tsp']
    methods = [(delta_inside_cycle_edge_exchange, 'edge'), (delta_inside_cycle_node_exchange, 'node')]
    algorithms = [(greedy_one_epoch, 'Greedy'), (steepest_one_epoch, 'Steepest')]
    # algorithms[0], algorithms[1] = algorithms[1], algorithms[0]
    starting_points = ['random_starting_solution', 'regret_starting_solution']
    for starting_point in starting_points:
        for algorithm, name_algorithm in tqdm(algorithms):
            for method, method_name in methods:
                for instance in instances:
                    for _ in range(N):
                        distance_matrix, nodes = read_file(instance)
                        if starting_point == 'random_starting_solution':
                            cycles = make_random_solution(len(nodes))
                            # print("Random starting solution")
                        elif starting_point == 'regret_starting_solution':
                            regret_solutions = read_best_solutions('best_solutions.json')
                            cycles = [regret_solutions[instance]['first_cycle'], regret_solutions[instance]['second_cycle']]
                            # print("Best starting solution")
                        
                        # print(instance)
                        # print(f"before {name_algorithm} ({method_name})", calc_cycles_length(distance_matrix, cycles))
                        
                        # TODO change N to other stop condition and run this N times
                        # for i in range(N):
                            # cycles = steepest_one_epoch(cycles, distance_matrix, delta_inside_cycle_node_exchange)
                        improvement = True
                        old_len = calc_cycles_length(distance_matrix, cycles)
                        while improvement:
                            cycles = algorithm(cycles, distance_matrix, method)
                            new_len = calc_cycles_length(distance_matrix, cycles)
                            if old_len - new_len < 0.0001:
                                improvement = False
                            old_len = new_len
                    save_result(f"{starting_point}-{name_algorithm}-{method_name}-{instance.split('.')[0]}", cycles[0], cycles[1], nodes)
                     
if __name__ == '__main__':
    run_experiments(1)