import json
import os

import numpy as np
from scipy.spatial.distance import pdist, squareform

from tspgrasp import Grasp


HERE = os.path.dirname(__file__)


def test_1():
    fpath = os.path.join(HERE, "test_1.json")
    with open(fpath, mode="r", encoding="utf8") as file:
        data = json.load(file)
    grasp = Grasp(seed=data["seed"])
    sol = grasp(np.array(data["distances"]), time_limit=100, max_moves=10000, max_iter=3)
    assert sol.tour == data["tour"], "Tour different from original"
    assert sol.cost == data["cost"], "Cost different from original"


def test_2():
    fpath = os.path.join(HERE, "test_2.json")
    with open(fpath, mode="r", encoding="utf8") as file:
        data = json.load(file)
    grasp = Grasp(seed=data["seed"])
    sol = grasp(np.array(data["distances"]), time_limit=100, max_moves=10000, max_iter=3)
    assert sol.tour == data["tour"], "Tour different from original"
    assert sol.cost == data["cost"], "Cost different from original"


def create_problem(filename, n_points, seed):
    np.random.seed(seed)
    X = np.random.random((n_points, 2))
    D = np.round(squareform(pdist(X)), decimals=8)
    pdata = {
        "n_points": n_points,
        "distances": D.tolist(),
        "seed": seed
    }

    grasp = Grasp(seed=seed)
    sol = grasp(np.array(pdata["distances"]), time_limit=100, max_moves=10000, max_iter=3)
    pdata["tour"] = sol.tour
    pdata["cost"] = sol.cost
    with open(filename, mode="w", encoding="utf8") as file:
        json.dump(pdata, file)


if __name__ == "__main__":
    create_problem("test_1.json", 50, 12)
    create_problem("test_2.json", 50, 42)
