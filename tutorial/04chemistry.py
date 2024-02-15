import pennylane as qml
from pennylane import numpy as np
from pennylane import qchem

# Symbols for the molecule, in this case H2
symbols = ['H','H']
# The coordinates of each atom inside the molecule
coordinates = np.array([[-0.673,0,0],[0.673,0,0]])
# Now let us obtain the molecular Hamiltonian
H, qubits = qchem.molecular_hamiltonian(symbols,coordinates)
# H is the hamiltonian, qubits is the number of qubits

# Now let us calculate the expectation value of the energy

WIRES = qubits 
dev = qml.device('default.qubit',wires = WIRES)

@qml.qnode(dev)

def exp_energy(state):
    '''
    The input is a state in the Jordan Wigner representation
    as a python array
    '''
    qml.BasisState(np.array(state), wires = range(WIRES))
    return qml.expval(H)

# The state [1,0,1,0] corresponds to an electron
# with spin up the first energy level, and one in
# the second energy level, both with spin up

print(exp_energy([1,0,1,0]))

# We can obtain the ground state using qchem.hf_state


hf = qchem.hf_state(electrons = 2, orbitals = 4)


print(exp_energy(hf))