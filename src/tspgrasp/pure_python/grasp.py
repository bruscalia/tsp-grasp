import time

import numpy as np

from tspgrasp.pure_python.problem import Problem
from tspgrasp.pure_python.constructive import SemiGreedy
from tspgrasp.pure_python.local_search import LocalSearch
from tspgrasp.solution import Solution


class Grasp:

    def __init__(self, alpha=(0.0, 1.0), max_moves=10000, max_iter=100, time_limit=60, seed=None):
        """GRASP for general TSP

        Parameters
        ----------
        alpha : tuple | float, optional
            Greediness factor (higher is more greedy), by default (0.0, 1.0)

        max_moves : int, optional
            Max moves by local search, by default 10000

        max_iter : int, optional
            Max iterations, by default 100

        time_limit : int, optional
            Time limit, by default 60

        seed : int, optional
            Numpy generator random seed, by default None
        """
        self.alpha = alpha
        self.max_moves = max_moves
        self.max_iter = max_iter
        self.time_limit = time_limit
        self.seed = seed
        self.costs = []

    def solve(self, D: np.ndarray, target=-np.inf) -> Solution:
        """Solves a TSP based on a generic 2-dimensional distances matrix

        Parameters
        ----------
        D : np.ndarray
            2-dimensional distances matrix

        target : float, optional
            Target to stop solution, by default -np.inf

        Returns
        -------
        Solution
            Results with properties:
            - tour : List[int] (depot is included twice)
            - cost : float
        """

        # Initialize problem
        n_nodes = D.shape[0]
        assert D.shape[0] == D.shape[1], "D must be a squared matrix"
        problem = Problem(n_nodes, D)

        # Initialize operators
        constructive = SemiGreedy(problem, alpha=self.alpha, seed=self.seed)
        local_search = LocalSearch(problem.D, max_iter=self.max_moves, seed=self.seed)

        # Initialize parameters
        best_cost = np.inf
        sol = None
        start_time = time.time()

        # Do main loop
        for _ in range(self.max_iter):

            # Break if exceeds time limit
            current_time = time.time()
            time_consumed = current_time - start_time
            if time_consumed > self.time_limit:
                break

            constructive.do()
            local_search.do(constructive.tour)
            self.costs.append(constructive.tour.cost)

            # Replace if it overcomes best so far
            if constructive.tour.cost < best_cost:
                sol = Solution(constructive.tour)
                best_cost = sol.cost

                # Break if better than target
                if best_cost <= target:
                    break

        return sol
