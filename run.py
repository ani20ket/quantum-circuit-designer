import networkx as nx
from core.problem_parser import parse_input
from core.problem_to_qubo import convert_to_qubo
from core.algorithm_selector import select_algorithm
from core.circuit_builder import build_circuit
from core.solver import solve_problem
from core.output_formatter import format_result
from core.hardware_aware_optimizer import optimize_for_backend
from qiskit_optimization.applications import Tsp
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.visualization import plot_circuit_layout
import matplotlib.pyplot as plt


def create_random_tsp_graph(n_nodes=4, seed=42):
    tsp = Tsp.create_random_instance(n_nodes, seed=seed)
    return tsp.graph

def main():
    # Step 1: Create random TSP problem
    graph = create_random_tsp_graph()
    user_input = {
        "problem_type": "tsp",
        "data": graph
    }

    # Step 2: Parse and convert
    parsed = parse_input(user_input)
    qp, tsp_instance = convert_to_qubo(parsed)

    # Step 3: Select QAOA algorithm
    algorithm = select_algorithm(parsed["type"])

    # Step 4: Force circuit generation (QAOA needs this)
    _ = MinimumEigenOptimizer(algorithm).solve(qp)

    # Step 5: Build and optimize the circuit
    circuit = build_circuit(algorithm)
    optimized_circuit = optimize_for_backend(circuit)

    # Optional: Visualize and save
    optimized_circuit.draw(output='mpl')
    plt.title("Optimized Quantum Circuit")
    plt.tight_layout()
    plt.savefig("optimized_qaoa_circuit.png")
    plt.close()

    # Step 6: Solve the problem
    result = solve_problem(qp, algorithm)

    # Step 7: Display solution
    solution = format_result(result, tsp_instance)
    print("\n✅ Solution:")
    print("Path:", solution["path"])
    print("Cost:", solution["cost"])

if __name__ == "__main__":
    main()
