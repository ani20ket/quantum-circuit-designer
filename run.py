from core.problem_parser import parse_input
from core.problem_to_qubo import convert_to_qubo
from core.algorithm_selector import select_algorithm
from core.circuit_builder import build_circuit
from core.solver import solve_problem
from core.output_formatter import format_result
from core.hardware_aware_optimizer import optimize_for_backend
from qiskit_optimization.applications import Tsp
from qiskit_optimization.algorithms import MinimumEigenOptimizer
import matplotlib.pyplot as plt
import networkx as nx


def create_random_tsp_graph(n_nodes=4, seed=42):
    tsp = Tsp.create_random_instance(n_nodes, seed=seed)
    return tsp.graph

def main():
    # Choose your problem type: tsp, eigenvalue, oracle_search
    user_input = {
        "problem_type": "tsp",
        "data": create_random_tsp_graph()
    }

    parsed = parse_input(user_input)
    algo = select_algorithm(parsed["type"])

    if parsed["type"] in ["tsp", "eigenvalue"]:
        qp, problem_instance = convert_to_qubo(parsed)

        if hasattr(algo, 'ansatz'):
            _ = MinimumEigenOptimizer(algo).solve(qp)

        circuit = build_circuit(algo)
        optimized = optimize_for_backend(circuit)

        optimized.draw(output='mpl')
        plt.title("Optimized Circuit")
        plt.savefig("optimized_circuit.png")
        plt.close()

        result = solve_problem(qp, algo)
        solution = format_result(result, problem_instance)

        print("\n Solution:")
        print("Path/Output:", solution["path"])
        print("Cost:", solution["cost"])

    elif parsed["type"] == "oracle_search":
        result = algo.run()
        print("\nGrover Result:")
        print(result)

    else:
        raise ValueError("Unsupported problem type for pipeline.")

if __name__ == "__main__":
    main()
