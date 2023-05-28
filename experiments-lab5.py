from lab4.utils import read_file, read_best_solutions
from lab4.utils import plot_result, save_result, calc_cycles_length
from tqdm import tqdm
import numpy as np
import time
from lab4.candidates_rework import candidates_moves_reworked
from lab4.MSLS import MSLS
from lab4.ILS import ils1, ils2
from lab5.evolutionary import *

def run_experiments(N=10):
    # instances = ['kroA200.tsp']
    # instances = ['kroB200.tsp']
    instances = ['kroA200.tsp', 'kroB200.tsp']
    # algorithms = [(MSLS, 'MSLS')]
    # algorithms = [(MSLS, 'MSLS'), (ils1, 'ILS1')]
    # algorithms = [(evolutionary, 'Evolutionary algorithm')]
    # algorithms = [(evolutionary, 'Evolutionary algorithm with local search')]
    algorithms = [(ils2, 'ILS2 algorithm with local search')]
    # algorithms = [(candidates_moves_reworked, 'Ruchy kandydatckie')]
    with open('test.txt', 'w') as results_file:
        for algorithm, name_algorithm in algorithms:
            for instance in instances:
                best_cycle = None
                best_cycle_len = float('inf')
                results_in_scope = []
                times = []
                totals = []

                for _ in tqdm(range(N)):
                    start = time.time()
                    distance_matrix, nodes = read_file(instance)
                    if name_algorithm == "ILS2 algorithm with local search" or name_algorithm == "ILS2" or name_algorithm == "Evolutionary algorithm with local search" or name_algorithm == "Evolutionary algorithm":
                        cycles, total_iterations = algorithm(distance_matrix, instance)
                    else:
                        cycles, total_iterations = algorithm(distance_matrix)
                    totals.append(total_iterations)
                    print(cycles)
                    end = time.time()
                    times.append(end - start)
                    results_in_scope.append(calc_cycles_length(distance_matrix, cycles))

                    if best_cycle_len > calc_cycles_length(distance_matrix, cycles):
                        best_cycle_len = calc_cycles_length(distance_matrix, cycles)
                        best_cycle = cycles
                
                results_file.write(f"{name_algorithm}\t{instance}\t = {np.mean(results_in_scope)} ({np.min(results_in_scope)} - {np.max(results_in_scope)}) | {np.mean(times)} ({np.min(times)} - {np.max(times)}) | {np.mean(totals)}\n")
                save_result(f"{name_algorithm}-{instance.split('.')[0]}", best_cycle[0], best_cycle[1], nodes)


if __name__ == '__main__':
    run_experiments(10)