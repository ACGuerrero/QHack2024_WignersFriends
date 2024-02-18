import pennylane as qml
import pennylane.numpy as np

dev = qml.device('default.qutrit', wires=1)
@qml.qnode(dev)
def example_circuit():
    qml.QutritBasisState(np.array([2]), wires=[0])
    return qml.state()
print(example_circuit())
