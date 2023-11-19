# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True, initializedcheck=False

from libcpp cimport bool
from libcpp.vector cimport vector

from tspgrasp.cython.node cimport Node
from tspgrasp.cython.problem cimport Problem
from tspgrasp.cython.tour cimport Tour
from tspgrasp.cython.random cimport RandomGen
from tspgrasp.cython.utils cimport cmax, cmin, carg_min, cpop


cdef class Constructive:

    cdef public:
        Tour tour
        Problem problem
        object nodes
        vector[int] queue
        RandomGen rng

    cpdef void do(self, Problem problem) except *
    cdef double calc_insertion(Constructive self, Node new) except *
    cdef void insert(Constructive self, Node new) except *
    cdef void start(Constructive self) except *
    cdef vector[double] calc_candidates(Constructive self) except *


cdef class CheapestArc(Constructive):
    pass


cdef class SemiGreedyArc(CheapestArc):

    cdef:
        double alpha[2]


cdef class CheapestInsertion(CheapestArc):

    cdef double calc_insertion(CheapestInsertion self, Node new) except *
    cdef void insert(CheapestInsertion self, Node new) except *


cdef class RandomInsertion(CheapestInsertion):
    pass


cdef class SemiGreedyInsertion(SemiGreedyArc):

    cdef double calc_insertion(SemiGreedyInsertion self, Node new) except *
    cdef void insert(SemiGreedyInsertion self, Node new) except *


cdef double clip(double value, double l, double u) except *


cdef vector[int] range_idx(vector[int] v) except *
