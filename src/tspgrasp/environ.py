from typing import List
import warnings

import numpy as np

from tspgrasp.solution import Solution

try:
    from tspgrasp.grasp import Grasp
    import tspgrasp.cython.constructive as tspconstr
    import tspgrasp.cython.simulated_annealing as tspsa
    import tspgrasp.cython.local_search as tspls
    cythonized = True
except ModuleNotFoundError as e:
    warnings.warn(f"Failed to import Cython implementations - Using pure Python - {e}")
    from tspgrasp.pypure.grasp import GrasPy as Grasp
    import tspgrasp.pypure.constructive as tspconstr
    import tspgrasp.pypure.simulated_annealing as tspsa
    import tspgrasp.pypure.local_search as tspls
    cythonized = False


class CheapestArc(tspconstr.CheapestArc):

    def __init__(self, seed: int = None):
        """Greedy adaptive construction for the TSP inserting the next node at the end of the partial tour.
        Depot nodes are randomly chosen.

        Parameters
        ----------
        seed : int, optional
            Random generator seed (differs behavior from cython to python), by default None
        """
        super().__init__(seed)

    def __call__(self, D: np.ndarray) -> Solution:
        """Solves a TSP based on a pairwise distance matrix.

        Parameters
        ----------
        D : np.ndarray
            2-dimensional distance matrix

        Returns
        -------
        Solution
            Attributes:
            - tour : List[int]
            - cost : float
        """
        return super().__call__(D)


class SemiGreedyArc(tspconstr.SemiGreedyArc):

    def __init__(self, alpha=(0.0, 1.0), seed=None):
        """Greedy-randomized constructive heuristic for the TSP. It inserts the next node
        at the end of the partial tour.
        Depot nodes are randomly chosen.

        Parameters
        ----------
        alpha : tuple, optional
            Alpha parameter - randomly generated at each iteration between range or fixed scalar.
            Use values closer to one for a more greedy approach. By default (0.0, 1.0).

        seed : int, optional
            Random generator seed (differs behavior from cython to python), by default None
        """
        super().__init__(alpha=alpha, seed=seed)

    def __call__(self, D: np.ndarray) -> Solution:
        """Solves a TSP based on a pairwise distance matrix.

        Parameters
        ----------
        D : np.ndarray
            2-dimensional distance matrix

        Returns
        -------
        Solution
            Attributes:
            - tour : List[int]
            - cost : float
        """
        return super().__call__(D)


class CheapestInsertion(tspconstr.CheapestInsertion):

    def __init__(self, seed=None):
        """Greedy adaptive construction for the TSP inserting the next node at the best position
        between two existing nodes of the partial tour.
        Depot nodes are randomly chosen.

        Parameters
        ----------
        seed : int, optional
            Random generator seed (differs behavior from cython to python), by default None
        """
        super().__init__(seed)

    def __call__(self, D: np.ndarray) -> Solution:
        """Solves a TSP based on a pairwise distance matrix.

        Parameters
        ----------
        D : np.ndarray
            2-dimensional distance matrix

        Returns
        -------
        Solution
            Attributes:
            - tour : List[int]
            - cost : float
        """
        return super().__call__(D)


class RandomInsertion(tspconstr.RandomInsertion):

    def __init__(self, seed=None):
        """Constructive heuristic for the TSP inserting a random next node at the best position
        between two existing nodes of the partial tour.
        Depot nodes are randomly chosen.

        Parameters
        ----------
        seed : int, optional
            Random generator seed (differs behavior from cython to python), by default None
        """
        super().__init__(seed)

    def __call__(self, D: np.ndarray) -> Solution:
        """Solves a TSP based on a pairwise distance matrix.

        Parameters
        ----------
        D : np.ndarray
            2-dimensional distance matrix

        Returns
        -------
        Solution
            Attributes:
            - tour : List[int]
            - cost : float
        """
        return super().__call__(D)


class SemiGreedyInsertion(tspconstr.SemiGreedyInsertion):

    def __init__(self, alpha=(0.0, 1.0), seed=None):
        """Greedy-randomized constructive heuristic for the TSP based on inserting the next node
        between two existing nodes of the partial tour.

        Parameters
        ----------
        alpha : tuple, optional
            Alpha parameter - randomly generated at each iteration between range or fixed scalar.
            Use values closer to one for a more greedy approach. By default (0.0, 1.0).

        seed : int, optional
            Random generator seed (differs behavior from cython to python), by default None
        """
        super().__init__(alpha, seed)

    def __call__(self, D: np.ndarray) -> Solution:
        """Solves a TSP based on a pairwise distance matrix.

        Parameters
        ----------
        D : np.ndarray
            2-dimensional distance matrix

        Returns
        -------
        Solution
            Attributes:
            - tour : List[int]
            - cost : float
        """
        return super().__call__(D)


class LocalSearch(tspls.LocalSearch):

    def __init__(self, seed: int = None):
        """Local Search (VNS with first improvement) implementation for TSP.

        Parameters
        ----------
        seed : int, optional
            Random generator seed (differs behavior from cython to python), by default None
        """
        super().__init__(seed)

    def __call__(self, seq: List[int], D: np.ndarray, max_iter=100000):
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
        return super().__call__(seq, D, max_iter)


class SimulatedAnnealing(tspsa.SimulatedAnnealing):

    def __init__(self, T_start=10.0, T_final=0.001, decay=0.99, seed=None):
        """Simulated Annealing for the TSP using a VNS.

        Parameters
        ----------
        T_start : float, optional
            Initial temperature in each search, by default 10.0

        T_final : float, optional
            Final temperature (stop searching), by default 0.001

        decay : float, optional
            Decay factor, by default 0.99

        seed : _type_, optional
            Random generator seed (differs behavior from cython to python), by default None
        """
        super().__init__(T_start, T_final, decay, seed)

    def __call__(self, seq: List[int], D: np.ndarray, max_iter=100000):
        """Solve a TSP based on an initial solution and a distance matrix.

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
        return super().__call__(seq, D, max_iter)
