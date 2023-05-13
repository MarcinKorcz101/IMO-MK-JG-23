from utils import read_file, read_best_solutions
from algorithm_utils import *
from utils import plot_result, save_result
from tqdm import tqdm
import numpy as np
import time

def run_experiments(N=100):
    instances = ['kroA200.tsp', 'kroB200.tsp']
    methods = [(delta_inside_cycle_edge_exchange, 'edge')]
    algorithms = [(steepest_one_epoch, 'Steepest')]
    starting_points = ['random_starting_solution']
    times_2 = []
    with open('results_lab2_test.txt', 'w') as results_file:
        for starting_point in starting_points:
            for algorithm, name_algorithm in tqdm(algorithms):
                for method, method_name in methods:
                    for instance in instances:
                        best_cycle = None
                        best_cycle_len = float('inf')
                        results_in_scope = []
                        times = []
                        for _ in tqdm(range(N)):
                            start = time.time()
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
                            improvement = True
                            old_len = calc_cycles_length(distance_matrix, cycles)
                            while improvement:
                                cycles = algorithm(cycles, distance_matrix, method)
                                new_len = calc_cycles_length(distance_matrix, cycles)
                                if old_len - new_len < 0.0001:
                                    improvement = False
                                old_len = new_len
                            end = time.time()
                            times.append(end - start)
                            results_in_scope.append(calc_cycles_length(distance_matrix, cycles))

                            if best_cycle_len > calc_cycles_length(distance_matrix, cycles):
                                best_cycle_len = calc_cycles_length(distance_matrix, cycles)
                                best_cycle = cycles
                        times_2.append(np.max(times))
                        results_file.write(f"{starting_point}\t{name_algorithm}\t{method_name}\t{instance}\t = {np.mean(results_in_scope)} ({np.min(results_in_scope)} - {np.max(results_in_scope)}) | {np.mean(times)} ({np.min(times)} - {np.max(times)})\n")
                        save_result(f"{starting_point}-{name_algorithm}-{method_name}-{instance.split('.')[0]}", best_cycle[0], best_cycle[1], nodes)
        max_time = np.max(times_2)
        print(f"Max time: {max_time}")
        # max_time = 2.16303
        # for starting_point in tqdm(starting_points):
        #     for method, method_name in methods:
        #         for instance in instances:
        #             best_cycle = None
        #             best_cycle_len = float('inf')
        #             results_in_scope = []
        #             times = []
        #             for _ in range(N):
        #                 start = time.time()
        #                 distance_matrix, nodes = read_file(instance)
        #                 if starting_point == 'random_starting_solution':
        #                     cycles = make_random_solution(len(nodes))
        #                     # print("Random starting solution")
        #                 elif starting_point == 'regret_starting_solution':
        #                     regret_solutions = read_best_solutions('best_solutions.json')
        #                     cycles = [regret_solutions[instance]['first_cycle'], regret_solutions[instance]['second_cycle']]
        #                     # print("Best starting solution")
                        
        #                 # print(instance)
        #                 # print(f"before {name_algorithm} ({method_name})", calc_cycles_length(distance_matrix, cycles))
        #                 improvement = True
        #                 old_len = calc_cycles_length(distance_matrix, cycles)

        #                 start = time.time()
        #                 while time.time() - start < max_time:
        #                     cycles = random_one_epoch(cycles, distance_matrix, method)
        #                     new_len = calc_cycles_length(distance_matrix, cycles)
        #                     if old_len - new_len < 0.0001:
        #                         improvement = False
        #                     old_len = new_len
        #                 times.append(time.time() - start)
        #                 results_in_scope.append(calc_cycles_length(distance_matrix, cycles))

        #                 if best_cycle_len > calc_cycles_length(distance_matrix, cycles):
        #                     best_cycle_len = calc_cycles_length(distance_matrix, cycles)
        #                     best_cycle = cycles
        #             times_2.append(np.max(times))
        #             results_file.write(f"{starting_point}\t{'Random_walk'}\t{method_name}\t{instance}\t = {np.mean(results_in_scope)}({np.min(results_in_scope)}-{np.max(results_in_scope)}) | {np.mean(times)}({np.min(times)}-{np.max(times)})\n")
        #             save_result(f"{starting_point}-{'Random_walk'}-{method_name}-{instance.split('.')[0]}", best_cycle[0], best_cycle[1], nodes)
                    
if __name__ == '__main__':
    run_experiments(100)