def format_result(result, problem_instance):
    """
    Converts Qiskit result to a human-readable format.

    Args:
        result: Qiskit OptimizationResult
        problem_instance: Original TSP or other problem object

    Returns:
        dict: Readable solution with path and cost
    """
    path = problem_instance.interpret(result.x)
    return {
        "path": path,
        "cost": result.fval
    }
