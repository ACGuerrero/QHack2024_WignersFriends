import pennylane as qml
from pennylane import numpy as np
import matplotlib.pyplot as plt

# This little script implements a two-qubit quantum
# circuit that prepares a Bell state and then rotates
# the first qubit by a variable angle around the z-axis.


# First we initialize the circuit. Qubits are called 
# "wires" in PennyLane. 


dev = qml.device('default.qubit', wires=2) 

# We now define a circuit
# To run the code we do it with a decorator, the
# argument is the device object dev
@qml.qnode(dev)
def circuit(theta):
    # Our circuit is very simple. It includes:
    # An X gate on the second qubit
    qml.PauliX(wires=1)
    # A CNOT gate between the two qubits
    qml.CNOT(wires=[1,0])
    # A rotation about the Y axis of angle theta
    qml.RY(theta,wires=0)
    # And it returns the expectation value of Z of the
    # first qubit
    return qml.expval(qml.PauliZ(wires=0))

# Now we try our function using an array of angles
thetas = np.arange(-np.pi,np.pi,0.01)
measurements = np.zeros(len(thetas))
for i, theta in enumerate(thetas):
    measurements[i] = circuit(theta)

plt.figure()
plt.plot(thetas,measurements)
plt.xlabel(r'$\theta$')
plt.ylabel(r'$\langle \sigma_{z} \rangle$')
plt.title('My first measurement circuit')
plt.savefig('figures/first_circuit.pdf')
plt.close()
