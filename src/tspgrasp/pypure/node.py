class Node:

    index: int
    prev: 'Node'
    next: 'Node'
    is_depot: bool
    cum_dist: float
    cum_rdist: float

    def __init__(
        self,
        index,
        is_depot=False
    ):
        self.index = index
        self.is_depot = is_depot
        self.cum_dist = 0.0
        self.cum_rdist = 0.0
        self.next = None
        self.prev = None

    def reset_dimensions(self):
        self.cum_dist = 0.0
        self.cum_rdist = 0.0
