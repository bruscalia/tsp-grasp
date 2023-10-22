# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True

import numpy as np


cdef class Problem:

    def __init__(self, n_nodes: int, D: np.ndarray) -> None:
        self.n_nodes = n_nodes
        self.D = np.array(D, dtype=np.double)[:, :]
