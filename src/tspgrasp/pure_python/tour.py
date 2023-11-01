import copy
from typing import List

import numpy as np

from tspgrasp.pure_python.node import Node


class Tour:

    depot: Node

    def __init__(self, depot: Node) -> None:
        self.depot = depot

    def __repr__(self) -> str:
        return str(self.solution)

    @property
    def solution(self) -> List[int]:
        sol = []
        first_it = True
        node = self.depot
        while (not node.is_depot) or (first_it):
            sol.append(node.index)
            node = node.next
            first_it = False
        sol.append(sol[0])
        return sol

    @property
    def nodes(self) -> List[Node]:
        sol = []
        first_it = True
        node = self.depot
        while (not node.is_depot) or (first_it):
            sol.append(node)
            node = node.next
            first_it = False
        return sol

    def copy(self):
        return copy.deepcopy(self)

    @property
    def cost(self):
        return self.depot.cum_dist

    def calc_costs(self, D: np.ndarray):

        first_it = True
        node = self.depot
        dist = 0.0
        rdist = 0.0

        node.cum_dist = dist
        node.cum_rdist = rdist
        while (not node.is_depot) or (first_it):
            node = node.next
            dist = dist + D[node.prev.index, node.index]
            rdist = rdist + D[node.index, node.prev.index] - D[node.prev.index, node.index]
            node.cum_dist = dist
            node.cum_rdist = rdist
            first_it = False
