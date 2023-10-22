import time

import numpy as np

from tspgrasp.problem import Problem
from tspgrasp.constructive import SemiGreedy
from tspgrasp.local_search import LocalSearch


class Grasp:

    def __init__(self, alpha=(0.0, 1.0), max_moves=10000, max_iter=100, time_limit=60, seed=None):
        self.alpha = alpha
        self.max_moves = max_moves
        self.max_iter = max_iter
        self.time_limit = time_limit
        self.seed = seed
        self.costs = []

    def solve(self, problem: Problem, target=-np.inf):

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
                sol = constructive.tour
                best_cost = sol.cost

                # Break if better than target
                if best_cost <= target:
                    break

        return sol
