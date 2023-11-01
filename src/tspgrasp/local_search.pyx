# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, embedsignature=True, initializedcheck=False

from libcpp cimport bool
from libcpp.random cimport mt19937
from libcpp.set cimport set
from libcpp.vector cimport vector

import numpy as np

from tspgrasp.node cimport Node
from tspgrasp.problem cimport Problem
from tspgrasp.random cimport RandomGen
from tspgrasp.tour cimport Tour

from tspgrasp.solution import Solution


cdef extern from "<cmath>" namespace "std":
    double ceil(double x)

cdef int compute_ceil(double value):
    return <int>ceil(value)


cdef class LocalSearch:

    def __cinit__(self):
        self.n_moves = 0
        self._D = np.empty((0, 0), dtype=np.double)[:, :]
        self._correlated_nodes = vector[vector[int]]()

    def __init__(self, seed=None) -> None:
        """Local Search (VNS) implementation for TSP

        Parameters
        ----------
        seed : int, optional
            Random generator seed, by default None
        """
        self._rng = RandomGen(seed)

    def __call__(self, vector[int] seq, double[:, :] D, max_iter=100000) -> Solution:
        """Solve a TSP based on an initial solution and a distance matrix

        Parameters
        ----------
        seq : List[int]
            Initial solution

        D : np.ndarray
            2d-distance matrix

        max_iter : int, optional
            Max number of moves, by default 100000

        Returns
        -------
        Solution
            Attributes:
            - tour : List[int]
            - cost : float
        """
        assert D.shape[0] == D.shape[1], "D must be a squared matrix"
        assert D.shape[0] == seq.size(), "D must be the same length as seq"
        problem = Problem(seq.size(), D)
        self.set_problem(problem)
        tour = Tour.new(seq)
        self.do(tour, max_iter=max_iter)
        sol = Solution(self.tour)
        return sol

    def do(self, Tour tour, int max_iter = 100000):

        cdef:
            int n_iter = 0
            bool proceed = True
            int v_index, u_index
            Node, u, v
            vector[int] customers
            vector[int] correlated_nodes

        self._prepare_search(tour)
        nodes = sorted(self.tour.nodes, key=lambda x: x.index)
        customers = [n.index for n in nodes if not n.is_depot]
        while proceed and n_iter < max_iter:
            n_iter = n_iter + 1
            proceed = False or n_iter <= 1
            self._rng.shuffle(customers)
            for u_index in customers:
                u = nodes[u_index]
                correlated_nodes = self._correlated_nodes[u.index]
                self._rng.shuffle(correlated_nodes)
                for v_index in correlated_nodes:
                    v = nodes[v_index]
                    if self.moves(u, v):
                        proceed = True
                        continue
            if not proceed:
                break

    def set_problem(LocalSearch self, Problem problem):
        self._D = problem.D

    cpdef void _prepare_search(LocalSearch self, Tour tour) except *:
        self.n_moves = 0
        self.tour = tour
        self._initialize_corr_nodes()

    cpdef bool moves(LocalSearch self, Node u, Node v) except *:
        if self.move_1(u, v):
            return True
        elif self.move_2(u, v):
            return True
        elif self.move_3(u, v):
            return True
        elif self.move_4(u, v):
            return True
        elif self.move_5(u, v):
            return True
        elif self.move_6(u, v):
            return True
        elif self.move_7(u, v):
            return True
        elif v.prev.is_depot:
            v = v.prev
            if self.move_1(u, v):
                return True
            elif self.move_2(u, v):
                return True
            elif self.move_3(u, v):
                return True
            else:
                return False
        else:
            return False

    cdef bool move_1(LocalSearch self, Node u, Node v) except *:

        cdef:
            Node x
            Node y
            double cost, cs_v, cs_u

        # Set succeeding nodes
        x = u.next
        y = v.next

        # Stop if u follows v
        if u.index == y.index:
            return False

        # Else compute costs
        else:
            cs_u = self._D[u.prev.index, x.index] - self._D[u.prev.index, u.index] \
                - self._D[u.index, x.index]
            cs_v = self._D[v.index, u.index] + self._D[u.index, y.index] \
                - self._D[v.index, y.index]
            cost = cs_u + cs_v

            # Update
            if self.eval_move(cost):
                return False
            else:
                self.insert_node(u, v)
                self.tour.calc_costs(self._D)
                self.n_moves = self.n_moves + 1
        return True

    cdef bool move_2(LocalSearch self, Node u, Node v) except *:

        cdef:
            Node x
            Node y
            double cost, cs_v, cs_u

        # Set succeeding nodes
        x = u.next
        y = v.next

        # Stop if u follows v, v follows u, or x is a depot
        if (u.index == y.index) or (v.index == x.index) or (x.is_depot):
            return False

        # Else compute costs
        else:
            cs_u = self._D[u.prev.index, x.next.index] - self._D[u.prev.index, u.index] \
                - self._D[x.index, x.next.index]
            cs_v = self._D[v.index, u.index] + self._D[x.index, y.index] \
                - self._D[v.index, y.index]
            cost = cs_u + cs_v

            # Update
            if self.eval_move(cost):
                return False
            else:
                self.insert_node(u, v)
                self.insert_node(x, u)
                self.tour.calc_costs(self._D)
                self.n_moves = self.n_moves + 1
        return True

    cdef bool move_3(LocalSearch self, Node u, Node v) except *:

        cdef:
            Node x
            Node y
            double cost, cs_v, cs_u

        # Set succeeding nodes
        x = u.next
        y = v.next

        # Stop if u follows v, v follows u, or x is a depot
        if (u.index == y.index) or (v.index == x.index) or (x.is_depot):
            return False

        # Else compute costs
        else:
            cs_u = self._D[u.prev.index, x.next.index] - self._D[u.prev.index, u.index] \
                - self._D[u.index, x.index] - self._D[x.index, x.next.index]
            cs_v = self._D[v.index, x.index] + self._D[x.index, u.index] \
                + self._D[u.index, y.index] - self._D[v.index, y.index]
            cost = cs_u + cs_v

            # Update
            if self.eval_move(cost):
                return False
            else:
                self.insert_node(x, v)
                self.insert_node(u, x)
                self.tour.calc_costs(self._D)
                self.n_moves = self.n_moves + 1
        return True

    cdef bool move_4(LocalSearch self, Node u, Node v) except *:

        cdef:
            Node x
            Node y
            double cost, cs_v, cs_u

        # Set succeeding nodes
        x = u.next
        y = v.next

        # Stop if u precedes or follows v, and break symmetry
        if (u.index == v.prev.index) or (u.index == y.index) or (v.index <= u.index):
            return False

        # Else compute costs
        else:
            cs_u = self._D[u.prev.index, v.index] + self._D[v.index, x.index] \
                - self._D[u.prev.index, u.index] - self._D[u.index, x.index]
            cs_v = self._D[v.prev.index, u.index] + self._D[u.index, y.index] \
                - self._D[v.prev.index, v.index] - self._D[v.index, y.index]
            cost = cs_u + cs_v

            # Update
            if self.eval_move(cost):
                return False
            else:
                self.swap_node(u, v)
                self.tour.calc_costs(self._D)
                self.n_moves = self.n_moves + 1

        return True

    cdef bool move_5(LocalSearch self, Node u, Node v) except *:

        cdef:
            Node x
            Node y
            double cost, cs_v, cs_u

        # Set succeeding nodes
        x = u.next
        y = v.next

        # Stop if either u or x precede or follow v, and break symmetry
        if (u.index == v.prev.index) or (x.index == v.prev.index) or (u.index == y.index)\
            or (x.is_depot) or (v.prev.is_depot):
                return False

        # Else compute costs
        else:
            cs_u = self._D[u.prev.index, v.index] + self._D[v.index, x.next.index] \
                - self._D[u.prev.index, u.index] - self._D[x.index, x.next.index]
            cs_v = self._D[v.prev.index, u.index] + self._D[x.index, y.index] \
                - self._D[v.prev.index, v.index] - self._D[v.index, y.index]
            cost = cs_u + cs_v

            # Update
            if self.eval_move(cost):
                return False
            else:
                self.swap_node(u, v)
                self.insert_node(x, u)
                self.tour.calc_costs(self._D)
                self.n_moves = self.n_moves + 1
        return True

    cdef bool move_6(LocalSearch self, Node u, Node v) except *:

        cdef:
            Node x
            Node y
            double cost, cs_v, cs_u

        # Set succeeding nodes
        x = u.next
        y = v.next

        # Stop if either x or y is depot, y precedes u, u follows v, v follows u, or v follows x
        if (x.is_depot) or (y.is_depot) or (y.index == u.prev.index) or (u.index == y.index) \
            or (x.index == v.index) or (v.index == x.next.index) or (v.prev.is_depot):
                return False

        # Else compute costs
        else:
            cs_u = self._D[u.prev.index, v.index] + self._D[y.index, x.next.index] \
                - self._D[u.prev.index, u.index] - self._D[x.index, x.next.index]
            cs_v = self._D[v.prev.index, u.index] + self._D[x.index, y.next.index] \
                - self._D[v.prev.index, v.index] - self._D[y.index, y.next.index]
            cost = cs_u + cs_v

            # Update
            if self.eval_move(cost):
                return False
            else:
                self.swap_node(u, v)
                self.swap_node(x, y)
                self.tour.calc_costs(self._D)
                self.n_moves = self.n_moves + 1
        return True

    cdef bool move_7(LocalSearch self, Node u, Node v) except *:

        cdef:
            Node x
            Node y
            Node node
            Node temp
            double cost
            int j

        # Set succeeding nodes
        x = u.next
        y = v.next

        # Stop if u follows v
        if (u.index == y.index) or (v.prev.is_depot) or (u.next.index == v.index):
            return False

        # Else compute costs
        else:
            cost = self._D[u.index, v.index] + self._D[x.index, y.index] \
                - self._D[u.index, x.index] - self._D[v.index, y.index] \
                    + v.cum_rdist - x.cum_rdist

        # If poor move stop
        if self.eval_move(cost):
            return False

        # Moves
        node = x.next
        x.prev = node
        x.next = y

        # Iterate until complete reversion
        while node.index != v.index:
            temp = node.next
            node.next = node.prev
            node.prev = temp
            node = temp

        # Final update
        v.next = v.prev
        v.prev = u
        u.next = v
        y.prev = x

        # Update
        self.tour.calc_costs(self._D)
        self.n_moves = self.n_moves + 1

        return True

    cdef bool eval_move(LocalSearch self, double cost) except *:
        return cost > -0.0001

    cdef void insert_node(LocalSearch self, Node u, Node v) except *:

        # Remove u from existing
        u.prev.next = u.next
        u.next.prev = u.prev

        # Insert u after v
        v.next.prev = u
        u.prev = v
        u.next = v.next
        v.next = u

    cdef void swap_node(LocalSearch self, Node u, Node v) except *:

        # Initialize neighbors
        u_preceding = u.prev
        u_succeeding = u.next
        v_preceding = v.prev
        v_succeeding = v.next

        # Swap on neighbors
        u_preceding.next = v
        u_succeeding.prev = v
        v_preceding.next = u
        v_succeeding.prev = u

        # Swap on nodes
        u.prev = v_preceding
        u.next = v_succeeding
        v.prev = u_preceding
        v.next = u_succeeding

    cdef void _initialize_corr_nodes(LocalSearch self) except *:
        cdef:
            int n_nodes, mid_size, i, j
            Node n
            vector[vector[int]] corr_nodes
            vector[int] customers

        n_nodes = self._D.shape[0]
        mid_size = compute_ceil(self._D.shape[0] / 2)
        corr_nodes = np.argpartition(self._D, mid_size, axis=1)[:, :mid_size].tolist()
        corr_sets = start_corr_sets(n_nodes)
        customers = [n.index for n in self.tour.nodes if not n.is_depot]
        for i in customers:
            for j in corr_nodes[i]:
                if (j != self.tour.depot.index) and (i != j):
                    corr_sets[i].insert(j)
                    corr_sets[j].insert(i)
        self._correlated_nodes = [list(corr_sets[i]) for i in range(n_nodes)]


cdef vector[set[int]] start_corr_sets(int n_nodes):
    cdef:
        vector[set[int]] out
        set[int] s
        int i

    i = 0
    while i < n_nodes:
        s = set[int]()
        out.push_back(s)
        i = i + 1

    return out

