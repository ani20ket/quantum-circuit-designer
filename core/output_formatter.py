def format_result(result, problem_instance):
    path = problem_instance.interpret(result.x)
    return {
        "path": path,
        "cost": result.fval
    }
