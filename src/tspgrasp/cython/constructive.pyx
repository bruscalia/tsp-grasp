# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True, initializedcheck=False

from libcpp cimport bool
from libcpp.vector cimport vector

from cython.operator cimport dereference as deref

import numpy as np

from tspgrasp.cython.node cimport Node
from tspgrasp.cython.problem cimport Problem
from tspgrasp.cython.tour cimport Tour
from tspgrasp.cython.random cimport RandomGen
from tspgrasp.cython.utils cimport cmax, cmin, carg_min, cpop

from tspgrasp.solution import Solution


cdef class CheapestArc:

    def __init__(self, seed=None):
        self.rng = RandomGen(seed)
        self.nodes = []
        self.queue = vector[int]()

    def __call__(self, double[:, :] D) -> Solution:
        cdef int n_nodes = D.shape[0]
        assert D.shape[0] == D.shape[1], "D must be a squared matrix"
        problem = Problem(n_nodes, D)
        self.do(problem)
        self.tour.calc_costs(D)
        sol = Solution(self.tour)
        return sol

    cdef double calc_insertion(CheapestArc self, Node new) except *:
        return self.problem.D[self.tour.depot.prev.index, new.index]

    cdef void insert(CheapestArc self, Node new) except *:
        self.tour.insert(new)

    cdef void start(CheapestArc self) except *:
        cdef:
            Node node
            int *firstptr
            int idx, first
        self.nodes = [Node(i) for i in range(self.problem.n_nodes)]
        self.queue = vector[int]()
        for node in self.nodes:
            self.queue.push_back(node.index)
        firstptr = self.rng.choice(self.queue)
        first = deref(firstptr)
        idx = cpop(self.queue, first)
        node = self.nodes[idx]
        self.tour = Tour(node)

    cdef vector[double] calc_candidates(CheapestArc self) except *:
        cdef:
            Node node
            vector[double] costs
            int idx
            double cost
        costs = vector[double]()
        for idx in self.queue:
            node = self.nodes[idx]
            cost = self.calc_insertion(node)
            costs.push_back(cost)
        return costs

    cpdef void do(self, Problem problem) except *:
        pass


cdef class GreedyCheapestArc(CheapestArc):

    cpdef void do(self, Problem problem) except *:
        cdef:
            int choice, idx, qsize
            vector[double] costs
            Node node
        self.problem = problem
        self.start()
        qsize = <int>self.queue.size()
        while qsize > 0:
            costs = self.calc_candidates()
            choice = carg_min(costs)
            idx = cpop(self.queue, choice)
            node = self.nodes[idx]
            self.insert(node)
            qsize = <int>self.queue.size()


cdef class SemiGreedy(CheapestArc):

    def __init__(self, alpha=(0.0, 1.0), seed=None):
        super().__init__(seed)
        if isinstance(alpha, float) or isinstance(alpha, int):
            alpha = (alpha, alpha)
        self.alpha[0] = alpha[0]
        self.alpha[1] = alpha[1]

    cpdef void do(self, Problem problem) except *:
        cdef:
            int i, idx, choice, qsize
            int *choiceptr
            double alpha, worst, best, tol
            vector[double] costs
            vector[int] rcl
            Node node

        self.problem = problem
        self.start()
        qsize = <int>self.queue.size()
        alpha = self.alpha[0] + self.rng.random() * (self.alpha[1] - self.alpha[0])
        alpha = clip(alpha, 0.000001, 0.9999)
        while qsize > 0:
            costs = self.calc_candidates()
            worst = cmax(costs)
            best = cmin(costs)
            tol = worst - alpha * (worst - best)
            rcl = vector[int]()
            for i in range(<int>costs.size()):
                if costs[i] <= tol:
                    rcl.push_back(i)
            choiceptr = self.rng.choice(rcl)
            choice = deref(choiceptr)
            idx = cpop(self.queue, choice)
            node = self.nodes[idx]
            self.insert(node)
            qsize = <int>self.queue.size()


cdef double clip(double value, double l, double u) except *:
    if value <= l:
        value = l
    elif value >= u:
        value = u
    return value
