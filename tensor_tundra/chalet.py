import pennylane as qml
import pennylane.numpy as np

# Define your device

dev = qml.device('default.mixed', wires = 1)


@qml.qnode(dev)
def random_gate(p,q,r):

    """
    Applies a Pauli X, Pauli Y, Pauli Z or does nothing at random.

    Args:
        - p (float): probability of applying Pauli X.
        - q (float): probability of applying Pauli Y.
        - r (float): probability of applying Pauli Z.

    Returns:
        - (np.tensor(float)): Measurement probabilities in the computational basis.

    """


    # Okay so I believe that there are many ways to solve this problem
    # Either we use a random number, or we create a quantum channel.
    # Pennylane accepts channels, we just need to give the Kraus operators.
    # In this case, they are nothing less than the Pauli operators with a sqrt factor
    x = qml.PauliX.compute_matrix()
    y = qml.PauliY.compute_matrix()
    z = qml.PauliZ.compute_matrix()
    # Now the Kraus operators
    kraus_ops = [np.sqrt(p)*x, np.sqrt(q)*y, np.sqrt(r)*z, np.sqrt(1-p-q-r)*np.eye(2)]
    # Now we apply the channel
    qml.QubitChannel(kraus_ops, wires = 0)

    # Measurement
    return qml.probs(wires = 0)

# Now let us call the circuit and print the probabilities
p = 0.1
q = 0.2
r = 0.3
print(random_gate(p, q, r))