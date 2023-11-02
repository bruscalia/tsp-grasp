import math
from typing import List

import numpy as np

from tspgrasp.pypure.node import Node
from tspgrasp.pypure.problem import Problem
from tspgrasp.solution import Solution
from tspgrasp.pypure.tour import Tour


class LocalSearch:

    _correlated_nodes: list

    def __init__(self, seed=None):
        self.n_moves = 0
        self._rng = np.random.default_rng(seed)
        self._D = np.empty((0, 0), dtype=np.double)
        self._correlated_nodes = []

    def __call__(self, seq: List[int], D: np.ndarray, max_iter=100000):
        assert D.shape[0] == D.shape[1], "D must be a squared matrix"
        assert D.shape[0] == len(seq), "D must be the same length as seq"
        problem = Problem(len(seq), D)
        self.set_problem(problem)
        tour = Tour.new(seq)
        self.do(tour, max_iter=max_iter)
        sol = Solution(self.tour)
        return sol

    def do(self, tour: Tour, max_iter: int = 100000):
        self._prepare_search(tour)
        nodes = sorted(self.tour.nodes, key=lambda x: x.index)
        customers = [n.index for n in nodes if not n.is_depot]
        n_iter = 0
        proceed = True
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

    def set_problem(self, problem: Problem):
        self._D = problem.D

    def _prepare_search(self, tour: Tour):
        self.n_moves = 0
        self.tour = tour
        self._initialize_corr_nodes()

    def moves(self, u: Node, v: Node) -> bool:
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

    def move_1(self, u: Node, v: Node) -> bool:

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

    def move_2(self, u: Node, v: Node) -> bool:

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

    def move_3(self, u: Node, v: Node) -> bool:

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

    def move_4(self, u: Node, v: Node) -> bool:

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

    def move_5(self, u: Node, v: Node) -> bool:

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

    def move_6(self, u: Node, v: Node) -> bool:

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

    def move_7(self, u: Node, v: Node) -> bool:

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

    def eval_move(self, cost: float):
        return cost > -0.0001

    def insert_node(self, u: Node, v: Node):

        # Remove u from existing
        u.prev.next = u.next
        u.next.prev = u.prev

        # Insert u after v
        v.next.prev = u
        u.prev = v
        u.next = v.next
        v.next = u

    def swap_node(self, u: Node, v: Node):

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

    def _initialize_corr_nodes(self):
        n_nodes = self._D.shape[0]
        mid_size = math.ceil(self._D.shape[0] / 2)
        corr_nodes = np.argpartition(self._D, mid_size, axis=1)[:, :mid_size].tolist()
        corr_sets = [set() for _ in range(n_nodes)]
        customers = [n.index for n in self.tour.nodes if not n.is_depot]
        for i in customers:
            for j in corr_nodes[i]:
                if (j != self.tour.depot.index) and (i != j):
                    corr_sets[i].add(j)
                    corr_sets[j].add(i)
        self._correlated_nodes = [list(corr_sets[i]) for i in range(n_nodes)]


class HistoryLS(LocalSearch):

    history: List[List[int]]

    def __call__(self, seq: List[int], D: np.ndarray, max_iter=100000):
        self.history = []
        return super().__call__(seq, D, max_iter)

    def moves(self, u: Node, v: Node) -> bool:
        if super().moves(u, v):
            self.history.append(self.tour.solution)
