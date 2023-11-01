# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True, initializedcheck=False

from libcpp.random cimport mt19937, random_device, uniform_int_distribution, uniform_real_distribution
from libcpp.vector cimport vector


cdef class RandomGen:

    def __cinit__(self, seed=None):
        self._rng = initialize_rng(seed=seed)

    cdef void shuffle(RandomGen self, vector[int] &v) except *:
        shuffle_inplace(v, self._rng)

    cdef double rand(RandomGen self) except *:
        return random_value(self._rng)

    cdef int* choice(RandomGen self, vector[int] &v) except *:
        return random_choice(v, self._rng)


cdef mt19937 initialize_rng(seed=None):
    cdef mt19937 rng
    if seed:
        rng = rng_from_seed(seed)
    else:
        rng = rng_from_rd()
    return rng


cdef mt19937 rng_from_seed(unsigned int seed) except *:
    return mt19937(seed)


cdef mt19937 rng_from_rd() except *:
    cdef random_device rd
    return mt19937(rd())


cdef void shuffle_inplace(vector[int] &v, mt19937 &rng) except *:
    cdef int i, j
    cdef int n = v.size()
    cdef uniform_int_distribution[int] dist

    for i in range(n-1, 0, -1):
        dist = uniform_int_distribution[int](0, i)
        j = dist(rng)
        v[i], v[j] = v[j], v[i]


cdef int* random_choice(vector[int] &v, mt19937 &rng) except *:
    cdef:
        int n
        uniform_int_distribution[int] dist
        int random_index = dist(rng)

    # Check if the vector is empty
    n = v.size()
    if n == 0:
        return NULL

    # Generate a random index between 0 and n - 1
    dist = uniform_int_distribution[int](0, n - 1)
    random_index = dist(rng)

    # Return the element at the random index
    return &v[random_index]


cdef double random_value(mt19937 &rng):
    cdef uniform_real_distribution[double] dist
    dist = uniform_real_distribution[double](0.0, 1.0)
    return dist(rng)
