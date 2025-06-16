from core.problem_parser import parse_input
from core.algorithm_selector import select_algorithm
from core.circuit_builder import build_circuit
from core.solver import solve_problem
from core.output_formatter import format_result
from core.hardware_aware_optimizer import optimize_for_backend
from qiskit_optimization.algorithms import MinimumEigenOptimizer
import matplotlib.pyplot as plt

def main():
    # 🔁 Swap this input to test different problems
    import networkx as nx
    graph = nx.cycle_graph(5)

    user_input = {
        "problem_type": "maxcut",  # Change to "tsp", "knapsack", etc. as needed
        "data": graph
    }

    parsed = parse_input(user_input)
    problem_type = parsed["type"]
    problem_obj = parsed["problem"]

    if problem_type in ["tsp", "maxcut", "knapsack", "vertex_cover"]:
        qp = problem_obj.to_quadratic_program()
        algorithm = select_algorithm(problem_type)

        _ = MinimumEigenOptimizer(algorithm).solve(qp)

        circuit = build_circuit(algorithm)
        optimized = optimize_for_backend(circuit)

        optimized.draw(output='mpl')
        plt.title("Optimized Quantum Circuit")
        plt.tight_layout()
        plt.savefig("optimized_circuit.png")
        plt.close()

        result = solve_problem(qp, algorithm)
        solution = format_result(result, problem_obj)

        print("\nSolution:")
        print("Path or Binary Output:", solution["path"])
        print("Cost:", solution["cost"])

    else:
        raise ValueError(f"Unsupported or unhandled problem type: {problem_type}")

if __name__ == "__main__":
    main()
