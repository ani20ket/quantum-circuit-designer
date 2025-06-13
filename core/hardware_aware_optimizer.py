from qiskit import transpile

def optimize_for_backend(circuit, backend=None):
    """
    Transpiles and optimizes a quantum circuit for a given backend.

    Args:
        circuit (QuantumCircuit): Original circuit.
        backend (Backend or None): Qiskit backend object. If None, defaults to basis_gates=['u3', 'cx'].

    Returns:
        QuantumCircuit: Transpiled and optimized circuit.
    """
    if backend:
        transpiled = transpile(circuit, backend=backend, optimization_level=3)
    else:
        transpiled = transpile(circuit, basis_gates=['u3', 'cx'], optimization_level=3)

    print("🧠 Hardware-Aware Optimization Summary:")
    print("Gate Count:", transpiled.count_ops())
    print("Depth:", transpiled.depth())

    return transpiled
