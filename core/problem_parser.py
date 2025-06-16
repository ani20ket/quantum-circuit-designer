from qiskit_optimization.applications import Tsp, Maxcut, Knapsack, VertexCover
import networkx as nx
import numpy as np

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

    elif problem_type == "portfolio":
        maxcut = Maxcut(data)
        return {"type": "maxcut", "problem": maxcut}

    elif problem_type == "vertex_cover":
        vc = VertexCover(data)
        return {"type": "vertex_cover", "problem": vc}

    elif problem_type == "eigenvalue":
        # Assumes input is already a Hamiltonian (SummedOp)
        return {"type": "eigenvalue", "problem": data}

    elif problem_type == "oracle_search":
        return {"type": "oracle_search", "problem": data}

    elif problem_type == "custom":
        return {"type": "custom", "problem": data}

    else:
        raise ValueError(f"Unknown problem type: {problem_type}")
