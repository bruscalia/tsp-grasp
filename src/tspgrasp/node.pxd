# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True

from libcpp cimport bool


cdef class Node:

    cdef public:
        int index
        Node prev
        Node next
        bool is_depot
        double cum_dist
        double cum_rdist

    cdef void reset_dimensions(Node self) except *
