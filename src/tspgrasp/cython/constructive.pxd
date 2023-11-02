# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True, initializedcheck=False

from libcpp cimport bool
from libcpp.vector cimport vector

from tspgrasp.cython.node cimport Node
from tspgrasp.cython.problem cimport Problem
from tspgrasp.cython.tour cimport Tour
from tspgrasp.cython.random cimport RandomGen
from tspgrasp.cython.utils cimport cmax, cmin, carg_min, cpop


cdef class CheapestArc:

    cdef public:
        Tour tour
        Problem problem
        object nodes
        vector[int] queue
        RandomGen rng

    cpdef void do(self, Problem problem) except *
    cdef double calc_insertion(CheapestArc self, Node new) except *
    cdef void insert(CheapestArc self, Node new) except *
    cdef void start(CheapestArc self) except *
    cdef vector[double] calc_candidates(CheapestArc self) except *


cdef class GreedyCheapestArc(CheapestArc):
    pass


cdef class SemiGreedy(CheapestArc):

    cdef:
        double alpha[2]
