import time

import numpy as np

from tspgrasp.problem import Problem
from tspgrasp.constructive import SemiGreedy
from tspgrasp.local_search import LocalSearch
from tspgrasp.solution import Solution


MAX_MOVES = 100000
MAX_ITER = 10000


class Grasp:

    def __init__(self, alpha=1.0, seed=None):
        """GRASP for general TSP

        Parameters
        ----------
        alpha : tuple | float, optional
            Greediness factor (higher is more greedy), by default 1.0

        seed : int, optional
            Numpy generator random seed, by default None
        """
        self.alpha = alpha
        self.seed = seed
        self.costs = []
        self.constructive = SemiGreedy(alpha=self.alpha, seed=seed)
        self.local_search = LocalSearch(seed=seed)

    def __call__(
        self,
        D: np.ndarray,
        max_iter=MAX_ITER,
        max_moves=MAX_MOVES,
        time_limit: float = float("inf"),
        target: float = -float("inf"),
    ) -> Solution:
        """Solves a TSP based on a generic 2-dimensional distances matrix

        Parameters
        ----------
        D : np.ndarray
            2-dimensional distances matrix

        max_iter : int
            Maximum number of complete iterations, by default 10000

        max_moves : int
            Maximum number of local search moves, by default 100000

        time_limit : float, optional
            Time limit to interrupt the solution, by default float("inf")

        target : float, optional
            Taget value for objective which interrupts optimization process, by default -float("inf")

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
        sol = self.solve(
            problem,
            max_iter=max_iter,
            max_moves=max_moves,
            time_limit=time_limit,
            target=target
        )
        return sol


    def solve(
        self,
        problem: Problem,
        max_iter: MAX_ITER,
        max_moves: MAX_MOVES,
        time_limit: float = float("inf"),
        target: float = -float("inf"),
    ) -> Solution:
        """Solves a TSP based on a generic 2-dimensional distances matrix

        Parameters
        ----------
        problem : Problem
            Instance with attributes `n_nodes` and `D`, a 2-dimensional distances matrix

        max_iter : int
            Maximum number of complete iterations, by default 10000

        max_moves : int
            Maximum number of local search moves, by default 100000

        time_limit : float, optional
            Time limit to interrupt the solution, by default float("inf")

        target : float, optional
            Taget value for objective which interrupts optimization process, by default -float("inf")

        Returns
        -------
        Solution
            Results with properties:
            - tour : List[int] (depot is included twice)
            - cost : float
        """

        # Initialize parameters
        best_cost = np.inf
        sol = None
        start_time = time.time()

        # Do main loop
        for _ in range(max_iter):

            # Break if exceeds time limit
            current_time = time.time()
            time_consumed = current_time - start_time
            if time_consumed > time_limit:
                break

            self.constructive.do(problem)
            self.local_search.do(self.constructive.tour, problem, max_iter=max_moves)
            self.costs.append(self.constructive.tour.cost)

            # Replace if it overcomes best so far
            if self.constructive.tour.cost < best_cost:
                sol = Solution(self.constructive.tour)
                best_cost = sol.cost

                # Break if better than target
                if best_cost <= target:
                    break

        return sol
