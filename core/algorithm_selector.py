from qiskit_algorithms import QAOA, VQE
from qiskit_algorithms.optimizers import COBYLA, SPSA
from qiskit.primitives import Sampler, Estimator
from qiskit.circuit.library import TwoLocal
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.circuit.library import ZFeatureMap
from qiskit import Aer
from qiskit.algorithms import Grover, AmplificationProblem

def select_algorithm(problem_type, backend=None):
    """
    Selects the appropriate algorithm object based on the problem type.
    """
    if problem_type == "tsp":
        qaoa = QAOA(sampler=Sampler(), optimizer=COBYLA(), reps=1)
        return qaoa

    elif problem_type == "eigenvalue":  # e.g. molecular energy
        ansatz = TwoLocal(rotation_blocks='ry', entanglement_blocks='cz', reps=2)
        vqe = VQE(ansatz=ansatz, optimizer=SPSA(), estimator=Estimator())
        return vqe

    elif problem_type == "oracle_search":
        # Example Grover circuit for a simple oracle: f(x) = 1 only if x = 11
        oracle = QuantumCircuit(2)
        oracle.cz(0, 1)
        oracle_problem = AmplificationProblem(oracle)
        grover = Grover(oracle_problem)
        return grover

    else:
        raise NotImplementedError(f"No algorithm implemented for type: {problem_type}")
