# distutils: language = c++

import numpy as np


cdef class Problem:

    def __cinit__(self, int n_nodes, D: np.ndarray) -> None:
        self.n_nodes = n_nodes
        self.D = np.array(D, dtype=np.double)[:, :]
