# Ocena ruchów z poprzednich iteracji
from algorithm_utils import get_node_pair, get_between_cycles_node_pair, delta_between_cycles_node_exchange, delta_inside_cycle_edge_exchange, exchange_edge_in_cycle, exchange_nodes_between_cycles

def get_node_pair_delta(cycles, distance_matrix):
    possibilities = []
    for cycle_idx, cycle in enumerate(cycles):
        for node1 in range(len(cycle)):
            for node2 in range(node1 + 1, len(cycle)):
                delta = delta_inside_cycle_edge_exchange(distance_matrix, cycles[cycle_idx], [cycle[node1], cycle[node2]])
                node1_next = 0 if node1+1 >= len(cycle) else node1+1
                node2_next = 0 if node2+1 >= len(cycle) else node2+1
                # if delta > 0: possibilities.append(([cycle[node1], cycle[node2]], delta_inside_cycle_edge_exchange, cycle_idx, delta, [cycle[node1_next]], [cycle[node2_next]]))
                if delta < 0: 
                    possibilities.append(([cycle[node1], cycle[node2]], delta_inside_cycle_edge_exchange, cycle_idx, delta, [cycle[node1_next]], [cycle[node2_next]]))
    return possibilities

def get_between_cycles_node_pair_delta(cycles, distance_matrix):
    possibilities = []
    for node1 in range(len(cycles[0])):
        for node2 in range(len(cycles[1])):
            delta = delta_between_cycles_node_exchange(distance_matrix, cycles, [cycles[0][node1], cycles[1][node2]])
            
            next1 = cycles[0][0] if node1+1 >= len(cycles[0]) else cycles[0][node1+1]
            next2 = cycles[1][0] if node2+1 >= len(cycles[1]) else cycles[1][node2+1]

            prev1 = cycles[0][node1-1]
            prev2 = cycles[1][node2-1]

            if delta < 0: 
                possibilities.append(([cycles[0][node1], cycles[1][node2]], delta_between_cycles_node_exchange, None, delta, [prev1, next1], [prev2, next2]))
            # if delta > 0: possibilities.append(([cycles[0][node1], cycles[1][node2]], delta_between_cycles_node_exchange, None, delta, [prev1, next1], [prev2, next2]))
    return possibilities

def get_prev_next(cycles, node):
    for cycle in cycles:
        if node in cycle:
            idx = cycle.index(node)
            prev_n = cycle[idx-1]
            next_n = cycle[0] if idx+1 >= len(cycle) else cycle[idx+1]
            return prev_n, next_n

def new_possibilities(possibility, cycles, distance_matrix):
    _, action, _, _, _, _ = possibility
    if action == delta_inside_cycle_edge_exchange:
        return get_node_pair_delta(cycles, distance_matrix)
    elif action == delta_between_cycles_node_exchange:
        return get_between_cycles_node_pair_delta(cycles, distance_matrix)
    else:
        ValueError("Fatal error")

def new_possibilities_2(possibility, cycles, distance_matrix):
    nodes, action, _, _, _, _ = possibility
    new_moves = []
    if action == delta_inside_cycle_edge_exchange:

        return get_node_pair_delta(cycles, distance_matrix)
    elif action == delta_between_cycles_node_exchange:
        for x in cycles[0]:
            delta = delta_between_cycles_node_exchange(distance_matrix, cycles, [x, nodes[1]])
            if delta < 0:
                node1 = x
                node2 = nodes[1]
                
                next1 = cycles[0][0] if node1+1 >= len(cycles[0]) else cycles[0][node1+1]
                next2 = (cycles[0].index(node2)+1)%len(cycles[0])

                prev1 = cycles[0][node1-1]
                prev2 = cycles[1][node2-1]
                new_moves.append(([x, nodes[1]], delta_between_cycles_node_exchange, None, delta, [prev1, next1], [prev2, next2]))
        for x in cycles[1]:
            delta = delta_between_cycles_node_exchange(distance_matrix, cycles, [nodes[0], x])
            if delta < 0:
                next1 = cycles[1][0] if node1+1 >= len(cycles[0]) else cycles[0][node1+1]
                next2 = cycles[1][0] if node2+1 >= len(cycles[1]) else cycles[1][node2+1]

                prev1 = cycles[0][node1-1]
                prev2 = cycles[1][node2-1]
                new_moves.append(([nodes[0], x], delta_between_cycles_node_exchange, None, delta, [cycles[0][cycles[0].index(nodes[0])-1], cycles[0][(cycles[0].index(nodes[0])+1)%len(cycles[0])]], [cycles[1][cycles[1].index(x)-1], cycles[1][(cycles[1].index(x)+1)%len(cycles[1])]]))
        # return get_between_cycles_node_pair_delta(cycles, distance_matrix
        return new_moves
    else:
        ValueError("Fatal error")


def check_all_edges(cycles, a, b):
    for i in range(2):
        status = check_edge(cycles[i], a, b)
        if status != 0: return i, status
    return None, 0

def check_edge(cycle, a, b):
    for i in range(len(cycle) - 1):
        x, y = cycle[i], cycle[i+1]
        if (a, b) == (x, y): return +1
        if (a, b) == (y, x): return -1

    x, y = cycle[-1], cycle[0]
    if (a, b) == (x, y): return +1
    if (a, b) == (y, x): return -1
    return 0

def moves_rate(cycles, distance_matrix):
    possibilities = get_node_pair_delta(cycles, distance_matrix)
    possibilities.extend(get_between_cycles_node_pair_delta(cycles, distance_matrix))
    possibilities.sort(key = lambda x: x[3])
    # print(possibilities)
    while True:
        new_move = None
        # print(len(possibilities))
        to_remove = []
        if len(possibilities) == 0: break
        for idx_possibility, possibility in enumerate(possibilities):
            # print(possibility)
            nodes, action, cycle_idx, _, connection1, connection2 = possibility
            if action == delta_inside_cycle_edge_exchange:
                cyc_idx1, result_1 = check_all_edges(cycles, nodes[0], connection1)
                cyc_idx2, result_2 = check_all_edges(cycles, nodes[1], connection2)
                
                if cyc_idx1 != cyc_idx2 or result_1 == 0 or result_2 == 0:
                    to_remove.append(idx_possibility)
                elif result_1 == result_2 == 1:
                    new_move = possibility  
                    to_remove.append(idx_possibility)
                    break
                elif result_1 == result_2 == -1:
                    new_move = possibility  
                    to_remove.append(idx_possibility)
                    break
                
            elif action == delta_between_cycles_node_exchange:
                result_1 = check_edge(cycles[0], connection1[0], nodes[0])
                result_2 = check_edge(cycles[0], nodes[0], connection1[1])
                result_3 = check_edge(cycles[1], connection2[0], nodes[1])
                result_4 = check_edge(cycles[1], nodes[1], connection2[1])

                if result_1 == 0 or result_2 == 0 or result_3 == 0 or result_4 == 0:
                    to_remove.append(idx_possibility)
                elif result_1 == result_2 and result_3 == result_4:   
                    new_move = possibility
            else:
                ValueError("Fatal error")

        print("TEEEEEEEEEEEST")

        if new_move is None: break
        
        possibilities.extend(new_possibilities_2(possibility, cycles, distance_matrix))

        if new_move[1] == delta_inside_cycle_edge_exchange:
            new_cycle = exchange_edge_in_cycle(cycles[new_move[3]], new_move[0])
            single_cycle = True
            best_cycle_idx = new_move[3]
        elif new_move[1] == delta_between_cycles_node_exchange:
            new_cycles = exchange_nodes_between_cycles(cycles, new_move[0])
            single_cycle = False
            # possibilities.remove(possibility)

        if single_cycle == True:
            cycles[best_cycle_idx] = new_cycle
        elif single_cycle == False:
            cycles = new_cycles
        # print(*reversed(to_remove))
        for x in reversed(to_remove):
            # print(x)
            possibilities.pop(x)

    return cycles