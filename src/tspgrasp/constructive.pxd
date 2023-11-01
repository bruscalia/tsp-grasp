# distutils: language = c++

from tspgrasp.node cimport Node
from tspgrasp.problem cimport Problem
from tspgrasp.tour cimport Tour


cdef class CheapestArc:

    cdef public:
        Tour tour
        Problem problem
        object nodes
        object queue
        object rng

    cdef double calc_insertion(CheapestArc self, Node new) except *

    cdef void insert(CheapestArc self, Node new) except *

    cdef void start(CheapestArc self) except *

    cdef object calc_candidates(CheapestArc self)


cdef class GreedyCheapestArc(CheapestArc):
    pass


cdef class SemiGreedy(CheapestArc):

    cdef:
        object alpha
