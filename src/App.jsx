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
  { id: 'timeseries', label: 'Time Series' },
  { id: 'model', label: 'Model Fitting' },
];

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [elecFit, setElecFit] = useState(null);
  const [showAnswerKey, setShowAnswerKey] = useState(false);

  useEffect(() => {
    loadAllMonthly()
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  const handleFitComplete = useCallback((result) => {
    setElecFit(result);
  }, []);

  if (loading) {
    return <div className="loading">Loading Greenfield Municipal Center data...</div>;
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
            <h2>Project Summary</h2>
            <div className="info-grid">
              <div className="info-card">
                <h3>Building</h3>
                <p>62,000 sq ft mixed-use government facility</p>
                <p>2 stories, ~1995 construction, mid-Atlantic CZ 4A</p>
              </div>
              <div className="info-card">
                <h3>Retrofit Package</h3>
                <ul>
                  <li>ECM-1: LED lighting + controls</li>
                  <li>ECM-2: Chiller/DX replacement</li>
                  <li>ECM-3: Roof insulation (R-15 → R-30)</li>
                  <li>ECM-4: VFDs on AHU supply fans</li>
                </ul>
              </div>
              <div className="info-card">
                <h3>Key Challenge</h3>
                <p>Data center expansion (NRA) in month 8 adds ~19,000 kWh/month, masking true savings of 10.5%.</p>
              </div>
            </div>
            <h2>Annual Summary</h2>
            <SummaryTable
              baseline={data.baseline}
              reporting={showAnswerKey ? data.noNRA : data.reporting}
              noNRA={data.noNRA}
            />
            <label className="toggle">
              <input
                type="checkbox"
                checked={showAnswerKey}
                onChange={(e) => setShowAnswerKey(e.target.checked)}
              />
              Show answer key (no-NRA reporting data)
            </label>
          </section>
        )}

        {activeTab === 'scatter' && (
          <section>
            <h2>Baseline Scatter Plots</h2>
            <p>Identify the change-point model shapes. Electric should show 5-parameter (heating + cooling legs); gas should show 3-parameter heating-only.</p>
            <ScatterPlot
              data={data.baseline}
              fuelType="electric"
              modelParams={elecFit?.elecParams}
              modelType={elecFit?.modelType}
            />
            <ScatterPlot
              data={data.baseline}
              fuelType="gas"
              modelParams={elecFit?.gasParams}
              modelType="3PH"
            />
          </section>
        )}

        {activeTab === 'timeseries' && (
          <section>
            <h2>Reporting Period Time Series</h2>
            <p>Compare baseline vs reporting period. Note the NRA step change starting in August (month 8). The red shaded region highlights where data center expansion inflates consumption.</p>
            <TimeSeriesPlot
              baseline={data.baseline}
              reporting={data.reporting}
              noNRA={showAnswerKey ? data.noNRA : null}
            />
            <label className="toggle">
              <input
                type="checkbox"
                checked={showAnswerKey}
                onChange={(e) => setShowAnswerKey(e.target.checked)}
              />
              Show no-NRA trace (answer key)
            </label>
          </section>
        )}

        {activeTab === 'model' && (
          <section>
            <h2>Change-Point Model Fitting</h2>
            <p>Fit a baseline model, then check ASHRAE Guideline 14 validation criteria (NMBE ±5%, CV(RMSE) ≤15%, R² ≥0.75 for monthly data).</p>
            <ModelFitter baseline={data.baseline} onFitComplete={handleFitComplete} />
          </section>
        )}
      </main>

      <footer>
        <p>CMVP Capstone Project — Greenfield Municipal Center — EnergyPlus 25.1.0 Simulation Data</p>
      </footer>
    </div>
  );
}

export default App;
