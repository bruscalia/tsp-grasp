class Node:

    def __init__(
        self,
        index,
        is_depot=False
    ):
        self.index = index
        self.is_depot = is_depot
        self.cum_dist = 0.0
        self.cum_rdist = 0.0

    def reset_dimensions(self):
        self.cum_dist = 0.0
        self.cum_rdist = 0.0
