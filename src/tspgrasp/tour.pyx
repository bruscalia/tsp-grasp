# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True

from libcpp cimport bool

import copy

from tspgrasp.node cimport Node


cdef class Tour:

    def __init__(self, Node depot) -> None:
        self.depot = depot

    def __repr__(self) -> str:
        return str(self.solution)

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
