from matplotlib import pyplot as plt
import numpy as np
import json

def calc_cycle_length(distance_matrix, cycle):
    cyc_len = 0.0
    # print(cycle)
    for i in range(len(cycle)):
        # print(i)
        if i == len(cycle) - 1: 
            cyc_len += distance_matrix[cycle[0]][cycle[-1]]
        else: 
            cyc_len += distance_matrix[cycle[i]][cycle[i + 1]]

    return cyc_len

def calc_cycles_length(distance_matrix, cycles):
    return calc_cycle_length(distance_matrix, cycles[0]) + calc_cycle_length(distance_matrix, cycles[1])

def calc_distance_matrix(nodes):
    N = len(nodes)
    distance_matrix = np.zeros(shape=(N, N)).tolist()

    for i in range(N):
        for j in range(i + 1, N):
            d = np.sqrt((nodes[i][0] - nodes[j][0]) ** 2 + (nodes[i][1] - nodes[j][1]) ** 2)
            distance_matrix[i][j] = distance_matrix[j][i] = np.round(d)
    return distance_matrix

def read_file(name):
    nodes = []
    with open(name, "r") as file:
        for i, line in enumerate(file):
            if line == "EOF\n": break
            if i >= 6:
                _, x, y = line.split()
                nodes.append([int(x), int(y)])

    return calc_distance_matrix(nodes), nodes

def read_best_solutions(name):
    with open(name, 'r') as f:
        solutions = json.load(f)

    return solutions

def prepare_plot_data(cycle1, cycle2, nodes):
    x = [nodes[i][0] for i in range(len(nodes))]
    y = [nodes[i][1] for i in range(len(nodes))]

    first_cycle_x = [nodes[i][0] for i in cycle1]
    first_cycle_x.append(nodes[cycle1[0]][0])
    first_cycle_y = [nodes[i][1] for i in cycle1]
    first_cycle_y.append(nodes[cycle1[0]][1])
    second_cycle_x = [nodes[i][0] for i in cycle2]
    second_cycle_x.append(nodes[cycle2[0]][0])
    second_cycle_y = [nodes[i][1] for i in cycle2]
    second_cycle_y.append(nodes[cycle2[0]][1])

    return x, y, first_cycle_x, first_cycle_y, second_cycle_x, second_cycle_y

def plot_result(title, cycle1, cycle2, nodes):
    x, y, first_cycle_x, first_cycle_y, second_cycle_x, second_cycle_y = prepare_plot_data(cycle1, cycle2, nodes)
    fig, ax = plt.subplots()
    ax.scatter(x, y, color='black')
    ax.set_xlabel("X coordinates")
    ax.set_ylabel("Y coordinates")
    ax.plot(first_cycle_x, first_cycle_y, 'blue')
    ax.plot(second_cycle_x, second_cycle_y, 'red')
    ax.set_title(title)
    plt.show()


def save_result(title, cycle1, cycle2, nodes):
    x, y, first_cycle_x, first_cycle_y, second_cycle_x, second_cycle_y = prepare_plot_data(cycle1, cycle2, nodes)
    fig, ax = plt.subplots()
    ax.scatter(x, y, color='black')
    ax.set_xlabel("X coordinates")
    ax.set_ylabel("Y coordinates")
    ax.plot(first_cycle_x, first_cycle_y, 'blue')
    ax.plot(second_cycle_x, second_cycle_y, 'red')
    ax.set_title(title)
    # plt.show()
    plt.savefig(f"plots/{title}.png")
    plt.close()