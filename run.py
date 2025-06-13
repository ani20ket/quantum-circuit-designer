import networkx as nx
from core.problem_parser import parse_input
from core.problem_to_qubo import convert_to_qubo
from core.algorithm_selector import select_algorithm
from core.circuit_builder import build_circuit
from core.solver import solve_problem
from core.output_formatter import format_result
from qiskit_optimization.applications import Tsp


def create_random_tsp_graph(n_nodes=4, seed=42):
    tsp = Tsp.create_random_instance(n_nodes, seed=seed)
    return tsp.graph


def main():
    graph = create_random_tsp_graph()
    user_input = {
        "problem_type": "tsp",
        "data": graph
    }

    parsed = parse_input(user_input)

    qp, tsp_instance = convert_to_qubo(parsed)

    algo = select_algorithm(parsed["type"])

    circuit = build_circuit(algo)
    print("Quantum circuit structure built.")

    result = solve_problem(qp, algo)

    solution = format_result(result, tsp_instance)
    print("\n✅ Solution:")
    print("Path:", solution["path"])
    print("Cost:", solution["cost"])


if __name__ == "__main__":
    main()
