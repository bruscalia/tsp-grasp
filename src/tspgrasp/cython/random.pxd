# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True, initializedcheck=False

from libcpp.random cimport mt19937
from libcpp.vector cimport vector


cdef class RandomGen:

    cdef:
        mt19937 _rng

    cdef void shuffle(RandomGen self, vector[int] &v) except *
    cdef double random(RandomGen self) except *
    cdef int* choice(RandomGen self, vector[int] &v) except *
