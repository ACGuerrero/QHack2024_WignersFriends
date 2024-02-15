import pennylane as qml
import pennylane.numpy as np
symbols = ["H", "H", "H"]

    # Create the molecule
d = 0.8
coordinates = np.array([[-d/2,-d/2,0],[0,d/2,0],[d/2,-d/2,0]])

# Get the hamiltonian and the number of qubits
hamiltonian , num_wires = qml.qchem.molecular_hamiltonian(symbols, coordinates, charge = 1)
# Prepare a state using fock method
hf = qml.qchem.hf_state(electrons = 2, orbitals = num_wires)
# Create a device
dev = qml.device('default.qubit',wires = num_wires)

# Preparing ground state
@qml.qnode(dev)
    
def circuit(params):
    qml.BasisState(hf, wires=range(num_wires))
    qml.DoubleExcitation(params[0], wires=[0, 1, 2, 3])
    qml.DoubleExcitation(params[1], wires=[0, 1, 4, 5])

    return qml.expval(hamiltonian)

opt = qml.GradientDescentOptimizer(stepsize = 0.4)
theta = np.array([0.,0.], requires_grad = True)

energy = [circuit(theta)]
angle = [theta]
max_iterations = 20

for n in range(max_iterations):
    theta, _ = opt.step_and_cost(circuit,theta)
    energy.append(circuit(theta))
    angle.append(theta)
    if n % 5 == 0:
        print('Iteration: ', n, 'Energy: ', circuit(theta))
print('Final energy: ', circuit(theta))
