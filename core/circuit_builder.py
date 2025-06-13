def build_circuit(algorithm):
    """
    Returns the ansatz/circuit structure of the algorithm (e.g., QAOA).

    Args:
        algorithm: A Qiskit algorithm object.

    Returns:
        QuantumCircuit
    """
    return algorithm.ansatz
