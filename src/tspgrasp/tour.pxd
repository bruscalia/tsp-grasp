# distutils: language = c++

from tspgrasp.node cimport Node


cdef class Tour:

    cdef public:
        Node depot

    cdef public void calc_costs(Tour self, double[:, :] D) except *
