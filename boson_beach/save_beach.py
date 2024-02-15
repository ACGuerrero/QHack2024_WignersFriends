import json
import pennylane as qml
import pennylane.numpy as np
from pennylane import qchem

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
    for r in bond_lengths:
        coordinates = np.array([0.0, 0.0, 0.0, 0.0, 0.0, r])
        mol = qchem.Molecule(symbols, coordinates)
        hf_energies.append(qchem.hf_energy(mol))
        
    return np.array(hf_energies)


if __name__ == "__main__":
    from pennylane_qchem import MolecularData

    r = 0.5
    symbols = "HH"
    geometry = np.array([
        [0.0, 0.0, -r/2],  # First nuclear position
        [0.0, 0.0, r/2]])

    # Convert geometry to Bohr atomic units
    geometry_bohr = geometry / 0.529177

    mol = MolecularData(geometry=geometry_bohr, symbols=symbols)
    energy = qml.qchem.hf_energy(mol)
    print(energy)

