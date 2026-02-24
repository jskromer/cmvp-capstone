/**
 * M&V statistics: NMBE, CV(RMSE), R-squared, fractional savings uncertainty.
 * Reference: ASHRAE Guideline 14-2023.
 */

export function mean(arr) {
  return arr.reduce((s, v) => s + v, 0) / arr.length;
}

export function nmbe(actual, predicted) {
  const n = actual.length;
  const yBar = mean(actual);
  const sumErr = actual.reduce((s, a, i) => s + (a - predicted[i]), 0);
  return (sumErr / ((n - 1) * yBar)) * 100;
}

export function cvrmse(actual, predicted) {
  const n = actual.length;
  const yBar = mean(actual);
  const mse = actual.reduce((s, a, i) => s + (a - predicted[i]) ** 2, 0) / (n - 2);
  return (Math.sqrt(mse) / yBar) * 100;
}

export function rSquared(actual, predicted) {
  const yBar = mean(actual);
  const ssTot = actual.reduce((s, a) => s + (a - yBar) ** 2, 0);
  const ssRes = actual.reduce((s, a, i) => s + (a - predicted[i]) ** 2, 0);
  return 1 - ssRes / ssTot;
}

/**
 * Fractional savings uncertainty at given confidence (default 90%).
 * Simplified formula from ASHRAE Guideline 14, Eq D-1.
 * FSU = t * CV(RMSE) / (F * sqrt(n))
 * where F = fractional savings, n = number of periods.
 */
export function fractionalSavingsUncertainty(
  actual,
  predicted,
  savingsFraction,
  confidence = 0.9
) {
  const n = actual.length;
  // t-value approximations for common confidence levels
  const tValues = { 0.8: 1.356, 0.9: 1.796, 0.95: 2.201, 0.99: 3.106 };
  const t = tValues[confidence] || 1.796;
  const cv = cvrmse(actual, predicted);
  if (savingsFraction === 0) return Infinity;
  return (t * (cv / 100)) / (savingsFraction * Math.sqrt(n));
}

/**
 * Five-parameter change-point model.
 * E = B + β_h * max(CP_h - T, 0) + β_c * max(T - CP_c, 0)
 */
export function fiveParam(oat, params) {
  const { B, betaH, cpH, betaC, cpC } = params;
  return oat.map(
    (t) => B + betaH * Math.max(cpH - t, 0) + betaC * Math.max(t - cpC, 0)
  );
}

/**
 * Three-parameter heating-only change-point model.
 * E = B + β_h * max(CP - T, 0)
 */
export function threeParamHeating(oat, params) {
  const { B, betaH, cp } = params;
  return oat.map((t) => B + betaH * Math.max(cp - t, 0));
}

/**
 * Brute-force grid search to fit a 5P model.
 * Returns best-fit { B, betaH, cpH, betaC, cpC }.
 */
export function fit5P(oat, energy) {
  const minT = Math.min(...oat);
  const maxT = Math.max(...oat);
  let bestSSE = Infinity;
  let bestParams = null;

  for (let cpH = minT + 2; cpH <= maxT - 5; cpH += 1) {
    for (let cpC = cpH + 3; cpC <= maxT - 1; cpC += 1) {
      // For given change points, solve for B, betaH, betaC via least squares
      // Design matrix: E = B + betaH * max(cpH - T, 0) + betaC * max(T - cpC, 0)
      const n = oat.length;
      let sx0 = 0, sx1 = 0, sx2 = 0;
      let sx0x0 = n, sx0x1 = 0, sx0x2 = 0;
      let sx1x1 = 0, sx1x2 = 0, sx2x2 = 0;
      let sy = 0, sx1y = 0, sx2y = 0;

      for (let i = 0; i < n; i++) {
        const x1 = Math.max(cpH - oat[i], 0);
        const x2 = Math.max(oat[i] - cpC, 0);
        const y = energy[i];
        sx1 += x1; sx2 += x2;
        sx1x1 += x1 * x1; sx1x2 += x1 * x2; sx2x2 += x2 * x2;
        sy += y; sx1y += x1 * y; sx2y += x2 * y;
      }

      // Solve 3x3 normal equations: [n, sx1, sx2; sx1, sx1x1, sx1x2; sx2, sx1x2, sx2x2] * [B, bH, bC]' = [sy, sx1y, sx2y]'
      const A = [
        [n, sx1, sx2],
        [sx1, sx1x1, sx1x2],
        [sx2, sx1x2, sx2x2],
      ];
      const b = [sy, sx1y, sx2y];
      const sol = solve3x3(A, b);
      if (!sol) continue;
      const [B, betaH, betaC] = sol;
      if (betaH < 0 || betaC < 0) continue;

      const pred = fiveParam(oat, { B, betaH, cpH, betaC, cpC });
      const sse = energy.reduce((s, e, i) => s + (e - pred[i]) ** 2, 0);
      if (sse < bestSSE) {
        bestSSE = sse;
        bestParams = { B, betaH, cpH, betaC, cpC };
      }
    }
  }
  return bestParams;
}

/**
 * Brute-force grid search to fit a 3P heating model.
 */
export function fit3PH(oat, energy) {
  const minT = Math.min(...oat);
  const maxT = Math.max(...oat);
  let bestSSE = Infinity;
  let bestParams = null;

  for (let cp = minT + 2; cp <= maxT - 1; cp += 0.5) {
    const n = oat.length;
    let sx1 = 0, sx1x1 = 0, sy = 0, sx1y = 0;
    for (let i = 0; i < n; i++) {
      const x1 = Math.max(cp - oat[i], 0);
      sx1 += x1; sx1x1 += x1 * x1;
      sy += energy[i]; sx1y += x1 * energy[i];
    }
    const det = n * sx1x1 - sx1 * sx1;
    if (Math.abs(det) < 1e-10) continue;
    const B = (sx1x1 * sy - sx1 * sx1y) / det;
    const betaH = (n * sx1y - sx1 * sy) / det;
    if (betaH < 0) continue;

    const pred = threeParamHeating(oat, { B, betaH, cp });
    const sse = energy.reduce((s, e, i) => s + (e - pred[i]) ** 2, 0);
    if (sse < bestSSE) {
      bestSSE = sse;
      bestParams = { B, betaH, cp };
    }
  }
  return bestParams;
}

function solve3x3(A, b) {
  // Cramer's rule for 3x3
  const det =
    A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1]) -
    A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0]) +
    A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]);
  if (Math.abs(det) < 1e-10) return null;

  const x0 =
    (b[0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1]) -
      A[0][1] * (b[1] * A[2][2] - A[1][2] * b[2]) +
      A[0][2] * (b[1] * A[2][1] - A[1][1] * b[2])) /
    det;
  const x1 =
    (A[0][0] * (b[1] * A[2][2] - A[1][2] * b[2]) -
      b[0] * (A[1][0] * A[2][2] - A[1][2] * A[2][0]) +
      A[0][2] * (A[1][0] * b[2] - b[1] * A[2][0])) /
    det;
  const x2 =
    (A[0][0] * (A[1][1] * b[2] - b[1] * A[2][1]) -
      A[0][1] * (A[1][0] * b[2] - b[1] * A[2][0]) +
      b[0] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])) /
    det;
  return [x0, x1, x2];
}
