import pennylane as qml

dev = qml.device('default.qubit', wires=3)

@qml.qnode(dev)

def circuit(state):
    qml.PauliX(wires = 0)
    qml.PauliX(wires = 1)
    qml.Toffoli(wires = [0,1,2])
    qml.PauliX(wires = 0)
    qml.PauliX(wires = 1)
    qml.PauliX(wires = 2)

state = [1,0,0]
drawer = qml.draw(circuit, show_all_wires=True, wire_order=[0,1])
print(drawer(state))