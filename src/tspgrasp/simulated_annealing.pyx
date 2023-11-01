# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True, initializedcheck=False

from libcpp cimport bool
from libc.math cimport exp
from libcpp.random cimport mt19937, uniform_int_distribution, uniform_real_distribution
from libcpp.set cimport set
from libcpp.vector cimport vector

import numpy as np

from tspgrasp.local_search cimport LocalSearch
from tspgrasp.node cimport Node
from tspgrasp.problem import Problem
from tspgrasp.tour cimport Tour


cdef class SimulatedAnnealing(LocalSearch):

    def __init__(self, T_start=10, T_final=1e-3, decay=0.99, seed=None):
        super().__init__(seed)
        self.T_start = T_start
        self.T_final = T_final
        self.T = T_start
        self.decay = decay

    def do(self, Tour tour, int max_iter = 100000):

        cdef:
            int n_iter = 0
            bool proceed = True
            int v_index, u_index
            Node, u, v
            vector[int] customers
            vector[int] correlated_nodes

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
                        self.T = self.T * self.decay
                        continue
            if not proceed:
                break

    cdef void _prepare_search(SimulatedAnnealing self, Tour tour):
        self.n_moves = 0
        self.tour = tour
        self._initialize_corr_nodes()
        self.T = self.T_start

    cdef bool eval_move(SimulatedAnnealing self, double cost) except *:
        cdef:
            bool make_move
        make_move = (cost <= -0.0001) or (exp(-(cost + self.T_final)/self.T) > self._rng.rand())
        return not make_move
