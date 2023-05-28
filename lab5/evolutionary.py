from lab4.candidates_rework import candidates_moves_reworked
from lab2.algorithm_utils import *
from lab1.GreedyAlgorithms import GreedyAlgorithms
import time
from copy import deepcopy
import numpy as np

N_POPULATION = 20
PATIENCE = 300
MUTATION_PROBABILITY = 0.2

def population_init(distance_matrix):
    population = []
    for _ in range(N_POPULATION):
        cycles = make_random_solution(len(distance_matrix))
        solution = candidates_moves_reworked(cycles, distance_matrix)
        cycle_len = calc_cycles_length(distance_matrix, cycles)
        population.append((solution, cycle_len))
    return population

def remove_unique_edges_in_cycles(first_parent, second_parent):
    output_solution = deepcopy(first_parent)
    removed_nodes = []
    last_n1 = last_n2 = -1

    for cycle_idx, first_parent_cycle in enumerate(first_parent):
        for idx in range(len(first_parent_cycle)):
            first_node = first_parent_cycle[idx]
            second_node = first_parent_cycle[(idx + 1) % len(first_parent_cycle)]
            edge_is_unique = True

            for second_parent_cycle in second_parent:
                if first_node in second_parent_cycle and second_node in second_parent_cycle:
                    first_node_idx = second_parent_cycle.index(first_node)
                    second_node_idx = second_parent_cycle.index(second_node)
                    adjacency = abs(first_node_idx - second_node_idx)

                    if adjacency == 1 or adjacency == len(second_parent_cycle) - 1:
                        edge_is_unique = False
                        break

            if edge_is_unique:
                if last_n1 == -1 and cycle_idx == 0:
                    last_n1 = output_solution[cycle_idx][idx]
                elif last_n2 == -1 and cycle_idx == 1:
                    last_n2 = output_solution[cycle_idx][idx]

                output_solution[cycle_idx][idx] = -1
                output_solution[cycle_idx][(idx + 1) % len(first_parent_cycle)] = -1
                removed_nodes.extend([first_node, second_node])

    return output_solution, removed_nodes, last_n1, last_n2

def remove_free_nodes(output_solution, removed_nodes):
    for cycle_idx, cycle in enumerate(output_solution):
        for idx in range(1, len(cycle)):
            if cycle[idx - 1] == -1 and cycle[(idx + 1) % len(cycle)] == -1:
                if cycle[idx] != -1:
                    output_solution[cycle_idx][idx] = -1
                    removed_nodes.append(cycle[idx])

    return output_solution, removed_nodes

def mutation(output_solution, removed_nodes):
    for cycle_idx, cycle in enumerate(output_solution):
        for idx in range(len(cycle)):
            if cycle[idx] != -1:
                if np.random.random() < MUTATION_PROBABILITY:
                    output_solution[cycle_idx][idx] = -1
                    removed_nodes.append(cycle[idx])

    return output_solution, removed_nodes

def repair(instance, distance_matrix, output_solution, l1, l2, if_local_search=True):
    ga = GreedyAlgorithms(instance, show_plot=False)
    ga.read()
    ga.first_cycle = output_solution[0]
    ga.second_cycle = output_solution[1]
    nodes_in_cycles = output_solution[0] + output_solution[1]
    current_len = ga.regret_greedy(nodes_in_cycles, l1, l2)
    current_solution = [ga.first_cycle, ga.second_cycle]

    if if_local_search:
        current_solution = candidates_moves_reworked(current_solution, distance_matrix)
        current_len = calc_cycles_length(distance_matrix, current_solution)
     
    return current_solution, current_len

def recombine(first_parent, second_parent):
    output_solution, removed_nodes, l1, l2 = remove_unique_edges_in_cycles(first_parent, second_parent)
    output_solution, removed_nodes = remove_free_nodes(output_solution, removed_nodes)
    output_solution, removed_nodes = mutation(output_solution, removed_nodes)

    for cycle_idx, cycle in enumerate(output_solution):
        new_cycle = []
        for node in cycle:
            if node != -1:
                new_cycle.append(node)
        output_solution[cycle_idx] = new_cycle

    for cycle_idx, cycle in enumerate(output_solution):
        if len(cycle) == 0:
            node = np.random.choice(removed_nodes)
            output_solution[cycle_idx].append(node)
            removed_nodes.remove(node)

    return output_solution, l1, l2

def selection(population):
    return (population[i][0] for i in np.random.choice(len(population), 2, replace=False))

def evolutionary(distance_matrix, instance):
    time_condition = 340
    no_improvement_counter = 0
    iterations = 0
    start = time.time()
    population = population_init(distance_matrix)
    best_solution, best_cycle_len = min(population, key = lambda sol: sol[1])
    worst_idx = np.argmax([sol[1] for sol in population])
    _, worst_cycle_len = population[worst_idx]

    while int(round(time.time())) - start < time_condition:
        iterations += 1
        first_parent, second_parent = selection(population)
        output_solution, l1, l2 = recombine(first_parent, second_parent)
        current_solution, current_len = repair(instance, distance_matrix, output_solution, l1, l2)

        if current_len < best_cycle_len:
            no_improvement_counter = 0
            best_cycle_len = current_len
            best_solution = current_solution
            population[worst_idx] = (best_solution, best_cycle_len)
            worst_idx = np.argmax([sol[1] for sol in population])
            _, worst_cycle_len = population[worst_idx]
        else:
            if current_len < worst_cycle_len:
                no_improvement_counter += 1

                weak_improvement = False
                for solution in population:
                    if abs(current_len - solution[1]) < 30:
                        weak_improvement = True
                        break

            if not weak_improvement:
                population[worst_idx] = (current_solution, current_len)
                worst_idx = np.argmax([sol[1] for sol in population])
                _, worst_cycle_len = population[worst_idx]

        if no_improvement_counter == PATIENCE: break
    return best_solution, iterations