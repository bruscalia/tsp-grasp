import numpy as np
from tspgrasp.pypure.node import Node

from tspgrasp.pypure.problem import Problem
from tspgrasp.pypure.tour import Tour
from tspgrasp.pypure.local_search import LocalSearch


class SimulatedAnnealing(LocalSearch):

    def __init__(self, T_start=10.0, T_final=1e-3, decay=0.99, seed=None):
        super().__init__(seed)
        self.T_start = T_start
        self.T_final = T_final
        self.T = T_start
        self.decay = decay

    def do(self, tour: Tour, max_iter: int = 100000):
        self._prepare_search(tour)
        nodes = sorted(self.tour.nodes, key=lambda x: x.index)
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
                        continue
            if not proceed:
                break

    def moves(self, u: Node, v: Node) -> bool:
        if super().moves(u, v):
            self.T = self.T * self.decay
            return True
        else:
            return False

    def _prepare_search(self, tour: Tour):
        super()._prepare_search(tour)
        self.T = self.T_start

    def eval_move(self, cost: float):
        make_move = (cost <= -0.0001) or (np.exp(-(cost + self.T_final)/self.T) > self._rng.random())
        return not make_move
