# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True


cdef class Problem:

    def __init__(self, int n_nodes, double[:, :] D) -> None:
        self.n_nodes = n_nodes
        self.D = D
