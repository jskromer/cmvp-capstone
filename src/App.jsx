import { useState, useEffect, useCallback } from 'react';
import { loadAllMonthly } from './utils/dataLoader';
import ScatterPlot from './components/ScatterPlot';
import TimeSeriesPlot from './components/TimeSeriesPlot';
import ModelFitter from './components/ModelFitter';
import SummaryTable from './components/SummaryTable';
import './App.css';

const TABS = [
  { id: 'overview', label: 'Overview' },
  { id: 'scatter', label: 'Scatter Plots' },
  { id: 'model', label: 'Model Fitting' },
  { id: 'timeseries', label: 'Time Series' },
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
                <h3>ECM-1: LED Lighting + Controls</h3>
                <p>T8 fluorescent → LED in Wings A &amp; B</p>
                <p>Occupancy and daylight controls</p>
              </div>
              <div className="info-card">
                <h3>ECM-2: Chiller/DX Replacement</h3>
                <p>Higher COP units across all wings</p>
              </div>
              <div className="info-card">
                <h3>ECM-3: Roof Insulation</h3>
                <p>R-15 → R-30 entire building envelope</p>
              </div>
              <div className="info-card">
                <h3>ECM-4: VFDs on AHU Fans</h3>
                <p>Variable frequency drives on AHU-1, 2, 3</p>
              </div>
            </div>

            <h2>Contract Context</h2>
            <p>15-year Energy Savings Performance Contract. Annual M&amp;V reporting required. Savings shortfall risk borne by ESCO; surplus shared 80/20 (owner/ESCO).</p>

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
      </main>

      <footer>
        <p>CMVP Capstone — EnergyPlus 25.1.0 Simulation · Mid-Atlantic CZ 4A</p>
      </footer>
    </div>
  );
}

export default App;
