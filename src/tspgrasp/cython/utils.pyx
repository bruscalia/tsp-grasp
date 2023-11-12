# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True, initializedcheck=False

from libcpp cimport bool
from libcpp.vector cimport vector

from typing import List


cdef extern from "math.h":
    double HUGE_VAL


def python_cmax(v: List[int]):
    return cmax(v)


cdef double cmax(vector[double] v):
    cdef:
        double best = -HUGE_VAL
        double x
    for x in v:
        if x > best:
            best = x
    return best


def python_cmin(v: List[int]):
    return cmin(v)


cdef double cmin(vector[double] v):
    cdef:
        double best = HUGE_VAL
        double x
    for x in v:
        if x < best:
            best = x
    return best


def python_carg_max(v: List[int]):
    return carg_max(v)


cdef int carg_max(vector[double] v):
    cdef:
        double best_cost = -HUGE_VAL
        int best_pos, i, n
    i = 0
    best_pos = -1
    n = <int>v.size()
    while i < n:
        if v[i] > best_cost:
            best_cost = v[i]
            best_pos = i
        i = i + 1
    return best_pos


def python_carg_min(v: List[int]):
    return carg_min(v)


cdef int carg_min(vector[double] v):
    cdef:
        double best_cost = HUGE_VAL
        int best_pos, i, n
    i = 0
    best_pos = -1
    n = <int>v.size()
    while i < n:
        if v[i] < best_cost:
            best_cost = v[i]
            best_pos = i
        i = i + 1
    return best_pos


def python_cpop(v: List[int], index):
    vv = vector[int]()
    for i in v:
        vv.push_back(i)
    x = cpop(vv, index)
    return vv, x


cdef int cpop(vector[int] &v, size_t index) except *:
    cdef:
        int n, value

    # Check if the position exists and fix
    n = <int>v.size()
    if index < 0:
        index = 0
    elif index >= n:
        index = n - 1

    # Pop
    value = v[index]
    v.erase(v.begin() + index)
    return value
