import math

# Constants
R = 8.314  # Gas constant in J/(mol·K)
F = 96485  # Faraday constant in C/mol

def nernst_equation(E_standard, T, n, Q):
    """
    Calculate the cell potential using the Nernst equation.
    
    Parameters:
    E_standard (float): Standard electrode potential in volts
    T (float): Temperature in Kelvin
    n (int): Number of moles of electrons transferred
    Q (float): Reaction quotient

    Returns:
    float: Cell potential in volts
    """
    return E_standard - (R * T / (n * F)) * math.log(Q)

# Example values
E_standard = 1.10  # Standard electrode potential for the reaction (in volts)
T = 298.15  # Temperature in Kelvin (25°C)
n = 2  # Number of moles of electrons transferred
Q = 0.01  # Reaction quotient

# Calculate cell potential
E_cell = nernst_equation(E_standard, T, n, Q)
print(f"Cell potential: {E_cell:.4f} V")
