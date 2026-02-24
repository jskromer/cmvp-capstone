import { useState, useEffect, useCallback } from 'react';
import { loadAllMonthly } from './utils/dataLoader';
import BuildingGraphic from './components/BuildingGraphic';
import ScatterPlot from './components/ScatterPlot';
import TimeSeriesPlot from './components/TimeSeriesPlot';
import ModelFitter from './components/ModelFitter';
import SummaryTable from './components/SummaryTable';
import SavingsCalculator from './components/SavingsCalculator';
import LightingStipulation from './components/LightingStipulation';
import FanAnalysis from './components/FanAnalysis';
import './App.css';

const TABS = [
  { id: 'overview', label: 'Overview', phase: 1 },
  { id: 'scatter', label: 'Scatter Plots', phase: 2 },
  { id: 'model', label: 'Model Fitting', phase: 2 },
  { id: 'lighting', label: 'Lighting Stipulation', phase: 2 },
  { id: 'vfd', label: 'VFD Analysis', phase: 2 },
  { id: 'timeseries', label: 'Time Series', phase: 3 },
  { id: 'savings', label: 'Savings Calculator', phase: 3 },
];

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [modelResult, setModelResult] = useState(null);
  const [showAnswerKey, setShowAnswerKey] = useState(false);

  useEffect(() => {
    loadAllMonthly()
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  const handleModelUpdate = useCallback((result) => {
    setModelResult(result);
  }, []);

  if (loading) {
    return <div className="loading">Loading Greenfield Municipal Center data…</div>;
  }

  if (!data) {
    return <div className="error">Failed to load data. Check that CSV files are in public/data/.</div>;
  }

  return (
    <div className="app">
      <header>
        <h1>Greenfield Municipal Center</h1>
        <p className="subtitle">CMVP Capstone — M&amp;V Workbench</p>
      </header>

      <nav className="tabs">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            className={activeTab === tab.id ? 'active' : ''}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      <main>
        {activeTab === 'overview' && (
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
        )}

        {activeTab === 'scatter' && (
          <section>
            <h2>Baseline Energy vs. Outdoor Air Temperature</h2>
            <div className="prompt-box">
              <strong>Observe</strong>
              What patterns do you see? How does energy use respond to temperature?
              How many distinct operating regimes can you identify?
            </div>
            <ScatterPlot
              data={data.baseline}
              fuelType="electric"
              modelParams={modelResult?.elecParams}
              modelType={modelResult?.elecModelType}
            />
            <ScatterPlot
              data={data.baseline}
              fuelType="gas"
              modelParams={modelResult?.gasParams}
              modelType="3PH"
            />
            <div className="prompt-box">
              <strong>Discuss</strong>
              Why does gas consumption have a different shape than electric?
              What building systems drive each pattern?
            </div>
          </section>
        )}

        {activeTab === 'model' && (
          <section>
            <h2>Baseline Model Fitting</h2>
            <p>Select a model type, fit it to the baseline data, and evaluate against ASHRAE Guideline 14 criteria.</p>
            <ModelFitter baseline={data.baseline} onModelUpdate={handleModelUpdate} />
          </section>
        )}

        {activeTab === 'lighting' && (
          <section>
            <h2>ECM-1: Lighting Stipulation</h2>
            <p>Calculate stipulated savings for the LED retrofit in Wings A and B.</p>
            <LightingStipulation />
          </section>
        )}

        {activeTab === 'vfd' && (
          <section>
            <h2>ECM-4: VFD Fan Analysis</h2>
            <p>Analyze pre- and post-retrofit fan performance data for each AHU.</p>
            <FanAnalysis />
          </section>
        )}

        {activeTab === 'timeseries' && (
          <section>
            <h2>Baseline vs. Reporting Period</h2>
            <div className="prompt-box">
              <strong>Observe</strong>
              Compare the baseline and reporting period traces month by month.
              Is the pattern what you expected? Are there any surprises?
            </div>
            <TimeSeriesPlot
              baseline={data.baseline}
              reporting={data.reporting}
              noNRA={showAnswerKey ? data.noNRA : null}
              elecParams={modelResult?.elecParams}
              gasParams={modelResult?.gasParams}
              elecModelType={modelResult?.elecModelType}
            />
            <div className="instructor-toggle">
              <label>
                <input
                  type="checkbox"
                  checked={showAnswerKey}
                  onChange={(e) => setShowAnswerKey(e.target.checked)}
                />
                Instructor: show answer key trace
              </label>
            </div>
          </section>
        )}

        {activeTab === 'savings' && (
          <section>
            <h2>Savings Calculation &amp; Reporting</h2>
            <p>Calculate avoided energy use, apply non-routine adjustments, and report savings with uncertainty.</p>
            <SavingsCalculator
              baseline={data.baseline}
              reporting={data.reporting}
              noNRA={data.noNRA}
              elecParams={modelResult?.elecParams}
              gasParams={modelResult?.gasParams}
              elecModelType={modelResult?.elecModelType}
            />
          </section>
        )}
      </main>

      <footer>
        <div style={{ display: 'flex', justifyContent: 'center', gap: 24, flexWrap: 'wrap', marginBottom: 16 }}>
          <a href="https://cfdesigns.vercel.app" target="_blank" rel="noopener noreferrer"
            style={{ fontSize: 13, color: '#b5632e', textDecoration: 'none', fontWeight: 600 }}>
            Counterfactual Designs →
          </a>
          <a href="https://mv-classmap.vercel.app" target="_blank" rel="noopener noreferrer"
            style={{ fontSize: 13, color: '#2d7d46', textDecoration: 'none', fontWeight: 600 }}>
            Learning Path →
          </a>
          <a href="https://mv-course.vercel.app" target="_blank" rel="noopener noreferrer"
            style={{ fontSize: 13, color: '#a67c28', textDecoration: 'none', fontWeight: 600 }}>
            IPMVP Reference →
          </a>
          <a href="https://bayesian-mv.vercel.app" target="_blank" rel="noopener noreferrer"
            style={{ fontSize: 13, color: '#7c5cbf', textDecoration: 'none', fontWeight: 600 }}>
            Bayesian Module →
          </a>
        </div>
        <div style={{ fontSize: 12, color: '#998d7e', marginBottom: 8 }}>
          <a href="https://counterfactual-designs.com" target="_blank" rel="noopener noreferrer"
            style={{ color: '#998d7e', textDecoration: 'none' }}>
            counterfactual-designs.com
          </a>
        </div>
        <p>CMVP Capstone — EnergyPlus 25.1.0 Simulation · Mid-Atlantic CZ 4A</p>
      </footer>
    </div>
  );
}

export default App;
