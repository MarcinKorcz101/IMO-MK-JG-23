from lab4.candidates_rework import candidates_moves_reworked
from lab2.algorithm_utils import *
from lab1.GreedyAlgorithms import GreedyAlgorithms
import time
from copy import deepcopy
import numpy as np

def perturbate(cycles, N=10):
    for _ in range(N):
        swap_type = np.random.choice([delta_between_cycles_node_exchange, delta_inside_cycle_edge_exchange])

        if swap_type == delta_between_cycles_node_exchange:
            nodes = [np.random.choice(cycles[0]), np.random.choice(cycles[1])]
            cycles = exchange_nodes_between_cycles(cycles, nodes)
        elif swap_type == delta_inside_cycle_edge_exchange:
            current_cycle = np.random.choice([0, 1])
            nodes = np.random.choice(cycles[current_cycle], size=2, replace=False)
            cycles[current_cycle] = exchange_edge_in_cycle(cycles[current_cycle], nodes)

    return cycles

def destroyold(best, destroy_coef):
    n_destroy = int((len(best[0]) + len(best[1])) * destroy_coef)
    n_destroy_paths = np.random.randint(np.floor(np.sqrt(n_destroy)), n_destroy // 2 + 1)
    paths_len = n_destroy // n_destroy_paths
    remaining = n_destroy % n_destroy_paths
    cyc_1_destroyed, cyc_2_destroyed = False, False

    for n in range(n_destroy_paths):
        current_cycle = np.random.choice([0, 1])
        start_node = np.random.randint(0, len(best[current_cycle]))

        if current_cycle == 0:
            last_nn1 = start_node
            cyc_1_destroyed = True
        else: 
            last_nn2 = start_node
            cyc_2_destroyed = True
        
        if n == n_destroy_paths - 1 and not cyc_1_destroyed:
            current_cycle = 0
            cyc_1_destroyed = True
            last_nn1 = start_node
        elif n == n_destroy_paths - 1 and not cyc_2_destroyed:
            current_cycle = 1
            cyc_2_destroyed = True
            last_nn2 = start_node

        for _ in range(paths_len):
            best[current_cycle].pop(start_node % len(best[current_cycle]))
            if remaining > 0:
                best[current_cycle].pop(start_node % len(best[current_cycle]))
                remaining -= 1
    return best, last_nn1, last_nn2, n_destroy

def destroy(best, destroy_coef):
    n_destroy = int((len(best[0]) + len(best[1])) * destroy_coef)

    n_destroy  = n_destroy // 2
    
    for current_cycle in range(2):
        n_paths = np.random.randint(np.floor(np.sqrt(n_destroy)), n_destroy // 2 + 1)
        paths_len = n_destroy // n_paths
        remaining = n_destroy % n_paths

        for _ in range(n_paths):
            start_node = np.random.randint(0, len(best[current_cycle]))

            if current_cycle == 0: last_nn1 = start_node
            else: last_nn2 = start_node

            for _ in range(paths_len):
                best[current_cycle].pop(start_node % len(best[current_cycle]))
                if remaining > 0:
                    best[current_cycle].pop(start_node % len(best[current_cycle]))
                    remaining -= 1
    return best, last_nn1, last_nn2, n_destroy

def repair(instance, distance_matrix, best, last_nn1, last_nn2, n_destroy):
    ga = GreedyAlgorithms(instance, show_plot=False)
    ga.read()
    ga.first_cycle = best[0]
    ga.second_cycle = best[1]
    nodes_in_cycles = best[0] + best[1]
    current_len = ga.regret_greedy(nodes_in_cycles, last_nn1, last_nn2)
    current_solution = [ga.first_cycle, ga.second_cycle]
    return current_solution, current_len

def ils1(distance_matrix):
    time_condition = 376
    total_iterations = 0
    cycles = make_random_solution(len(distance_matrix))
    best_solution = candidates_moves_reworked(cycles, distance_matrix)
    best_cycle_len = calc_cycles_length(distance_matrix, cycles)
    start = time.time()
    while int(round(time.time())) - start < time_condition:
        total_iterations += 1
        best = deepcopy(best_solution)
        perturbate_cycles = perturbate(best)
        current_solution = candidates_moves_reworked(perturbate_cycles, distance_matrix)
        current_len = calc_cycles_length(distance_matrix, current_solution)

        if current_len < best_cycle_len:
            best_solution = current_solution
            best_cycle_len = current_len

    return best_solution, total_iterations

def ils2(distance_matrix, instance, destroy_coef=0.2, with_local_search=True):
    time_condition = 370
    total_iterations = 0
    cycles = make_random_solution(len(distance_matrix))
    best_solution = candidates_moves_reworked(cycles, distance_matrix)
    best_cycle_len = calc_cycles_length(distance_matrix, cycles)
    start = time.time()
   
    while int(round(time.time())) - start < time_condition:
        total_iterations += 1
        best = deepcopy(best_solution)
        best, last_nn1, last_nn2, n_destroy = destroy(best, destroy_coef)
        current_solution, current_len = repair(instance, distance_matrix, best, last_nn1, last_nn2, n_destroy)
        if with_local_search:
            current_solution = candidates_moves_reworked(current_solution, distance_matrix)
            current_len = calc_cycles_length(distance_matrix, current_solution)

        if current_len < best_cycle_len:
            best_solution = current_solution
            best_cycle_len = current_len

    return best_solution, total_iterations