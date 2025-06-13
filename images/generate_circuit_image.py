from core.problem_to_qubo import convert_to_qubo
from core.problem_parser import parse_input
from core.algorithm_selector import select_algorithm
from core.circuit_builder import build_circuit
from qiskit_optimization.applications import Tsp
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

    # Step 3: Select QAOA algorithm and build circuit
    algorithm = select_algorithm(parsed["type"])
    # circuit = build_circuit(algorithm)

    # Run a dummy problem to initialize the ansatz properly
    from qiskit_optimization.applications import Tsp

    # Create a dummy QUBO just to generate the circuit
    dummy_graph = Tsp.create_random_instance(3, seed=1).graph
    dummy_tsp = Tsp(dummy_graph)
    dummy_qp = dummy_tsp.to_quadratic_program()

    # Use the actual algorithm
    algorithm = select_algorithm("tsp")

    # Run algorithm once to trigger circuit generation
    from qiskit_optimization.algorithms import MinimumEigenOptimizer
    dummy_solver = MinimumEigenOptimizer(algorithm)
    dummy_solver.solve(dummy_qp)

    # Now safely get the ansatz
    circuit = algorithm.ansatz

    # Step 4: Draw and save the circuit
    print("Saving circuit diagram as 'qaoa_circuit.png'...")
    circuit.decompose().decompose().draw(output='mpl')
    plt.tight_layout()
    plt.savefig("qaoa_circuit.png")
    plt.close()
    print("✅ Circuit image saved.")

if __name__ == "__main__":
    main()
