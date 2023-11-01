import warnings

try:
    from tspgrasp.grasp import Grasp
    from tspgrasp.constructive import GreedyCheapestArc, SemiGreedy
    from tspgrasp.simulated_annealing import SimulatedAnnealing
    from tspgrasp.local_search import LocalSearch

except:
    warnings.warn("Failed to import Cython implementations - Using pure Python")
    from tspgrasp.pure_python.grasp import GrasPy as Grasp
    from tspgrasp.pure_python.constructive import GreedyCheapestArc, SemiGreedy
    from tspgrasp.pure_python.simulated_annealing import SimulatedAnnealing
    from tspgrasp.pure_python.local_search import LocalSearch
