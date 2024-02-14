import json
import pennylane as qml
import pennylane.numpy as np

dev = qml.device('default.qubit', wires = 2)

@qml.qnode(dev)
def trotterize(alpha, beta, time, depth):
    """This quantum circuit implements the Trotterization of a Hamiltonian given by a linear combination
    of tensor products of X and Z Pauli gates.

    Args:
        alpha (float): The coefficient of the XX term in the Hamiltonian, as in the statement of the problem.
        beta (float): The coefficient of the YY term in the Hamiltonian, as in the statement of the problem.
        time (float): Time interval during which the quantum state evolves under the interactions specified by the Hamiltonian.
        depth (int): The Trotterization depth.

    Returns:
        (numpy.array): The probabilities of measuring each computational basis state.
    """


    # Put your code here #
    
    for i in range(depth):
        qml.IsingXX(2*alpha*time/depth, wires = [0,1])
        qml.IsingZZ(2*beta*time/depth, wires = [0,1])
    # Return the probabilities
    return qml.probs(wires=[0, 1])

alpha = 0.5
beta = 0.5
depth = 1
time = 1.0
drawer = qml.draw(trotterize, show_all_wires=True, wire_order=[0,1])
print(drawer(alpha, beta, time, depth))
