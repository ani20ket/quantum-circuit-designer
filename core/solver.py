from qiskit_optimization.algorithms import MinimumEigenOptimizer

def solve_problem(qubo, algorithm):
    """
    Solves the optimization problem using the given algorithm.

    Args:
        qubo: A QUBO/QuadraticProgram object.
        algorithm: A Qiskit algorithm instance (e.g., QAOA).

    Returns:
        OptimizationResult
    """
    solver = MinimumEigenOptimizer(algorithm)
    return solver.solve(qubo)
