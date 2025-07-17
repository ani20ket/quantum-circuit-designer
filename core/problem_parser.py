from qiskit_optimization.applications import Tsp, Maxcut, Knapsack


def parse_input(user_input):
    problem_type = user_input["problem_type"]
    data = user_input["data"]

    if problem_type == "tsp":
        tsp = Tsp(data)
        return {"type": "tsp", "problem": tsp}

    elif problem_type == "maxcut":
        maxcut = Maxcut(data)
        return {"type": "maxcut", "problem": maxcut}

    elif problem_type == "knapsack":
        values = data["values"]
        weights = data["weights"]
        max_weight = data["max_weight"]
        knapsack = Knapsack(values, weights, max_weight)
        return {"type": "knapsack", "problem": knapsack}

    else:
        raise ValueError(f"Unknown problem type: {problem_type}")
