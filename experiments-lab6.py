from lab6.greedy_modified import greedy_local_search, calculate_similarity
from lab6.algorithm_utils import *
import random
from lab6.utils import read_file, read_best_solutions, plot_result
from tqdm import tqdm
import matplotlib.pyplot as plt

def run_experiments(N = 1000):
    instances = ['kroa100.tsp', 'krob100.tsp']
    # instances = ['kroa100.tsp']
    for instance in instances:
        cycles = []
        best_sol_len = float('inf')
        best_sol = None
        best_idx = None
        lengths = []
        distance_matrix, nodes = read_file(instance)
        for i in tqdm(range(N)):
            cycle = greedy_local_search(distance_matrix, nodes)
            length = calc_cycles_length(distance_matrix, cycle)
            lengths.append(length)
            if length < best_sol_len:
                best_sol_len = length
                best_sol = cycle
                best_idx = i
            cycles.append(cycle)
        print("best solution for ", instance, " is ", best_sol_len)

        similarities_vert = np.ones((N, N))
        similarities_edge = np.ones((N, N))
        
        for i in range(N):
            for j in range(N):
                if i == j:
                    continue
                similarities_vert[i,j] = (calculate_similarity(cycles[i], cycles[j]))
                similarities_edge[i,j] = (calculate_similarity(cycles[i], cycles[j], edges=True))
        # print(similarities_vert)
        mean_similarity_vert = np.mean(similarities_vert, axis=1)
        mean_similarity_edge = np.mean(similarities_edge, axis=1)
        optimal_similarity_vert = similarities_vert[best_idx, :]
        optimal_similarity_edge = similarities_edge[best_idx, :]
        # print(np.corrcoef(mean_similarity_vert, lengths))
        corr_vert = np.corrcoef(mean_similarity_vert, lengths)[1,0]
        corr_edge = np.corrcoef(mean_similarity_edge, lengths)[1,0]
        fig, ax = plt.subplots(1,2, figsize=(12,5))
        print(len(lengths), len(mean_similarity_vert))
        print(lengths)
        print(mean_similarity_vert)
        ax[0].scatter(lengths, mean_similarity_vert)
        ax[0].set_title(f"verticies (corr = {round(corr_vert,4)})")
        ax[0].set(xlabel="Distance", ylabel="Mean similarity")

        ax[1].scatter(lengths, mean_similarity_edge)
        ax[1].set_title(f"edge (corr = {round(corr_edge,4)})")
        ax[1].set(xlabel="Distance", ylabel="Mean similarity")

        fig.suptitle(f"Mean similarity vs distance | {instance}")
        fig.savefig("plots/mean_similarity_vs_distance_" + instance + ".png")

        # correlation to optimal
        lengths_no_opt = lengths.copy()
        lengths_no_opt.pop(best_idx)
        optimal_similarity_vert_no_opt = optimal_similarity_vert.copy()
        optimal_similarity_vert_no_opt = np.delete(optimal_similarity_vert_no_opt, best_idx)
        optimal_similarity_edge_no_opt = optimal_similarity_edge.copy()
        optimal_similarity_edge_no_opt = np.delete(optimal_similarity_edge_no_opt, best_idx)
        corr_vert = np.corrcoef(optimal_similarity_vert_no_opt, lengths_no_opt)[1,0]
        corr_edge = np.corrcoef(optimal_similarity_edge_no_opt, lengths_no_opt)[1,0]
        fig, ax = plt.subplots(1,2, figsize=(12,5))
        ax[0].scatter(lengths_no_opt, optimal_similarity_vert_no_opt)
        ax[0].set_title(f"verticies (corr = {round(corr_vert,4)})")
        ax[0].set(xlabel="Distance", ylabel="Mean similarity")

        ax[1].scatter(lengths_no_opt, optimal_similarity_edge_no_opt)
        ax[1].set_title(f"edge (corr = {round(corr_edge,4)})")
        ax[1].set(xlabel="Distance", ylabel="Mean similarity")

        fig.suptitle(f"Similarity to optimal vs distance | {instance}")
        fig.savefig("plots/similarity_to_optimal_vs_distance_" + instance + ".png")


if __name__ == '__main__':
    run_experiments(1000)