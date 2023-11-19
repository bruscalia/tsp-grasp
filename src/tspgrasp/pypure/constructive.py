from abc import abstractmethod
from typing import List

import numpy as np

from tspgrasp.pypure.node import Node
from tspgrasp.pypure.problem import Problem
from tspgrasp.pypure.tour import Tour
from tspgrasp.solution import Solution


class Constructive:

    nodes: List[Node]
    queue: List[Node]
    problem: Problem
    tour: Tour

    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed)
        self.problem = None
        self.tour = None
        self.nodes = []
        self.queue = []

    def __call__(self, D: np.ndarray) -> Solution:
        n_nodes = D.shape[0]
        assert D.shape[0] == D.shape[1], "D must be a squared matrix"
        problem = Problem(n_nodes, D)
        self.do(problem)
        self.tour.calc_costs(D)
        sol = Solution(self.tour)
        return sol

    def calc_insertion(self, new: Node) -> float:
        cost = self.problem.D[self.tour.depot.prev.index, new.index]
        return cost

    def insert(self, new: Node):
        self.tour.insert(new)

    def start(self):
        self.nodes = [Node(i) for i in range(self.problem.n_nodes)]
        self.queue = [n for n in self.nodes]
        first = self.rng.choice(len(self.queue))
        node = self.queue.pop(first)
        self.tour = Tour(node)

    def calc_candidates(self) -> List[float]:
        costs = []
        for node in self.queue:
            costs.append(self.calc_insertion(node))
        return costs

    @abstractmethod
    def do(self, problem: Problem):
        pass


class CheapestArc(Constructive):

    def do(self, problem: Problem):
        self.problem = problem
        self.start()
        while len(self.queue) > 0:
            costs = self.calc_candidates()
            choice = np.argmin(costs)
            nd = self.queue.pop(choice)
            self.insert(nd)
        return self.tour.cost


class SemiGreedyArc(CheapestArc):

    def __init__(self, alpha=(0.0, 1.0), seed=None):
        super().__init__(seed)
        if isinstance(alpha, float) or isinstance(alpha, int):
            alpha = (alpha, alpha)
        self.alpha = alpha

    def do(self, problem: Problem):
        self.problem = problem
        self.start()
        alpha = self.alpha[0] + self.rng.random() * (self.alpha[1] - self.alpha[0])
        alpha = np.clip(alpha, 0.000001, 0.99999)
        while len(self.queue) > 0:
            costs = self.calc_candidates()
            worst = max(costs)
            best = min(costs)
            tol = worst - alpha * (worst - best)
            rcl = [i for i in range(len(costs)) if costs[i] <= tol]
            choice = self.rng.choice(rcl)
            nd = self.queue.pop(choice)
            self.insert(nd)
        return self.tour.cost


class CheapestInsertion(CheapestArc):

    def calc_insertion(self, new: Node) -> float:
        node: Node
        cost = float("inf")
        for node in self.tour.nodes:
            cfrom = self.problem.D[node.index, new.index]
            cnext = self.problem.D[new.index, node.next.index]
            cbase = self.problem.D[node.index, node.next.index]
            c = cfrom + cnext - cbase
            if c < cost:
                new.prev = node
                cost = c
        return cost

    def insert(self, new: Node):
        node = new.prev
        new.next = node.next
        node.next.prev = new
        node.next = new


class RandomInsertion(CheapestInsertion):

    def do(self, problem: Problem):
        self.problem = problem
        self.start()
        while len(self.queue) > 0:
            choice = np.random.choice(len(self.queue))
            nd = self.queue.pop(choice)
            self.calc_insertion(nd)
            self.insert(nd)
        return self.tour.cost


class SemiGreedyInsertion(CheapestInsertion, SemiGreedyArc):

    def __init__(self, alpha=(0, 1), seed=None):
        SemiGreedyArc.__init__(self, alpha, seed)

    def do(self, problem: Problem):
        return SemiGreedyArc.do(self, problem)


class HistoryGreedyArc(CheapestArc):

    history: List[List[int]]

    def __call__(self, D: np.ndarray) -> Solution:
        sol = super().__call__(D)
        self.history = []
        for j in range(len(sol.tour)):
            self.history.append(sol.tour[:j + 1])
        return sol


class HistoryGreedyInsertion(CheapestInsertion):

    history: List[List[int]]

    def __call__(self, D: np.ndarray) -> Solution:
        self.history = []
        sol = super().__call__(D)
        return sol

    def start(self):
        super().start()
        self.history.append(self.tour.solution)

    def insert(self, new: Node):
        super().insert(new)
        self.history.append(self.tour.solution)
