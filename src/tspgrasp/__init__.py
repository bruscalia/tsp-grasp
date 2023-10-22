import warnings

try:
    from tspgrasp.grasp import Grasp
    from tspgrasp.problem import Problem

except:
    warnings.warn("Failed to import Cython implementations - Using pure Python")
    from tspgrasp.pure_python.grasp import Grasp
    from tspgrasp.pure_python.problem import Problem
