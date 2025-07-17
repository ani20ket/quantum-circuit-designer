from qiskit_optimization.algorithms import MinimumEigenOptimizer

def solve_problem(qubo, algorithm):
    solver = MinimumEigenOptimizer(algorithm)
    return solver.solve(qubo)
