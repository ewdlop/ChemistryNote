import numpy as np
from scipy import signal
from scipy.constants import c, h, k, N_A
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum

class SpectroscopyType(Enum):
    IR = "Infrared"
    RAMAN = "Raman"
    UV_VIS = "UV-Visible"
    NMR = "Nuclear Magnetic Resonance"
    MASS = "Mass Spectrometry"

@dataclass
class SpectralPeak:
    wavelength: float
    intensity: float
    assignment: str
    width: float

class MolecularSpectroscopyAnalyzer:
    def __init__(self):
        # Common functional groups and their IR frequencies (cm⁻¹)
        self.ir_functional_groups = {
            "O-H stretch": (3200, 3600),
            "N-H stretch": (3300, 3500),
            "C-H stretch": (2850, 3000),
            "C=O stretch": (1670, 1780),
            "C=C stretch": (1620, 1680),
            "C≡N stretch": (2200, 2260),
            "NO₂ stretch": (1500, 1570)
        }

        # UV-Vis chromophore data (nm)
        self.uv_chromophores = {
            "C=C": (170, 190),
            "C=O": (270, 290),
            "C=N": (230, 250),
            "C≡C": (170, 180),
            "Benzene": (230, 270)
        }

        # NMR chemical shift ranges (ppm)
        self.nmr_shifts = {
            "CH3": (0.7, 1.3),
            "CH2": (1.2, 1.4),
            "CH": (1.4, 1.7),
            "OH": (1.5, 5.5),
            "Aromatic": (6.5, 8.5)
        }

    def generate_ir_spectrum(self, functional_groups: List[str], 
                           noise_level: float = 0.02) -> Tuple[np.ndarray, np.ndarray]:
        """Generate IR spectrum for given functional groups."""
        wavenumbers = np.linspace(500, 4000, 3500)
        spectrum = np.zeros_like(wavenumbers)

        for group in functional_groups:
            if group in self.ir_functional_groups:
                center = np.mean(self.ir_functional_groups[group])
                width = (self.ir_functional_groups[group][1] - 
                        self.ir_functional_groups[group][0]) / 2
                peak = self._generate_peak(wavenumbers, center, width)
                spectrum += peak

        # Add noise
        noise = np.random.normal(0, noise_level, size=wavenumbers.shape)
        spectrum += noise
        return wavenumbers, spectrum

    def analyze_ir_spectrum(self, wavenumbers: np.ndarray, 
                          spectrum: np.ndarray) -> List[SpectralPeak]:
        """Analyze IR spectrum to identify functional groups."""
        peaks = []
        # Find peaks using signal processing
        peak_indices = signal.find_peaks(spectrum, height=0.1, distance=50)[0]
        
        for idx in peak_indices:
            wave_num = wavenumbers[idx]
            intensity = spectrum[idx]
            assignment = self._identify_ir_peak(wave_num)
            width = self._calculate_peak_width(spectrum, idx)
            peaks.append(SpectralPeak(wave_num, intensity, assignment, width))
        
        return peaks

    def generate_uv_vis_spectrum(self, chromophores: List[str], 
                               noise_level: float = 0.02) -> Tuple[np.ndarray, np.ndarray]:
        """Generate UV-Vis spectrum for given chromophores."""
        wavelengths = np.linspace(150, 400, 2500)
        spectrum = np.zeros_like(wavelengths)

        for chromophore in chromophores:
            if chromophore in self.uv_chromophores:
                center = np.mean(self.uv_chromophores[chromophore])
                width = (self.uv_chromophores[chromophore][1] - 
                        self.uv_chromophores[chromophore][0]) / 2
                peak = self._generate_peak(wavelengths, center, width)
                spectrum += peak

        noise = np.random.normal(0, noise_level, size=wavelengths.shape)
        spectrum += noise
        return wavelengths, spectrum

    def analyze_uv_vis_spectrum(self, wavelengths: np.ndarray, 
                              spectrum: np.ndarray) -> List[SpectralPeak]:
        """Analyze UV-Vis spectrum to identify chromophores."""
        peaks = []
        peak_indices = signal.find_peaks(spectrum, height=0.1, distance=50)[0]
        
        for idx in peak_indices:
            wavelength = wavelengths[idx]
            intensity = spectrum[idx]
            assignment = self._identify_uv_peak(wavelength)
            width = self._calculate_peak_width(spectrum, idx)
            peaks.append(SpectralPeak(wavelength, intensity, assignment, width))
        
        return peaks

    def generate_nmr_spectrum(self, proton_environments: List[str], 
                            noise_level: float = 0.02) -> Tuple[np.ndarray, np.ndarray]:
        """Generate NMR spectrum for given proton environments."""
        chemical_shifts = np.linspace(0, 10, 1000)
        spectrum = np.zeros_like(chemical_shifts)

        for environment in proton_environments:
            if environment in self.nmr_shifts:
                center = np.mean(self.nmr_shifts[environment])
                width = (self.nmr_shifts[environment][1] - 
                        self.nmr_shifts[environment][0]) / 2
                peak = self._generate_peak(chemical_shifts, center, width/5)
                spectrum += peak

        noise = np.random.normal(0, noise_level, size=chemical_shifts.shape)
        spectrum += noise
        return chemical_shifts, spectrum

    def analyze_nmr_spectrum(self, chemical_shifts: np.ndarray, 
                           spectrum: np.ndarray) -> List[SpectralPeak]:
        """Analyze NMR spectrum to identify proton environments."""
        peaks = []
        peak_indices = signal.find_peaks(spectrum, height=0.1, distance=50)[0]
        
        for idx in peak_indices:
            shift = chemical_shifts[idx]
            intensity = spectrum[idx]
            assignment = self._identify_nmr_peak(shift)
            width = self._calculate_peak_width(spectrum, idx)
            peaks.append(SpectralPeak(shift, intensity, assignment, width))
        
        return peaks

    def _generate_peak(self, x: np.ndarray, center: float, 
                      width: float, shape: str = 'gaussian') -> np.ndarray:
        """Generate a spectral peak with specified shape."""
        if shape == 'gaussian':
            return np.exp(-((x - center) ** 2) / (2 * width ** 2))
        elif shape == 'lorentzian':
            return width / (np.pi * ((x - center) ** 2 + width ** 2))
        else:
            raise ValueError(f"Unknown peak shape: {shape}")

    def _identify_ir_peak(self, wavenumber: float) -> str:
        """Identify functional group from IR wavenumber."""
        for group, (low, high) in self.ir_functional_groups.items():
            if low <= wavenumber <= high:
                return group
        return "Unknown"

    def _identify_uv_peak(self, wavelength: float) -> str:
        """Identify chromophore from UV-Vis wavelength."""
        for chromophore, (low, high) in self.uv_chromophores.items():
            if low <= wavelength <= high:
                return chromophore
        return "Unknown"

    def _identify_nmr_peak(self, shift: float) -> str:
        """Identify proton environment from NMR chemical shift."""
        for environment, (low, high) in self.nmr_shifts.items():
            if low <= shift <= high:
                return environment
        return "Unknown"

    def _calculate_peak_width(self, spectrum: np.ndarray, peak_idx: int) -> float:
        """Calculate width at half maximum of a peak."""
        half_max = spectrum[peak_idx] / 2
        left_idx = right_idx = peak_idx
        
        while left_idx > 0 and spectrum[left_idx] > half_max:
            left_idx -= 1
        while right_idx < len(spectrum) - 1 and spectrum[right_idx] > half_max:
            right_idx += 1
            
        return right_idx - left_idx

    def plot_spectrum(self, x: np.ndarray, y: np.ndarray, 
                     peaks: List[SpectralPeak], 
                     spec_type: SpectroscopyType):
        """Plot spectrum with peak assignments."""
        plt.figure(figsize=(12, 6))
        
        # Plot spectrum
        plt.plot(x, y, 'b-', label='Spectrum')
        
        # Plot peak markers and labels
        for peak in peaks:
            plt.plot(peak.wavelength, peak.intensity, 'ro')
            plt.annotate(peak.assignment, 
                        (peak.wavelength, peak.intensity),
                        xytext=(10, 10), 
                        textcoords='offset points',
                        arrowprops=dict(arrowstyle='->'))

        # Set labels based on spectroscopy type
        if spec_type == SpectroscopyType.IR:
            plt.xlabel('Wavenumber (cm⁻¹)')
            plt.ylabel('Transmittance')
        elif spec_type == SpectroscopyType.UV_VIS:
            plt.xlabel('Wavelength (nm)')
            plt.ylabel('Absorbance')
        elif spec_type == SpectroscopyType.NMR:
            plt.xlabel('Chemical Shift (ppm)')
            plt.ylabel('Intensity')

        plt.title(f'{spec_type.value} Spectrum')
        plt.grid(True)
        plt.legend()
        plt.show()

# Example usage
if __name__ == "__main__":
    analyzer = MolecularSpectroscopyAnalyzer()

    # Generate and analyze IR spectrum
    print("Analyzing IR Spectrum...")
    wavenumbers, ir_spectrum = analyzer.generate_ir_spectrum(
        ["O-H stretch", "C=O stretch", "C-H stretch"]
    )
    ir_peaks = analyzer.analyze_ir_spectrum(wavenumbers, ir_spectrum)
    analyzer.plot_spectrum(wavenumbers, ir_spectrum, ir_peaks, SpectroscopyType.IR)

    # Generate and analyze UV-Vis spectrum
    print("\nAnalyzing UV-Vis Spectrum...")
    wavelengths, uv_spectrum = analyzer.generate_uv_vis_spectrum(
        ["C=C", "Benzene"]
    )
    uv_peaks = analyzer.analyze_uv_vis_spectrum(wavelengths, uv_spectrum)
    analyzer.plot_spectrum(wavelengths, uv_spectrum, uv_peaks, SpectroscopyType.UV_VIS)

    # Generate and analyze NMR spectrum
    print("\nAnalyzing NMR Spectrum...")
    shifts, nmr_spectrum = analyzer.generate_nmr_spectrum(
        ["CH3", "Aromatic", "OH"]
    )
    nmr_peaks = analyzer.analyze_nmr_spectrum(shifts, nmr_spectrum)
    analyzer.plot_spectrum(shifts, nmr_spectrum, nmr_peaks, SpectroscopyType.NMR)
