import { useState, useEffect, useCallback } from 'react';
import { ScenarioProvider } from './scenarios/ScenarioContext';
import { useScenario } from './scenarios/useScenario';
import { loadScenarioData } from './utils/dataLoader';
import ScenarioSelector from './components/ScenarioSelector';
import GreenfieldOverview from './components/GreenfieldOverview';
import ScatterPlot from './components/ScatterPlot';
import TimeSeriesPlot from './components/TimeSeriesPlot';
import ModelFitter from './components/ModelFitter';
import SummaryTable from './components/SummaryTable';
import SavingsCalculator from './components/SavingsCalculator';
import LightingStipulation from './components/LightingStipulation';
import FanAnalysis from './components/FanAnalysis';
import SloOverview from './components/SloOverview';
import CalibrationView from './components/CalibrationView';
import SensitivityAnalysis from './components/SensitivityAnalysis';
import ForwardModelSavings from './components/ForwardModelSavings';
import CompetentCounterfactual from './components/CompetentCounterfactual';
import MnvScorePanel from './components/MnvScorePanel';
import './App.css';

function AppContent() {
  const { scenario } = useScenario();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [modelResult, setModelResult] = useState(null);
  const [showAnswerKey, setShowAnswerKey] = useState(false);
  const [dataScenarioId, setDataScenarioId] = useState(null);

  // Load data when scenario changes
  if (scenario.id !== dataScenarioId) {
    setDataScenarioId(scenario.id);
    setData(null);
    setLoading(true);
    // Reset tab if current tab doesn't exist in new scenario
    if (!scenario.tabs.some(t => t.id === activeTab)) {
      setActiveTab('overview');
    }
  }

  useEffect(() => {
    let cancelled = false;
    loadScenarioData(scenario)
      .then((d) => { if (!cancelled) { setData(d); setLoading(false); } })
      .catch(() => { if (!cancelled) { setData(null); setLoading(false); } });
    return () => { cancelled = true; };
  }, [scenario]);

  const handleModelUpdate = useCallback((result) => {
    setModelResult(result);
  }, []);

  if (loading) {
    return <div className="loading">Loading {scenario.name} data…</div>;
  }

  if (!data) {
    return <div className="error">Failed to load data for {scenario.name}.</div>;
  }

  const isGreenfield = scenario.id === 'greenfield';
  const isSlo = scenario.id === 'slo';

  return (
    <div className="app">
      <header>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
          <h1 style={{ margin: 0 }}>{scenario.name}</h1>
          <ScenarioSelector />
        </div>
        <p className="subtitle">{scenario.subtitle}</p>
      </header>

      <nav className="tabs">
        {scenario.tabs.map((tab) => (
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
        {/* === GREENFIELD TABS === */}
        {isGreenfield && activeTab === 'overview' && (
          <GreenfieldOverview
            data={data}
            showAnswerKey={showAnswerKey}
            setShowAnswerKey={setShowAnswerKey}
          />
        )}

        {isGreenfield && activeTab === 'scatter' && (
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

        {isGreenfield && activeTab === 'model' && (
          <section>
            <h2>Baseline Model Fitting</h2>
            <p>Select a model type, fit it to the baseline data, and evaluate against ASHRAE Guideline 14 criteria.</p>
            <ModelFitter baseline={data.baseline} onModelUpdate={handleModelUpdate} />
          </section>
        )}

        {activeTab === 'lighting' && (
          <section>
            <h2>{isSlo ? 'ECM-1: Lighting Stipulation' : 'ECM-1: Lighting Stipulation'}</h2>
            <p>Calculate stipulated savings for the LED retrofit{isSlo ? ' across all 5 floors' : ' in Wings A and B'}.</p>
            <LightingStipulation
              fixtureData={scenario.fixtureData}
              electricRate={scenario.electricRate}
            />
          </section>
        )}

        {isGreenfield && activeTab === 'vfd' && (
          <section>
            <h2>ECM-4: VFD Fan Analysis</h2>
            <p>Analyze pre- and post-retrofit fan performance data for each AHU.</p>
            <FanAnalysis />
          </section>
        )}

        {isGreenfield && activeTab === 'timeseries' && (
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

        {isGreenfield && activeTab === 'savings' && (
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
              onNavigate={setActiveTab}
            />
          </section>
        )}

        {/* === SLO TABS === */}
        {isSlo && activeTab === 'overview' && (
          <SloOverview data={data} scenario={scenario} />
        )}

        {isSlo && activeTab === 'scatter' && (
          <section>
            <h2>Energy Signature — Monthly Consumption vs. Temperature</h2>
            <div className="prompt-box">
              <strong>Observe</strong>
              San Luis Obispo is in California Climate Zone 3C — a mild, cooling-dominated marine climate.
              How does this energy signature differ from a heating-dominated building?
            </div>
            <ScatterPlot
              data={data.baseline}
              fuelType="electric"
            />
            <ScatterPlot
              data={data.baseline}
              fuelType="gas"
            />
            <div className="prompt-box">
              <strong>Discuss</strong>
              The electric profile shows a clear cooling response. What about gas?
              Why is gas consumption so much lower than at a mid-Atlantic site?
            </div>
          </section>
        )}

        {isSlo && activeTab === 'calibration' && (
          <CalibrationView data={data} />
        )}

        {isSlo && activeTab === 'sensitivity' && (
          <SensitivityAnalysis data={data} />
        )}

        {isSlo && activeTab === 'ecm-savings' && (
          <ForwardModelSavings data={data} />
        )}

        {isSlo && activeTab === 'counterfactual' && (
          <CompetentCounterfactual data={data} />
        )}

        {isSlo && activeTab === 'mnvscore' && (
          <MnvScorePanel scenario={scenario} />
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
        <p>CMVP Capstone — {isGreenfield ? 'EnergyPlus 25.1.0 Simulation · Mid-Atlantic CZ 4A' : 'Calibrated EnergyPlus Forward Model · California CZ 3C'}</p>
      </footer>
    </div>
  );
}

function App() {
  return (
    <ScenarioProvider>
      <AppContent />
    </ScenarioProvider>
  );
}

export default App;
