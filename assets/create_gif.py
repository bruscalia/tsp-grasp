import os
from PIL import Image
from typing import List

import numpy as np
from scipy.spatial.distance import squareform, pdist
import matplotlib.pyplot as plt

from tspgrasp.pypure.constructive import HistoryGreedy
from tspgrasp.pypure.local_search import HistoryLS


def plot_frame(coordinates, solution):
    fig, ax = plt.subplots(figsize=[3, 3], dpi=300)
    tour = np.array(solution, dtype=int)
    ax.scatter(coordinates[:, 0], coordinates[:, 1], color="#C80033", s=4)  #FF4EBF
    ax.plot(coordinates[tour, 0], coordinates[tour, 1], color="#C80033")
    plt.axis('off')
    fig.tight_layout()


def create_gif(output: str, files: List[str], duration=50, **kwargs):
    frames = []
    for image_path in files:
        image = Image.open(image_path)
        frames.append(image)
    frames[0].save(output, save_all=True, append_images=frames[1:],
                   duration=duration, disposal=2, **kwargs)


if __name__ == "__main__":

    np.random.seed(12)

    # Initialize data
    N = 200
    X = np.random.random((N, 2)) * np.array([[1, 1]])
    D = squareform(pdist(X))

    # Greedy phase
    greedy = HistoryGreedy(seed=12)
    sol_greedy = greedy(D)

    # Local search
    ls = HistoryLS(seed=12)
    ls(sol_greedy.tour[:-1], D)

    greedy_frames = []
    for j, s in enumerate(greedy.history):
        plot_frame(X, s[:-1])
        filename = f"tmp/greedy_frame_{j}.png"
        greedy_frames.append(filename)
        plt.savefig(filename, transparent=True, dpi=300)
        plt.close()

    plot_frame(X, ls.history[0])
    filename = f"tmp/greedy_frame_{j + 1}.png"
    greedy_frames.append(filename)
    plt.savefig(filename, transparent=True, dpi=300)
    plt.close()

    ls_frames = []
    for j, s in enumerate(ls.history):
        plot_frame(X, s)
        filename = f"tmp/ls_frame_{j}.png"
        ls_frames.append(filename)
        plt.savefig(filename, transparent=True, dpi=300)
        plt.close()

    # Save last frame from LS
    plt.savefig("solution.png", transparent=True, dpi=300)

    # Step 2: Convert PNGs into GIF
    create_gif('greedy.gif', greedy_frames, duration=30)
    create_gif('ls.gif', ls_frames, duration=150)

    # Optionally, remove the PNGs to cleanup
    for png_file in greedy_frames:
        os.remove(png_file)
    for png_file in ls_frames:
        os.remove(png_file)
