import numpy as np
from scipy.spatial.distance import squareform, pdist
import matplotlib.pyplot as plt

from tspgrasp.pypure.constructive import HistoryGreedyArc
from tspgrasp.pypure.local_search import HistoryLS


def plot_frame(coordinates, solution):
    fig, ax = plt.subplots(figsize=[3, 3], dpi=300)
    tour = np.array(solution, dtype=int)
    ax.scatter(coordinates[:, 0], coordinates[:, 1], color="#FF5580", s=4)  #FF4EBF
    ax.plot(coordinates[tour, 0], coordinates[tour, 1], color="#FF5580")
    plt.axis('off')
    fig.tight_layout()


if __name__ == "__main__":

    np.random.seed(12)

    # Initialize data
    N = 300
    X = np.random.random((N, 2)) * np.array([[1, 1]])
    D = squareform(pdist(X))

    # Greedy phase
    greedy = HistoryGreedyArc(seed=12)
    sol_greedy = greedy(D)

    # Local search
    ls = HistoryLS(seed=12)
    ls(sol_greedy.tour[:-1], D)

    # Save last frame from LS
    plot_frame(X, greedy.history[0][:-1])
    plt.savefig("slides/1start.png", transparent=True, dpi=300)

    plot_frame(X, greedy.history[75][:-1])
    plt.savefig("slides/2mid1_greedy.png", transparent=True, dpi=300)

    plot_frame(X, greedy.history[150][:-1])
    plt.savefig("slides/3mid2_greedy.png", transparent=True, dpi=300)

    plot_frame(X, greedy.history[-1])
    plt.savefig("slides/4final_greedy.png", transparent=True, dpi=300)

    plot_frame(X, ls.history[int(len(ls.history) / 2)])
    plt.savefig("slides/5ls_mid.png", transparent=True, dpi=300)

    plot_frame(X, ls.history[-1])
    plt.savefig("slides/6final_ls.png", transparent=True, dpi=300)
