# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True

from abc import abstractmethod

import numpy as np

from tspgrasp.node cimport Node
from tspgrasp.problem cimport Problem
from tspgrasp.tour cimport Tour


cdef class CheapestArc:

    def __init__(self, Problem problem, seed=None):
        self.rng = np.random.default_rng(seed)
        self.problem = problem
        self.nodes = []
        self.queue = []

    cdef double calc_insertion(CheapestArc self, Node new) except *:
        cost = self.problem.D[self.tour.depot.prev.index, new.index]
        return cost

    cdef void insert(CheapestArc self, Node new) except *:
        new.prev = self.tour.depot.prev
        self.tour.depot.prev.next = new
        new.next = self.tour.depot
        self.tour.depot.prev = new

    cdef void start(CheapestArc self) except *:
        cdef:
            Node node
            int first
        self.nodes = [Node(i) for i in range(self.problem.n_nodes)]
        self.queue = [n for n in self.nodes]
        first = self.rng.choice(len(self.queue))
        node = self.queue.pop(first)
        node.next = node
        node.prev = node
        node.is_depot = True
        self.tour = Tour(node)

    cdef object calc_candidates(CheapestArc self):
        cdef:
            Node node
        costs = []
        for node in self.queue:
            costs.append(self.calc_insertion(node))
        return costs

    @abstractmethod
    def do(self):
        pass


cdef class GreedyCheapestArc(CheapestArc):

    def do(self):
        self.start()
        while len(self.queue) > 0:
            costs = self.calc_candidates()
            choice = np.argmin(costs)
            nd = self.queue.pop(choice)
            self.insert(nd)
        return self.tour.cost


cdef class SemiGreedy(CheapestArc):

    def __init__(self, problem: Problem, alpha=(0.0, 1.0), seed=None):
        super().__init__(problem, seed)
        if isinstance(alpha, float) or isinstance(alpha, int):
            alpha = (alpha, alpha)
        self.alpha = alpha

    def do(self):
        cdef:
            double alpha
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
        return self.tour.cost
