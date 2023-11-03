from typing import List

try:
    from tspgrasp.cython.tour import Tour
except:
    from tspgrasp.pypure.tour import Tour


class Solution:
    """TSP Solution
    """

    _tour: Tour
    tour: List[int]
    """List of node indexes in solution. Depot is repeated at the end.
    """
    cost: float
    """Cost of solution
    """

    def __init__(self, tour: Tour):
        self._tour = tour
        self.tour = tour.solution
        self.cost = tour.cost

    def __repr__(self) -> str:
        return f"Cost: {self.cost}\nTour: {self.tour}"
