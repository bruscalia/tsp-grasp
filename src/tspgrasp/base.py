from abc import abstractmethod
import time
import logging
from typing import List

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
    """List of costs generated throughout iterations"""

    @abstractmethod
    def __init__(self, constructive=None, local_search=None, seed=None):
        """Greedy Randomized Adaptive Search Procedure for the TSP.

        Parameters
        ----------
        constructive : Any, optional
            Constructive heuristic. Current options available are `CheapestArc`,
            `SemiGreedyArc`, `CheapestInsertion`, `RandomInsertion`, and `SemiGreedyInsertion`,
            which should be instantiated beforehand.
            By default None, which instantiates a `CheapestArc` operator.

        local_search : Any, optional
            Local search heuristic. Current options available are `LocalSearch`
            and `SimulatedAnnealing`, which should be instantiated beforehand.
            By default None, which uses `LocalSearch`, a VNS with first improvement

        seed : int, optional
            Random generator seed (differs behavior from cython to python), by default None
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
        """Solves a TSP based on a generic 2-dimensional distance matrix

        Parameters
        ----------
        D : np.ndarray
            2-dimensional distance matrix

        max_iter : int
            Maximum number of complete iterations, by default 10000

        max_moves : int
            Maximum number of local search moves, by default 100000

        time_limit : float, optional
            Time limit (s) to interrupt the solution, by default float("inf")

        target : float, optional
            Taget value for objective which interrupts optimization process, by default -float("inf")

        verbose : bool, optional
            Either or not to print messages during solution

        Returns
        -------
        Solution
            Attributes:
            - tour : List[int]
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
        # Set problem on local search
        self.local_search.set_problem(problem)

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
            self.local_search.do(self.constructive.tour, max_iter=max_moves)
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
