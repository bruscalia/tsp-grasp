from typing import List

try:
    from tspgrasp.tour import Tour
except:
    from tspgrasp.pure_python.tour import Tour


class Solution:

    _tour: Tour
    tour: List[int]
    cost: float

    def __init__(self, tour: Tour):
        self._tour = tour
        self.tour = tour.solution
        self.cost = tour.cost
