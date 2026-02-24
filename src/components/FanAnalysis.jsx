import { useState, useEffect, useMemo } from 'react';
import Plot from 'react-plotly.js';
import { loadFanData } from '../utils/dataLoader';

const CREAM_BG = '#f5f0e8';

export default function FanAnalysis() {
  const [fanData, setFanData] = useState(null);
  const [selectedAHU, setSelectedAHU] = useState('ahu1');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFanData().then(d => { setFanData(d); setLoading(false); });
  }, []);

  const analysis = useMemo(() => {
    if (!fanData) return null;

    // Split into pre (2024) and post (2025) by datetime
    const pre = fanData.filter(d => d.datetime && d.datetime.startsWith('2024'));
    const post = fanData.filter(d => d.datetime && d.datetime.startsWith('2025'));

    const getKW = (d) => d[`${selectedAHU}_fan_kw`];
    const getSpeed = (d) => d[`${selectedAHU}_fan_speed_pct`];
    const getCFM = (d) => d[`${selectedAHU}_fan_cfm`];

    // Filter out zero-speed points (AHU off)
    const preOn = pre.filter(d => getSpeed(d) > 0);
    const postOn = post.filter(d => getSpeed(d) > 0);

    return { pre, post, preOn, postOn, getKW, getSpeed, getCFM };
  }, [fanData, selectedAHU]);

  if (loading) return <div className="loading">Loading fan data...</div>;
  if (!analysis) return null;

  const { preOn, postOn, getKW, getSpeed, getCFM } = analysis;

  const ahuLabels = {
    ahu1: 'AHU-1 (Wing A — 15 HP)',
    ahu2: 'AHU-2 (Wing B — 10 HP)',
    ahu3: 'AHU-3 (Common — 5 HP)',
  };

  // Summary stats
  const preAvgKW = preOn.length > 0 ? preOn.reduce((s, d) => s + getKW(d), 0) / preOn.length : 0;
  const postAvgKW = postOn.length > 0 ? postOn.reduce((s, d) => s + getKW(d), 0) / postOn.length : 0;
  const preMaxKW = preOn.length > 0 ? Math.max(...preOn.map(d => getKW(d))) : 0;
  const postMaxKW = postOn.length > 0 ? Math.max(...postOn.map(d => getKW(d))) : 0;

  return (
    <div>
      {/* VFD illustration */}
      <svg viewBox="0 0 600 90" style={{ width: "100%", maxWidth: 600, display: "block", margin: "0 auto 1rem" }}>
        {/* Before */}
        <text x="150" y="14" textAnchor="middle" fontSize="11" fill="#7f8c8d" fontWeight="600">BASELINE (constant speed)</text>
        <rect x="80" y="22" width="140" height="48" fill="#f9f6f0" stroke="#d5ccc0" rx="6" />
        {/* Motor */}
        <circle cx="130" cy="46" r="16" fill="none" stroke="#e74c3c" strokeWidth="2.5" />
        <text x="130" y="50" textAnchor="middle" fontSize="8" fill="#e74c3c" fontWeight="700">100%</text>
        {/* Fan blades */}
        <line x1="165" y1="36" x2="185" y2="30" stroke="#95a5a6" strokeWidth="2" />
        <line x1="165" y1="46" x2="190" y2="46" stroke="#95a5a6" strokeWidth="2" />
        <line x1="165" y1="56" x2="185" y2="62" stroke="#95a5a6" strokeWidth="2" />

        {/* Arrow */}
        <text x="300" y="50" textAnchor="middle" fontSize="24" fill="#27ae60">→</text>

        {/* After */}
        <text x="450" y="14" textAnchor="middle" fontSize="11" fill="#7f8c8d" fontWeight="600">RETROFIT (VFD — variable speed)</text>
        <rect x="380" y="22" width="140" height="48" fill="#f9f6f0" stroke="#d5ccc0" rx="6" />
        {/* VFD box */}
        <rect x="392" y="32" width="28" height="28" fill="#27ae60" rx="3" />
        <text x="406" y="50" textAnchor="middle" fontSize="7" fill="white" fontWeight="700">VFD</text>
        {/* Motor */}
        <circle cx="450" cy="46" r="16" fill="none" stroke="#27ae60" strokeWidth="2.5" />
        <text x="450" y="50" textAnchor="middle" fontSize="8" fill="#27ae60" fontWeight="700">65%</text>
        {/* Fan blades (smaller) */}
        <line x1="475" y1="39" x2="492" y2="35" stroke="#95a5a6" strokeWidth="1.5" />
        <line x1="475" y1="46" x2="495" y2="46" stroke="#95a5a6" strokeWidth="1.5" />
        <line x1="475" y1="53" x2="492" y2="57" stroke="#95a5a6" strokeWidth="1.5" />
      </svg>

      <div className="controls">
        <label>
          Select AHU:
          <select value={selectedAHU} onChange={e => setSelectedAHU(e.target.value)}>
            <option value="ahu1">AHU-1 (Wing A — 15 HP)</option>
            <option value="ahu2">AHU-2 (Wing B — 10 HP)</option>
            <option value="ahu3">AHU-3 (Common — 5 HP)</option>
          </select>
        </label>
      </div>

      {/* Fan Law scatter: Speed vs Power */}
      <Plot
        data={[
          {
            x: preOn.map(d => getSpeed(d)),
            y: preOn.map(d => getKW(d)),
            mode: 'markers',
            marker: { size: 8, color: '#e74c3c', opacity: 0.6 },
            name: 'Baseline (pre-VFD)',
          },
          {
            x: postOn.map(d => getSpeed(d)),
            y: postOn.map(d => getKW(d)),
            mode: 'markers',
            marker: { size: 8, color: '#27ae60', opacity: 0.6 },
            name: 'Reporting (post-VFD)',
          },
        ]}
        layout={{
          title: { text: `${ahuLabels[selectedAHU]} — Fan Power vs. Speed`, font: { size: 15, color: '#1a365d' } },
          xaxis: { title: 'Fan Speed (%)', gridcolor: '#e8e0d0' },
          yaxis: { title: 'Fan Power (kW)', gridcolor: '#e8e0d0' },
          height: 420,
          paper_bgcolor: CREAM_BG,
          plot_bgcolor: 'white',
          font: { family: 'Segoe UI, sans-serif' },
          margin: { t: 50, r: 30, b: 50, l: 60 },
          legend: { x: 0.01, y: 0.99, bgcolor: 'rgba(245,240,232,0.8)' },
        }}
        useResizeHandler style={{ width: '100%' }}
      />

      {/* Power vs OAT */}
      <Plot
        data={[
          {
            x: preOn.map(d => d.oat_f),
            y: preOn.map(d => getKW(d)),
            mode: 'markers',
            marker: { size: 7, color: '#e74c3c', opacity: 0.5 },
            name: 'Baseline',
          },
          {
            x: postOn.map(d => d.oat_f),
            y: postOn.map(d => getKW(d)),
            mode: 'markers',
            marker: { size: 7, color: '#27ae60', opacity: 0.5 },
            name: 'Post-VFD',
          },
        ]}
        layout={{
          title: { text: `${ahuLabels[selectedAHU]} — Fan Power vs. Outdoor Temperature`, font: { size: 15, color: '#1a365d' } },
          xaxis: { title: 'Outdoor Air Temperature (°F)', gridcolor: '#e8e0d0' },
          yaxis: { title: 'Fan Power (kW)', gridcolor: '#e8e0d0' },
          height: 400,
          paper_bgcolor: CREAM_BG,
          plot_bgcolor: 'white',
          font: { family: 'Segoe UI, sans-serif' },
          margin: { t: 50, r: 30, b: 50, l: 60 },
          legend: { x: 0.01, y: 0.99, bgcolor: 'rgba(245,240,232,0.8)' },
        }}
        useResizeHandler style={{ width: '100%' }}
      />

      {/* Summary cards */}
      <div className="info-grid" style={{ marginTop: '1rem' }}>
        <div className="info-card">
          <h3>Baseline (Pre-VFD)</h3>
          <p>Avg power: <strong>{preAvgKW.toFixed(2)} kW</strong></p>
          <p>Peak power: <strong>{preMaxKW.toFixed(2)} kW</strong></p>
          <p>Operating hours measured: {preOn.length}</p>
        </div>
        <div className="info-card">
          <h3>Post-VFD</h3>
          <p>Avg power: <strong style={{ color: '#27ae60' }}>{postAvgKW.toFixed(2)} kW</strong></p>
          <p>Peak power: <strong>{postMaxKW.toFixed(2)} kW</strong></p>
          <p>Operating hours measured: {postOn.length}</p>
        </div>
        <div className="info-card">
          <h3>Reduction</h3>
          <p style={{ fontSize: '1.3rem', fontWeight: 700, color: '#27ae60' }}>
            {preAvgKW > 0 ? ((1 - postAvgKW / preAvgKW) * 100).toFixed(0) : 0}% avg power reduction
          </p>
          <p>Fan affinity law: Power ∝ Speed³</p>
          <p style={{ fontSize: '0.8rem', color: '#8c8478' }}>
            A 35% speed reduction → ~73% power reduction
          </p>
        </div>
      </div>

      <div className="prompt-box">
        <strong>Observe</strong>
        Does the Speed vs. Power relationship follow the cubic fan law?
        Why does the post-VFD data show variable speed while baseline is constant?
        What does this tell you about the approach selection for ECM-4?
      </div>

      <div className="prompt-box">
        <strong>Metering Plan</strong>
        This is continuous performance verification (cf. IPMVP Option B).
        What meters are needed? Where should they be installed?
        How long should the measurement period be? What about data loss?
      </div>
    </div>
  );
}
