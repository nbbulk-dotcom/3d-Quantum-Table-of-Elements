import numpy as np

def elem_freq(volume, density, energy):
    """
    Calculates the elemental resonance frequency based on volume, density, and energy.
    This function embeds π modulation to align with spiral ignition protocols.

    Parameters:
        volume (float): Elemental volume (cm³/mol)
        density (float): Elemental density (g/cm³)
        energy (float): Ionization energy (eV)

    Returns:
        float: Resonance frequency (scalar)
    """
    if volume <= 0 or density <= 0 or energy <= 0:
        raise ValueError("All inputs must be positive and non-zero.")
    
    freq = np.sqrt(energy / (volume * density)) * (1 + np.pi)
    return round(freq, 6)
