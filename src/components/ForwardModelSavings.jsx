import { useMemo } from 'react';
import Plot from 'react-plotly.js';

const CREAM_BG = '#f5f0e8';
const ECM_COLORS = ['#f39c12', '#2980b9', '#27ae60'];

export default function ForwardModelSavings({ data }) {
  const ecmData = data.ecmSavings;
  const ecms = ecmData.ecms;
  const fmt = v => v.toLocaleString(undefined, { maximumFractionDigits: 0 });

  // Waterfall chart traces
  const waterfallTrace = useMemo(() => {
    const names = ['Baseline', ...ecms.map(e => e.name), 'Post-Retrofit'];
    const values = [
      ecmData.base_electricity_kwh,
      ...ecms.map(e => -e.savings_kwh),
      0,  // placeholder — Plotly calculates total
    ];

    return [{
      type: 'waterfall',
      orientation: 'v',
      x: names,
      y: values,
      measure: ['absolute', ...ecms.map(() => 'relative'), 'total'],
      textposition: 'outside',
      text: [
        `${fmt(ecmData.base_electricity_kwh)} kWh`,
        ...ecms.map(e => `-${fmt(e.savings_kwh)}`),
        `${fmt(ecmData.base_electricity_kwh - ecmData.total_savings_kwh)} kWh`,
      ],
      connector: { line: { color: '#d5ccc0' } },
      decreasing: { marker: { color: '#27ae60' } },
      increasing: { marker: { color: '#e74c3c' } },
      totals: { marker: { color: '#2980b9' } },
    }];
  }, [ecms, ecmData]);

  // Bar chart with uncertainty bands
  const uncertaintyTraces = useMemo(() => {
    return [{
      type: 'bar',
      x: ecms.map(e => e.name),
      y: ecms.map(e => e.savings_kwh),
      error_y: {
        type: 'data',
        array: ecms.map(e => e.savings_kwh * e.uncertainty_pct / 100),
        visible: true,
        color: '#4a4540',
        thickness: 2,
        width: 6,
      },
      marker: { color: ECM_COLORS },
      text: ecms.map(e => `${fmt(e.savings_kwh)} kWh ±${e.uncertainty_pct}%`),
      textposition: 'outside',
    }];
  }, [ecms]);

  return (
    <section>
      <h2>Forward Model ECM Savings</h2>
      <p>Projected savings from calibrated EnergyPlus simulation with uncertainty from sensitivity analysis.</p>

      <div className="prompt-box">
        <strong>Key Concept</strong>
        In a forward model approach, savings are estimated by comparing the calibrated baseline simulation
        against a modified simulation with each ECM applied. The sensitivity analysis provides uncertainty
        bounds — if a parameter could shift the prediction by ±X%, that propagates into savings uncertainty.
      </div>

      {/* Waterfall chart */}
      <Plot
        data={waterfallTrace}
        layout={{
          title: { text: 'Baseline → Post-Retrofit Waterfall', font: { size: 15, color: '#1a365d' } },
          yaxis: { title: 'Annual Electricity (kWh)', gridcolor: '#e0d8c8' },
          showlegend: false,
          height: 420,
          margin: { t: 50, r: 40, b: 100, l: 80 },
          paper_bgcolor: CREAM_BG,
          plot_bgcolor: 'white',
          font: { family: 'Segoe UI, sans-serif', size: 12 },
        }}
        useResizeHandler
        style={{ width: '100%' }}
      />

      {/* Savings with uncertainty */}
      <Plot
        data={uncertaintyTraces}
        layout={{
          title: { text: 'ECM Savings with Uncertainty Bands', font: { size: 15, color: '#1a365d' } },
          yaxis: { title: 'Savings (kWh)', gridcolor: '#e0d8c8' },
          showlegend: false,
          height: 380,
          margin: { t: 50, r: 40, b: 80, l: 80 },
          paper_bgcolor: CREAM_BG,
          plot_bgcolor: 'white',
          font: { family: 'Segoe UI, sans-serif', size: 12 },
        }}
        useResizeHandler
        style={{ width: '100%' }}
      />

      {/* ECM detail cards */}
      <h3>ECM Savings Breakdown</h3>
      <div className="info-grid">
        {ecms.map((ecm, i) => (
          <div key={ecm.ecm_id} className="info-card" style={{ borderLeft: `4px solid ${ECM_COLORS[i]}` }}>
            <h3>
              <span className="ecm-tag" style={{
                background: ECM_COLORS[i] + '30',
                color: ECM_COLORS[i],
              }}>ECM-{ecm.ecm_id}</span>
              {ecm.name}
            </h3>
            <p style={{ fontSize: '1.2rem', fontWeight: 700, color: '#27ae60' }}>
              {fmt(ecm.savings_kwh)} kWh/yr ({ecm.savings_pct}%)
            </p>
            <p>Cost savings: ${fmt(ecm.cost_savings)}/yr</p>
            <p style={{ fontSize: '0.85rem', color: '#4a4540' }}>{ecm.description}</p>
            <p style={{ fontSize: '0.8rem', color: '#8c8478' }}>
              Parameter change: {ecm.parameter_change}
            </p>
            <p style={{ fontSize: '0.8rem', color: '#8c8478' }}>
              Uncertainty: ±{ecm.uncertainty_pct}%
            </p>
            <p style={{ fontSize: '0.8rem', color: '#8c8478', fontStyle: 'italic' }}>
              {ecm.approach}: {ecm.method} (cf. {ecm.ipmvp})
            </p>
          </div>
        ))}
      </div>

      {/* Totals */}
      <div className="info-grid" style={{ marginTop: '1rem' }}>
        <div className="info-card">
          <h3>Total Package Savings</h3>
          <p style={{ fontSize: '1.3rem', fontWeight: 700, color: '#27ae60' }}>
            {fmt(ecmData.total_savings_kwh)} kWh/yr ({ecmData.total_savings_pct}%)
          </p>
          <p>${fmt(ecmData.total_cost_savings)}/yr at ${ecmData.electric_rate}/kWh</p>
        </div>
        <div className="info-card">
          <h3>Interactive Effects Note</h3>
          <p style={{ fontSize: '0.9rem', color: '#4a4540' }}>
            {ecmData.note}
          </p>
        </div>
      </div>

      <div className="prompt-box">
        <strong>Discuss</strong>
        The uncertainty bands differ across ECMs. ECM-1 (lighting) has ±8% uncertainty while
        ECM-3 (VAV optimization) has ±15%. Why? How does parameter confidence propagate
        into savings uncertainty? How would you communicate this to a building owner?
      </div>

      <div className="prompt-box">
        <strong>Compare</strong>
        In the Greenfield inverse model scenario, savings uncertainty comes from model fit statistics
        (CV(RMSE), fractional savings uncertainty). Here, uncertainty comes from parameter sensitivity.
        Which approach gives you more insight into <em>where</em> the uncertainty comes from?
      </div>
    </section>
  );
}
