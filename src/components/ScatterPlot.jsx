import { useMemo } from 'react';
import Plot from 'react-plotly.js';
import { fiveParam, threeParamHeating } from '../utils/statistics';

const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

export default function ScatterPlot({ data, fuelType, modelParams, modelType }) {
  const traces = useMemo(() => {
    if (!data || data.length === 0) return [];
    const oat = data.map((d) => d.avg_oat_f);
    const energy = fuelType === 'electric'
      ? data.map((d) => d.total_kwh)
      : data.map((d) => d.total_therms);
    const labels = data.map((d) => MONTHS[d.month - 1]);

    const result = [
      {
        x: oat,
        y: energy,
        mode: 'markers+text',
        text: labels,
        textposition: 'top center',
        marker: { size: 14, color: fuelType === 'electric' ? '#1f77b4' : '#d62728' },
        name: fuelType === 'electric' ? 'Monthly kWh' : 'Monthly therms',
      },
    ];

    // Add model fit line if params provided
    if (modelParams) {
      const sortedOAT = [...oat].sort((a, b) => a - b);
      const fineOAT = [];
      for (let t = sortedOAT[0] - 2; t <= sortedOAT[sortedOAT.length - 1] + 2; t += 0.5) {
        fineOAT.push(t);
      }
      let predicted;
      if (modelType === '5P') {
        predicted = fiveParam(fineOAT, modelParams);
      } else if (modelType === '3PH') {
        predicted = threeParamHeating(fineOAT, modelParams);
      }
      if (predicted) {
        result.push({
          x: fineOAT,
          y: predicted,
          mode: 'lines',
          line: { color: '#2ca02c', width: 2, dash: 'dash' },
          name: `${modelType} Model Fit`,
        });
      }
    }

    return result;
  }, [data, fuelType, modelParams, modelType]);

  const yLabel = fuelType === 'electric' ? 'Monthly Electricity (kWh)' : 'Monthly Gas (therms)';
  const title = fuelType === 'electric'
    ? 'Baseline: Monthly Electricity vs Avg OAT'
    : 'Baseline: Monthly Gas vs Avg OAT';

  return (
    <Plot
      data={traces}
      layout={{
        title,
        xaxis: { title: 'Average Outdoor Air Temperature (°F)' },
        yaxis: { title: yLabel },
        showlegend: true,
        height: 500,
        margin: { t: 60, r: 40, b: 60, l: 80 },
      }}
      useResizeHandler
      style={{ width: '100%' }}
    />
  );
}
