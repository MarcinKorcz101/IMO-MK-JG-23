from utils import read_file, read_best_solutions
from algorithm_utils import *
from utils import plot_result, save_result
from tqdm import tqdm
import numpy as np
import time
from candidates import candidates_moves
from moves_rate import moves_rate

def run_experiments(N=1):
    instances = ['kroA200.tsp', 'kroB200.tsp']
    algorithms = [(candidates_moves, 'Ruchy kandydatckie')]
    algorithms = [(moves_rate, 'Lokalne przeszukiwanie')]
    with open('results_lab3_moves.txt', 'w') as results_file:
        for algorithm, name_algorithm in algorithms:
            for instance in instances:

                best_cycle = None
                best_cycle_len = float('inf')
                results_in_scope = []
                times = []

                for _ in tqdm(range(N)):
                    start = time.time()
                    distance_matrix, nodes = read_file(instance)
                    
                    cycles = make_random_solution(len(nodes))
                    
                    cycles = algorithm(cycles, distance_matrix)
                        
                    end = time.time()
                    times.append(end - start)

                    results_in_scope.append(calc_cycles_length(distance_matrix, cycles))

                    if best_cycle_len > calc_cycles_length(distance_matrix, cycles):
                        best_cycle_len = calc_cycles_length(distance_matrix, cycles)
                        best_cycle = cycles

                
                results_file.write(f"{name_algorithm}\t{instance}\t = {np.mean(results_in_scope)} ({np.min(results_in_scope)} - {np.max(results_in_scope)}) | {np.mean(times)} ({np.min(times)} - {np.max(times)})\n")
                save_result(f"{name_algorithm}-{instance.split('.')[0]}", best_cycle[0], best_cycle[1], nodes)


if __name__ == '__main__':
    run_experiments(10)