import pennylane as qml
from pennylane import numpy as np



dev = qml.device("default.qubit", wires=1)
    
def beam_splitter_matrix(r):
    return np.array([[r,np.sqrt(1-r**2)],[np.sqrt(1-r**2),-r]])

@qml.qnode(dev)

def my_circuit(r):
    qml.QubitUnitary(beam_splitter_matrix(r), wires=0)

    # First measurement
    
    result = qml.sample(qml.PauliZ(0))

    # Depending on the measurement outcome, apply a second beam splitter
    if result[0] == 1:
        qml.QubitUnitary(beam_splitter_matrix(r), wires=0)

    # Return the probabilities of being in the states 0 and 1
    return qml.probs(wires=[0])

r = 0.1

drawer = qml.draw(my_circuit, show_all_wires=True, wire_order=[0,1])
print(drawer(r))

result = my_circuit(r)
print(result)
