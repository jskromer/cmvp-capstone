import BuildingGraphic from './BuildingGraphic';
import SummaryTable from './SummaryTable';

export default function GreenfieldOverview({ data, showAnswerKey, setShowAnswerKey }) {
  return (
    <section>
      <BuildingGraphic />

      <h2>The Building</h2>
      <div className="info-grid">
        <div className="info-card wing-a">
          <h3>Wing A — Office</h3>
          <p>35,000 sq ft · 2 floors</p>
          <p>Open-plan + private offices</p>
          <p>AHU-1: Gas furnace, DX cooling, 15 HP fan</p>
          <p>M–F 7am–6pm</p>
        </div>
        <div className="info-card wing-b">
          <h3>Wing B — Library</h3>
          <p>15,000 sq ft · 2 floors</p>
          <p>Reading rooms, stacks, meeting rooms</p>
          <p>AHU-2: Heat pump, DX cooling, 10 HP fan</p>
          <p>M–Sat 8am–9pm, Sun 12–5pm</p>
        </div>
        <div className="info-card wing-c">
          <h3>Wing C — Data Center</h3>
          <p>2,000 sq ft</p>
          <p>IT infrastructure, 24/7 operation</p>
          <p>CRAC-1: 5-ton DX</p>
        </div>
        <div className="info-card wing-cm">
          <h3>Common Areas</h3>
          <p>10,000 sq ft</p>
          <p>Lobby, corridors, mechanical</p>
          <p>AHU-3: Gas furnace, DX cooling, 5 HP fan</p>
          <p>M–F 6am–10pm</p>
        </div>
      </div>

      <h2>Retrofit Package (ESPC)</h2>
      <div className="info-grid">
        <div className="info-card">
          <h3>
            <span className="ecm-tag" style={{ background: '#fef3cd', color: '#856404' }}>ECM-1</span>
            LED Lighting + Controls
          </h3>
          <p>T8 fluorescent → LED in Wings A &amp; B</p>
          <p>Occupancy and daylight controls</p>
          <p style={{ fontSize: '0.8rem', color: '#8c8478', fontStyle: 'italic' }}>
            Key parameter measurement (cf. Option A)
          </p>
        </div>
        <div className="info-card">
          <h3>
            <span className="ecm-tag" style={{ background: '#d1ecf1', color: '#0c5460' }}>ECM-2</span>
            Chiller/DX Replacement
          </h3>
          <p>Higher COP units across all wings</p>
          <p style={{ fontSize: '0.8rem', color: '#8c8478', fontStyle: 'italic' }}>
            Captured by whole-facility model
          </p>
        </div>
        <div className="info-card">
          <h3>
            <span className="ecm-tag" style={{ background: '#f8d7da', color: '#721c24' }}>ECM-3</span>
            Roof Insulation
          </h3>
          <p>R-15 → R-30 entire building envelope</p>
          <p style={{ fontSize: '0.8rem', color: '#8c8478', fontStyle: 'italic' }}>
            Whole facility — affects both fuels
          </p>
        </div>
        <div className="info-card">
          <h3>
            <span className="ecm-tag" style={{ background: '#d4edda', color: '#155724' }}>ECM-4</span>
            VFDs on AHU Fans
          </h3>
          <p>Variable frequency drives on AHU-1, 2, 3</p>
          <p style={{ fontSize: '0.8rem', color: '#8c8478', fontStyle: 'italic' }}>
            Continuous performance verification (cf. Option B)
          </p>
        </div>
      </div>

      <h2>Contract Context</h2>
      <p>
        15-year Energy Savings Performance Contract. Annual M&amp;V reporting required.
        Savings shortfall risk borne by ESCO; surplus shared 80/20 (owner/ESCO).
      </p>

      <div style={{
        background: '#f5f0e8', border: '1px solid #e0d8cc', borderRadius: 8,
        padding: '12px 16px', margin: '16px 0', fontSize: '0.9rem'
      }}>
        <strong style={{ color: '#b5632e' }}>Prerequisites:</strong>{' '}
        This capstone builds on concepts from the{' '}
        <a href="https://cfdesigns.vercel.app/#/fundamentals" target="_blank" rel="noopener noreferrer"
          style={{ color: '#2980b9', fontWeight: 500 }}>
          Statistical Foundations
        </a>{' '}and{' '}
        <a href="https://cfdesigns.vercel.app/#/workbench" target="_blank" rel="noopener noreferrer"
          style={{ color: '#2980b9', fontWeight: 500 }}>
          Workbench
        </a>{' '}modules.
      </div>

      <h2>Baseline Year Summary</h2>
      <SummaryTable
        baseline={data.baseline}
        reporting={data.reporting}
        noNRA={showAnswerKey ? data.noNRA : null}
        showAnswerKey={showAnswerKey}
        sqft={62000}
      />
      <div className="instructor-toggle">
        <label>
          <input
            type="checkbox"
            checked={showAnswerKey}
            onChange={(e) => setShowAnswerKey(e.target.checked)}
          />
          Instructor: show answer key data
        </label>
      </div>
    </section>
  );
}
