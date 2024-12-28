import numpy as np
import matplotlib.pyplot as plt

# Simulate Chromatogram Peaks
def generate_chromatogram():
    """Generate a simulated chromatogram."""
    time = np.linspace(0, 10, 1000)  # Time in minutes
    # Gaussian peaks for compounds
    peaks = [
        (3, 1.5, 100),  # (Retention time, width, intensity)
        (5, 0.8, 150),
        (7, 1.2, 200)
    ]
    chromatogram = sum(intensity * np.exp(-((time - rt)**2) / (2 * width**2))
                       for rt, width, intensity in peaks)
    return time, chromatogram

time, chromatogram = generate_chromatogram()
plt.plot(time, chromatogram)
plt.title("Simulated Chromatogram")
plt.xlabel("Time (minutes)")
plt.ylabel("Intensity")
plt.show()

# Simulate Mass Spectrum for a Compound
def generate_mass_spectrum():
    """Generate a simulated mass spectrum."""
    mass_to_charge = np.array([50, 75, 100, 125, 150])  # m/z values
    intensities = np.array([10, 40, 80, 20, 60])  # Corresponding intensities
    return mass_to_charge, intensities

mz, intensities = generate_mass_spectrum()
plt.bar(mz, intensities, width=5, color='blue', edgecolor='black')
plt.title("Simulated Mass Spectrum")
plt.xlabel("m/z (mass-to-charge ratio)")
plt.ylabel("Intensity")
plt.show()
