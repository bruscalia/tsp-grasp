# distutils: language = c++

import numpy as np


cdef class Problem:

    cdef public:
        int n_nodes
        double[:, :] D
