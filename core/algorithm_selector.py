from qiskit_algorithms import QAOA, VQE, Grover
from qiskit_algorithms.optimizers import COBYLA, SPSA
from qiskit.primitives import Sampler, Estimator
from qiskit.circuit.library import TwoLocal
from qiskit import QuantumCircuit
from qiskit.algorithms import AmplificationProblem

def select_algorithm(problem_type):
    """
    Selects and returns the appropriate algorithm based on the problem type.
    """

    if problem_type in ["tsp", "maxcut", "knapsack", "vertex_cover", "portfolio", "custom"]:
        qaoa = QAOA(sampler=Sampler(), optimizer=COBYLA(), reps=1)
        return qaoa

    elif problem_type == "eigenvalue":
        ansatz = TwoLocal(rotation_blocks='ry', entanglement_blocks='cz', reps=2)
        vqe = VQE(ansatz=ansatz, optimizer=SPSA(), estimator=Estimator())
        return vqe

    elif problem_type == "oracle_search":
        oracle = QuantumCircuit(2)
        oracle.cz(0, 1)
        oracle_problem = AmplificationProblem(oracle)
        grover = Grover(oracle_problem)
        return grover

    else:
        raise NotImplementedError(f"No algorithm available for: {problem_type}")
