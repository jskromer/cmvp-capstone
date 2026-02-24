import { useState, useMemo } from 'react';

const FIXTURE_DATA = [
  { id: 1, space: "Wing A — Open Office (2nd floor)", qty: 120, baseW: 128, retroW: 40, hours: 2860 },
  { id: 2, space: "Wing A — Open Office (1st floor)", qty: 120, baseW: 128, retroW: 40, hours: 2860 },
  { id: 3, space: "Wing A — Private Offices", qty: 80, baseW: 96, retroW: 32, hours: 2600 },
  { id: 4, space: "Wing A — Conference Rooms", qty: 40, baseW: 128, retroW: 40, hours: 1200 },
  { id: 5, space: "Wing A — Corridors & Restrooms", qty: 60, baseW: 64, retroW: 20, hours: 3380 },
  { id: 6, space: "Wing B — Reading Rooms", qty: 100, baseW: 128, retroW: 40, hours: 3900 },
  { id: 7, space: "Wing B — Stacks", qty: 150, baseW: 96, retroW: 32, hours: 2600 },
  { id: 8, space: "Wing B — Meeting Rooms", qty: 30, baseW: 128, retroW: 40, hours: 1500 },
  { id: 9, space: "Wing B — Circulation & Entry", qty: 40, baseW: 64, retroW: 20, hours: 4160 },
];

export default function LightingStipulation() {
  // Students can edit hours for each space
  const [hoursOverrides, setHoursOverrides] = useState({});

  const getHours = (id, defaultH) => hoursOverrides[id] ?? defaultH;

  const rows = useMemo(() => {
    return FIXTURE_DATA.map(f => {
      const hours = getHours(f.id, f.hours);
      const deltaW = f.baseW - f.retroW;
      const kwhSaved = (f.qty * deltaW * hours) / 1000;
      return { ...f, hours, deltaW, kwhSaved };
    });
  }, [hoursOverrides]);

  const totals = useMemo(() => ({
    qty: rows.reduce((s, r) => s + r.qty, 0),
    baseKw: rows.reduce((s, r) => s + r.qty * r.baseW, 0) / 1000,
    retroKw: rows.reduce((s, r) => s + r.qty * r.retroW, 0) / 1000,
    deltaKw: rows.reduce((s, r) => s + r.qty * r.deltaW, 0) / 1000,
    kwhSaved: rows.reduce((s, r) => s + r.kwhSaved, 0),
  }), [rows]);

  const fmt = v => v.toLocaleString(undefined, { maximumFractionDigits: 0 });

  return (
    <div>
      {/* Stipulation illustration */}
      <svg viewBox="0 0 600 100" style={{ width: "100%", maxWidth: 600, display: "block", margin: "0 auto 1rem" }}>
        <defs>
          <linearGradient id="glow" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
            <stop offset="0%" stopColor="#f1c40f" stopOpacity="0.4" />
            <stop offset="100%" stopColor="#f1c40f" stopOpacity="0" />
          </linearGradient>
        </defs>
        {/* Before */}
        <text x="150" y="15" textAnchor="middle" fontSize="12" fill="#7f8c8d" fontWeight="600">BASELINE</text>
        <rect x="90" y="25" width="120" height="50" fill="#f9f6f0" stroke="#d5ccc0" rx="6" />
        {/* T8 tubes */}
        {[110, 140, 170].map(x => (
          <g key={`t8-${x}`}>
            <rect x={x} y="38" width="8" height="24" fill="#ffeaa7" rx="2" />
            <rect x={x+1} y="40" width="6" height="20" fill="#fdcb6e" rx="1" />
          </g>
        ))}
        <text x="150" y="90" textAnchor="middle" fontSize="10" fill="#e74c3c" fontWeight="600">128W T8 Fluorescent</text>

        {/* Arrow */}
        <text x="300" y="55" textAnchor="middle" fontSize="24" fill="#27ae60">→</text>

        {/* After */}
        <text x="450" y="15" textAnchor="middle" fontSize="12" fill="#7f8c8d" fontWeight="600">RETROFIT</text>
        <rect x="390" y="25" width="120" height="50" fill="#f9f6f0" stroke="#d5ccc0" rx="6" />
        {/* LED panels */}
        {[410, 440, 470].map(x => (
          <g key={`led-${x}`}>
            <rect x={x} y="38" width="12" height="24" fill="#fff" stroke="#f1c40f" strokeWidth="1.5" rx="3" />
            <circle cx={x+6} cy={50} r="4" fill="#f1c40f" opacity="0.6" />
          </g>
        ))}
        <text x="450" y="90" textAnchor="middle" fontSize="10" fill="#27ae60" fontWeight="600">40W LED Panel</text>
      </svg>

      <div className="prompt-box">
        <strong>ECM-1: Key Parameter Measurement (cf. IPMVP Option A)</strong>
        Fixture wattage is measured (or verified from spec sheets). Operating hours are stipulated based on building schedules.
        You can adjust the hours for each space below. What is your basis for each value?
      </div>

      {/* Fixture inventory table */}
      <div style={{ overflowX: 'auto' }}>
        <table className="stats-table">
          <thead>
            <tr>
              <th>Space</th>
              <th>Qty</th>
              <th>Baseline (W)</th>
              <th>Retrofit (W)</th>
              <th>ΔW</th>
              <th>Annual Hours</th>
              <th>kWh Saved</th>
            </tr>
          </thead>
          <tbody>
            {rows.map(r => (
              <tr key={r.id}>
                <td style={{ fontSize: '0.85rem' }}>{r.space}</td>
                <td>{r.qty}</td>
                <td>{r.baseW}</td>
                <td>{r.retroW}</td>
                <td style={{ fontWeight: 600 }}>{r.deltaW}</td>
                <td>
                  <input
                    type="number"
                    value={r.hours}
                    onChange={e => setHoursOverrides(prev => ({ ...prev, [r.id]: +e.target.value }))}
                    style={{
                      width: 70, padding: '3px 6px', border: '1px solid #d5ccc0',
                      borderRadius: 4, fontSize: '0.85rem', textAlign: 'right', background: '#fffaf3',
                    }}
                    min={0} max={8760}
                  />
                </td>
                <td style={{ fontWeight: 600, color: '#27ae60' }}>{fmt(r.kwhSaved)}</td>
              </tr>
            ))}
            <tr style={{ fontWeight: 700, background: '#f5f0e8' }}>
              <td>TOTAL</td>
              <td>{fmt(totals.qty)} fixtures</td>
              <td>{totals.baseKw.toFixed(1)} kW</td>
              <td>{totals.retroKw.toFixed(1)} kW</td>
              <td>{totals.deltaKw.toFixed(1)} kW</td>
              <td>—</td>
              <td style={{ color: '#27ae60' }}>{fmt(totals.kwhSaved)} kWh</td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Summary cards */}
      <div className="info-grid" style={{ marginTop: '1rem' }}>
        <div className="info-card">
          <h3>Connected Load Reduction</h3>
          <p style={{ fontSize: '1.3rem', fontWeight: 700, color: '#2980b9' }}>{totals.deltaKw.toFixed(1)} kW</p>
          <p>{fmt(totals.qty)} fixtures × avg {((totals.deltaKw / totals.qty) * 1000).toFixed(0)}W reduction</p>
        </div>
        <div className="info-card">
          <h3>Annual Stipulated Savings</h3>
          <p style={{ fontSize: '1.3rem', fontWeight: 700, color: '#27ae60' }}>{fmt(totals.kwhSaved)} kWh/yr</p>
          <p>${fmt(totals.kwhSaved * 0.105)} at $0.105/kWh</p>
        </div>
        <div className="info-card">
          <h3>Interactive Effect</h3>
          <p style={{ fontSize: '0.9rem', color: '#4a4540' }}>
            Less lighting heat → less cooling load in summer, but more heating in winter.
            This is captured by the whole-facility model, not the stipulation.
          </p>
        </div>
      </div>

      <div className="prompt-box">
        <strong>Discuss</strong>
        How does the stipulated lighting savings compare to the whole-facility model total?
        Why might they differ? What role do interactive effects play?
      </div>
    </div>
  );
}
