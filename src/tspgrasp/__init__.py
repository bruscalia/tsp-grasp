import warnings

try:
    from tspgrasp.grasp import Grasp

except:
    warnings.warn("Failed to import Cython implementations - Using pure Python")
    from tspgrasp.pure_python.grasp import Grasp
