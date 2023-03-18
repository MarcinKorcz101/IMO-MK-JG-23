from matplotlib import pyplot as plt
import numpy as np

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class GreedyAlgorithms:
    def __init__(self, instance):
        self.instance = instance # instance file name
        self.distance_matrix = None
        self.N = 0 # number of nodes
        self.nodes, self.first_cycle, self.second_cycle = [], [], []

    def read(self):
        with open(self.instance, "r") as file:
            for i, line in enumerate(file):
                if line == "EOF\n": break
                if i >= 6:
                    _, x, y = line.split()
                    node = Node(int(x), int(y))
                    self.nodes.append(node)

        self.N = len(self.nodes)
        self.calc_distance_matrix()
    
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
        ax.set_xlabel("X coordisntes")
        ax.set_ylabel("Y coordisntes")
        ax.plot(first_cycle_x, first_cycle_y, 'blue')
        ax.plot(second_cycle_x, second_cycle_y, 'red')
        ax.set_title(title)
        plt.show()

    def calc_distance_matrix(self):
        self.distance_matrix = np.zeros(shape=(self.N, self.N)).tolist()

        for i in range(self.N):
            for j in range(i + 1, self.N):
                d = np.sqrt((self.nodes[i].x - self.nodes[j].x) ** 2 + (self.nodes[i].y - self.nodes[j].y) ** 2)
                self.distance_matrix[i][j] = self.distance_matrix[j][i] = np.round(d)

    def calc_cycle_length(self, cycle):
        cyc_len = 0.0

        for i in range(len(cycle)):
            if i == len(cycle) - 1: cyc_len += self.distance_matrix[cycle[0]][cycle[-1]]
            else: cyc_len += self.distance_matrix[cycle[i]][cycle[i + 1]]

        return cyc_len

    def choose_nodes(self):
        a = np.random.randint(0, self.N - 1)
        b = None
        max_distance = np.NINF
        
        for node in range(self.N):
            if a != node:
                distance = self.distance_matrix[a][node]

                if distance > max_distance:
                    max_distance = distance
                    b = node
                    
        self.first_cycle = [a]
        self.second_cycle = [b]

    def choose_k_nodes(self, cycle, node, k):
        distances = []
        min_distance = np.Inf

        for n in range(1, len(cycle) + 1):
            new_cycle = cycle.copy()
            new_cycle.insert(n, node)
            distance = self.calc_cycle_length(new_cycle)
            distances.append(distance)

            if distance < min_distance:
                min_distance = distance
                new_position = n

        return sorted(distances)[:k], new_position

    def nearest_cycle_node(self, node, nodes_in_cycles, cycle):
        new_node = None
        min_distance = np.Inf

        for n in range(self.N):
            if n != node and n not in nodes_in_cycles:
                distances, position = self.choose_k_nodes(cycle, n, k=1)

                if distances[0] < min_distance:
                    min_distance = distances[0]
                    new_node = n
                    new_position = position

        return new_node, new_position

    def nearest_node(self, node, used_nodes):
        nearest_node, min_distance = None, None
        
        for n in range(self.N):
            if n != node and n not in used_nodes:
                
                if min_distance is None:
                    min_distance = self.distance_matrix[node][n]
                    nearest_node = n
                else:
                    distance = self.distance_matrix[node][n]

                    if distance < min_distance:
                        nearest_node = n
                        min_distance = distance

        return nearest_node

    def add_to_cycle(self, node, cycle_number):
        if cycle_number == 1: cycle = self.first_cycle.copy()
        elif cycle_number == 2: cycle = self.second_cycle.copy()

        for new_node_index in range(1, len(cycle) + 1):
            new_cycle = cycle.copy()
            new_cycle.insert(new_node_index, node)
            distance = self.calc_cycle_length(new_cycle)

            if new_node_index == 1:
                min_distance = distance
                best_insertion = new_node_index
            else:
                if distance < min_distance:
                    min_distance = distance
                    best_insertion = new_node_index

        if cycle_number == 1: self.first_cycle.insert(best_insertion, node)
        elif cycle_number == 2: self.second_cycle.insert(best_insertion, node)

    def nn_greedy(self, nodes_in_cycles, last_first_nearest_node, last_second_nearest_node):
        for _ in range(int(self.N / 2) - 1):
            first_nearest_node = self.nearest_node(last_first_nearest_node, nodes_in_cycles)
            nodes_in_cycles.append(first_nearest_node)
            self.add_to_cycle(first_nearest_node, 1)
            last_first_nearest_node = first_nearest_node

            second_nearest_node = self.nearest_node(last_second_nearest_node, nodes_in_cycles)
            nodes_in_cycles.append(second_nearest_node)
            self.add_to_cycle(second_nearest_node, 2)
            last_second_nearest_node = second_nearest_node

        if self.N % 2 == 1:
            first_nearest_node = self.nearest_node(last_first_nearest_node, nodes_in_cycles)
            nodes_in_cycles.append(first_nearest_node)
            self.add_to_cycle(first_nearest_node, 1)

        self.plot_result("Cycles created with the Nearest Neighbor approach")
        print('Total length of both cycles: {}'.format(self.calc_cycle_length(self.first_cycle) + self.calc_cycle_length(self.second_cycle)))

    def cycle_greedy(self, nodes_in_cycles, last_first_nearest_node, last_second_nearest_node):
        for _ in range(int(self.N / 2) - 1):
            first_nearest_node, ins = self.nearest_cycle_node(last_first_nearest_node, nodes_in_cycles, self.first_cycle)
            self.first_cycle.insert(ins, first_nearest_node)
            nodes_in_cycles.append(first_nearest_node)

            second_nearest_node, ins2 = self.nearest_cycle_node(last_second_nearest_node, nodes_in_cycles, self.second_cycle)
            self.second_cycle.insert(ins2, second_nearest_node)
            nodes_in_cycles.append(second_nearest_node)

            last_first_nearest_node = first_nearest_node
            last_second_nearest_node = second_nearest_node

        if self.N % 2 == 1:
            first_nearest_node = self.nearest_node(last_first_nearest_node, nodes_in_cycles)
            nodes_in_cycles.append(first_nearest_node)
            self.add_to_cycle(first_nearest_node, 1)

        self.plot_result("Cycles created with the Greedy Cycle approach")
        print('Total length of both cycles: {}'.format(self.calc_cycle_length(self.first_cycle) + self.calc_cycle_length(self.second_cycle)))

    def regret_greedy():
        pass

    def run(self, method):
        self.choose_nodes()
        last_first_nearest_node = self.first_cycle[0]
        last_second_nearest_node = self.second_cycle[0]
        nodes_in_cycles = [last_first_nearest_node, last_second_nearest_node]

        if method in ['nearest neighbour']: self.nn_greedy(nodes_in_cycles, last_first_nearest_node, last_second_nearest_node)
        elif method in ['cycle']: self.cycle_greedy(nodes_in_cycles, last_first_nearest_node, last_second_nearest_node)
        elif method in ['regret']: self.regret_greedy()
        else:
            print("Method not supported")
            return