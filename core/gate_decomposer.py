from qiskit import transpile


def decompose_circuit(circuit, basis_gates=None, optimization_level=1):
    """
    Transpiles the circuit into a target gate basis and returns decomposed version.

    Args:
        circuit (QuantumCircuit): The original circuit.
        basis_gates (list): Target basis gates (e.g., ['u3', 'cx']).
        optimization_level (int): Qiskit's transpile optimization level (0-3).

    Returns:
        QuantumCircuit: Decomposed and optimized circuit.
    """
    transpiled = transpile(
        circuit,
        basis_gates=basis_gates or ['u3', 'cx'],
        optimization_level=optimization_level
    )
    return transpiled
