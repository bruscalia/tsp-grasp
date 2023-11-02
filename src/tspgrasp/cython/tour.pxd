# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True, initializedcheck=False

from tspgrasp.cython.node cimport Node


cdef class Tour:

    cdef public:
        Node depot

    cdef public void insert(Tour self, Node new) except *
    cdef public void calc_costs(Tour self, double[:, :] D) except *
