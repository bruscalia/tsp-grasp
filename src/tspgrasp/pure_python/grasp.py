import numpy as np

from tspgrasp.grasp import Grasp as GraspCython
from tspgrasp.pure_python.constructive import SemiGreedy
from tspgrasp.pure_python.local_search import LocalSearch
from tspgrasp.pure_python.problem import Problem
from tspgrasp.solution import Solution


MAX_MOVES = 100000
MAX_ITER = 10000


class GrasPy(GraspCython):

    def __init__(self, alpha=1.0, seed=None):
        self.alpha = alpha
        self.seed = seed
        self.costs = []
        self.constructive = SemiGreedy(alpha=self.alpha, seed=seed)
        self.local_search = LocalSearch(seed=seed)

    def __call__(
        self,
        D: np.ndarray,
        max_iter: MAX_ITER,
        max_moves: MAX_MOVES,
        time_limit: float = float("inf"),
        target: float = -float("inf"),
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
            target=target
        )
        return sol
