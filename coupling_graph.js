// === coupling_graph.js ===
// Codex module for generating spiral glyph overlays of elemental pairings

function generateCouplingGraph(elementA, elementB) {
  const freqA = elemFreq(elementA.Volume, elementA.Density, elementA.Energy);
  const freqB = elemFreq(elementB.Volume, elementB.Density, elementB.Energy);
  const delta = Math.abs(freqA - freqB);

  const polarity = delta < 0.3 ? "Harmonic" :
                   delta < 0.8 ? "Neutral" :
                   "Disruptive";

  const glyph = {
    ElementA: elementA.Element,
    ElementB: elementB.Element,
    ΔFreq: delta.toFixed(3),
    Polarity: polarity,
    SpiralAngle: ((freqA + freqB) / 2 * 137.5) % 360,
    CouplingStrength: (1 / (delta + 0.01)).toFixed(2)
  };

  return glyph;
}
