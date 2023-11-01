# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True

from libcpp cimport bool
from libcpp.random cimport mt19937, random_device, uniform_int_distribution
from libcpp.set cimport set
from libcpp.vector cimport vector

import numpy as np

from tspgrasp.node cimport Node
from tspgrasp.tour cimport Tour
from tspgrasp.random cimport RandomGen


cdef class LocalSearch:

    cdef public:
        int max_iter
        int n_moves

    cdef:
        Tour _tour
        RandomGen _rng
        double[:, :] _D
        vector[vector[int]] _correlated_nodes

    cdef bool moves(LocalSearch self, Node u, Node v) except *
    cdef bool move_1(LocalSearch self, Node u, Node v) except *
    cdef bool move_2(LocalSearch self, Node u, Node v) except *
    cdef bool move_3(LocalSearch self, Node u, Node v) except *
    cdef bool move_4(LocalSearch self, Node u, Node v) except *
    cdef bool move_5(LocalSearch self, Node u, Node v) except *
    cdef bool move_6(LocalSearch self, Node u, Node v) except *
    cdef bool move_7(LocalSearch self, Node u, Node v) except *
    cdef bool eval_move(LocalSearch self, double cost) except *
    cdef void insert_node(LocalSearch self, Node u, Node v) except *
    cdef void swap_node(LocalSearch self, Node u, Node v) except *
    cdef void initialize_corr_nodes(LocalSearch self) except *
