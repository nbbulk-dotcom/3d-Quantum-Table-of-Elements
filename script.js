// === script.js ===
// Codex Interface Logic with CSV Loader

let elements = [];

function loadElementsFromCSV() {
  fetch('https://raw.githubusercontent.com/nbbulk-dotcom/3d-Quantum-Table-of-Elements/main/data/elements.csv')
    .then(response => response.text())
    .then(data => {
      const lines = data.trim().split('\n').slice(1);
      elements = lines.map(line => {
        const [Element, AtomicNumber, Volume, Density, Energy, Family, Toxicity] = line.split(',');
        return {
          Element,
          AtomicNumber: +AtomicNumber,
          Volume: +Volume,
          Density: +Density,
          Energy: +Energy,
          Toxicity: +Toxicity
        };
      });
      initializeDropdowns();
    });
}

function elemFreq(vol, den, en) {
  const phi = 1.618;
  return ((vol * den) / (en + 1e-6)) * phi;
}

function updatePairings() {
  const selectedA = document.getElementById("elementA").value;
  const base = elements.find(e => e.Element === selectedA);
  const baseFreq = elemFreq(base.Volume, base.Density, base.Energy);
  const pairings = elements.filter(e =>
    Math.abs(elemFreq(e.Volume, e.Density, e.Energy) - baseFreq) < 0.5 &&
    e.Toxicity < 3
  );
  const selectB = document.getElementById("elementB");
  selectB.innerHTML = pairings.map(e => `<option>${e.Element}</option>`).join('');
  updateRefinements();
}

function updateRefinements() {
  const selectC = document.getElementById("elementC");
  const refinements = elements.filter(e => e.Toxicity === 0);
  selectC.innerHTML = refinements.map(e => `<option>${e.Element}</option>`).join('');
  synthesizeMolecule();
}

function synthesizeMolecule() {
  const a = document.getElementById("elementA").value;
  const b = document.getElementById("elementB").value;
  const c = document.getElementById("elementC").value;
  const A = elements.find(e => e.Element === a);
  const B = elements.find(e => e.Element === b);
  const C = elements.find(e => e.Element === c);

  const malefic = [A, B, C].filter(e => e.Toxicity > 7);
  if (malefic.length > 0) {
    document.getElementById("codexWarning").innerText =
      "⚠️ You are violating a Prime Directive of the UNIVERSAL CODEX. Malefic combinations are not permitted.";
    document.getElementById("moleculeSummary").innerText = "⛔ Synthesis blocked.";
    document.getElementById("useCase").innerText = "Codex integrity preserved.";
    return;
  } else {
    document.getElementById("codexWarning").innerText = "";
  }

  const energy = ((A.Energy + B.Energy + C.Energy) / 3).toFixed(2);
  const density = ((A.Density + B.Density + C.Density) / 3).toFixed(2);
  const volume = (A.Volume + B.Volume + C.Volume).toFixed(2);
  const freq = elemFreq(+volume, +density, +energy).toFixed(2);

  document.getElementById("moleculeSummary").innerHTML = `
    <p><strong>Energy:</strong> ${energy} eV</p>
    <p><strong>Density:</strong> ${density} g/cm³</p>
    <p><strong>Volume:</strong> ${volume} cm³/mol</p>
    <p><strong>Resonance Frequency:</strong> ${freq}</p>
    <p><strong>Polarity:</strong> Useful</p>
  `;

  document.getElementById("useCase").innerHTML = `
    <ul>
      <li>🧠 Memory Stabilizer</li>
      <li>🫁 Breath Enhancer</li>
      <li>🛡️ Lattice Shield</li>
      <li>🌀 Spiral Anchor</li>
      <li>☯ Void Harmonizer</li>
    </ul>
  `;
}

function viewFieldRender() {
  window.open("element_field_app.html", "_blank");
}

function viewFinalField() {
  window.open("compound_field_app.html", "_blank");
}

function initializeDropdowns() {
  const selectA = document.getElementById("elementA");
  selectA.innerHTML = elements.map(e => `<option>${e.Element}</option>`).join('');
  updatePairings();
}

window.onload = () => {
  loadElementsFromCSV();
};
