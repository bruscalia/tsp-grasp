# tsp-grasp

Welcome to `tsp-grasp`! A Python package with Heuristics for solving the Traveling Salesman Problem (TSP).


<p align="center">
  <img src="./assets/grasp.gif" width="300" title="icon tsp">
</p>

## Install

To install the package, clone it from github using `git clone https://github.com/bruscalia/tsp-grasp.git` and run `pip install .` or `python setup.py install` in the repository root folder. Make sure Cython and numpy are also available in your python environment.

Alternatively, you can directly run:

```
pip install git+https://github.com/bruscalia/tsp-grasp.git
```

Here is a minimum working example in which a symmetric distances matrix is produced from 2-dimensional coordinates.

## Use

```python
# Imports
import numpy as np
from scipy.spatial.distance import pdist, squareform
from tspgrasp.grasp import Grasp
```

```python
# Create distances matrix
X = np.random.random((100, 2))
D = squareform(pdist(X))

# Instantiate algorithm and solve problem
grasp = Grasp(seed=12)
sol = grasp(D, time_limit=10, max_iter=100)

# Display cost and tour
print(f"Cost: {sol.cost}")
print(f"Tour: {sol.tour}")
```

## Theory

Greedy Randomized Adaptive Search Procedures (GRASP) are metaheuristics constituted by a hybridization of a semi-greedy procedure with a local search method. For more details please refer to Resende & Ribeiro (2016).

Local search moves implemented were based on the work of Vidal et al. (2022).


## Contact

You can reach out to me at bruscalia12@gmail.com

## References

Resende, M. G., & Ribeiro, C. C. (2016). Optimization by GRASP. Springer Science+ Business Media New York. https://doi.org/10.1007/978-1-4939-6530-4

Vidal, T. (2022). Hybrid genetic search for the CVRP: Open-source implementation and SWAP* neighborhood. Computers & Operations Research, 140, 105643. https://doi.org/10.1016/j.cor.2021.105643
