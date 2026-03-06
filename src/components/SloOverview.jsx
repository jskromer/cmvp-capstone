import SloGraphic from './SloGraphic';
import SummaryTable from './SummaryTable';

export default function SloOverview({ data, scenario }) {
  return (
    <section>
      <SloGraphic />

      <h2>The Building</h2>
      <div className="info-grid">
        <div className="info-card" style={{ borderLeft: '4px solid #2980b9' }}>
          <h3>Building Profile</h3>
          <p>90,000 sq ft · 5 stories · 1980s construction</p>
          <p>DOE Large Office prototype (VAV with reheat)</p>
          <p>San Luis Obispo, CA — Climate Zone 3C</p>
          <p>Marine climate: mild winters, warm dry summers</p>
        </div>
        <div className="info-card" style={{ borderLeft: '4px solid #8e44ad' }}>
          <h3>HVAC System</h3>
          <p>Variable Air Volume (VAV) with hot water reheat</p>
          <p>Centrifugal chiller (COP 3.2, 15 years old)</p>
          <p>Gas-fired boiler for reheat coils</p>
          <p>15 thermal zones across 5 floors</p>
        </div>
        <div className="info-card" style={{ borderLeft: '4px solid #e67e22' }}>
          <h3>Utility Rates (California)</h3>
          <p>Electric: $0.170/kWh (PG&amp;E commercial)</p>
          <p>Demand: $18.00/kW-month</p>
          <p>Gas: $1.20/therm</p>
          <p>Emissions: 0.53 lb CO₂/kWh (CAMX grid)</p>
        </div>
        <div className="info-card" style={{ borderLeft: '4px solid #e74c3c' }}>
          <h3>M&amp;V Approach</h3>
          <p>Calibrated simulation / forward model (cf. Option D)</p>
          <p>EnergyPlus 25.1.0 baseline model</p>
          <p>Calibrated to monthly utility data</p>
          <p>Sensitivity analysis for uncertainty</p>
        </div>
      </div>

      <h2>Proposed Retrofit Package</h2>
      <div className="info-grid">
        <div className="info-card">
          <h3>
            <span className="ecm-tag" style={{ background: '#fef3cd', color: '#856404' }}>ECM-1</span>
            LED Lighting Retrofit
          </h3>
          <p>T8 fluorescent → LED panels, all 5 floors</p>
          <p>LPD reduction: 10.8 → 7.0 W/m² (−35%)</p>
          <p style={{ fontSize: '0.8rem', color: '#8c8478', fontStyle: 'italic' }}>
            Retrofit isolation: key parameter measurement (cf. Option A)
          </p>
        </div>
        <div className="info-card">
          <h3>
            <span className="ecm-tag" style={{ background: '#d1ecf1', color: '#0c5460' }}>ECM-2</span>
            Chiller Replacement
          </h3>
          <p>Replace aging centrifugal chiller</p>
          <p>COP improvement: 3.2 → 4.0 (+25%)</p>
          <p style={{ fontSize: '0.8rem', color: '#8c8478', fontStyle: 'italic' }}>
            Whole facility: calibrated simulation / forward model (cf. Option D)
          </p>
        </div>
        <div className="info-card">
          <h3>
            <span className="ecm-tag" style={{ background: '#d4edda', color: '#155724' }}>ECM-3</span>
            VAV Box Optimization
          </h3>
          <p>Optimize minimum flow setpoints and schedules</p>
          <p>Equivalent to ~15% fan efficiency improvement</p>
          <p style={{ fontSize: '0.8rem', color: '#8c8478', fontStyle: 'italic' }}>
            Whole facility: calibrated simulation / forward model (cf. Option D)
          </p>
        </div>
      </div>

      <h2>Forward Model Context</h2>
      <div className="prompt-box">
        <strong>Key Distinction</strong>
        Unlike the Greenfield scenario (inverse/statistical model from meter data), this building uses a
        <strong> calibrated simulation (forward model)</strong>. The direction of inference is reversed:
        physical parameters → predicted energy, not observed data → inferred relationships.
        The model must be calibrated to metered data before it can be trusted for savings estimation.
      </div>

      <div style={{
        background: '#fff3cd', border: '1px solid #ffc107', borderRadius: 8,
        padding: '12px 16px', margin: '16px 0', fontSize: '0.9rem'
      }}>
        <strong style={{ color: '#856404' }}>Gas Model Limitation:</strong>{' '}
        The DOE prototype model uses electric reheat coils internally, though the actual building has gas-fired
        reheat. Gas calibration was not performed — the utility gas data is real, but gas savings cannot be
        reliably estimated from this model. Students must disclose this limitation.
      </div>

      <h2>Annual Energy Summary</h2>
      <SummaryTable
        baseline={data.baseline}
        sqft={scenario.sqft}
      />
    </section>
  );
}
