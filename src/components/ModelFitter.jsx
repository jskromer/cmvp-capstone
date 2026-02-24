import { useState, useMemo } from 'react';
import {
  fit5P,
  fit3PH,
  fiveParam,
  threeParamHeating,
  nmbe,
  cvrmse,
  rSquared,
  fractionalSavingsUncertainty,
} from '../utils/statistics';

export default function ModelFitter({ baseline, onFitComplete }) {
  const [modelType, setModelType] = useState('5P');

  const fitResult = useMemo(() => {
    if (!baseline || baseline.length === 0) return null;

    const oat = baseline.map((d) => d.avg_oat_f);
    const kwh = baseline.map((d) => d.total_kwh);
    const therms = baseline.map((d) => d.total_therms);

    let elecParams = null;
    let gasParams = null;
    let elecPred = [];
    let gasPred = [];

    if (modelType === '5P') {
      elecParams = fit5P(oat, kwh);
      if (elecParams) elecPred = fiveParam(oat, elecParams);
    }

    gasParams = fit3PH(oat, therms);
    if (gasParams) gasPred = threeParamHeating(oat, gasParams);

    const elecStats = elecParams
      ? {
          NMBE: nmbe(kwh, elecPred).toFixed(2),
          'CV(RMSE)': cvrmse(kwh, elecPred).toFixed(2),
          'R²': rSquared(kwh, elecPred).toFixed(4),
        }
      : null;

    const gasStats = gasParams
      ? {
          NMBE: nmbe(therms, gasPred).toFixed(2),
          'CV(RMSE)': cvrmse(therms, gasPred).toFixed(2),
          'R²': rSquared(therms, gasPred).toFixed(4),
        }
      : null;

    return { elecParams, gasParams, elecStats, gasStats, modelType };
  }, [baseline, modelType]);

  const handleFit = () => {
    if (fitResult && onFitComplete) {
      onFitComplete(fitResult);
    }
  };

  return (
    <div className="model-fitter">
      <h3>Change-Point Model Fitting</h3>
      <div className="controls">
        <label>
          Electric Model:
          <select value={modelType} onChange={(e) => setModelType(e.target.value)}>
            <option value="5P">5-Parameter (heating + cooling)</option>
            <option value="3PH">3-Parameter (heating only)</option>
          </select>
        </label>
        <button onClick={handleFit}>Fit Model</button>
      </div>

      {fitResult?.elecStats && (
        <div className="stats-panel">
          <h4>Electric Model — {modelType}</h4>
          <table className="stats-table">
            <thead>
              <tr>
                <th>Statistic</th>
                <th>Value</th>
                <th>ASHRAE Guideline 14 Limit</th>
                <th>Pass?</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>NMBE</td>
                <td>{fitResult.elecStats.NMBE}%</td>
                <td>±5% (monthly)</td>
                <td>{Math.abs(parseFloat(fitResult.elecStats.NMBE)) <= 5 ? 'PASS' : 'FAIL'}</td>
              </tr>
              <tr>
                <td>CV(RMSE)</td>
                <td>{fitResult.elecStats['CV(RMSE)']}%</td>
                <td>15% (monthly)</td>
                <td>{parseFloat(fitResult.elecStats['CV(RMSE)']) <= 15 ? 'PASS' : 'FAIL'}</td>
              </tr>
              <tr>
                <td>R²</td>
                <td>{fitResult.elecStats['R²']}</td>
                <td>≥0.75</td>
                <td>{parseFloat(fitResult.elecStats['R²']) >= 0.75 ? 'PASS' : 'FAIL'}</td>
              </tr>
            </tbody>
          </table>
          {fitResult.elecParams && (
            <div className="params">
              <strong>Parameters: </strong>
              {modelType === '5P'
                ? `B=${fitResult.elecParams.B.toFixed(0)}, βh=${fitResult.elecParams.betaH.toFixed(0)}, CPh=${fitResult.elecParams.cpH.toFixed(1)}°F, βc=${fitResult.elecParams.betaC.toFixed(0)}, CPc=${fitResult.elecParams.cpC.toFixed(1)}°F`
                : `B=${fitResult.elecParams.B.toFixed(0)}, βh=${fitResult.elecParams.betaH.toFixed(0)}, CP=${fitResult.elecParams.cp.toFixed(1)}°F`}
            </div>
          )}
        </div>
      )}

      {fitResult?.gasStats && (
        <div className="stats-panel">
          <h4>Gas Model — 3P Heating</h4>
          <table className="stats-table">
            <thead>
              <tr>
                <th>Statistic</th>
                <th>Value</th>
                <th>ASHRAE Guideline 14 Limit</th>
                <th>Pass?</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>NMBE</td>
                <td>{fitResult.gasStats.NMBE}%</td>
                <td>±5%</td>
                <td>{Math.abs(parseFloat(fitResult.gasStats.NMBE)) <= 5 ? 'PASS' : 'FAIL'}</td>
              </tr>
              <tr>
                <td>CV(RMSE)</td>
                <td>{fitResult.gasStats['CV(RMSE)']}%</td>
                <td>15%</td>
                <td>{parseFloat(fitResult.gasStats['CV(RMSE)']) <= 15 ? 'PASS' : 'FAIL'}</td>
              </tr>
              <tr>
                <td>R²</td>
                <td>{fitResult.gasStats['R²']}</td>
                <td>≥0.75</td>
                <td>{parseFloat(fitResult.gasStats['R²']) >= 0.75 ? 'PASS' : 'FAIL'}</td>
              </tr>
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
