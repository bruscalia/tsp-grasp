# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True, initializedcheck=False

from libcpp cimport bool
from libcpp.vector cimport vector


cdef double cmax(vector[double] v)


cdef double cmin(vector[double] v)


cdef int carg_max(vector[double] v)


cdef int carg_min(vector[double] v)


cdef int cpop(vector[int] &v, size_t index) except *
