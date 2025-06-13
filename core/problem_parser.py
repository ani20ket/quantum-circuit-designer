def parse_input(user_input):
    """
    Parses the user input dictionary and extracts problem type, parameters, and constraints.

    Args:
        user_input (dict): Input with keys like 'problem_type', 'graph', 'constraints'.

    Returns:
        dict: Structured internal representation of the problem.
    """
    problem_type = user_input.get("problem_type")
    data = user_input.get("data")
    constraints = user_input.get("constraints", {})

    return {
        "type": problem_type,
        "data": data,
        "constraints": constraints
    }
