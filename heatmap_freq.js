// === heatmap_freq.js ===
// Codex module for generating frequency-based color gradients

function getFrequencyColor(freq) {
  // Normalize frequency range (example: 0.0 to 20.0)
  const minFreq = 0.0;
  const maxFreq = 20.0;
  const normalized = Math.min(Math.max((freq - minFreq) / (maxFreq - minFreq), 0), 1);

  // Map to color gradient: blue → green → yellow → red
  const r = Math.floor(255 * Math.pow(normalized, 2));
  const g = Math.floor(255 * (1 - Math.abs(normalized - 0.5) * 2));
  const b = Math.floor(255 * (1 - normalized));

  return `rgb(${r},${g},${b})`;
}

function applyHeatmapToElement(element) {
  const freq = elemFreq(element.Volume, element.Density, element.Energy);
  return {
    Element: element.Element,
    Frequency: freq.toFixed(2),
    Color: getFrequencyColor(freq)
  };
}
