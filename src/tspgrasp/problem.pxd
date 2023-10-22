# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True

from libcpp cimport bool

import numpy as np


cdef class Problem:

    cdef public:
        int n_nodes
        double[:, :] D
