# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True, initializedcheck=False

from libcpp cimport bool
from libcpp.vector cimport vector

import copy

from tspgrasp.cython.node cimport Node


cdef class Tour:

    def __init__(self, Node depot) -> None:
        depot.next = depot
        depot.prev = depot
        depot.is_depot = True
        self.depot = depot

    def __repr__(self) -> str:
        return str(self.solution)

    @classmethod
    def new(cls, vector[int] seq):
        cdef:
            Node node
            Tour tour
            int i
        i = seq.front()
        seq.erase(seq.begin())
        node = Node(i, is_depot=True)
        tour = cls(node)
        for i in seq:
            node = Node(i, is_depot=False)
            tour.insert(node)
        return tour

    @property
    def solution(self):
        sol = []
        first_it = True
        node = self.depot
        while (not node.is_depot) or (first_it):
            sol.append(node.index)
            node = node.next
            first_it = False
        sol.append(sol[0])
        return sol

    @property
    def nodes(self):
        sol = []
        first_it = True
        node = self.depot
        while (not node.is_depot) or (first_it):
            sol.append(node)
            node = node.next
            first_it = False
        return sol

    def copy(self):
        return copy.deepcopy(self)

    @property
    def cost(self):
        return self.depot.cum_dist

    cdef public void insert(Tour self, Node new) except *:
        new.prev = self.depot.prev
        self.depot.prev.next = new
        new.next = self.depot
        self.depot.prev = new

    cdef public void calc_costs(Tour self, double[:, :] D) except *:

        cdef:
            bool first_it = True
            Node node = self.depot
            double dist = 0.0
            double rdist = 0.0

        node.cum_dist = dist
        node.cum_rdist = rdist
        while (not node.is_depot) or (first_it):
            node = node.next
            dist = dist + D[node.prev.index, node.index]
            rdist = rdist + D[node.index, node.prev.index] - D[node.prev.index, node.index]
            node.cum_dist = dist
            node.cum_rdist = rdist
            first_it = False
