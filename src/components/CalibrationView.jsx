import { useMemo } from 'react';
import Plot from 'react-plotly.js';

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const CREAM_BG = '#f5f0e8';

export default function CalibrationView({ data }) {
  const cal = data.calibration;
  const diag = cal.diagnostics;
  const limits = cal.ashrae_g14_limits;
  const monthly = cal.monthly_comparison;

  const nmbePasses = Math.abs(diag.nmbe_pct) <= limits.monthly_nmbe_pct;
  const cvrmsePasses = diag.cvrmse_pct <= limits.monthly_cvrmse_pct;

  const traces = useMemo(() => [
    {
      x: MONTHS,
      y: monthly.measured_kwh,
      type: 'bar',
      name: 'Metered (Utility Bills)',
      marker: { color: '#2980b9' },
    },
    {
      x: MONTHS,
      y: monthly.simulated_kwh,
      type: 'bar',
      name: 'Simulated (EnergyPlus)',
      marker: { color: '#e67e22' },
    },
  ], [monthly]);

  return (
    <section>
      <h2>Calibration Assessment</h2>
      <p>Compare the calibrated EnergyPlus model output against actual metered utility data.</p>

      <div className="prompt-box">
        <strong>Context</strong>
        A forward model must be calibrated before it can be trusted for savings estimation.
        ASHRAE Guideline 14-2023 defines acceptance criteria for monthly calibration:
        |NMBE| ≤ 5% and CV(RMSE) ≤ 15%.
      </div>

      {/* ASHRAE G14 Results */}
      <div className="info-grid">
        <div className="info-card">
          <h3>NMBE (Normalized Mean Bias Error)</h3>
          <p style={{ fontSize: '1.5rem', fontWeight: 700 }}>
            <span className={nmbePasses ? 'pass' : 'fail'}>{diag.nmbe_pct.toFixed(2)}%</span>
          </p>
          <p>Limit: ≤ {limits.monthly_nmbe_pct}%</p>
          <p className={nmbePasses ? 'pass' : 'fail'} style={{ fontWeight: 600 }}>
            {nmbePasses ? 'PASS' : 'FAIL'}
          </p>
          <p style={{ fontSize: '0.8rem', color: '#8c8478' }}>
            Measures systematic over- or under-prediction
          </p>
        </div>
        <div className="info-card">
          <h3>CV(RMSE) (Coefficient of Variation)</h3>
          <p style={{ fontSize: '1.5rem', fontWeight: 700 }}>
            <span className={cvrmsePasses ? 'pass' : 'fail'}>{diag.cvrmse_pct.toFixed(2)}%</span>
          </p>
          <p>Limit: ≤ {limits.monthly_cvrmse_pct}%</p>
          <p className={cvrmsePasses ? 'pass' : 'fail'} style={{ fontWeight: 600 }}>
            {cvrmsePasses ? 'PASS' : 'FAIL'}
          </p>
          <p style={{ fontSize: '0.8rem', color: '#8c8478' }}>
            Measures scatter / random error
          </p>
        </div>
        <div className="info-card">
          <h3>Annual Totals</h3>
          <p>Simulated: {diag.annual_simulated_kwh.toLocaleString()} kWh</p>
          <p>Metered: {diag.annual_measured_kwh.toLocaleString()} kWh</p>
          <p>Difference: {diag.annual_difference_kwh.toLocaleString()} kWh ({diag.annual_difference_pct}%)</p>
          <p style={{ fontSize: '0.8rem', color: '#8c8478' }}>
            Model over-predicts by {diag.annual_difference_pct}%
          </p>
        </div>
      </div>

      {/* Monthly comparison chart */}
      <Plot
        data={traces}
        layout={{
          title: { text: 'Monthly Calibration: Metered vs. Simulated', font: { size: 15, color: '#1a365d' } },
          xaxis: { title: 'Month', gridcolor: '#e0d8c8' },
          yaxis: { title: 'Electricity (kWh)', gridcolor: '#e0d8c8' },
          barmode: 'group',
          showlegend: true,
          height: 420,
          margin: { t: 50, r: 40, b: 55, l: 80 },
          paper_bgcolor: CREAM_BG,
          plot_bgcolor: 'white',
          font: { family: 'Segoe UI, sans-serif', size: 12 },
        }}
        useResizeHandler
        style={{ width: '100%' }}
      />

      {/* Calibration adjustments */}
      <h3>Calibration Adjustments Applied</h3>
      <table className="stats-table">
        <thead>
          <tr>
            <th>Parameter</th>
            <th>Change</th>
            <th>Rationale</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(cal.calibration_adjustments).map(([key, adj]) => (
            <tr key={key}>
              <td style={{ fontWeight: 500 }}>{key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}</td>
              <td style={{ fontWeight: 600, color: adj.change.startsWith('-') ? '#e74c3c' : '#27ae60' }}>{adj.change}</td>
              <td style={{ fontSize: '0.85rem' }}>{adj.rationale}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Parameter provenance */}
      <h3>Key Parameter Documentation</h3>
      <table className="stats-table">
        <thead>
          <tr>
            <th>Parameter</th>
            <th>Value</th>
            <th>Source</th>
            <th>Evidence</th>
            <th>Confidence</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(cal.parameters).map(([key, p]) => (
            <tr key={key}>
              <td style={{ fontWeight: 500 }}>{p.name.toUpperCase()}</td>
              <td>{p.value} {p.units}</td>
              <td>{p.source}</td>
              <td style={{ fontSize: '0.85rem' }}>{p.evidence}</td>
              <td>
                <span style={{
                  padding: '2px 8px',
                  borderRadius: 4,
                  fontSize: '0.8rem',
                  fontWeight: 600,
                  background: p.confidence === 'high' ? '#d4edda' : p.confidence === 'moderate' ? '#fff3cd' : '#f8d7da',
                  color: p.confidence === 'high' ? '#155724' : p.confidence === 'moderate' ? '#856404' : '#721c24',
                }}>
                  {p.confidence}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Gas limitation */}
      <div style={{
        background: '#fff3cd', border: '1px solid #ffc107', borderRadius: 8,
        padding: '12px 16px', margin: '16px 0', fontSize: '0.9rem'
      }}>
        <strong style={{ color: '#856404' }}>Gas Model Limitation:</strong>{' '}
        The DOE prototype uses electric reheat internally. Gas calibration was not performed.
        The model passes ASHRAE G14 for electricity but cannot predict gas consumption.
        This must be disclosed in any savings report.
      </div>

      <div className="prompt-box">
        <strong>Discuss</strong>
        This model passes both G14 criteria for electricity. But look at the monthly profile —
        the simulation over-predicts winter months and under-predicts summer. Why?
        Does passing G14 mean the model is "correct"? What does calibration actually prove?
      </div>

      <div className="prompt-box">
        <strong>Compare</strong>
        In the Greenfield scenario, the inverse model's gas CV(RMSE) fails the 15% threshold.
        Here, the forward model passes for electricity but can't model gas at all.
        What are the tradeoffs between inverse and forward model approaches?
      </div>
    </section>
  );
}
