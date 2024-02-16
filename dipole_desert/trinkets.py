import json
import pennylane as qml
import pennylane.numpy as np


    
def preparing_matrix(c0,c1):
    h = qml.matrix(qml.Hadamard(1))
    cx = qml.matrix(qml.CNOT([1,2]))
    id = np.eye(2)

    U1 = c0*np.matmul(cx,np.kron(h,id))
    U2 = c1*np.kron(id,h)
    return U1+U2

dev = qml.device('default.qubit', wires=[0,1,2])

@qml.qnode(dev)
def cloning_machine(coefficients,wire):
    """
    Returns the reduced density matrix on a wire for the cloning machine circuit.
    
    Args:
        - coefficients (np.array(float)): an array [c0,c1] containing the coefficients parametrizing
        the input state fed into the middle and bottom wires of the cloning machine.
        wire (int): The wire on which we calculate the reduced density matrix.

    Returns:
        - np.tensor(complex): The reduced density matrix on wire = wire, as returned by qml.density_matrix.
    
    """
    
    matrix = preparing_matrix(coefficients[0],coefficients[1])
    qml.QubitUnitary(matrix, wires=[1,2])

    qml.CNOT([0,1])
    qml.CNOT([0,2])
    qml.CNOT([1,0])
    qml.CNOT([2,0])
    # Return the reduced density matrix
    return qml.density_matrix(wires=wire)


def fidelity(coefficients):
    
    
    densit00=cloning_machine(coefficients,wire=0)
    densit10=cloning_machine(coefficients,wire=1)

    fidelity_0 = qml.math.fidelity(densit00, np.outer([1, 0], [1, 0]))
    fidelity_1 = qml.math.fidelity(densit10, np.outer([1, 0], [1, 0]))
    
    return [fidelity_0, fidelity_1]


"print(fidelity([0.5773502691896258, 0.5773502691896257]))"
print(fidelity([0.2, 0.8848857801796105]))

coefficients = [0.2, 0.8848857801796105]
drawer = qml.draw(cloning_machine, show_all_wires=True)
print(drawer(coefficients,wire=0))