try:
    from tspgrasp.grasp import Grasp
    from tspgrasp.problem import Problem
    cythonized = True

except:
    from tspgrasp.pure_python.grasp import Grasp
    from tspgrasp.pure_python.problem import Problem
    cythonized = False
