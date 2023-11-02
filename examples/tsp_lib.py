from scipy.spatial.distance import squareform, pdist

from tspgrasp import Grasp, read_tsp_file


if __name__ == "__main__":
    X = read_tsp_file("instances/xqc2175.txt")
    D = squareform(pdist(X))
    grasp = Grasp(seed=42)
    sol = grasp(D, max_iter=1000, time_limit=180)
    print(sol.cost)
    print(sol.tour)
