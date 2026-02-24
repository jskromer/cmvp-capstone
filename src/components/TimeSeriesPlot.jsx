import { useMemo } from 'react';
import Plot from 'react-plotly.js';

const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const CREAM_BG = '#f5f0e8';

export default function TimeSeriesPlot({ baseline, reporting, noNRA }) {
  const traces = useMemo(() => {
    if (!baseline || !reporting) return [];
    const months = baseline.map(d => MONTHS[d.month - 1]);
    const result = [
      {
        x: months,
        y: baseline.map(d => d.total_kwh),
        mode: 'lines+markers',
        marker: { size: 10 },
        line: { color: '#2980b9', width: 2, dash: 'dash' },
        name: 'Baseline Year',
      },
      {
        x: months,
        y: reporting.map(d => d.total_kwh),
        mode: 'lines+markers',
        marker: { size: 10 },
        line: { color: '#e74c3c', width: 2 },
        name: 'Reporting Year',
      },
    ];
    if (noNRA) {
      result.push({
        x: months,
        y: noNRA.map(d => d.total_kwh),
        mode: 'lines+markers',
        marker: { size: 8 },
        line: { color: '#27ae60', width: 2 },
        name: 'Answer Key (no NRA)',
      });
    }
    return result;
  }, [baseline, reporting, noNRA]);

  return (
    <Plot
      data={traces}
      layout={{
        title: { text: 'Monthly Electricity: Baseline vs. Reporting Period', font: { size: 15, color: '#1a365d' } },
        xaxis: { title: 'Month', gridcolor: '#e0d8c8' },
        yaxis: { title: 'Monthly Electricity (kWh)', gridcolor: '#e0d8c8' },
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
  );
}
