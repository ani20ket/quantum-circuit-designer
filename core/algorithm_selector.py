from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler

def select_algorithm(problem_type, **kwargs):
    """
    Selects the appropriate quantum algorithm based on problem type.

    Returns:
        Qiskit MinimumEigenOptimizer-compatible instance
    """
    if problem_type == "tsp":
        qaoa = QAOA(sampler=Sampler(), optimizer=COBYLA(), reps=1)
        return qaoa

    raise NotImplementedError("Algorithm selection only supports TSP for now.")
