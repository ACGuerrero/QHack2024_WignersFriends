import json
import pennylane as qml
import pennylane.numpy as np

symbols = ["H", "H", "H"]


def h3_ground_energy(bond_length):
    
    """
    Uses VQE to calculate the ground energy of the H3+ molecule with the given bond length.
    
    Args:
        - bond_length(float): The bond length of the H3+ molecule modelled as an
        equilateral triangle.
    Returns:
        - Union[float, np.tensor, np.array]: A float-like output containing the ground 
        state of the H3+ molecule with the given bond length.
    """
    
    # Create the molecule
    d = bond_length
    coordinates = np.array([[-d/2,-d/2,0],[0,d/2,0],[d/2,-d/2,0]])
    coordinates1 = np.array([[0,0,0],[d/2,d,0],[d,0,0]])

    # Get the hamiltonian and the number of qubits
    hamiltonian , num_wires = qml.qchem.molecular_hamiltonian(symbols, coordinates, charge = 1)
    hamiltonian1 , num_wires1 = qml.qchem.molecular_hamiltonian(symbols, coordinates1, charge = 1)
    # Prepare a state using fock method
    hf = qml.qchem.hf_state(electrons = 2, orbitals = num_wires)
    hf1 = qml.qchem.hf_state(electrons = 2, orbitals = num_wires)
    # Create a device
    dev = qml.device('default.qubit',wires = num_wires)

    # Preparing ground state
    @qml.qnode(dev)
    def exp_energy(state):
        qml.BasisState(np.array(state), wires = range(num_wires))
        return qml.expval(hamiltonian)
    
    print(exp_energy(hf))
    print(exp_energy(hf1))
    
    def energy_to_minimize(angles):
        qml.BasisState(hf, wires = range(num_wires))
        qml.DoubleExcitation(angles[0], wires = [0,1,2,3])
        qml.DoubleExcitation(angles[1], wires = [0,1,4,5])
        return qml.expval(hamiltonian)

    opt = qml.GradientDescentOptimizer(stepsize = 0.1)

    angles = np.array([0.,0.], requires_grad = True)
    energies = [energy_to_minimize(angles)]
    angles_list = [angles]
    num_it = 20

    for i in range(num_it):
        angles, _ = opt.step_and_cost(energy_to_minimize,angles)
        energies.append(energy_to_minimize(angles))
        angles_list.append(angles)
        if i % 5 == 0:
            print(f"Step {i}, Energy {energies[-1]}")
    return energies[-1]

if __name__ == '__main__':
    bond_length = 0.8
    print(h3_ground_energy(bond_length))