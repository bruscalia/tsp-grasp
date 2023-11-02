import os
from PIL import Image
from typing import List

import numpy as np
from scipy.spatial.distance import squareform, pdist
import matplotlib.pyplot as plt

from tspgrasp import Grasp


def plot_frame(coordinates, solution):
    fig, ax = plt.subplots(figsize=[6.4, 3.2], dpi=300)
    tour = np.array(solution, dtype=int)
    ax.scatter(coordinates[:, 0], coordinates[:, 1], color="#C80033", s=4)  #FF4EBF
    ax.plot(coordinates[tour, 0], coordinates[tour, 1], color="#C80033")
    plt.axis('off')
    fig.tight_layout()


if __name__ == "__main__":

    np.random.seed(12)

    # Initialize data
    N = 1000
    X = np.random.random((N, 2)) * np.array([[6.4, 3.2]])
    D = squareform(pdist(X))

    # Grasp
    grasp = Grasp(seed=12)
    sol = grasp(D, time_limit=60)

    # Save last frame from LS
    plot_frame(X, sol.tour)
    plt.savefig("cover.png", transparent=True, dpi=300)
