from time import time
from copy import deepcopy
import pandas as pd
import numpy as np

inside_cycle_edge_exchange = 0
between_cycles_node_exchange = 1

def distance(a, b):
    return np.round(np.sqrt(np.sum((a - b) ** 2)))

def get_node(cycles, a):
    i = None
    try:
        i = cycles[0].index(a)
    except:
        i = None

    if i is not None: return 0, i
    i = None
    try:
        i = cycles[1].index(a)
    except:
        i = None

    if i is not None: return 1, i
    assert False, 'Node must be in one of the cycles'

def reverse(xs, i, j):
    n = len(xs)
    d = (j - i) % n
    for k in range(abs(d)//2+1):
        a, b = (i + k) % n, (i + d - k) % n
        xs[a], xs[b] = xs[b], xs[a]

def check_edges(cycle, node1, node2):
    for i in range(len(cycle) - 1):
        x, y = cycle[i], cycle[i + 1]
        if (node1, node2) == (x, y):
            return 1
        if (node1, node2) == (y, x):
            return -1
        
    x, y = cycle[-1], cycle[0]
    if (node1, node2) == (x, y):
        return 1
    if (node1, node2) == (y, x):
        return -1
    return 0

def delta_edge_exchange(cities, cycle, i, j):
    size = len(cycle)
    nodes = cycle[i], cycle[(i + 1) % size], cycle[j], cycle[(j + 1) % size]

    return (delta_inside_cycle_edge_exchange(cities, *nodes), *nodes)

def check_all_edges(cycles, node1, node2):
    for i in range(2):
        status = check_edges(cycles[i], node1, node2)
        if status != 0:
            return i, status
    return None, 0

def delta_between_cycles_node_exchange(dist_mat, x1, y1, z1, x2, y2, z2):
    return dist_mat[x1][y2] + dist_mat[z1][y2] - dist_mat[x1][y1] - dist_mat[z1][y1] + dist_mat[x2][y1] + dist_mat[z2][y1] - dist_mat[x2][y2] - dist_mat[z2][y2]

def exchange_nodes_between_cycles(cities, cycles, cyc1, i, cyc2, j):
    cycle1, cycle2 = cycles[cyc1], cycles[cyc2]
    n = len(cycle1)
    m = len(cycle2)

    x1, y1, z1 = cycle1[(i - 1) % n], cycle1[i], cycle1[(i + 1) % n]
    x2, y2, z2 = cycle2[(j - 1) % m], cycle2[j], cycle2[(j + 1) % m]

    delta = delta_between_cycles_node_exchange(cities, x1, y1, z1, x2, y2, z2)
    move = delta, between_cycles_node_exchange, cyc1, cyc2, x1, y1, z1, x2, y2, z2
    return delta, move

def delta_inside_cycle_edge_exchange(cities, a, b, c, d):
    if a == d or a == b or a == c or b == c or b == d or c == d:
        return 1e8
    return cities[a][c] + cities[b][d] - cities[a][b] - cities[c][d]

def get_starting_possibilities(cities, cycles):
    moves = []
    for k in range(2):
        cycle = cycles[k]

        n = len(cycle)
        possible_edges = [(i, (i + d) % n) for i in range(n) for d in range(2, n - 1)]

        for i, j in possible_edges:
            delta, a, b, c, d = delta_edge_exchange(cities, cycle, i, j)
            if delta < 0:
                moves.append((delta, inside_cycle_edge_exchange, a, b, c, d))

    possible_nodes = [(i, j) for i in range(len(cycles[0])) for j in range(len(cycles[1]))]
    for i, j in possible_nodes:
        delta, move = exchange_nodes_between_cycles(cities, cycles, 0, i, 1, j)
        if delta < 0:
            moves.append(move)
    return moves
 
def make_move(cycles, move):
    action = move[1]
    if action == inside_cycle_edge_exchange:
        _, _, a, _, c, _ = move
        (cycle1, i) = get_node(cycles, a)
        (cycle2, j) = get_node(cycles, c)
        cycle = cycles[cycle1]
        n = len(cycle)
        reverse(cycle, (i + 1) % n, j)
    elif action == between_cycles_node_exchange:
        _, _, cycle1, cycle2, _, a, _, _, b, _ = move
        i, j = cycles[cycle1].index(a), cycles[cycle2].index(b)
        cycles[cycle1][i], cycles[cycle2][j] = cycles[cycle2][j], cycles[cycle1][i]

def check_edge_connection(cycles, possibility):
    _, _, cycle1, cycle2, x1, y1, z1, x2, y2, z2 = possibility
    first_cyc1 = check_edges(cycles[cycle1], x1, y1)
    first_cyc2 = check_edges(cycles[cycle1], y1, z1)
    second_cyc1 = check_edges(cycles[cycle2], x2, y2)
    second_cyc2 = check_edges(cycles[cycle2], y2, z2)
    return first_cyc1, first_cyc2, second_cyc1, second_cyc2
    
def new_possibilities(distance_matrix, cycles, possibility):
    action = possibility[1]
    possibilities = []

    if action == inside_cycle_edge_exchange:
        _, _, a, b, c, d = possibility

        if a in cycles[0]:
            cycle = cycles[0]
        else:
            cycle = cycles[1]

        n = len(cycle)
        possible_edges = [(i, (i + d) % n) for i in range(n) for d in range(2, n - 1)]

        for i, j in possible_edges:
            delta, a, b, c, d = delta_edge_exchange(distance_matrix, cycle, i, j)
            if delta < 0:
                possibilities.append((delta, inside_cycle_edge_exchange, a, b, c, d))

    elif action == between_cycles_node_exchange:
        _, _, cycle1, cycle2, _, y1, _, _, y2, _ = possibility

        for k in range(len(cycles[cycle2])):
            delta, possibility = exchange_nodes_between_cycles(distance_matrix, cycles, cycle1, cycles[cycle1].index(y2), cycle2, k)
            if delta < 0:
                possibilities.append(possibility)

        for k in range(len(cycles[cycle1])):
            delta, possibility = exchange_nodes_between_cycles(distance_matrix, cycles, cycle2, cycles[cycle2].index(y1), cycle1, k)
            if delta < 0:
                possibilities.append(possibility)

    return possibilities

def moves_rate(cycles, distance_matrix):
    cycles = deepcopy(cycles)
    possibilities = get_starting_possibilities(distance_matrix, cycles)
    possibilities = sorted(possibilities, key = lambda delta: delta[0])
    
    while True:
        remove_possibilities = []
        best_move = None

        for possibility_idx, possibility in enumerate(possibilities):
            action = possibility[1]

            if action == inside_cycle_edge_exchange:
                _, _, a, b, c, d = possibility
                (cycle1, same_dir1), (cycle2, same_dir2) = check_all_edges(cycles, a, b), check_all_edges(cycles, c, d)

                if cycle1 != cycle2 or same_dir1 == 0 or same_dir2 == 0:
                    remove_possibilities.append(possibility_idx)
                elif same_dir1 == same_dir2 == 1:
                    remove_possibilities.append(possibility_idx)
                    best_move = possibility
                    break
                elif same_dir1 == same_dir2 == -1:
                    remove_possibilities.append(possibility_idx)
                    best_move = possibility[0], inside_cycle_edge_exchange, b, a, d, c
                    break

            elif action == between_cycles_node_exchange:
                same_dir1, same_dir2, same_dir3, same_dir4 = check_edge_connection(cycles, possibility)
                
                if possibility[2] == possibility[3] or same_dir1 == 0 or same_dir2 == 0 or same_dir3 == 0 or same_dir4 == 0:
                    remove_possibilities.append(possibility_idx)
                elif same_dir1 == same_dir2 and same_dir3 == same_dir4:
                    remove_possibilities.append(possibility_idx)
                    best_move = possibility
                    break
                
        if best_move is None: break           
        for i in reversed(remove_possibilities):
            del(possibilities[i])
        make_move(cycles, best_move)
        new_moves = new_possibilities(distance_matrix, cycles, best_move)
        possibilities = sorted(list(set(possibilities).union(set(new_moves))), key = lambda x: x[0])
    return cycles