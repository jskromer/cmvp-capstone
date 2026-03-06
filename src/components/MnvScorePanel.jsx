import { useState, useMemo } from 'react';
import Plot from 'react-plotly.js';

const CREAM_BG = '#f5f0e8';

const DIMENSIONS = [
  { key: 'measurement_method', title: 'Measurement Method', icon: '◈', description: 'What measurement approach is used?' },
  { key: 'boundary_scope', title: 'Boundary & Scope', icon: '⬡', description: 'What is the measurement boundary?' },
  { key: 'duration_cadence', title: 'Duration & Cadence', icon: '◷', description: 'How long and how frequently?' },
  { key: 'use_case_fit', title: 'Use Case Fit', icon: '◎', description: 'Is the approach matched to the use case?' },
  { key: 'savings_isolation', title: 'Savings Isolation', icon: '⊕', description: 'Can savings be attributed to a specific ECM?' },
  { key: 'interactive_effects', title: 'Interactive Effects', icon: '⋈', description: 'Are HVAC-lighting interactions captured?' },
  { key: 'baseline_robustness', title: 'Baseline Robustness', icon: '⊞', description: 'How robust is the baseline construction?' },
  { key: 'uncertainty_quantification', title: 'Uncertainty Quantification', icon: '±', description: 'Is uncertainty quantified?' },
];

const FLAGS = {
  sufficient: { label: 'Sufficient', bg: '#ecfdf5', border: '#86efac', color: '#166534', value: 3 },
  limited: { label: 'Limited', bg: '#fffbeb', border: '#fcd34d', color: '#92400e', value: 2 },
  not_addressed: { label: 'Not Addressed', bg: '#fef2f2', border: '#fca5a5', color: '#991b1b', value: 1 },
};

// Reference scores for instructor view — what a well-considered answer looks like
const REFERENCE_SCORES = {
  1: { // ECM-1: LED Lighting
    measurement_method: 'sufficient',
    boundary_scope: 'sufficient',
    duration_cadence: 'limited',
    use_case_fit: 'sufficient',
    savings_isolation: 'sufficient',
    interactive_effects: 'limited',
    baseline_robustness: 'sufficient',
    uncertainty_quantification: 'limited',
  },
  2: { // ECM-2: Chiller Replacement
    measurement_method: 'sufficient',
    boundary_scope: 'sufficient',
    duration_cadence: 'sufficient',
    use_case_fit: 'sufficient',
    savings_isolation: 'limited',
    interactive_effects: 'sufficient',
    baseline_robustness: 'limited',
    uncertainty_quantification: 'limited',
  },
  3: { // ECM-3: VAV Optimization
    measurement_method: 'limited',
    boundary_scope: 'sufficient',
    duration_cadence: 'sufficient',
    use_case_fit: 'sufficient',
    savings_isolation: 'limited',
    interactive_effects: 'sufficient',
    baseline_robustness: 'limited',
    uncertainty_quantification: 'not_addressed',
  },
};

export default function MnvScorePanel({ scenario }) {
  const ecms = scenario.ecms;
  const [selectedEcm, setSelectedEcm] = useState(ecms[0].id);
  const [scores, setScores] = useState({}); // { ecmId: { dimension: flag } }
  const [showReference, setShowReference] = useState(false);

  const currentScores = scores[selectedEcm] || {};

  const updateScore = (dimension, flag) => {
    setScores(prev => ({
      ...prev,
      [selectedEcm]: {
        ...(prev[selectedEcm] || {}),
        [dimension]: flag,
      },
    }));
  };

  const completedCount = Object.keys(currentScores).length;

  // Radar chart data
  const radarTraces = useMemo(() => {
    const traces = [];
    const dimLabels = DIMENSIONS.map(d => d.title);

    // Student scores for each ECM
    ecms.forEach((ecm, i) => {
      const ecmScores = scores[ecm.id];
      if (!ecmScores || Object.keys(ecmScores).length === 0) return;

      const values = DIMENSIONS.map(d => FLAGS[ecmScores[d.key]]?.value || 0);

      traces.push({
        type: 'scatterpolar',
        r: [...values, values[0]], // close the polygon
        theta: [...dimLabels, dimLabels[0]],
        fill: 'toself',
        fillcolor: ['rgba(41, 128, 185, 0.1)', 'rgba(231, 126, 34, 0.1)', 'rgba(39, 174, 96, 0.1)'][i],
        line: { color: ['#2980b9', '#e67e22', '#27ae60'][i], width: 2 },
        name: `ECM-${ecm.id}: ${ecm.name}`,
      });
    });

    // Reference overlay
    if (showReference) {
      ecms.forEach((ecm, i) => {
        const ref = REFERENCE_SCORES[ecm.id];
        if (!ref) return;
        const values = DIMENSIONS.map(d => FLAGS[ref[d.key]]?.value || 0);
        traces.push({
          type: 'scatterpolar',
          r: [...values, values[0]],
          theta: [...dimLabels, dimLabels[0]],
          fill: 'none',
          line: {
            color: ['#2980b9', '#e67e22', '#27ae60'][i],
            width: 1.5,
            dash: 'dot',
          },
          name: `ECM-${ecm.id} Reference`,
        });
      });
    }

    return traces;
  }, [scores, showReference, ecms]);

  const hasAnyScores = Object.values(scores).some(s => Object.keys(s).length > 0);

  return (
    <section>
      <h2>MnVScore Self-Assessment</h2>
      <p>Evaluate the M&amp;V methodology for each ECM across 8 dimensions.</p>

      <div className="prompt-box">
        <strong>How to Use</strong>
        For each ECM, evaluate your proposed M&amp;V approach against 8 quality dimensions.
        Rate each dimension as "Sufficient," "Limited," or "Not Addressed."
        Be honest in your self-assessment — the goal is reflection, not a perfect score.
        When complete, the radar chart reveals your methodology's profile and any blind spots.
      </div>

      {/* ECM selector */}
      <div className="controls" style={{ marginBottom: '1rem' }}>
        <label>
          Evaluate ECM:
          <select
            value={selectedEcm}
            onChange={(e) => setSelectedEcm(Number(e.target.value))}
          >
            {ecms.map(ecm => (
              <option key={ecm.id} value={ecm.id}>
                ECM-{ecm.id}: {ecm.name}
                {scores[ecm.id] && Object.keys(scores[ecm.id]).length === DIMENSIONS.length ? ' ✓' : ''}
              </option>
            ))}
          </select>
        </label>
      </div>

      {/* Current ECM info */}
      <div className="info-card" style={{ marginBottom: '1rem', borderLeft: '4px solid #2980b9' }}>
        <h3>ECM-{selectedEcm}: {ecms.find(e => e.id === selectedEcm)?.name}</h3>
        <p>
          {ecms.find(e => e.id === selectedEcm)?.approach}: {ecms.find(e => e.id === selectedEcm)?.method}{' '}
          (cf. {ecms.find(e => e.id === selectedEcm)?.ipmvp})
        </p>
      </div>

      {/* Dimension assessment grid */}
      {DIMENSIONS.map(dim => (
        <div key={dim.key} style={{
          background: 'white', border: '1px solid #e0d8cc', borderRadius: 8,
          padding: '0.75rem 1rem', marginBottom: '0.5rem',
          borderLeft: `4px solid ${
            currentScores[dim.key]
              ? FLAGS[currentScores[dim.key]].border
              : '#d5ccc0'
          }`,
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
            <div style={{ flex: 1, minWidth: 200 }}>
              <span style={{ fontSize: '1.1rem', marginRight: '0.5rem' }}>{dim.icon}</span>
              <strong style={{ color: '#1a365d' }}>{dim.title}</strong>
              <p style={{ margin: '0.25rem 0 0', fontSize: '0.85rem', color: '#8c8478' }}>{dim.description}</p>
              {showReference && REFERENCE_SCORES[selectedEcm] && (
                <p style={{ margin: '0.25rem 0 0', fontSize: '0.8rem', color: '#2980b9', fontStyle: 'italic' }}>
                  Reference: {FLAGS[REFERENCE_SCORES[selectedEcm][dim.key]]?.label}
                </p>
              )}
            </div>
            <div style={{ display: 'flex', gap: '0.4rem' }}>
              {Object.entries(FLAGS).map(([key, flag]) => (
                <button
                  key={key}
                  onClick={() => updateScore(dim.key, key)}
                  style={{
                    padding: '0.3rem 0.6rem', borderRadius: 6,
                    border: `1.5px solid ${flag.border}`,
                    cursor: 'pointer', fontWeight: 500, fontSize: '0.8rem',
                    background: currentScores[dim.key] === key ? flag.bg : 'white',
                    color: flag.color,
                    opacity: currentScores[dim.key] === key ? 1 : 0.6,
                  }}
                >
                  {flag.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      ))}

      {/* Progress indicator */}
      <p style={{ fontSize: '0.85rem', color: '#8c8478', textAlign: 'center', margin: '1rem 0' }}>
        ECM-{selectedEcm}: {completedCount} of {DIMENSIONS.length} dimensions assessed
        {completedCount === DIMENSIONS.length && ' — Complete!'}
      </p>

      {/* Radar chart */}
      {hasAnyScores && (
        <>
          <h3>Methodology Profile</h3>
          <Plot
            data={radarTraces}
            layout={{
              title: { text: 'MnVScore Radar — ECM Comparison', font: { size: 15, color: '#1a365d' } },
              polar: {
                radialaxis: {
                  visible: true,
                  range: [0, 3.5],
                  tickvals: [1, 2, 3],
                  ticktext: ['Not Addressed', 'Limited', 'Sufficient'],
                  gridcolor: '#e0d8c8',
                },
                angularaxis: {
                  gridcolor: '#e0d8c8',
                },
                bgcolor: 'white',
              },
              showlegend: true,
              height: 500,
              margin: { t: 50, r: 80, b: 40, l: 80 },
              paper_bgcolor: CREAM_BG,
              font: { family: 'Segoe UI, sans-serif', size: 11 },
            }}
            useResizeHandler
            style={{ width: '100%' }}
          />
        </>
      )}

      {/* Instructor toggle */}
      <div className="instructor-toggle">
        <label>
          <input
            type="checkbox"
            checked={showReference}
            onChange={(e) => setShowReference(e.target.checked)}
          />
          Instructor: show reference scores
        </label>
      </div>

      <div className="prompt-box">
        <strong>Reflect</strong>
        Compare the radar profiles across the 3 ECMs. Where are the gaps? Which ECM has the strongest
        methodology? The weakest? How would you explain the differences to a building owner who asks
        "How confident are you in these savings numbers?"
      </div>

      <div className="prompt-box">
        <strong>Discuss</strong>
        The MnVScore forces you to self-assess rather than outsource judgment to a formula.
        Where did you struggle most? Which dimension was hardest to evaluate?
        What would change your assessment from "limited" to "sufficient"?
      </div>
    </section>
  );
}
