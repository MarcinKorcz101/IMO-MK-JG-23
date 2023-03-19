from lab1.GreedyAlgorithms import GreedyAlgorithms
import numpy as np
import json

def computational_experiment():
    methods = ['nearest neighbour', 'cycle', 'regret']
    instances = ['lab1/kroa100.tsp', 'lab1/krob100.tsp']

    results = {}

    for method in methods:
        for instance in instances:
            experiment = []
            best_x, best_y = None, None

            for _ in range(100):
                ga = GreedyAlgorithms(instance, show_plot = False)
                ga.read()
                distance, x, y = ga.run(method)
                experiment.append(distance)
                if distance == min(experiment):
                    best_x = x
                    best_y = y

            results[method + instance] = [np.mean(experiment), min(experiment), max(experiment), best_x, best_y]

    with open("results.json", "w") as f:
        json.dump(results, f)

if __name__ == '__main__':
    # ga = GreedyAlgorithms('lab1/kroa100.tsp')
    # ga.read()
    # ga.run('nearest neighbour') # specify method - one of [nearest neighbour, cycle, regret]
    # ga.run('cycle')
    # ga.run('regret')
    computational_experiment()