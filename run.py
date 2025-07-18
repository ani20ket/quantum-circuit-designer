from core.problem_parser import parse_input
from core.algorithm_selector import select_algorithm
from core.solver import solve_problem
from core.output_formatter import format_result
from core.evaluate_circuit import evaluate_circuit
import random
import warnings
warnings.filterwarnings("ignore")

from qiskit.providers.fake_provider import FakeLima, FakeManhattan, FakeJakarta
import matplotlib.pyplot as plt
import pandas as pd


def main():
    problem_types = ["maxcut", "tsp", "knapsack"]

    backends = {
        "FakeLima": FakeLima(),
        "FakeManhattan": FakeManhattan(),
        "FakeJakarta": FakeJakarta(),
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
                "backend": backend_name,
                "1Q Error": eval_result.get("error_breakdown", {}).get("1-qubit", None),
                "2Q Error": eval_result.get("error_breakdown", {}).get("2-qubit", None)
            })
            results.append(eval_result)

            if eval_result["transpiled_circuit"]:
                print(f"[{problem_type} on {backend_name}] - depth: {eval_result['depth']}, error: {eval_result['estimated_error']}")
            else:
                print(f"[{problem_type} on {backend_name}] - Unsupported: {eval_result['error_msg']}")

            if eval_result["transpiled_circuit"]:
                eval_result["transpiled_circuit"].draw(output="mpl", fold=100)
                plt.title(f"{problem_type} on {backend_name}")
                plt.tight_layout()
                plt.savefig(f"{problem_type}_{backend_name}.png")
                plt.close()

    # Output summary
    df = pd.DataFrame(results)
    print("\nSummary:")
    print(df[["problem", "backend", "depth", "estimated_error", "1Q Error", "2Q Error", "gate_count"]])

    df.to_csv("evaluation_summary.csv", index=False)

    # Filter and plot valid error values only
    df = df[pd.to_numeric(df["1Q Error"], errors="coerce").notnull()]
    df["1Q Error"] = df["1Q Error"].astype(float)
    df["2Q Error"] = df["2Q Error"].astype(float)

    fig, ax = plt.subplots(figsize=(10, 6))
    df.plot(kind='bar', x='problem', y=['1Q Error', '2Q Error'], ax=ax, title="1Q vs 2Q Error by Problem")
    plt.tight_layout()
    plt.savefig("1Q_vs_2Q_error.png")
    plt.close()


if __name__ == "__main__":
    main()
