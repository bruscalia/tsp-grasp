# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True, initializedcheck=False

from libcpp cimport bool
from libc.math cimport exp
from libcpp.random cimport mt19937, uniform_int_distribution, uniform_real_distribution
from libcpp.set cimport set
from libcpp.vector cimport vector

import numpy as np

from tspgrasp.local_search cimport LocalSearch
from tspgrasp.node cimport Node
from tspgrasp.problem import Problem
from tspgrasp.tour cimport Tour


cdef class SimulatedAnnealing(LocalSearch):

    cdef public:
        double T_start
        double T_final
        double T
        double decay

    cdef void _prepare_search(SimulatedAnnealing self, Tour tour) except *
    cdef bool eval_move(SimulatedAnnealing self, double cost) except *
