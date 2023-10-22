import numpy as np


class Problem:

    n_nodes: int
    D: np.ndarray

    def __init__(self, n_nodes: int, D: np.ndarray) -> None:
        self.n_nodes = n_nodes
        self.D = D
