import Papa from 'papaparse';

async function fetchCSV(path) {
  const res = await fetch(path);
  const text = await res.text();
  return new Promise((resolve, reject) => {
    Papa.parse(text, {
      header: true,
      dynamicTyping: true,
      skipEmptyLines: true,
      complete: (results) => resolve(results.data),
      error: (err) => reject(err),
    });
  });
}

async function fetchJSON(path) {
  const res = await fetch(path);
  return res.json();
}

// Greenfield-specific loaders (kept for backward compatibility)
export async function loadBaselineMonthly() {
  return fetchCSV('/data/greenfield_baseline_monthly.csv');
}

export async function loadReportingMonthly() {
  return fetchCSV('/data/greenfield_reporting_monthly.csv');
}

export async function loadReportingNoNRA() {
  return fetchCSV('/data/greenfield_reporting_no_nra_monthly.csv');
}

export async function loadBaselineHourly() {
  return fetchCSV('/data/greenfield_baseline_hourly.csv');
}

export async function loadReportingHourly() {
  return fetchCSV('/data/greenfield_reporting_hourly.csv');
}

export async function loadFanData() {
  return fetchCSV('/data/greenfield_ecm4_fan_data.csv');
}

export async function loadAllMonthly() {
  const [baseline, reporting, noNRA] = await Promise.all([
    loadBaselineMonthly(),
    loadReportingMonthly(),
    loadReportingNoNRA(),
  ]);
  return { baseline, reporting, noNRA };
}

// Scenario-aware loaders
export async function loadScenarioData(scenario) {
  const paths = scenario.dataPaths;

  if (scenario.id === 'greenfield') {
    return loadAllMonthly();
  }

  if (scenario.id === 'slo') {
    const [baseline, sensitivity, ecmSavings, calibration] = await Promise.all([
      fetchCSV(paths.baselineMonthly),
      fetchJSON(paths.sensitivity),
      fetchJSON(paths.ecmSavings),
      fetchJSON(paths.calibration),
    ]);
    return { baseline, sensitivity, ecmSavings, calibration };
  }

  throw new Error(`Unknown scenario: ${scenario.id}`);
}
