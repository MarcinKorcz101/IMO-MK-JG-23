# Ruchy kadndydackie TODO
import numpy as np
import copy
from algorithm_utils import *
from utils import read_file, read_best_solutions, plot_result, save_result
import pprint

def find_candidates(distance_matrix, k):
    candidates = []
    for i in range(len(distance_matrix)):
        candidates.append([])
        for j in range(len(distance_matrix)):
            if i != j:
                candidates[i].append((distance_matrix[i][j], j))
        candidates[i].sort()
        candidates[i] = [x[1] for x in candidates[i][:k]]
    return candidates

def find_cycle_idx(cycles, node):
    for i in range(len(cycles)):
        if node in cycles[i]:
            return i
    return None


def candidates_moves(cycles, distance_matrix, K=10):

    candidates_list = find_candidates(distance_matrix, K)
    # print(candidates_list)
    while True:
        best_delta = 0
        best_move = None
        for a in range(len(distance_matrix)):
            a_cycle_idx = find_cycle_idx(cycles, a)
            # print(a, candidates_list[a])
            for b in candidates_list[a]:
                b_cycle_idx = find_cycle_idx(cycles, b)
                if b in cycles[1]:
                    b_cycle_idx = 1
                if a_cycle_idx == b_cycle_idx:
                    delta = delta_inside_cycle_edge_exchange(distance_matrix, cycles[a_cycle_idx], [a, b])
                    if delta < best_delta:
                        best_delta = delta
                        best_move = (a, b, a_cycle_idx, delta_inside_cycle_edge_exchange)
                else:
                    if a_cycle_idx == 0:
                        first = a
                        second = b
                    else:
                        first = b
                        second = a
                    
                    delta = delta_between_cycles_node_exchange(distance_matrix, cycles, [first, second])
                    
                    if delta < best_delta:
                        best_delta = delta
                        best_move = (a, b, None, delta_between_cycles_node_exchange)
        if best_move == None:
            break

        a, b, cycle_idx, action = best_move

        if action == delta_inside_cycle_edge_exchange:
            new_cycle = exchange_edge_in_cycle(cycles[cycle_idx], [a, b])
            cycles[cycle_idx] = new_cycle
        elif action == delta_between_cycles_node_exchange:
            if find_cycle_idx(cycles, a) == 0:
                first = a
                second = b
            else:
                first = b
                second = a
            new_cycles = exchange_nodes_between_cycles(cycles, [first, second])
            cycles = new_cycles

    return cycles
    