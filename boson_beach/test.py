import pennylane as qml
import pennylane.numpy as np

molecules = {
    "H2": 
        {"symbols": ["H", "H"], "E0": 0, "E_dissociation": 0, "bond lengths": np.arange(0.5, 9.3, 0.3)}, 
    "Li2": 
        {"symbols": ["Li", "Li"], "E0": 0, "E_dissociation": 0, "bond lengths": np.arange(3.5, 8.3, 0.3)}, 
    "LiH": 
        {"symbols": ["Li", "H"], "E0": 0, "E_dissociation": 0, "bond lengths": np.arange(2.0, 6.6, 0.3)}
}


def potential_energy_surface(symbols, bond_lengths):
    """Calculates the molecular energy over various bond lengths (AKA the 
    potential energy surface) using the Hartree Fock method.
    
    Args:
        symbols (list(string)): 
            A list of atomic symbols that comprise the diatomic molecule of interest.
        bond_lengths (numpy.tensor): Bond lengths to calculate the energy over.

        
    Returns:
        hf_energies (numpy.tensor): 
            The Hartree Fock energies at every bond length value.
    """


    hf_energies = []

    # Put your code here #
    for i in range(len(bond_lengths)):
        print('Now obtaining the energy for the bond length:', bond_lengths[i])
        d = bond_lengths[i]
        geometry = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, d]], requires_grad = False)
        
        mol = qml.qchem.Molecule(symbols, geometry)
        
        hf_energies.append(qml.qchem.hf_energy(mol)())
        
    return np.array(hf_energies)

# Calculate the energies for the Li2 molecule
hf_energies = potential_energy_surface(molecules["Li2"]["symbols"], molecules["Li2"]["bond lengths"])