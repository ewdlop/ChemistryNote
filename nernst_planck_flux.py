def nernst_planck_flux(D_i, z_i, C_i, dC_dx, dphi_dx):
    """
    Calculate the ion flux using the Nernst-Planck equation.
    
    Parameters:
    D_i (float): Diffusion coefficient of ion i
    z_i (int): Valence of ion i
    C_i (float): Concentration of ion i
    dC_dx (float): Concentration gradient of ion i
    dphi_dx (float): Electric potential gradient

    Returns:
    float: Flux of ion i
    """
    flux = -D_i * (dC_dx + (z_i * F / (R * T)) * C_i * dphi_dx)
    return flux

# Example values
D_i = 1e-5  # Diffusion coefficient in cm^2/s
z_i = 1  # Valence for potassium ion (K+)
C_i = 100  # Concentration in mM
dC_dx = -0.1  # Concentration gradient in mM/cm
dphi_dx = 0.01  # Electric potential gradient in V/cm

# Calculate ion flux
flux_np = nernst_planck_flux(D_i, z_i, C_i, dC_dx, dphi_dx)
print(f"Nernst-Planck flux: {flux_np:.4e} mol/s/cm^2")
