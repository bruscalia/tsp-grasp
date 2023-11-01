from abc import abstractmethod
import time
import logging
from typing import Any, List

import numpy as np

from tspgrasp.solution import Solution


MAX_MOVES = 100000
MAX_ITER = 10000


# Initialize logger
log = logging.getLogger(__name__)


class BaseGrasp:

    constructive: object
    local_search: object
    costs: List[float]

    @abstractmethod
    def __init__(self, constructive=None, local_search=None, seed=None):
        """GRASP for general TSP

        Parameters
        ----------
        constructive : Any, optional
            Adaptive constructive heuristic - see `grasp.constructive`,
            by default None, which uses `GreedyCheapestArc`

        local_search : Any, optional
            Local search heuristic - see `grasp.local_search`,
            by default None, which uses `LocalSearch`

        seed : int, optional
            Numpy generator random seed, by default None
        """
        pass

    @abstractmethod
    def __call__(
        self,
        D: np.ndarray,
        max_iter: int = MAX_ITER,
        max_moves: int = MAX_MOVES,
        time_limit: float = float("inf"),
        target: float = -float("inf"),
        verbose: bool = False
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

        verbose : bool, optional
            Either or not to print messages during solution

        Returns
        -------
        Solution
            Results with properties:
            - tour : List[int] (depot is included twice)
            - cost : float
        """
        pass


    def solve(
        self,
        problem: object,
        max_iter: MAX_ITER,
        max_moves: MAX_MOVES,
        time_limit: float = float("inf"),
        target: float = -float("inf"),
        verbose: bool = False
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

        verbose : bool, optional
            Either or not to print messages during solution

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
                if verbose:
                    log.info(f"New best solution {best_cost}")

                # Break if better than target
                if best_cost <= target:
                    break

        return sol
