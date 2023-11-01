import numpy as np

from tspgrasp.pure_python.problem import Problem
from tspgrasp.pure_python.tour import Tour
from tspgrasp.pure_python.local_search import LocalSearch


class SimulatedAnnealing(LocalSearch):

    def __init__(self, T_start=10, T_final=1e-3, decay=0.99, seed=None):
        super().__init__(seed)
        self.T_start = T_start
        self.T_final = T_final
        self.T = T_start
        self.decay = decay

    def do(self, tour: Tour, problem: Problem, max_iter=100000):
        n_iter = 0
        proceed = True
        self._tour = Tour(tour.depot)
        self._D = problem.D
        self.initialize_corr_nodes()
        self.n_moves = 0
        self.T = self.T_start
        nodes = sorted(self._tour.nodes, key=lambda x: x.index)
        customers = [n.index for n in nodes if not n.is_depot]
        while proceed and n_iter < max_iter and self.T >= self.T_final:
            n_iter = n_iter + 1
            proceed = False or n_iter <= 1
            self._rng.shuffle(customers)
            for u_index in customers:
                u = nodes[u_index]
                correlated_nodes = self._correlated_nodes[u.index]
                self._rng.shuffle(correlated_nodes)
                for v_index in correlated_nodes:
                    v = nodes[v_index]
                    if self.moves(u, v):
                        proceed = True
                        self.T = self.T * self.decay
                        continue
            if not proceed:
                break

    def eval_move(self, cost: float):
        make_move = (cost <= -0.0001) or (np.exp(-(cost + self.T_final)/self.T) > self._rng.random())
        return not make_move
