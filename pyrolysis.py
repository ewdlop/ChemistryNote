def pyrolysis(plastic_mass):
    """
    Simulate the pyrolysis process to convert plastic into oil, gas, and char.
    
    Parameters:
    plastic_mass (float): Mass of plastic waste in kilograms

    Returns:
    dict: Masses of oil, gas, and char produced
    """
    # Conversion ratios (these are hypothetical values for demonstration purposes)
    oil_ratio = 0.6  # 60% of plastic mass converted to oil
    gas_ratio = 0.3  # 30% of plastic mass converted to gas
    char_ratio = 0.1  # 10% of plastic mass converted to char

    oil_mass = plastic_mass * oil_ratio
    gas_mass = plastic_mass * gas_ratio
    char_mass = plastic_mass * char_ratio

    return {
        'oil_mass': oil_mass,
        'gas_mass': gas_mass,
        'char_mass': char_mass
    }

# Example usage
plastic_mass = 1000  # Mass of plastic waste in kilograms

# Simulate pyrolysis
products = pyrolysis(plastic_mass)

print(f"From {plastic_mass} kg of plastic waste, we get:")
print(f"Oil: {products['oil_mass']} kg")
print(f"Gas: {products['gas_mass']} kg")
print(f"Char: {products['char_mass']} kg")
