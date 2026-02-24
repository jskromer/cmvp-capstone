import { useMemo } from 'react';
import Plot from 'react-plotly.js';

const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

export default function TimeSeriesPlot({ baseline, reporting, noNRA }) {
  const traces = useMemo(() => {
    if (!baseline || !reporting) return [];
    const months = baseline.map((d) => MONTHS[d.month - 1]);
    const result = [
      {
        x: months,
        y: baseline.map((d) => d.total_kwh),
        mode: 'lines+markers',
        marker: { size: 10 },
        line: { color: '#1f77b4', dash: 'dash' },
        name: 'Baseline',
      },
      {
        x: months,
        y: reporting.map((d) => d.total_kwh),
        mode: 'lines+markers',
        marker: { size: 10 },
        line: { color: '#d62728' },
        name: 'Reporting (w/ NRA)',
      },
    ];
    if (noNRA) {
      result.push({
        x: months,
        y: noNRA.map((d) => d.total_kwh),
        mode: 'lines+markers',
        marker: { size: 10 },
        line: { color: '#2ca02c' },
        name: 'Reporting (no NRA)',
      });
    }
    return result;
  }, [baseline, reporting, noNRA]);

  return (
    <Plot
      data={traces}
      layout={{
        title: 'Monthly Electric: Baseline vs Reporting Period',
        xaxis: { title: 'Month' },
        yaxis: { title: 'Monthly Electricity (kWh)' },
        showlegend: true,
        height: 500,
        margin: { t: 60, r: 40, b: 60, l: 80 },
        shapes: [
          {
            type: 'rect',
            x0: 7.5, y0: 0, x1: 11.5, y1: 1,
            yref: 'paper',
            fillcolor: 'rgba(255,0,0,0.08)',
            line: { width: 0 },
          },
          {
            type: 'line',
            x0: 7.5, y0: 0, x1: 7.5, y1: 1,
            yref: 'paper',
            line: { color: 'red', dash: 'dot' },
          },
        ],
        annotations: [
          {
            x: 9.5,
            y: 1.02,
            yref: 'paper',
            text: 'NRA: DC Expansion',
            showarrow: false,
            font: { color: 'red', size: 12 },
          },
        ],
      }}
      useResizeHandler
      style={{ width: '100%' }}
    />
  );
}
