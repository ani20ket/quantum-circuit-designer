from qiskit import transpile
from qiskit.providers.backend import Backend
from qiskit.transpiler.exceptions import TranspilerError
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
import random

def evaluate_circuit(circuit, backend: Backend, optimization_level: int = 3) -> dict:
    result = {}

    try:
        transpiled = transpile(circuit, backend=backend, optimization_level=optimization_level)
        result["transpiled_circuit"] = transpiled
        result["gate_count"] = transpiled.count_ops()
        result["depth"] = transpiled.depth()
        result["width"] = transpiled.width()
        result["size"] = transpiled.size()
        result["num_qubits"] = transpiled.num_qubits

        # Attempt estimated error (might fail if no properties)
        try:
            props = backend.properties()
            total_error = 0.0
            for gate, count in transpiled.count_ops().items():
                gate_errors = [
                    g.error
                    for g in props.gates
                    if g.gate == gate and hasattr(g, 'error')
                ]
                avg_error = sum(gate_errors) / len(gate_errors) if gate_errors else 0
                total_error += count * avg_error
            result["estimated_error"] = round(total_error, 5)
        except Exception:
            result["estimated_error"] = "Unavailable"

        # Always simulate with noise
        try:
            noise_model = NoiseModel()
            noise_model.add_all_qubit_quantum_error(depolarizing_error(0.3, 1), ['rz', 'sx'])
            noise_model.add_all_qubit_quantum_error(depolarizing_error(0.4, 2), ['cx'])

            coupling_map = [[i, i + 1] for i in range(transpiled.num_qubits - 1)]

            simulator = AerSimulator()

            # Bind parameters if circuit has any
            if transpiled.parameters:
                param_bindings = {param: random.uniform(0, 2 * 3.1416) for param in transpiled.parameters}
                transpiled = transpiled.bind_parameters(param_bindings)

            job = simulator.run(
                transpiled,
                shots=1024,
                noise_model=noise_model,
                basis_gates=['rz', 'sx', 'cx'],
                coupling_map=coupling_map
            )

            sim_result = job.result()
            counts = sim_result.get_counts()

            total_shots = sum(counts.values())
            most_common = max(counts, key=counts.get)
            error_rate = 1 - (counts[most_common] / total_shots)

            result["simulated_error_rate"] = round(error_rate, 5)

        except Exception as e:
            result["simulated_error_rate"] = f"SimError: {str(e)}"

    except TranspilerError as e:
        result.update({
            "transpiled_circuit": None,
            "gate_count": {},
            "depth": "N/A",
            "width": "N/A",
            "size": "N/A",
            "num_qubits": "Too many",
            "estimated_error": "Unsupported",
            "simulated_error_rate": "Unsupported",
            "error_msg": str(e)
        })

    return result
