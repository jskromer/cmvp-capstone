import { useState, useMemo } from 'react';
import Plot from 'react-plotly.js';
import { fiveParam, threeParamHeating } from '../utils/statistics';

const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const CREAM_BG = '#f5f0e8';

export default function TimeSeriesPlot({ baseline, reporting, noNRA, elecParams, gasParams, elecModelType }) {
  const [fuel, setFuel] = useState('electric');

  const traces = useMemo(() => {
    if (!baseline || !reporting) return [];
    const months = baseline.map(d => MONTHS[d.month - 1]);
    const isElec = fuel === 'electric';
    const key = isElec ? 'total_kwh' : 'total_therms';
    const unit = isElec ? 'kWh' : 'therms';

    const result = [
      {
        x: months,
        y: baseline.map(d => d[key]),
        mode: 'lines+markers',
        marker: { size: 10 },
        line: { color: '#2980b9', width: 2, dash: 'dash' },
        name: `Baseline Year (${unit})`,
      },
      {
        x: months,
        y: reporting.map(d => d[key]),
        mode: 'lines+markers',
        marker: { size: 10 },
        line: { color: '#e74c3c', width: 2 },
        name: `Reporting Year (${unit})`,
      },
    ];

    // Model prediction overlay (counterfactual for reporting weather)
    if (isElec && elecParams) {
      const reportOAT = reporting.map(d => d.avg_oat_f);
      const pred = elecModelType === '5P'
        ? fiveParam(reportOAT, elecParams)
        : threeParamHeating(reportOAT, elecParams);
      result.push({
        x: months,
        y: pred,
        mode: 'lines+markers',
        marker: { size: 8, symbol: 'diamond' },
        line: { color: '#8e44ad', width: 2, dash: 'dot' },
        name: 'Model Prediction (counterfactual)',
      });
    }

    if (!isElec && gasParams) {
      const reportOAT = reporting.map(d => d.avg_oat_f);
      const pred = threeParamHeating(reportOAT, gasParams);
      result.push({
        x: months,
        y: pred,
        mode: 'lines+markers',
        marker: { size: 8, symbol: 'diamond' },
        line: { color: '#8e44ad', width: 2, dash: 'dot' },
        name: 'Model Prediction (counterfactual)',
      });
    }

    if (noNRA) {
      result.push({
        x: months,
        y: noNRA.map(d => d[key]),
        mode: 'lines+markers',
        marker: { size: 8 },
        line: { color: '#27ae60', width: 2 },
        name: `Answer Key — no NRA (${unit})`,
      });
    }

    return result;
  }, [baseline, reporting, noNRA, elecParams, gasParams, elecModelType, fuel]);

  const title = fuel === 'electric'
    ? 'Monthly Electricity: Baseline vs. Reporting Period'
    : 'Monthly Gas: Baseline vs. Reporting Period';

  return (
    <div>
      <div className="controls" style={{ marginBottom: '0.5rem' }}>
        <label>
          Fuel:
          <select value={fuel} onChange={e => setFuel(e.target.value)} style={{ marginLeft: 8 }}>
            <option value="electric">Electric (kWh)</option>
            <option value="gas">Gas (therms)</option>
          </select>
        </label>
      </div>

      <Plot
        data={traces}
        layout={{
          title: { text: title, font: { size: 15, color: '#1a365d' } },
          xaxis: { title: 'Month', gridcolor: '#e8e0d0' },
          yaxis: { title: fuel === 'electric' ? 'Monthly Electricity (kWh)' : 'Monthly Gas (therms)', gridcolor: '#e8e0d0' },
          showlegend: true,
          legend: { x: 0.01, y: 0.99, bgcolor: 'rgba(245,240,232,0.8)' },
          height: 500,
          margin: { t: 50, r: 40, b: 55, l: 80 },
          paper_bgcolor: CREAM_BG,
          plot_bgcolor: 'white',
          font: { family: 'Segoe UI, sans-serif', size: 12 },
        }}
        useResizeHandler
        style={{ width: '100%' }}
      />

      {fuel === 'gas' && (
        <div className="prompt-box">
          <strong>Observe</strong>
          Gas consumption in the reporting year is higher than baseline.
          Does this mean the retrofit made things worse? What else could explain this?
        </div>
      )}
    </div>
  );
}
