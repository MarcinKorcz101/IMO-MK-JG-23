from lab6.algorithm_utils import *
import time

def greedy_local_search(distance_matrix, nodes, number_of_iterations=1000):    
    cycles = make_random_solution(len(nodes))
    # start = time.time()
    for i in range(number_of_iterations):
        cycles = greedy_one_epoch(cycles, distance_matrix, delta_inside_cycle_node_exchange)
    # print("czas ", time.time() - start)
    
    # print("after greedy 1", calc_cycle_length(distance_matrix, cycles[0]))
    # print("after greedy 2", calc_cycle_length(distance_matrix, cycles[1]))
    # print("after greedy BOTH", calc_cycles_length(distance_matrix, cycles))
    return cycles


def calculate_similarity(solution_1, solution_2, edges=False):
    if edges:
        # calculate similarity of two solutions based on number of common edges
        solution_1_edges = set()
        solution_2_edges = set()
        for cycle in solution_1:
            for i in range(len(cycle) - 1):
                solution_1_edges.add((cycle[i], cycle[i + 1]))
            solution_1_edges.add((cycle[-1], cycle[0]))
        for cycle in solution_2:
            for i in range(len(cycle) - 1):
                solution_2_edges.add((cycle[i], cycle[i + 1]))
            solution_2_edges.add((cycle[-1], cycle[0]))
        
        intersection = len(solution_1_edges.intersection(solution_2_edges))
        return intersection
    
    # calculate similarity of two solutions based on number of common vertices
    solution_1_vertices_1 = set(solution_1[0])
    solution_1_vertices_2 = set(solution_1[1])
    solution_2_vertices_1 = set(solution_2[0])
    solution_2_vertices_2 = set(solution_2[1])

    intersection_1 = len(solution_1_vertices_1.intersection(solution_2_vertices_1))
    intersection_2 = len(solution_1_vertices_2.intersection(solution_2_vertices_2))
    intersection_3 = len(solution_1_vertices_1.intersection(solution_2_vertices_2))
    intersection_4 = len(solution_1_vertices_2.intersection(solution_2_vertices_1))
    
    return max(intersection_1 + intersection_2, intersection_3 + intersection_4)