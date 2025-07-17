from core.problem_parser import parse_input
from core.algorithm_selector import select_algorithm
from core.solver import solve_problem
from core.output_formatter import format_result
from core.evaluate_circuit import evaluate_circuit
from qiskit_aer import AerSimulator
import random
import warnings
warnings.filterwarnings("ignore")

from qiskit.providers.fake_provider import FakeLima, FakeManhattan, FakeJakarta
import matplotlib.pyplot as plt


def main():
    problem_types = ["maxcut", "tsp", "knapsack"]

    backends = {
        "FakeLima": AerSimulator.from_backend(FakeLima()),
        "FakeManhattan": AerSimulator.from_backend(FakeManhattan()),
        "FakeJakarta": AerSimulator.from_backend(FakeJakarta()),
    }

    results = []

    for problem_type in problem_types:
        print(f"\nEvaluating problem: {problem_type}")
        import networkx as nx
        if problem_type == "maxcut":
            data = nx.cycle_graph(4)
        elif problem_type == "tsp":
            data = nx.complete_graph(4)
            for (u, v) in data.edges():
                data[u][v]["weight"] = random.randint(1, 10)
        elif problem_type == "knapsack":
            data = {"values": [3, 4, 5], "weights": [2, 3, 4], "max_weight": 5}
        else:
            continue

        user_input = {"problem_type": problem_type, "data": data}
        parsed = parse_input(user_input)
        qp = parsed["problem"].to_quadratic_program()
        algorithm = select_algorithm(problem_type)

        result = solve_problem(qp, algorithm)
        solution = format_result(result, parsed["problem"])
        print("Solution:", solution)

        circuit = algorithm.ansatz

        for backend_name, backend in backends.items():
            eval_result = evaluate_circuit(circuit, backend)
            eval_result.update({
                "problem": problem_type,
                "backend": backend_name
            })
            results.append(eval_result)

            if eval_result["transpiled_circuit"]:
                print(f"[{problem_type} on {backend_name}] - depth: {eval_result['depth']}, error: {eval_result['simulated_error_rate']}")
            else:
                print(f"[{problem_type} on {backend_name}] - Unsupported: {eval_result['error_msg']}")

            if eval_result["transpiled_circuit"]:
                eval_result["transpiled_circuit"].draw(output="mpl", fold=100)
                plt.title(f"{problem_type} on {backend_name}")
                plt.tight_layout()
                plt.savefig(f"{problem_type}_{backend_name}.png")
                plt.close()

    print("\nSummary:")
    for r in results:
        print(f"{r['problem']} on {r['backend']}: depth={r['depth']}, error={r['simulated_error_rate']}, gates={r['gate_count']}")


if __name__ == "__main__":
    main()
