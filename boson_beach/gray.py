import pennylane as qml
import pennylane.numpy as np

def binary_to_grey(num_wires):

    """
    A function mapping binary encoded qubits to gray code.

    Args:
        num_wires (int): The number of qubits.

    """


    # Put your solution here #
    for i in range(num_wires-1,0,-1):
        qml.CNOT(wires=[i-1, i])
    

num_wires = 4
drawer = qml.draw(binary_to_grey, show_all_wires=True)
print(drawer(num_wires))