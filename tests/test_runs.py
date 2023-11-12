import pytest

# Imports
import numpy as np
from scipy.spatial.distance import pdist, squareform
from tspgrasp import (
    Grasp, CheapestArc, SemiGreedyArc, CheapestInsertion, RandomInsertion,
    SemiGreedyInsertion, LocalSearch, SimulatedAnnealing,
)


np.random.seed(12)
X = np.random.random((50, 2))
D = squareform(pdist(X))


def test_grasp_normal():
    grasp = Grasp(seed=12)
    sol = grasp(D, max_iter=3)
    assert sol is not None, "Grasp failed"


def test_repeated_results():
    grasp = Grasp(seed=12)
    sol = grasp(D, max_iter=3)
    grasp = Grasp(seed=12)
    sol2 = grasp(D, max_iter=3)
    assert sol.cost == sol2.cost, "Random seed failed to produce repeated results"


def test_ls():
    ls = LocalSearch(seed=12)
    sol = ls(list(range(D.shape[0])), D)
    assert sol is not None, "Local Search failed"


def test_sa():
    ls = SimulatedAnnealing(T_start=0.1, T_final=1e-4, decay=0.99, seed=12)
    sol = ls(list(range(D.shape[0])), D)
    assert sol is not None, "Simulated Annealing failed"


def test_greedy():
    greedy = CheapestArc(seed=12)
    sol = greedy(D)
    assert sol is not None, "Greedy failed"


@pytest.mark.parametrize('constructive', [CheapestInsertion, RandomInsertion])
def test_insertion(constructive):
    greedy = constructive(seed=12)
    sol = greedy(D)
    assert sol is not None, "Semi-greedy failed"


@pytest.mark.parametrize('constructive', [SemiGreedyInsertion, SemiGreedyArc])
@pytest.mark.parametrize('alpha', [0.0, 0.5, 1.0, (0.0, 1.0), (0.5, 0.9)])
def test_semigreedy(constructive, alpha):
    greedy = constructive(alpha=alpha, seed=12)
    sol = greedy(D)
    assert sol is not None, "Semi-greedy failed"


@pytest.mark.parametrize('constructive', [SemiGreedyInsertion, SemiGreedyArc])
@pytest.mark.parametrize('alpha', [0.0, 0.5, 1.0, (0.0, 1.0), (0.5, 0.9)])
def test_grasp_with_semi(constructive, alpha):
    greedy = constructive(alpha=alpha, seed=12)
    grasp = Grasp(constructive=greedy, seed=12)
    sol = grasp(D, max_iter=3)
    assert sol is not None, "Grasp with Semi-greedy failed"


def test_grasp_with_sa():
    ls = SimulatedAnnealing(T_start=0.1, T_final=1e-4, decay=0.99, seed=12)
    grasp = Grasp(local_search=ls, seed=12)
    sol = grasp(D, max_iter=3)
    assert sol is not None, "Grasp with Simulated Annealing failed"


@pytest.mark.parametrize('alpha', [0.0, 0.5, (0.5, 0.9)])
def test_different_results(alpha):
    greedy = CheapestArc(seed=12)
    sol1 = greedy(D)
    sgreedy = SemiGreedyArc(alpha=alpha, seed=12)
    sol2 = sgreedy(D)
    assert sol1.cost != sol2.cost, "Greedy and SemiGreedyArc are the same!"


def test_ls_vs_sa():
    sa = SimulatedAnnealing(T_start=0.1, T_final=1e-4, decay=0.99, seed=12)
    sol1 = sa(list(range(D.shape[0])), D)
    ls = LocalSearch(seed=12)
    sol2 = ls(list(range(D.shape[0])), D)
    assert sol1.cost != sol2.cost, "LS and SA are the same!"
