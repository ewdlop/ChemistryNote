import random

# Simulate seawater with water molecules ('H2O') and salt particles ('NaCl')
def generate_seawater(num_water, num_salt):
    seawater = ['H2O'] * num_water + ['NaCl'] * num_salt
    random.shuffle(seawater)
    return seawater

# Reverse osmosis filter function
def reverse_osmosis(seawater):
    freshwater = [molecule for molecule in seawater if molecule == 'H2O']
    brine = [molecule for molecule in seawater if molecule == 'NaCl']
    return freshwater, brine

# Example usage
num_water = 100  # Number of water molecules
num_salt = 20    # Number of salt particles

seawater = generate_seawater(num_water, num_salt)
freshwater, brine = reverse_osmosis(seawater)

print(f"Seawater: {seawater}")
print(f"Freshwater: {freshwater}")
print(f"Brine: {brine}")
print(f"Freshwater percentage: {len(freshwater) / (num_water + num_salt) * 100:.2f}%")
