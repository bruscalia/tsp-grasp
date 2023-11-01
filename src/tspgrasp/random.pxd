# distutils: language = c++

from libcpp.random cimport mt19937
from libcpp.vector cimport vector


cdef class RandomGen:

    cdef:
        mt19937 _rng

    cdef void shuffle(RandomGen self, vector[int] &v) except *
    cdef double rand(RandomGen self) except *
    cdef int* choice(RandomGen self, vector[int] &v) except *
