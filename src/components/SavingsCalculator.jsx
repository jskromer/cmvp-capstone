import { useState, useMemo } from 'react';
import Plot from 'react-plotly.js';
import { fiveParam, threeParamHeating, cvrmse, fractionalSavingsUncertainty } from '../utils/statistics';

const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const CREAM_BG = '#f5f0e8';

// Rates
const ELEC_RATE = 0.105;  // $/kWh
const GAS_RATE = 1.15;    // $/therm
const CO2_ELEC = 0.000417; // metric tons CO₂/kWh (mid-Atlantic grid)
const CO2_GAS = 0.005302;  // metric tons CO₂/therm

export default function SavingsCalculator({ baseline, reporting, noNRA, elecParams, gasParams, elecModelType }) {
  const [applyNRA, setApplyNRA] = useState(false);
  const [nraKwhPerMonth, setNraKwhPerMonth] = useState(15000);
  const [nraStartMonth, setNraStartMonth] = useState(8);

  const results = useMemo(() => {
    if (!baseline || !reporting || !elecParams || !gasParams) return null;

    const oat = reporting.map(d => d.avg_oat_f);
    const actualKwh = reporting.map(d => d.total_kwh);
    const actualTherms = reporting.map(d => d.total_therms);

    // Counterfactual predictions using baseline model + reporting weather
    const predKwh = elecModelType === '5P'
      ? fiveParam(oat, elecParams)
      : threeParamHeating(oat, elecParams);
    const predTherms = threeParamHeating(oat, gasParams);

    // Monthly savings
    const monthly = MONTHS.map((m, i) => {
      const nraAdj = applyNRA && (i + 1) >= nraStartMonth ? nraKwhPerMonth : 0;
      const adjActualKwh = actualKwh[i] - nraAdj;
      const elecSavings = predKwh[i] - adjActualKwh;
      const gasSavings = predTherms[i] - actualTherms[i];
      return {
        month: m,
        idx: i,
        oat: oat[i],
        predKwh: predKwh[i],
        actualKwh: actualKwh[i],
        nraAdj,
        adjActualKwh,
        elecSavings,
        predTherms: predTherms[i],
        actualTherms: actualTherms[i],
        gasSavings,
        elecCost: elecSavings * ELEC_RATE,
        gasCost: gasSavings * GAS_RATE,
        elecCO2: elecSavings * CO2_ELEC,
        gasCO2: gasSavings * CO2_GAS,
      };
    });

    const totals = {
      predKwh: monthly.reduce((s, r) => s + r.predKwh, 0),
      actualKwh: monthly.reduce((s, r) => s + r.actualKwh, 0),
      nraAdj: monthly.reduce((s, r) => s + r.nraAdj, 0),
      adjActualKwh: monthly.reduce((s, r) => s + r.adjActualKwh, 0),
      elecSavings: monthly.reduce((s, r) => s + r.elecSavings, 0),
      predTherms: monthly.reduce((s, r) => s + r.predTherms, 0),
      actualTherms: monthly.reduce((s, r) => s + r.actualTherms, 0),
      gasSavings: monthly.reduce((s, r) => s + r.gasSavings, 0),
      elecCost: monthly.reduce((s, r) => s + r.elecCost, 0),
      gasCost: monthly.reduce((s, r) => s + r.gasCost, 0),
      elecCO2: monthly.reduce((s, r) => s + r.elecCO2, 0),
      gasCO2: monthly.reduce((s, r) => s + r.gasCO2, 0),
    };

    totals.totalCost = totals.elecCost + totals.gasCost;
    totals.totalCO2 = totals.elecCO2 + totals.gasCO2;
    totals.elecPct = totals.predKwh > 0 ? (totals.elecSavings / totals.predKwh * 100) : 0;
    totals.gasPct = totals.predTherms > 0 ? (totals.gasSavings / totals.predTherms * 100) : 0;

    // Fractional savings uncertainty (electric)
    const baseOat = baseline.map(d => d.avg_oat_f);
    const baseKwh = baseline.map(d => d.total_kwh);
    const basePred = elecModelType === '5P' ? fiveParam(baseOat, elecParams) : threeParamHeating(baseOat, elecParams);
    const cv = cvrmse(baseKwh, basePred);
    const fracSavings = totals.predKwh > 0 ? totals.elecSavings / totals.predKwh : 0;
    const fsu90 = fracSavings > 0 ? fractionalSavingsUncertainty(baseKwh, basePred, fracSavings, 0.9) : null;

    return { monthly, totals, cv, fracSavings, fsu90 };
  }, [baseline, reporting, elecParams, gasParams, elecModelType, applyNRA, nraKwhPerMonth, nraStartMonth]);

  if (!elecParams || !gasParams) {
    return (
      <div className="prompt-box">
        <strong>First</strong>
        Fit baseline models in the Model Fitting tab before calculating savings.
      </div>
    );
  }

  if (!results) return null;

  const { monthly, totals, fsu90 } = results;
  const fmt = v => v.toLocaleString(undefined, { maximumFractionDigits: 0 });
  const fmt1 = v => v.toFixed(1);

  return (
    <div>
      {/* NRA Controls */}
      <div className="stats-panel">
        <h4>Non-Routine Adjustment</h4>
        <div className="slider-group">
          <label>
            <input type="checkbox" checked={applyNRA} onChange={e => setApplyNRA(e.target.checked)} />
            Apply NRA to reporting data
          </label>
          {applyNRA && (
            <>
              <label>
                Start month:
                <select value={nraStartMonth} onChange={e => setNraStartMonth(+e.target.value)}>
                  {MONTHS.map((m, i) => <option key={m} value={i + 1}>{m}</option>)}
                </select>
              </label>
              <label>
                Adjustment:
                <input type="range" min={5000} max={25000} step={1000}
                  value={nraKwhPerMonth} onChange={e => setNraKwhPerMonth(+e.target.value)} />
                <span className="slider-value">{fmt(nraKwhPerMonth)} kWh/mo</span>
              </label>
            </>
          )}
        </div>
      </div>

      {/* Savings chart */}
      <Plot
        data={[
          {
            x: MONTHS, y: monthly.map(r => r.predKwh),
            type: 'bar', name: 'Counterfactual (predicted)',
            marker: { color: '#2980b9', opacity: 0.5 },
          },
          {
            x: MONTHS, y: monthly.map(r => r.adjActualKwh),
            type: 'bar', name: applyNRA ? 'Actual (NRA adjusted)' : 'Actual',
            marker: { color: applyNRA ? '#27ae60' : '#e74c3c' },
          },
        ]}
        layout={{
          title: { text: 'Monthly Electric: Counterfactual vs. Actual', font: { size: 15, color: '#1a365d' } },
          barmode: 'group',
          xaxis: { title: 'Month' },
          yaxis: { title: 'kWh' },
          height: 400,
          paper_bgcolor: CREAM_BG,
          plot_bgcolor: 'white',
          font: { family: 'Segoe UI, sans-serif' },
          margin: { t: 50, r: 30, b: 50, l: 70 },
          legend: { x: 0.01, y: 0.99, bgcolor: 'rgba(245,240,232,0.8)' },
        }}
        useResizeHandler style={{ width: '100%' }}
      />

      {/* Monthly savings table */}
      <h4 style={{ color: '#1a365d', marginTop: '1.5rem' }}>Monthly Electric Savings</h4>
      <div style={{ overflowX: 'auto' }}>
        <table className="stats-table">
          <thead>
            <tr>
              <th>Month</th>
              <th>OAT (°F)</th>
              <th>Predicted (kWh)</th>
              <th>Actual (kWh)</th>
              {applyNRA && <th>NRA Adj (kWh)</th>}
              <th>Savings (kWh)</th>
              <th>Savings ($)</th>
            </tr>
          </thead>
          <tbody>
            {monthly.map(r => (
              <tr key={r.month} style={r.elecSavings < 0 ? { background: '#fef3f2' } : {}}>
                <td style={{ fontWeight: 600 }}>{r.month}</td>
                <td>{fmt1(r.oat)}</td>
                <td>{fmt(r.predKwh)}</td>
                <td>{fmt(r.actualKwh)}</td>
                {applyNRA && <td style={{ color: r.nraAdj > 0 ? '#e67e22' : '#999' }}>{r.nraAdj > 0 ? `-${fmt(r.nraAdj)}` : '—'}</td>}
                <td style={{ fontWeight: 600, color: r.elecSavings >= 0 ? '#27ae60' : '#e74c3c' }}>
                  {fmt(r.elecSavings)}
                </td>
                <td>${r.elecCost.toFixed(0)}</td>
              </tr>
            ))}
            <tr style={{ fontWeight: 700, background: '#f5f0e8' }}>
              <td>TOTAL</td>
              <td>—</td>
              <td>{fmt(totals.predKwh)}</td>
              <td>{fmt(totals.actualKwh)}</td>
              {applyNRA && <td style={{ color: '#e67e22' }}>{fmt(totals.nraAdj)}</td>}
              <td style={{ color: totals.elecSavings >= 0 ? '#27ae60' : '#e74c3c' }}>
                {fmt(totals.elecSavings)} ({fmt1(totals.elecPct)}%)
              </td>
              <td>${fmt(totals.elecCost)}</td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Valuation summary */}
      <div className="info-grid" style={{ marginTop: '1.5rem' }}>
        <div className="info-card">
          <h3>Cost Savings</h3>
          <p style={{ fontSize: '1.5rem', fontWeight: 700, color: totals.totalCost >= 0 ? '#27ae60' : '#e74c3c' }}>
            ${fmt(totals.totalCost)}/yr
          </p>
          <p>Electric: ${fmt(totals.elecCost)} ({fmt(totals.elecSavings)} kWh × ${ELEC_RATE}/kWh)</p>
          <p>Gas: ${fmt(totals.gasCost)} ({fmt(totals.gasSavings)} therms × ${GAS_RATE}/therm)</p>
        </div>
        <div className="info-card">
          <h3>CO₂ Reduction</h3>
          <p style={{ fontSize: '1.5rem', fontWeight: 700, color: totals.totalCO2 >= 0 ? '#27ae60' : '#e74c3c' }}>
            {fmt1(totals.totalCO2)} metric tons/yr
          </p>
          <p>Electric: {fmt1(totals.elecCO2)} t ({CO2_ELEC * 1000} kg/kWh)</p>
          <p>Gas: {fmt1(totals.gasCO2)} t ({CO2_GAS} t/therm)</p>
        </div>
        <div className="info-card">
          <h3>Uncertainty (Electric)</h3>
          {fsu90 !== null && fsu90 !== Infinity ? (
            <>
              <p style={{ fontSize: '1.5rem', fontWeight: 700, color: fsu90 <= 0.5 ? '#27ae60' : '#e67e22' }}>
                ±{(fsu90 * 100).toFixed(1)}%
              </p>
              <p>Fractional savings uncertainty at 90% confidence</p>
              <p style={{ fontSize: '0.8rem', color: '#8c8478' }}>
                {fsu90 <= 0.5 ? 'Savings are statistically significant' : 'Savings may not be statistically significant'}
              </p>
            </>
          ) : (
            <p style={{ color: '#e67e22' }}>Cannot compute — fit models first or savings fraction is zero</p>
          )}
        </div>
      </div>

      {!applyNRA && (
        <div className="prompt-box">
          <strong>Notice</strong>
          Without NRA adjustment, some months show negative savings (consumption went up).
          What happened? Enable the NRA toggle and adjust the parameters.
        </div>
      )}

      {applyNRA && (
        <div className="prompt-box">
          <strong>Reflect</strong>
          How did you determine the NRA magnitude? What evidence supports your adjustment?
          What happens to savings uncertainty when you change the NRA amount?
        </div>
      )}
    </div>
  );
}
