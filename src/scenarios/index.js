// Scenario configurations for multi-scenario CMVP capstone
// Each scenario defines its building context, tab structure, data paths, and fixture data

export const SCENARIOS = {
  greenfield: {
    id: 'greenfield',
    name: 'Greenfield Municipal Center',
    subtitle: 'CMVP Capstone — M&V Workbench',
    sqft: 62000,
    climate: 'Mid-Atlantic CZ 4A',
    electricRate: 0.100,   // $/kWh blended
    gasRate: 1.17,         // $/therm blended
    demandRate: 12.50,     // $/kW-month
    emissionFactor: 0.85,  // lb CO₂/kWh
    gasEmissionFactor: 11.7, // lb CO₂/therm
    tabs: [
      { id: 'overview', label: 'Overview', phase: 1 },
      { id: 'scatter', label: 'Scatter Plots', phase: 2 },
      { id: 'model', label: 'Model Fitting', phase: 2 },
      { id: 'lighting', label: 'Lighting Stipulation', phase: 2 },
      { id: 'vfd', label: 'VFD Analysis', phase: 2 },
      { id: 'timeseries', label: 'Time Series', phase: 3 },
      { id: 'savings', label: 'Savings Calculator', phase: 3 },
    ],
    dataPaths: {
      baselineMonthly: '/data/greenfield_baseline_monthly.csv',
      reportingMonthly: '/data/greenfield_reporting_monthly.csv',
      reportingNoNRA: '/data/greenfield_reporting_no_nra_monthly.csv',
      baselineHourly: '/data/greenfield_baseline_hourly.csv',
      reportingHourly: '/data/greenfield_reporting_hourly.csv',
      fanData: '/data/greenfield_ecm4_fan_data.csv',
    },
    fixtureData: [
      { id: 1, space: "Wing A — Open Office (2nd floor)", qty: 120, baseW: 128, retroW: 40, hours: 2860 },
      { id: 2, space: "Wing A — Open Office (1st floor)", qty: 120, baseW: 128, retroW: 40, hours: 2860 },
      { id: 3, space: "Wing A — Private Offices", qty: 80, baseW: 96, retroW: 32, hours: 2600 },
      { id: 4, space: "Wing A — Conference Rooms", qty: 40, baseW: 128, retroW: 40, hours: 1200 },
      { id: 5, space: "Wing A — Corridors & Restrooms", qty: 60, baseW: 64, retroW: 20, hours: 3380 },
      { id: 6, space: "Wing B — Reading Rooms", qty: 100, baseW: 128, retroW: 40, hours: 3900 },
      { id: 7, space: "Wing B — Stacks", qty: 150, baseW: 96, retroW: 32, hours: 2600 },
      { id: 8, space: "Wing B — Meeting Rooms", qty: 30, baseW: 128, retroW: 40, hours: 1500 },
      { id: 9, space: "Wing B — Circulation & Entry", qty: 40, baseW: 64, retroW: 20, hours: 4160 },
    ],
    ecms: [
      { id: 1, name: 'LED Lighting + Controls', approach: 'Retrofit isolation', method: 'Key parameter measurement', ipmvp: 'Option A' },
      { id: 2, name: 'Chiller/DX Replacement', approach: 'Student decides', method: 'Student decides', ipmvp: '—' },
      { id: 3, name: 'Roof Insulation', approach: 'Whole facility', method: 'Statistical / inverse model', ipmvp: 'Option C' },
      { id: 4, name: 'VFDs on AHU Fans', approach: 'Retrofit isolation', method: 'Continuous performance verification', ipmvp: 'Option B' },
    ],
  },

  slo: {
    id: 'slo',
    name: 'SLO Large Office',
    subtitle: 'CMVP Capstone — Forward Model Workbench',
    sqft: 90000,
    climate: 'California CZ 3C (San Luis Obispo)',
    electricRate: 0.170,   // $/kWh (California commercial)
    gasRate: 1.20,         // $/therm
    demandRate: 18.00,     // $/kW-month
    emissionFactor: 0.53,  // lb CO₂/kWh (CAMX grid)
    gasEmissionFactor: 11.7, // lb CO₂/therm
    tabs: [
      { id: 'overview', label: 'Overview', phase: 1 },
      { id: 'scatter', label: 'Energy Signature', phase: 1 },
      { id: 'calibration', label: 'Calibration Assessment', phase: 2 },
      { id: 'sensitivity', label: 'Sensitivity Analysis', phase: 2 },
      { id: 'lighting', label: 'Lighting Stipulation', phase: 2 },
      { id: 'ecm-savings', label: 'ECM Savings', phase: 3 },
      { id: 'counterfactual', label: 'Competent Counterfactual', phase: 3 },
      { id: 'mnvscore', label: 'MnVScore', phase: 3 },
    ],
    dataPaths: {
      baselineMonthly: '/data/slo_baseline_monthly.csv',
      sensitivity: '/data/slo_sensitivity_results.json',
      ecmSavings: '/data/slo_ecm_savings.json',
      calibration: '/data/slo_calibration_summary.json',
    },
    fixtureData: [
      { id: 1, space: "Floor 1 — Open Office", qty: 180, baseW: 96, retroW: 32, hours: 2860 },
      { id: 2, space: "Floor 1 — Private Offices", qty: 60, baseW: 96, retroW: 32, hours: 2600 },
      { id: 3, space: "Floor 1 — Lobby & Corridors", qty: 45, baseW: 64, retroW: 20, hours: 4160 },
      { id: 4, space: "Floor 2 — Open Office", qty: 200, baseW: 96, retroW: 32, hours: 2860 },
      { id: 5, space: "Floor 2 — Conference Rooms", qty: 35, baseW: 128, retroW: 40, hours: 1200 },
      { id: 6, space: "Floor 3 — Open Office", qty: 200, baseW: 96, retroW: 32, hours: 2860 },
      { id: 7, space: "Floor 3 — Break Rooms", qty: 20, baseW: 64, retroW: 20, hours: 2600 },
      { id: 8, space: "Floors 4–5 — Executive Suites", qty: 160, baseW: 96, retroW: 32, hours: 2400 },
      { id: 9, space: "Floors 4–5 — Corridors & Restrooms", qty: 70, baseW: 64, retroW: 20, hours: 3380 },
    ],
    ecms: [
      { id: 1, name: 'LED Lighting Retrofit', approach: 'Retrofit isolation', method: 'Key parameter measurement', ipmvp: 'Option A' },
      { id: 2, name: 'Chiller Replacement', approach: 'Whole facility', method: 'Calibrated simulation / forward model', ipmvp: 'Option D' },
      { id: 3, name: 'VAV Box Optimization', approach: 'Whole facility', method: 'Calibrated simulation / forward model', ipmvp: 'Option D' },
    ],
  },
};

export const SCENARIO_LIST = Object.values(SCENARIOS);
export const DEFAULT_SCENARIO = 'greenfield';
