# distutils: language = c++

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
