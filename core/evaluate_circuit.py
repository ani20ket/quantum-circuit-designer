from qiskit import transpile
from qiskit.providers.backend import Backend
from qiskit.transpiler.exceptions import TranspilerError
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

        # Accurate error breakdown
        try:
            props = backend.properties()
            one_q_error = 0.0
            two_q_error = 0.0
            one_q_count = 0
            two_q_count = 0

            for instr, qargs, _ in transpiled.data:
                gate_name = instr.name
                qubits = [q.index for q in qargs]

                try:
                    gate_prop = props.gate_error(gate_name, qubits)
                    if len(qubits) == 1:
                        one_q_error += gate_prop
                        one_q_count += 1
                    elif len(qubits) == 2:
                        two_q_error += gate_prop
                        two_q_count += 1
                except Exception:
                    continue

            result["error_breakdown"] = {
                "1-qubit": round(one_q_error, 5),
                "2-qubit": round(two_q_error, 5),
            }
            result["estimated_error"] = round(one_q_error + two_q_error, 5)
        except Exception:
            result["estimated_error"] = "Unavailable"
            result["error_breakdown"] = {"1-qubit": "Unavailable", "2-qubit": "Unavailable"}

    except TranspilerError as e:
        result.update({
            "transpiled_circuit": None,
            "gate_count": {},
            "depth": "N/A",
            "width": "N/A",
            "size": "N/A",
            "num_qubits": "Too many",
            "estimated_error": "Unsupported",
            "error_breakdown": {"1-qubit": "Unsupported", "2-qubit": "Unsupported"},
            "error_msg": str(e)
        })

    return result
