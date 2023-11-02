# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True, initializedcheck=False

import numpy as np


cdef class Problem:

    cdef public:
        int n_nodes
        double[:, :] D
