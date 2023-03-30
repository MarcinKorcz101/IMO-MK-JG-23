from matplotlib import pyplot as plt
import numpy as np

def calc_distance_matrix(nodes):
    N = len(nodes)
    distance_matrix = np.zeros(shape=(N, N)).tolist()

    for i in range(N):
        for j in range(i + 1, N):
            d = np.sqrt((nodes[i][0] - nodes[j][0]) ** 2 + (nodes[i][1] - nodes[j][1]) ** 2)
            distance_matrix[i][j] = distance_matrix[j][i] = np.round(d)
    return distance_matrix

def read(name):
        nodes = []
        with open(name, "r") as file:
            for i, line in enumerate(file):
                if line == "EOF\n": break
                if i >= 6:
                    _, x, y = line.split()
                    nodes.append([int(x), int(y)])

        return calc_distance_matrix(nodes)

def calc_cycle_length(distance_matrix, cycle):
    cyc_len = 0.0

    for i in range(len(cycle)):
        if i == len(cycle) - 1: cyc_len += distance_matrix[cycle[0]][cycle[-1]]
        else: cyc_len += distance_matrix[cycle[i]][cycle[i + 1]]

    return cyc_len

def prepare_plot_data(self):
    x = [node.x for node in self.nodes]
    y = [node.y for node in self.nodes]

    first_cycle_x = [self.nodes[node].x for node in self.first_cycle]
    first_cycle_y = [self.nodes[node].y for node in self.first_cycle]
    first_cycle_x.append(self.nodes[self.first_cycle[0]].x)
    first_cycle_y.append(self.nodes[self.first_cycle[0]].y)

    second_cycle_x = [self.nodes[node].x for node in self.second_cycle]
    second_cycle_y = [self.nodes[node].y for node in self.second_cycle]
    second_cycle_x.append(self.nodes[self.second_cycle[0]].x)
    second_cycle_y.append(self.nodes[self.second_cycle[0]].y)

    return x, y, first_cycle_x, first_cycle_y, second_cycle_x, second_cycle_y

def plot_result(self, title):
    x, y, first_cycle_x, first_cycle_y, second_cycle_x, second_cycle_y = self.prepare_plot_data()
    fig, ax = plt.subplots()
    ax.scatter(x, y, color='black')
    ax.set_xlabel("X coordinates")
    ax.set_ylabel("Y coordinates")
    ax.plot(first_cycle_x, first_cycle_y, 'blue')
    ax.plot(second_cycle_x, second_cycle_y, 'red')
    ax.set_title(title)
    plt.show()
