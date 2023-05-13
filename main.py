from lab1.GreedyAlgorithms import GreedyAlgorithms
import numpy as np
import json
from tqdm import tqdm
from time import time

def computational_experiment():
    methods = ['regret']
    instances = ['lab3/kroA200.tsp', 'lab3/kroB200.tsp']

    results = {}
    times = {}
    for method in methods:
        for instance in instances:
            experiment = []
            mes_times = []
            best_x, best_y = None, None

            for _ in tqdm(range(10)):
                start_time = time()
                ga = GreedyAlgorithms(instance, show_plot = False)
                ga.read()
                distance, x, y = ga.run(method)
                experiment.append(distance)
                mes_times.append(time() - start_time)
                if distance == min(experiment):
                    best_x = x
                    best_y = y
                    ga.save_result(f'TwoRegret-{instance.split("/")[-1].split(".")[0]}')
            results[method + instance] = [np.mean(experiment), min(experiment), max(experiment), best_x, best_y]
            times[method + instance] = [np.mean(mes_times), min(mes_times), max(mes_times)]

    with open("results.json", "w") as f:
        json.dump(results, f)
        json.dump(times, f)

if __name__ == '__main__':
    # ga = GreedyAlgorithms('lab1/kroa100.tsp', show_plot = True)
    # ga.read()
    # ga.run('regret') # specify method - one of [nearest neighbour, cycle, regret]
    # ga.run('cycle')
    # ga.run('regret')
    computational_experiment()