import math

# Constants
F = 96485  # Faraday constant in C/mol
R = 8.314  # Gas constant in J/(mol·K)
T = 310.15  # Temperature in Kelvin (37°C)

def ghk_flux(P_i, z_i, V_m, C_i_out, C_i_in):
    """
    Calculate the ion flux using the GHK flux equation.
    
    Parameters:
    P_i (float): Permeability of the membrane to ion i
    z_i (int): Valence of ion i
    V_m (float): Membrane potential in volts
    C_i_out (float): Concentration of ion i outside the cell
    C_i_in (float): Concentration of ion i inside the cell

    Returns:
    float: Flux of ion i
    """
    numerator = C_i_out - C_i_in * math.exp(-z_i * F * V_m / (R * T))
    denominator = 1 - math.exp(-z_i * F * V_m / (R * T))
    flux = P_i * (z_i**2 * F**2 * V_m / (R * T)) * (numerator / denominator)
    return flux

# Example values
P_i = 1e-7  # Permeability in cm/s
z_i = 1  # Valence for potassium ion (K+)
V_m = -0.07  # Membrane potential in volts
C_i_out = 5  # Concentration outside the cell in mM
C_i_in = 140  # Concentration inside the cell in mM

# Calculate ion flux
flux = ghk_flux(P_i, z_i, V_m, C_i_out, C_i_in)
print(f"Ion flux: {flux:.4e} mol/s/cm^2")
