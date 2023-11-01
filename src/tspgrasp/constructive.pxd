# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True, initializedcheck=False

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

    cpdef public void do(self, Problem problem) except *
    cdef double calc_insertion(CheapestArc self, Node new) except *
    cdef void insert(CheapestArc self, Node new) except *
    cdef void start(CheapestArc self) except *
    cdef object calc_candidates(CheapestArc self)


cdef class GreedyCheapestArc(CheapestArc):
    pass


cdef class SemiGreedy(CheapestArc):

    cdef:
        object alpha
