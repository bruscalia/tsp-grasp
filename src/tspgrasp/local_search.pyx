# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True

from libcpp cimport bool

import numpy as np

from tspgrasp.node cimport Node
from tspgrasp.tour cimport Tour


cdef class LocalSearch:

    def __init__(self, double[:, :] D, max_iter=10000, seed=None) -> None:
        self.D = D
        self.max_iter = max_iter
        self._rng = np.random.default_rng(seed)
        self.n_moves = 0

    @property
    def tour(self) -> Tour:
        return self._tour

    @property
    def rng(self) -> np.random.Generator:
        return self._rng

    def do(self, tour: Tour):

        cdef:
            int n_iter = 0
            bool proceed = True
            int v_index, u_index
            Node, u, v

        self._tour = Tour(tour.depot)
        self.n_moves = 0
        pool = sorted(self._tour.nodes, key=lambda x: x.index)
        while proceed and n_iter < self.max_iter:
            n_iter = n_iter + 1
            proceed = False or n_iter <= 1
            candidates = list(range(len(pool)))
            self._rng.shuffle(candidates)
            for u_index in candidates:
                u = pool[u_index]
                if u.is_depot:
                    continue
                correlated_nodes = list(range(len(pool)))
                correlated_nodes.remove(u_index)
                self._rng.shuffle(correlated_nodes)
                for v_index in correlated_nodes:
                    v = pool[v_index]
                    if self.move_1(u, v):
                        proceed = True
                        continue
                    elif self.move_2(u, v):
                        proceed = True
                        continue
                    elif self.move_3(u, v):
                        proceed = True
                        continue
                    elif self.move_4(u, v):
                        proceed = True
                        continue
                    elif self.move_5(u, v):
                        proceed = True
                        continue
                    elif self.move_6(u, v):
                        proceed = True
                        continue
                    elif self.move_7(u, v):
                        proceed = True
                        continue
            if not proceed:
                break

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
            cs_u = self.D[u.prev.index, x.index] - self.D[u.prev.index, u.index] \
                - self.D[u.index, x.index]
            cs_v = self.D[v.index, u.index] + self.D[u.index, y.index] \
                - self.D[v.index, y.index]
            cost = cs_u + cs_v

            # Update
            if cost > -1e-4:
                return False
            else:
                self.insert_node(u, v)
                self._tour.calc_costs(self.D)
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
            cs_u = self.D[u.prev.index, x.next.index] - self.D[u.prev.index, u.index] \
                - self.D[x.index, x.next.index]
            cs_v = self.D[v.index, u.index] + self.D[x.index, y.index] \
                - self.D[v.index, y.index]
            cost = cs_u + cs_v

            # Update
            if cost > -1e-4:
                return False
            else:
                self.insert_node(u, v)
                self.insert_node(x, u)
                self._tour.calc_costs(self.D)
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
            cs_u = self.D[u.prev.index, x.next.index] - self.D[u.prev.index, u.index] \
                - self.D[u.index, x.index] - self.D[x.index, x.next.index]
            cs_v = self.D[v.index, x.index] + self.D[x.index, u.index] \
                + self.D[u.index, y.index] - self.D[v.index, y.index]
            cost = cs_u + cs_v

            # Update
            if cost > -1e-4:
                return False
            else:
                self.insert_node(x, v)
                self.insert_node(u, x)
                self._tour.calc_costs(self.D)
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
            cs_u = self.D[u.prev.index, v.index] + self.D[v.index, x.index] \
                - self.D[u.prev.index, u.index] - self.D[u.index, x.index]
            cs_v = self.D[v.prev.index, u.index] + self.D[u.index, y.index] \
                - self.D[v.prev.index, v.index] - self.D[v.index, y.index]
            cost = cs_u + cs_v

            # Update
            if cost > -1e-4:
                return False
            else:
                self.swap_node(u, v)
                self._tour.calc_costs(self.D)
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
            cs_u = self.D[u.prev.index, v.index] + self.D[v.index, x.next.index] \
                - self.D[u.prev.index, u.index] - self.D[x.index, x.next.index]
            cs_v = self.D[v.prev.index, u.index] + self.D[x.index, y.index] \
                - self.D[v.prev.index, v.index] - self.D[v.index, y.index]
            cost = cs_u + cs_v

            # Update
            if cost > -1e-4:
                return False
            else:
                self.swap_node(u, v)
                self.insert_node(x, u)
                self._tour.calc_costs(self.D)
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
            cs_u = self.D[u.prev.index, v.index] + self.D[y.index, x.next.index] \
                - self.D[u.prev.index, u.index] - self.D[x.index, x.next.index]
            cs_v = self.D[v.prev.index, u.index] + self.D[x.index, y.next.index] \
                - self.D[v.prev.index, v.index] - self.D[y.index, y.next.index]
            cost = cs_u + cs_v

            # Update
            if cost > -1e-4:
                return False
            else:
                self.swap_node(u, v)
                self.swap_node(x, y)
                self._tour.calc_costs(self.D)
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
        if (u.index == y.index) or (v.prev.is_depot):
            return False

        # Else compute costs
        else:
            cost = self.D[u.index, v.index] + self.D[x.index, y.index] \
                - self.D[u.index, x.index] - self.D[v.index, y.index] \
                    + v.cum_rdist - x.cum_rdist

        # If poor move stop
        if cost > -1e-4:
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
        self._tour.calc_costs(self.D)
        self.n_moves = self.n_moves + 1

        return True

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
