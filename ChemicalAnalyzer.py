import re
from typing import Dict, List, Tuple
import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt
from scipy.constants import N_A  # Avogadro's number

@dataclass
class Element:
    symbol: str
    atomic_number: int
    atomic_mass: float
    electronegativity: float
    oxidation_states: List[int]

class ChemicalAnalyzer:
    def __init__(self):
        # Initialize periodic table data (subset for example)
        self.periodic_table = {
            'H': Element('H', 1, 1.008, 2.20, [-1, 1]),
            'O': Element('O', 8, 15.999, 3.44, [-2, -1, 1, 2]),
            'C': Element('C', 6, 12.011, 2.55, [-4, -3, -2, -1, 1, 2, 3, 4]),
            'N': Element('N', 7, 14.007, 3.04, [-3, -2, -1, 1, 2, 3, 4, 5]),
            'Na': Element('Na', 11, 22.990, 0.93, [1]),
            'Cl': Element('Cl', 17, 35.45, 3.16, [-1, 1, 3, 5, 7])
        }
        
    def parse_formula(self, formula: str) -> Dict[str, int]:
        """Parse chemical formula into element counts."""
        pattern = r'([A-Z][a-z]*)(\d*)'
        elements = {}
        for element, count in re.findall(pattern, formula):
            elements[element] = int(count) if count else 1
        return elements

    def balance_equation(self, reactants: str, products: str) -> Tuple[List[int], List[int]]:
        """Balance chemical equation using matrix method."""
        # Split equations into compounds
        reactant_compounds = reactants.split(' + ')
        product_compounds = products.split(' + ')
        
        # Get all unique elements
        elements = set()
        for compound in reactant_compounds + product_compounds:
            elements.update(self.parse_formula(compound).keys())
        
        # Create coefficient matrix
        matrix = []
        for element in elements:
            row = []
            # Add reactant coefficients
            for compound in reactant_compounds:
                parsed = self.parse_formula(compound)
                row.append(parsed.get(element, 0))
            # Add product coefficients (negative)
            for compound in product_compounds:
                parsed = self.parse_formula(compound)
                row.append(-parsed.get(element, 0))
            matrix.append(row)
        
        # Solve using numpy
        matrix = np.array(matrix, dtype=float)
        rank = np.linalg.matrix_rank(matrix)
        nullspace = np.linalg.null_space(matrix)
        
        if nullspace.size == 0:
            raise ValueError("No solution exists")
        
        # Get the simplest integer solution
        coefficients = nullspace[:, 0]
        coefficients = coefficients / np.gcd.reduce(abs(coefficients).astype(int))
        coefficients = coefficients.astype(int)
        
        n_reactants = len(reactant_compounds)
        return coefficients[:n_reactants], coefficients[n_reactants:]

    def calculate_molar_mass(self, formula: str) -> float:
        """Calculate molar mass of a compound."""
        elements = self.parse_formula(formula)
        total_mass = 0
        for element, count in elements.items():
            if element not in self.periodic_table:
                raise ValueError(f"Unknown element: {element}")
            total_mass += self.periodic_table[element].atomic_mass * count
        return total_mass

    def calculate_oxidation_states(self, formula: str) -> Dict[str, int]:
        """Calculate oxidation states of elements in a compound."""
        elements = self.parse_formula(formula)
        n_elements = len(elements)
        
        # Simple rules for common compounds
        if n_elements == 2:
            element1, element2 = elements.keys()
            if element1 in ['Na', 'K', 'Li'] and element2 in ['Cl', 'F', 'Br', 'I']:
                return {element1: 1, element2: -1}
        
        # More complex cases would require additional rules
        return {element: 0 for element in elements}

    def analyze_reaction(self, reactants: str, products: str) -> dict:
        """Analyze a chemical reaction comprehensively."""
        try:
            r_coeff, p_coeff = self.balance_equation(reactants, products)
            reactant_compounds = reactants.split(' + ')
            product_compounds = products.split(' + ')
            
            analysis = {
                'balanced_equation': ' + '.join(f"{c if c>1 else ''}{r}" 
                    for c, r in zip(r_coeff, reactant_compounds)) + 
                    ' → ' + ' + '.join(f"{c if c>1 else ''}{p}" 
                    for c, p in zip(p_coeff, product_compounds)),
                'molar_masses': {
                    'reactants': {r: self.calculate_molar_mass(r) for r in reactant_compounds},
                    'products': {p: self.calculate_molar_mass(p) for p in product_compounds}
                },
                'oxidation_states': {
                    'reactants': {r: self.calculate_oxidation_states(r) for r in reactant_compounds},
                    'products': {p: self.calculate_oxidation_states(p) for p in product_compounds}
                }
            }
            return analysis
        except Exception as e:
            return {'error': str(e)}

    def plot_energy_diagram(self, reactants_energy: float, products_energy: float, 
                          activation_energy: float, reaction_name: str = ""):
        """Plot reaction energy diagram."""
        plt.figure(figsize=(10, 6))
        
        # Reaction coordinate points
        x = np.array([0, 0.5, 1])
        y = np.array([reactants_energy, reactants_energy + activation_energy, products_energy])
        
        # Plot energy curve
        reaction_coordinate = np.linspace(0, 1, 100)
        energy_curve = self._interpolate_energy_curve(x, y, reaction_coordinate)
        plt.plot(reaction_coordinate, energy_curve, 'b-', linewidth=2)
        
        # Add labels and arrows
        plt.plot([0], [reactants_energy], 'ro', label='Reactants')
        plt.plot([1], [products_energy], 'go', label='Products')
        plt.plot([0.5], [reactants_energy + activation_energy], 'ko', label='Transition State')
        
        # Add energy differences
        plt.arrow(0.1, reactants_energy + activation_energy/2, 0, activation_energy/2, 
                 head_width=0.03, head_length=0.5, fc='r', ec='r')
        plt.text(0.15, reactants_energy + activation_energy/2, f'Ea = {activation_energy:.1f} kJ/mol')
        
        dH = products_energy - reactants_energy
        plt.arrow(0.8, min(reactants_energy, products_energy) + abs(dH)/2, 
                 0, dH/10, head_width=0.03, head_length=0.5, fc='g', ec='g')
        plt.text(0.85, min(reactants_energy, products_energy) + abs(dH)/2, 
                f'ΔH = {dH:.1f} kJ/mol')
        
        plt.xlabel('Reaction Coordinate')
        plt.ylabel('Energy (kJ/mol)')
        plt.title(f'Energy Diagram: {reaction_name}')
        plt.legend()
        plt.grid(True)
        plt.show()

    def _interpolate_energy_curve(self, x: np.ndarray, y: np.ndarray, 
                                reaction_coordinate: np.ndarray) -> np.ndarray:
        """Create smooth energy curve using interpolation."""
        from scipy.interpolate import interp1d
        f = interp1d(x, y, kind='quadratic')
        return f(reaction_coordinate)

    def calculate_equilibrium_constant(self, delta_G: float, temperature: float = 298.15) -> float:
        """Calculate equilibrium constant from Gibbs free energy."""
        R = 8.314  # Gas constant in J/(mol·K)
        return np.exp(-delta_G / (R * temperature))

# Example usage
if __name__ == "__main__":
    analyzer = ChemicalAnalyzer()
    
    # Analyze water formation reaction
    result = analyzer.analyze_reaction("H2 + O2", "H2O")
    print("Water Formation Analysis:")
    print(json.dumps(result, indent=2))
    
    # Plot energy diagram for a sample reaction
    analyzer.plot_energy_diagram(
        reactants_energy=0,
        products_energy=-40,
        activation_energy=20,
        reaction_name="Sample Exothermic Reaction"
    )
    
    # Calculate equilibrium constant
    K = analyzer.calculate_equilibrium_constant(delta_G=-37.2e3)  # Example ΔG in J/mol
    print(f"\nEquilibrium Constant (K) at 25°C: {K:.2e}")
