# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True, initializedcheck=False

import numpy as np

from tspgrasp.node cimport Node
from tspgrasp.problem cimport Problem
from tspgrasp.tour cimport Tour

from tspgrasp.solution import Solution


cdef class CheapestArc:

    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed)
        self.nodes = []
        self.queue = []

    def __call__(self, double[:, :] D):
        cdef int n_nodes = D.shape[0]
        assert D.shape[0] == D.shape[1], "D must be a squared matrix"
        problem = Problem(n_nodes, D)
        self.do(problem)
        sol = Solution(self.tour)
        return sol

    cdef double calc_insertion(CheapestArc self, Node new) except *:
        cost = self.problem.D[self.tour.depot.prev.index, new.index]
        return cost

    cdef void insert(CheapestArc self, Node new) except *:
        self.tour.insert(new)

    cdef void start(CheapestArc self) except *:
        cdef:
            Node node
            int first
        self.nodes = [Node(i) for i in range(self.problem.n_nodes)]
        self.queue = [n for n in self.nodes]
        first = self.rng.choice(len(self.queue))
        node = self.queue.pop(first)
        self.tour = Tour(node)

    cdef object calc_candidates(CheapestArc self):
        cdef:
            Node node
        costs = []
        for node in self.queue:
            costs.append(self.calc_insertion(node))
        return costs

    cpdef public void do(self, Problem problem) except *:
        pass


cdef class GreedyCheapestArc(CheapestArc):

    cpdef public void do(self, Problem problem) except *:
        self.problem = problem
        self.start()
        while len(self.queue) > 0:
            costs = self.calc_candidates()
            choice = np.argmin(costs)
            nd = self.queue.pop(choice)
            self.insert(nd)


cdef class SemiGreedy(CheapestArc):

    def __init__(self, alpha=(0.0, 1.0), seed=None):
        super().__init__(seed)
        if isinstance(alpha, float) or isinstance(alpha, int):
            alpha = (alpha, alpha)
        self.alpha = alpha

    cpdef public void do(self, Problem problem) except *:
        cdef:
            double alpha
        self.problem = problem
        self.start()
        alpha = self.alpha[0] + self.rng.random() * (self.alpha[1] - self.alpha[0]) - 1e-6
        while len(self.queue) > 0:
            costs = self.calc_candidates()
            worst = max(costs)
            best = min(costs)
            tol = worst - alpha * (worst - best)
            rcl = [i for i in range(len(costs)) if costs[i] <= tol]
            choice = self.rng.choice(rcl)
            nd = self.queue.pop(choice)
            self.insert(nd)
