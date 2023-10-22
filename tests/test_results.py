import json

import numpy as np
from scipy.spatial.distance import pdist, squareform

from tspgrasp import Grasp, Problem


def test_1():
    with open("test_1.json", mode="r", encoding="utf8") as file:
        data = json.load(file)
    problem = Problem(data["n_points"], np.array(data["distances"]))
    grasp = Grasp(alpha=data["alpha"], seed=data["seed"], time_limit=100, max_moves=10000, max_iter=3)
    sol = grasp.solve(problem)
    assert sol.solution == data["tour"], "Tour different from original"
    assert sol.cost == data["cost"], "Cost different from original"


def test_2():
    with open("test_2.json", mode="r", encoding="utf8") as file:
        data = json.load(file)
    problem = Problem(data["n_points"], np.array(data["distances"]))
    grasp = Grasp(alpha=data["alpha"], seed=data["seed"], time_limit=100, max_moves=10000, max_iter=3)
    sol = grasp.solve(problem)
    assert sol.solution == data["tour"], "Tour different from original"
    assert sol.cost == data["cost"], "Cost different from original"


def create_problem(filename, n_points, alpha, seed):
    np.random.seed(seed)
    X = np.random.random((n_points, 2))
    D = np.round(squareform(pdist(X)), decimals=8)
    pdata = {
        "n_points": n_points,
        "distances": D.tolist(),
        "alpha": alpha,
        "seed": seed
    }

    problem = Problem(n_points, D)
    grasp = Grasp(alpha=alpha, seed=seed, time_limit=100, max_moves=10000, max_iter=3)
    sol = grasp.solve(problem)
    pdata["tour"] = sol.solution
    pdata["cost"] = sol.cost
    with open(filename, mode="w", encoding="utf8") as file:
        json.dump(pdata, file)


if __name__ == "__main__":
    create_problem("test_1.json", 50, 1.0, 12)
    create_problem("test_2.json", 50, [0.2, 1.0], 42)
