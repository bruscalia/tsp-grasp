# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True

from libcpp cimport bool


cdef class Problem:

    cdef public:
        int n_nodes
        double[:, :] D
