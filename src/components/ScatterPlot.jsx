import { useMemo } from 'react';
import Plot from 'react-plotly.js';
import { fiveParam, threeParamHeating } from '../utils/statistics';

const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const CREAM_BG = '#FFF8F0';

export default function ScatterPlot({ data, fuelType, modelParams, modelType }) {
  const traces = useMemo(() => {
    if (!data || data.length === 0) return [];
    const oat = data.map(d => d.avg_oat_f);
    const energy = fuelType === 'electric'
      ? data.map(d => d.total_kwh)
      : data.map(d => d.total_therms);
    const labels = data.map(d => MONTHS[d.month - 1]);

    const result = [{
      x: oat, y: energy,
      mode: 'markers+text',
      text: labels,
      textposition: 'top center',
      textfont: { size: 11, color: '#4a4540' },
      marker: {
        size: 14,
        color: fuelType === 'electric' ? '#2980b9' : '#e74c3c',
        line: { width: 1, color: 'white' },
      },
      name: fuelType === 'electric' ? 'Monthly kWh' : 'Monthly therms',
    }];

    if (modelParams) {
      const sortedOAT = [...oat].sort((a, b) => a - b);
      const fineOAT = [];
      for (let t = sortedOAT[0] - 3; t <= sortedOAT[sortedOAT.length - 1] + 3; t += 0.5) {
        fineOAT.push(t);
      }
      let predicted;
      if (modelType === '5P') predicted = fiveParam(fineOAT, modelParams);
      else if (modelType === '3PH') predicted = threeParamHeating(fineOAT, modelParams);

      if (predicted) {
        result.push({
          x: fineOAT, y: predicted,
          mode: 'lines',
          line: { color: '#27ae60', width: 2.5 },
          name: 'Model Fit',
        });
      }
    }

    return result;
  }, [data, fuelType, modelParams, modelType]);

  const yLabel = fuelType === 'electric' ? 'Monthly Electricity (kWh)' : 'Monthly Gas (therms)';
  const title = fuelType === 'electric'
    ? 'Baseline: Monthly Electricity vs. Outdoor Air Temperature'
    : 'Baseline: Monthly Gas vs. Outdoor Air Temperature';

  return (
    <Plot
      data={traces}
      layout={{
        title: { text: title, font: { size: 15, color: '#1a365d' } },
        xaxis: { title: 'Average Outdoor Air Temperature (°F)', gridcolor: '#e8e0d0' },
        yaxis: { title: yLabel, gridcolor: '#e8e0d0' },
        showlegend: true,
        height: 480,
        margin: { t: 50, r: 40, b: 55, l: 80 },
        paper_bgcolor: CREAM_BG,
        plot_bgcolor: 'white',
        font: { family: 'Segoe UI, sans-serif', size: 12 },
      }}
      useResizeHandler
      style={{ width: '100%' }}
    />
  );
}
