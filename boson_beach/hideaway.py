import json
import pennylane as qml
import pennylane.numpy as np

# Write any helper functions you need here
def myhadamard(wires):
    qml.RX(np.pi, wires = wires)
    qml.RY(np.pi/2, wires = wires)

def mycnot(wires):
    myhadamard(wires = wires[1])
    qml.CZ(wires = wires)
    myhadamard(wires = wires[1])


def GHZ_circuit(noise_param,n_qubits):

    """
    Quantum circuit that prepares an imperfect GHZ state using gates native to a neutral atom device.

    Args:
        - noise_param (float): Parameter that quantifies the noise in the CZ gate, modelled as a 
        depolarizing channel on the target qubit. noise_param is the parameter of the depolarizing channel
        following the PennyLane convention.
        - n_qubits (int): The number of qubits in the prepared GHZ state.
    Returns:
        - (np.tensor): A density matrix, as returned by `qml.state`, representing the imperfect GHZ state.
    
    """
    # Put your code here
    myhadamard(wires = 0)
    for i in range(n_qubits-1):
        mycnot(wires = [i, i+1])
        qml.DepolarizingChannel(noise_param, wires = i+1)
    return qml.state()


def GHZ_fidelity(noise_param, n_qubits):

    """
    Calculates the fidelity between the imperfect GHZ state returned by GHZ_circuit and the ideal GHZ state.

    Args:
        - noise_param (float): Parameter that quantifies the noise in the CZ gate, modelled as a 
        depolarizing channel on the target qubit. noise_param is the parameter of the depolarizing channel
        following the PennyLane convention.
        - n_qubits (int): The number of qubits in the GHZ state.
    Returns:
        - (float): The fidelity between the noisy and ideal GHZ states.
    """
    
    dev = qml.device('default.mixed', wires=n_qubits)
    
    GHZ_QNode = qml.QNode(GHZ_circuit,dev)
    
    # Use GHZ_QNode to find the fidelity between
    # the noisy GHZ state and an ideal GHZ state
    noisy = GHZ_circuit(noise_param, n_qubits)
    ideal = GHZ_circuit(0., n_qubits)
    return qml.math.fidelity(noisy, ideal)

n_qubits = 3
noise_param = 0.1
dev = qml.device('default.mixed', wires=n_qubits)
GHZ_QNode = qml.QNode(GHZ_circuit,dev)
result = GHZ_circuit(noise_param,n_qubits)
print(result)