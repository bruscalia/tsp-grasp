# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True

from libcpp cimport bool

import numpy as np

from tspgrasp.node cimport Node
from tspgrasp.tour cimport Tour


cdef class LocalSearch:

    cdef public:
        double[:, :] D
        int max_iter
        int n_moves

    cdef:
        Tour _tour
        object _rng

    cdef bool move_1(LocalSearch self, Node u, Node v) except *
    cdef bool move_2(LocalSearch self, Node u, Node v) except *
    cdef bool move_3(LocalSearch self, Node u, Node v) except *
    cdef bool move_4(LocalSearch self, Node u, Node v) except *
    cdef bool move_5(LocalSearch self, Node u, Node v) except *
    cdef bool move_6(LocalSearch self, Node u, Node v) except *
    cdef bool move_7(LocalSearch self, Node u, Node v) except *
    cdef void insert_node(LocalSearch self, Node u, Node v) except *
    cdef void swap_node(LocalSearch self, Node u, Node v) except *
