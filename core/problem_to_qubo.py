from qiskit_optimization import QuadraticProgram
from qiskit_optimization.applications import Tsp

def convert_to_qubo(parsed_problem):
    """
    Converts a structured problem into a QUBO using Qiskit Optimization.

    Args:
        parsed_problem (dict): Output of parse_input().

    Returns:
        QuadraticProgram, object: QUBO and the problem instance (e.g., Tsp)
    """
    if parsed_problem["type"] == "tsp":
        graph = parsed_problem["data"]
        tsp = Tsp(graph)
        qp = tsp.to_quadratic_program()
        return qp, tsp

    raise NotImplementedError("Only TSP is currently supported.")
