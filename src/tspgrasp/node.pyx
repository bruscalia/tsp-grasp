# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True

from libcpp cimport bool


cdef class Node:

    def __init__(
        self,
        index,
        is_depot=False
    ):
        self.index = index
        self.is_depot = is_depot
        self.cum_dist = 0.0
        self.cum_rdist = 0.0

    cdef void reset_dimensions(Node self) except *:
        self.cum_dist = 0.0
        self.cum_rdist = 0.0
