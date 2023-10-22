# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True

from libcpp cimport bool

import copy

from tspgrasp.node cimport Node


cdef class Tour:

    cdef public:
        Node depot

    cdef public void calc_costs(Tour self, double[:, :] D) except *
