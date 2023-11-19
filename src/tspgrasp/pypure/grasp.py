import numpy as np

from tspgrasp.base import BaseGrasp
from tspgrasp.pypure.constructive import CheapestArc
from tspgrasp.pypure.local_search import LocalSearch
from tspgrasp.pypure.problem import Problem
from tspgrasp.solution import Solution


MAX_MOVES = 100000
MAX_ITER = 10000


class GrasPy(BaseGrasp):

    def __init__(self, constructive=None, local_search=None, seed=None):
        self.seed = seed
        self.costs = []
        if constructive is None:
            constructive = CheapestArc(seed=seed)
        if local_search is None:
            local_search = LocalSearch(seed=seed)
        self.constructive = constructive
        self.local_search = local_search

    def __call__(
        self,
        D: np.ndarray,
        max_iter: int = MAX_ITER,
        max_moves: int = MAX_MOVES,
        time_limit: float = float("inf"),
        target: float = -float("inf"),
        verbose: bool = False
    ) -> Solution:
        # Initialize problem
        n_nodes = D.shape[0]
        assert D.shape[0] == D.shape[1], "D must be a squared matrix"
        problem = Problem(n_nodes, D)
        sol = self.solve(
            problem,
            max_iter=max_iter,
            max_moves=max_moves,
            time_limit=time_limit,
            target=target,
            verbose=verbose
        )
        return sol
