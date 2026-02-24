import { useState, useMemo, useEffect } from 'react';
import Plot from 'react-plotly.js';
import {
  fit5P, fit3PH, fiveParam, threeParamHeating,
  nmbe, cvrmse, rSquared,
} from '../utils/statistics';

const CREAM_BG = '#FFF8F0';

function ValidationRow({ label, value, limit, limitLabel, passTest }) {
  const passed = passTest(parseFloat(value));
  return (
    <tr>
      <td>{label}</td>
      <td>{value}%</td>
      <td>{limitLabel}</td>
      <td className={passed ? 'pass' : 'fail'}>{passed ? '✓ PASS' : '✗ FAIL'}</td>
    </tr>
  );
}

function R2Row({ value }) {
  const passed = parseFloat(value) >= 0.75;
  return (
    <tr>
      <td>R²</td>
      <td>{value}</td>
      <td>≥ 0.75</td>
      <td className={passed ? 'pass' : 'fail'}>{passed ? '✓ PASS' : '✗ FAIL'}</td>
    </tr>
  );
}

export default function ModelFitter({ baseline, onModelUpdate }) {
  const [elecModelType, setElecModelType] = useState('5P');
  const [manualCPH, setManualCPH] = useState(null);
  const [manualCPC, setManualCPC] = useState(null);
  const [useManual, setUseManual] = useState(false);
  const [hasFit, setHasFit] = useState(false);

  // Auto-fit results (computed once per model type)
  const autoFit = useMemo(() => {
    if (!baseline || baseline.length === 0) return null;
    const oat = baseline.map(d => d.avg_oat_f);
    const kwh = baseline.map(d => d.total_kwh);
    const therms = baseline.map(d => d.total_therms);

    let elecParams = null;
    if (elecModelType === '5P') {
      elecParams = fit5P(oat, kwh);
    } else {
      elecParams = fit3PH(oat, kwh);
    }

    const gasParams = fit3PH(oat, therms);

    return { elecParams, gasParams, oat, kwh, therms };
  }, [baseline, elecModelType]);

  // Initialize manual sliders from auto-fit
  useEffect(() => {
    if (autoFit?.elecParams && elecModelType === '5P') {
      if (manualCPH === null) setManualCPH(Math.round(autoFit.elecParams.cpH));
      if (manualCPC === null) setManualCPC(Math.round(autoFit.elecParams.cpC));
    }
  }, [autoFit, elecModelType]);

  // Active fit: either auto or manual override
  const activeFit = useMemo(() => {
    if (!autoFit) return null;
    const { oat, kwh, therms, gasParams } = autoFit;

    let elecParams;
    if (useManual && elecModelType === '5P' && manualCPH !== null && manualCPC !== null) {
      // Re-solve OLS with fixed change points
      const n = oat.length;
      const x1 = oat.map(t => Math.max(manualCPH - t, 0));
      const x2 = oat.map(t => Math.max(t - manualCPC, 0));

      let sx1=0, sx2=0, sx1x1=0, sx1x2=0, sx2x2=0, sy=0, sx1y=0, sx2y=0;
      for (let i = 0; i < n; i++) {
        sx1 += x1[i]; sx2 += x2[i];
        sx1x1 += x1[i]*x1[i]; sx1x2 += x1[i]*x2[i]; sx2x2 += x2[i]*x2[i];
        sy += kwh[i]; sx1y += x1[i]*kwh[i]; sx2y += x2[i]*kwh[i];
      }
      const A = [[n,sx1,sx2],[sx1,sx1x1,sx1x2],[sx2,sx1x2,sx2x2]];
      const b = [sy, sx1y, sx2y];
      const det = A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1]) - A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0]) + A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0]);
      if (Math.abs(det) > 1e-10) {
        const B = (b[0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1]) - A[0][1]*(b[1]*A[2][2]-A[1][2]*b[2]) + A[0][2]*(b[1]*A[2][1]-A[1][1]*b[2])) / det;
        const betaH = (A[0][0]*(b[1]*A[2][2]-A[1][2]*b[2]) - b[0]*(A[1][0]*A[2][2]-A[1][2]*A[2][0]) + A[0][2]*(A[1][0]*b[2]-b[1]*A[2][0])) / det;
        const betaC = (A[0][0]*(A[1][1]*b[2]-b[1]*A[2][1]) - A[0][1]*(A[1][0]*b[2]-b[1]*A[2][0]) + b[0]*(A[1][0]*A[2][1]-A[1][1]*A[2][0])) / det;
        elecParams = { B, betaH: Math.max(betaH, 0), cpH: manualCPH, betaC: Math.max(betaC, 0), cpC: manualCPC };
      } else {
        elecParams = autoFit.elecParams;
      }
    } else {
      elecParams = autoFit.elecParams;
    }

    // Compute predictions and stats
    let elecPred = [], elecStats = null;
    if (elecParams) {
      elecPred = elecModelType === '5P'
        ? fiveParam(oat, elecParams)
        : threeParamHeating(oat, elecParams);
      elecStats = {
        NMBE: nmbe(kwh, elecPred).toFixed(2),
        CVRMSE: cvrmse(kwh, elecPred).toFixed(2),
        R2: rSquared(kwh, elecPred).toFixed(4),
      };
    }

    let gasPred = [], gasStats = null;
    if (gasParams) {
      gasPred = threeParamHeating(oat, gasParams);
      gasStats = {
        NMBE: nmbe(therms, gasPred).toFixed(2),
        CVRMSE: cvrmse(therms, gasPred).toFixed(2),
        R2: rSquared(therms, gasPred).toFixed(4),
      };
    }

    return {
      elecParams, gasParams, elecPred, gasPred, elecStats, gasStats,
      oat, kwh, therms, elecModelType,
    };
  }, [autoFit, useManual, manualCPH, manualCPC, elecModelType]);

  const handleFit = () => {
    setHasFit(true);
    if (activeFit && onModelUpdate) {
      onModelUpdate({
        elecParams: activeFit.elecParams,
        gasParams: activeFit.gasParams,
        elecModelType,
      });
    }
  };

  const handleReset = () => {
    setUseManual(false);
    if (autoFit?.elecParams && elecModelType === '5P') {
      setManualCPH(Math.round(autoFit.elecParams.cpH));
      setManualCPC(Math.round(autoFit.elecParams.cpC));
    }
  };

  // Residual plots
  const residualTraces = useMemo(() => {
    if (!hasFit || !activeFit?.elecPred?.length) return null;
    const { oat, kwh, elecPred } = activeFit;
    const residuals = kwh.map((y, i) => y - elecPred[i]);
    return { oat, elecPred, residuals };
  }, [hasFit, activeFit]);

  const plotLayout = {
    paper_bgcolor: CREAM_BG,
    plot_bgcolor: 'white',
    font: { family: 'Segoe UI, sans-serif' },
    margin: { t: 40, r: 30, b: 50, l: 60 },
    height: 280,
  };

  return (
    <div className="model-fitter">
      <div className="controls">
        <label>
          Electric model type:
          <select value={elecModelType} onChange={(e) => {
            setElecModelType(e.target.value);
            setHasFit(false);
            setUseManual(false);
            setManualCPH(null);
            setManualCPC(null);
          }}>
            <option value="5P">5-Parameter (two change points)</option>
            <option value="4P">4-Parameter (cooling only)</option>
            <option value="3PH">3-Parameter (heating only)</option>
          </select>
        </label>
        <button onClick={handleFit}>Fit Model</button>
      </div>

      {hasFit && elecModelType === '5P' && (
        <div className="slider-group">
          <label>
            <input type="checkbox" checked={useManual} onChange={e => setUseManual(e.target.checked)} />
            Override change points
          </label>
          {useManual && (
            <>
              <label>
                Heating CP:
                <input type="range" min={30} max={60} step={1}
                  value={manualCPH ?? 35} onChange={e => setManualCPH(+e.target.value)} />
                <span className="slider-value">{manualCPH}°F</span>
              </label>
              <label>
                Cooling CP:
                <input type="range" min={55} max={80} step={1}
                  value={manualCPC ?? 71} onChange={e => setManualCPC(+e.target.value)} />
                <span className="slider-value">{manualCPC}°F</span>
              </label>
              <button className="btn-secondary" onClick={handleReset}>Reset to auto</button>
            </>
          )}
        </div>
      )}

      {hasFit && activeFit?.elecStats && (
        <div className="stats-panel">
          <h4>Electric Model — {elecModelType}{useManual ? ' (manual change points)' : ''}</h4>
          <table className="stats-table">
            <thead><tr><th>Statistic</th><th>Value</th><th>ASHRAE G14 Limit</th><th>Result</th></tr></thead>
            <tbody>
              <ValidationRow label="NMBE" value={activeFit.elecStats.NMBE}
                limitLabel="±5% (monthly)" passTest={v => Math.abs(v) <= 5} />
              <ValidationRow label="CV(RMSE)" value={activeFit.elecStats.CVRMSE}
                limitLabel="≤ 15% (monthly)" passTest={v => v <= 15} />
              <R2Row value={activeFit.elecStats.R2} />
            </tbody>
          </table>
          {activeFit.elecParams && (
            <div className="params">
              {elecModelType === '5P'
                ? `B = ${activeFit.elecParams.B.toFixed(0)} kWh | βh = ${activeFit.elecParams.betaH.toFixed(0)} | CPh = ${activeFit.elecParams.cpH.toFixed(1)}°F | βc = ${activeFit.elecParams.betaC.toFixed(0)} | CPc = ${activeFit.elecParams.cpC.toFixed(1)}°F`
                : `B = ${activeFit.elecParams.B.toFixed(0)} kWh | βh = ${activeFit.elecParams.betaH.toFixed(0)} | CP = ${activeFit.elecParams.cp.toFixed(1)}°F`
              }
            </div>
          )}
        </div>
      )}

      {hasFit && activeFit?.gasStats && (
        <div className="stats-panel">
          <h4>Gas Model — 3P Heating</h4>
          <table className="stats-table">
            <thead><tr><th>Statistic</th><th>Value</th><th>ASHRAE G14 Limit</th><th>Result</th></tr></thead>
            <tbody>
              <ValidationRow label="NMBE" value={activeFit.gasStats.NMBE}
                limitLabel="±5% (monthly)" passTest={v => Math.abs(v) <= 5} />
              <ValidationRow label="CV(RMSE)" value={activeFit.gasStats.CVRMSE}
                limitLabel="≤ 15% (monthly)" passTest={v => v <= 15} />
              <R2Row value={activeFit.gasStats.R2} />
            </tbody>
          </table>
          {activeFit.gasParams && (
            <div className="params">
              B = {activeFit.gasParams.B.toFixed(0)} therms | βh = {activeFit.gasParams.betaH.toFixed(1)} | CP = {activeFit.gasParams.cp.toFixed(1)}°F
            </div>
          )}
        </div>
      )}

      {hasFit && activeFit?.gasStats && parseFloat(activeFit.gasStats.CVRMSE) > 15 && (
        <div className="prompt-box">
          <strong>Discussion</strong>
          The gas model fails the CV(RMSE) criterion. Does that mean it's unusable?
          What could explain the higher scatter in gas data? What would you do?
        </div>
      )}

      {residualTraces && (
        <>
          <h4 style={{ marginTop: '1.5rem', color: '#1a365d' }}>Residual Diagnostics — Electric</h4>
          <div className="residual-row">
            <Plot
              data={[{
                x: residualTraces.elecPred,
                y: residualTraces.residuals,
                mode: 'markers',
                marker: { size: 12, color: '#2980b9' },
                name: 'Residuals',
              }, {
                x: [Math.min(...residualTraces.elecPred), Math.max(...residualTraces.elecPred)],
                y: [0, 0],
                mode: 'lines',
                line: { color: '#999', dash: 'dash' },
                showlegend: false,
              }]}
              layout={{ ...plotLayout, title: 'Residuals vs. Fitted',
                xaxis: { title: 'Fitted Value (kWh)' }, yaxis: { title: 'Residual (kWh)' } }}
              useResizeHandler style={{ width: '100%' }}
            />
            <Plot
              data={[{
                x: residualTraces.oat,
                y: residualTraces.residuals,
                mode: 'markers',
                marker: { size: 12, color: '#e67e22' },
                name: 'Residuals',
              }, {
                x: [Math.min(...residualTraces.oat), Math.max(...residualTraces.oat)],
                y: [0, 0],
                mode: 'lines',
                line: { color: '#999', dash: 'dash' },
                showlegend: false,
              }]}
              layout={{ ...plotLayout, title: 'Residuals vs. OAT',
                xaxis: { title: 'Outdoor Air Temperature (°F)' }, yaxis: { title: 'Residual (kWh)' } }}
              useResizeHandler style={{ width: '100%' }}
            />
          </div>
          <div className="prompt-box">
            <strong>Check</strong>
            Do the residuals show any patterns? Random scatter is good.
            A pattern suggests the model is missing something systematic.
          </div>
        </>
      )}
    </div>
  );
}
