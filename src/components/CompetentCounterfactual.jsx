import { useState } from 'react';

const CRITERIA = [
  {
    id: 'provenance',
    name: 'Parameter Provenance',
    question: 'Can you trace every model input to a documented source?',
    description: 'Each parameter has a stated source (audit, nameplate, assumption, design documents) with evidence description.',
    guidance: 'Look at the Calibration tab\'s parameter documentation table. Are any sources missing?',
  },
  {
    id: 'plausibility',
    name: 'Physical Plausibility',
    question: 'Are all parameter values within physically reasonable bounds?',
    description: 'Values fall within plausible ranges for this building type, vintage, and climate.',
    guidance: 'The calibration metadata includes plausible bounds for each parameter. Did any adjusted values land outside them?',
  },
  {
    id: 'sensitivity_aware',
    name: 'Sensitivity Awareness',
    question: 'Do you know which parameters drive the most uncertainty?',
    description: 'High-sensitivity parameters with low-confidence evidence have been identified and documented.',
    guidance: 'Cross-reference the sensitivity rankings with confidence levels. Window SHGC is high-sensitivity but low-confidence — is that acceptable?',
  },
  {
    id: 'calibration_honest',
    name: 'Honest Calibration',
    question: 'Does the calibration accurately represent model capability?',
    description: 'Passing ASHRAE G14 criteria is reported without overstating what calibration proves.',
    guidance: 'The model passes G14 for electricity but not gas. Is this clearly disclosed? Does "passing" mean "accurate"?',
  },
  {
    id: 'limitations_disclosed',
    name: 'Limitations Disclosed',
    question: 'Are all known limitations explicitly stated?',
    description: 'Gas model limitation, monthly seasonal pattern mismatch, and interactive effects are documented.',
    guidance: 'The gas reheat mismatch, prototype schedule differences, and savings non-additivity should all appear in any report.',
  },
];

export default function CompetentCounterfactual({ data }) {
  const [assessments, setAssessments] = useState({});
  const [showReference, setShowReference] = useState(false);

  const sens = data.sensitivity;

  const updateAssessment = (id, value) => {
    setAssessments(prev => ({ ...prev, [id]: value }));
  };

  const completedCount = Object.keys(assessments).length;
  const passCount = Object.values(assessments).filter(v => v === 'yes').length;

  return (
    <section>
      <h2>Competent Counterfactual Assessment</h2>
      <p>Evaluate whether this calibrated simulation meets the standard for a "competent counterfactual" — a model trustworthy enough for savings inference.</p>

      <div className="prompt-box">
        <strong>Key Concept</strong>
        A competent counterfactual is not just a model that passes calibration metrics. It requires:
        documented parameter provenance, physical plausibility, sensitivity awareness, honest
        representation of capability, and transparent disclosure of limitations. The M&amp;V professional's
        judgment about model competence is itself an inference — and must be defensible.
      </div>

      {/* Parameter provenance table */}
      <h3>Parameter Provenance Summary</h3>
      <table className="stats-table">
        <thead>
          <tr>
            <th>Parameter</th>
            <th>Sensitivity Rank</th>
            <th>Source Category</th>
            <th>Confidence</th>
            <th>Risk</th>
          </tr>
        </thead>
        <tbody>
          {sens.rankings.filter(r => r.abs_sensitivity > 0).map(r => {
            const isHighRisk = r.rank <= 3 && (r.confidence === 'low' || r.confidence === 'moderate');
            return (
              <tr key={r.parameter}>
                <td style={{ fontWeight: 500 }}>{r.display_name || r.parameter}</td>
                <td>#{r.rank} ({r.delta_pct > 0 ? '+' : ''}{r.delta_pct.toFixed(1)}%)</td>
                <td>{r.source || '—'}</td>
                <td>
                  <span style={{
                    padding: '2px 8px', borderRadius: 4, fontSize: '0.8rem', fontWeight: 600,
                    background: r.confidence === 'high' ? '#d4edda' : r.confidence === 'moderate' ? '#fff3cd' : '#f8d7da',
                    color: r.confidence === 'high' ? '#155724' : r.confidence === 'moderate' ? '#856404' : '#721c24',
                  }}>
                    {r.confidence}
                  </span>
                </td>
                <td>
                  {isHighRisk && (
                    <span style={{
                      padding: '2px 8px', borderRadius: 4, fontSize: '0.8rem', fontWeight: 600,
                      background: '#f8d7da', color: '#721c24',
                    }}>
                      HIGH SENSITIVITY + LOW CONFIDENCE
                    </span>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>

      {/* 5-criteria checklist */}
      <h3>Competence Checklist</h3>
      <p style={{ fontSize: '0.9rem', color: '#8c8478' }}>
        For each criterion, assess whether the SLO calibrated model meets the standard.
        Be honest — identifying gaps is more valuable than checking every box.
      </p>

      {CRITERIA.map(c => (
        <div key={c.id} style={{
          background: 'white', border: '1px solid #e0d8cc', borderRadius: 8,
          padding: '1rem 1.25rem', marginBottom: '0.75rem',
          borderLeft: `4px solid ${
            assessments[c.id] === 'yes' ? '#27ae60' :
            assessments[c.id] === 'partial' ? '#f39c12' :
            assessments[c.id] === 'no' ? '#e74c3c' : '#d5ccc0'
          }`,
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '1rem', flexWrap: 'wrap' }}>
            <div style={{ flex: 1, minWidth: 250 }}>
              <h4 style={{ margin: '0 0 0.25rem', color: '#1a365d' }}>{c.name}</h4>
              <p style={{ margin: '0 0 0.5rem', fontWeight: 500 }}>{c.question}</p>
              <p style={{ margin: 0, fontSize: '0.85rem', color: '#8c8478' }}>{c.description}</p>
              {showReference && (
                <p style={{ margin: '0.5rem 0 0', fontSize: '0.85rem', color: '#2980b9', fontStyle: 'italic' }}>
                  {c.guidance}
                </p>
              )}
            </div>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              {['yes', 'partial', 'no'].map(val => (
                <button
                  key={val}
                  onClick={() => updateAssessment(c.id, val)}
                  style={{
                    padding: '0.3rem 0.75rem', borderRadius: 6, border: '1px solid',
                    cursor: 'pointer', fontWeight: 500, fontSize: '0.85rem',
                    background: assessments[c.id] === val
                      ? (val === 'yes' ? '#d4edda' : val === 'partial' ? '#fff3cd' : '#f8d7da')
                      : 'white',
                    borderColor: val === 'yes' ? '#27ae60' : val === 'partial' ? '#f39c12' : '#e74c3c',
                    color: val === 'yes' ? '#155724' : val === 'partial' ? '#856404' : '#721c24',
                  }}
                >
                  {val === 'yes' ? 'Yes' : val === 'partial' ? 'Partial' : 'No'}
                </button>
              ))}
            </div>
          </div>
        </div>
      ))}

      {/* Summary */}
      {completedCount === CRITERIA.length && (
        <div className="info-card" style={{ marginTop: '1rem' }}>
          <h3>Assessment Summary</h3>
          <p>
            <span style={{ color: '#27ae60', fontWeight: 600 }}>{passCount}</span> of {CRITERIA.length} criteria fully met.
            {passCount === CRITERIA.length
              ? ' This model appears to meet the standard for a competent counterfactual.'
              : passCount >= 3
                ? ' The model has gaps that should be documented and disclosed.'
                : ' Significant deficiencies identified — additional work needed before this model can support savings claims.'
            }
          </p>
        </div>
      )}

      {/* Instructor toggle */}
      <div className="instructor-toggle">
        <label>
          <input
            type="checkbox"
            checked={showReference}
            onChange={(e) => setShowReference(e.target.checked)}
          />
          Instructor: show reference guidance
        </label>
      </div>

      <div className="prompt-box">
        <strong>Reflection</strong>
        The model's competence assessment from the calibration metadata says "investment grade."
        Do you agree? What would need to change for you to upgrade (or downgrade) that assessment?
        How would you communicate model limitations to a non-technical building owner?
      </div>
    </section>
  );
}
