import { useMemo } from 'react';
import Plot from 'react-plotly.js';

const CREAM_BG = '#f5f0e8';

export default function SensitivityAnalysis({ data }) {
  const sens = data.sensitivity;
  const rankings = sens.rankings;

  // Build tornado chart data — sorted by absolute impact
  const sorted = useMemo(() =>
    [...rankings]
      .filter(r => r.abs_sensitivity > 0)
      .sort((a, b) => b.abs_sensitivity - a.abs_sensitivity),
    [rankings]
  );

  const tornadoTraces = useMemo(() => {
    const labels = sorted.map(r => r.display_name || r.parameter);
    const base = sens.base_electricity_kwh;

    // For each parameter: low and high relative to base
    const lowDeltas = sorted.map(r => {
      // Percentage change from base when parameter is -15%
      return ((r.low_kwh - base) / base * 100);
    });
    const highDeltas = sorted.map(r => {
      return ((r.high_kwh - base) / base * 100);
    });

    return [
      {
        type: 'bar',
        orientation: 'h',
        y: labels,
        x: lowDeltas,
        name: '-15% Parameter',
        marker: { color: '#2980b9' },
        hovertemplate: '%{y}: %{x:.1f}% energy change<extra>-15%</extra>',
      },
      {
        type: 'bar',
        orientation: 'h',
        y: labels,
        x: highDeltas,
        name: '+15% Parameter',
        marker: { color: '#e74c3c' },
        hovertemplate: '%{y}: %{x:.1f}% energy change<extra>+15%</extra>',
      },
    ];
  }, [sorted, sens.base_electricity_kwh]);

  return (
    <section>
      <h2>Parameter Sensitivity Analysis</h2>
      <p>Each model input was perturbed ±{(sens.perturbation * 100).toFixed(0)}% to measure its impact on predicted annual electricity.</p>

      <div className="prompt-box">
        <strong>Context</strong>
        Sensitivity analysis reveals which parameters matter most. If a high-sensitivity parameter
        has low-confidence evidence, uncertainty in your savings estimate increases. This drives
        measurement decisions: which parameters should you invest in measuring more precisely?
      </div>

      {/* Tornado chart */}
      <Plot
        data={tornadoTraces}
        layout={{
          title: { text: 'Tornado Chart: Parameter Impact on Annual Electricity', font: { size: 15, color: '#1a365d' } },
          xaxis: {
            title: 'Change in Annual Electricity (%)',
            gridcolor: '#e0d8c8',
            zeroline: true,
            zerolinecolor: '#4a4540',
            zerolinewidth: 2,
          },
          yaxis: {
            autorange: 'reversed',
            gridcolor: '#e0d8c8',
          },
          barmode: 'relative',
          showlegend: true,
          height: 400,
          margin: { t: 50, r: 40, b: 55, l: 200 },
          paper_bgcolor: CREAM_BG,
          plot_bgcolor: 'white',
          font: { family: 'Segoe UI, sans-serif', size: 12 },
        }}
        useResizeHandler
        style={{ width: '100%' }}
      />

      {/* Detailed rankings table */}
      <h3>Parameter Rankings</h3>
      <table className="stats-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Parameter</th>
            <th>Δ kWh (±15%)</th>
            <th>Δ %</th>
            <th>Source</th>
            <th>Confidence</th>
            <th>Priority</th>
          </tr>
        </thead>
        <tbody>
          {rankings.map((r) => {
            const isHigh = sens.recommendations.high_priority.includes(r.parameter);
            return (
              <tr key={r.parameter}>
                <td style={{ fontWeight: 700 }}>#{r.rank}</td>
                <td style={{ fontWeight: 500 }}>{r.display_name || r.parameter}</td>
                <td>{r.abs_sensitivity > 0 ? `±${Math.round(r.abs_sensitivity).toLocaleString()}` : '—'}</td>
                <td style={{
                  fontWeight: 600,
                  color: Math.abs(r.delta_pct) > 5 ? '#e74c3c' : Math.abs(r.delta_pct) > 1 ? '#e67e22' : '#8c8478',
                }}>
                  {r.delta_pct !== 0 ? `${r.delta_pct > 0 ? '+' : ''}${r.delta_pct.toFixed(1)}%` : '—'}
                </td>
                <td style={{ fontSize: '0.85rem' }}>{r.source || '—'}</td>
                <td>
                  {r.confidence && r.confidence !== 'n/a' ? (
                    <span style={{
                      padding: '2px 8px',
                      borderRadius: 4,
                      fontSize: '0.8rem',
                      fontWeight: 600,
                      background: r.confidence === 'high' ? '#d4edda' : r.confidence === 'moderate' ? '#fff3cd' : '#f8d7da',
                      color: r.confidence === 'high' ? '#155724' : r.confidence === 'moderate' ? '#856404' : '#721c24',
                    }}>
                      {r.confidence}
                    </span>
                  ) : (
                    <span style={{ color: '#8c8478', fontSize: '0.8rem' }}>{r.confidence || '—'}</span>
                  )}
                </td>
                <td>
                  <span style={{
                    padding: '2px 8px',
                    borderRadius: 4,
                    fontSize: '0.8rem',
                    fontWeight: 600,
                    background: isHigh ? '#f8d7da' : '#d4edda',
                    color: isHigh ? '#721c24' : '#155724',
                  }}>
                    {isHigh ? 'HIGH' : 'LOW'}
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>

      <div className="prompt-box">
        <strong>Exercise</strong>
        Of the 8 parameters, which 3 would you prioritize for additional measurement or verification?
        Consider both the sensitivity ranking and the current confidence level.
        A parameter with high sensitivity and low confidence is a bigger risk than one with high sensitivity and high confidence.
      </div>

      <div className="prompt-box">
        <strong>Discuss</strong>
        Why do infiltration and boiler efficiency show zero impact? What does this tell you about the
        model structure? Is zero sensitivity the same as "this parameter doesn't matter"?
      </div>
    </section>
  );
}
