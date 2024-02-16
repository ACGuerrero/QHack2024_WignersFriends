import json
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


def ground_energy(hf_energies):
    """Finds the minimum energy of a molecule given its potential energy surface.
    
    Args: 
        hf_energies (numpy.tensor): 

    Returns:
        (float): The minumum energy in units of hartrees.
    """

    ind = np.argmin(hf_energies)
    return hf_energies[ind]

def reaction():
    """Calculates the energy of the reactants, the activation energy, and the energy of 
    the products in that order.

    Returns:
        (numpy.tensor): [E_reactants, E_activation, E_products]
    """
    molecules = {
        "H2": 
            {"symbols": ["H", "H"], "E0": 0, "E_dissociation": 0, "bond lengths": np.arange(0.5, 9.3, 0.3)}, 
        "Li2": 
            {"symbols": ["Li", "Li"], "E0": 0, "E_dissociation": 0, "bond lengths": np.arange(3.5, 8.3, 0.3)}, 
        "LiH": 
            {"symbols": ["Li", "H"], "E0": 0, "E_dissociation": 0, "bond lengths": np.arange(2.0, 6.6, 0.3)}
    }

    for molecule in molecules.keys():
        # Put your code here #
        # call potential_energy_surface with the values from the dictionary
        print('Now obtaining the energies for the molecule:', molecule)
        hf_energies = potential_energy_surface(symbols = molecules[molecule]["symbols"], bond_lengths = molecules[molecule]["bond lengths"])
        print('The energies are:', hf_energies)
        E0 = ground_energy(hf_energies)
        # Update E0 in the dictionary
        molecules[molecule]["E0"] = E0
        Emax = hf_energies[-1]
        E_dissoc = np.abs(E0 - Emax)
        # Update E_dissociation in the dictionary
        molecules[molecule]["E_dissociation"] = E_dissoc

    # Calculate the following and don't forget to balance the chemical reaction!
    E_reactants = molecules["H2"]["E0"]+ molecules["Li2"]["E0"]
    E_dissoc = molecules["H2"]["E_dissociation"]+ molecules["Li2"]["E_dissociation"]
    E_activation = E_reactants + E_dissoc
    E_products = 2*molecules["LiH"]["E0"]

    return np.array([E_reactants, E_activation, E_products])

print (reaction())