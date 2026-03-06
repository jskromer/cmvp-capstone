#!/usr/bin/env python3
"""
Transform SLO Large Office EnergyPlus-MCP data into CMVP capstone app format.

Source files (in ~/EnergyPlus-MCP/energyplus-mcp-server/):
  - sample_files/slo_large_office_utility_data.csv
  - outputs/calibration_tuned_v2/eplusout.csv
  - outputs/sensitivity/sensitivity_analysis.json
  - outputs/calibration_tuned_v2/slo_large_office_baseline.json

Output files (to public/data/):
  - slo_baseline_monthly.csv
  - slo_sensitivity_results.json
  - slo_ecm_savings.json
  - slo_calibration_summary.json
"""

import csv
import json
import os
from pathlib import Path

# Paths
EPLUS_MCP = Path.home() / "EnergyPlus-MCP" / "energyplus-mcp-server"
OUTPUT_DIR = Path(__file__).parent.parent / "public" / "data"

UTILITY_CSV = EPLUS_MCP / "sample_files" / "slo_large_office_utility_data.csv"
HOURLY_CSV = EPLUS_MCP / "outputs" / "calibration_tuned_v2" / "eplusout.csv"
SENSITIVITY_JSON = EPLUS_MCP / "outputs" / "sensitivity" / "sensitivity_analysis.json"
BASELINE_JSON = EPLUS_MCP / "outputs" / "calibration_tuned_v2" / "slo_large_office_baseline.json"


def compute_monthly_oat(hourly_csv_path):
    """Extract monthly average OAT from EnergyPlus hourly output (column 2, Celsius → Fahrenheit)."""
    monthly_temps = {m: [] for m in range(1, 13)}

    with open(hourly_csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # skip header
        for row in reader:
            if not row or not row[0].strip():
                continue
            # Date format: " 01/01  01:00:00"
            date_str = row[0].strip()
            month = int(date_str.split('/')[0])
            temp_c = float(row[1])
            temp_f = temp_c * 9 / 5 + 32
            monthly_temps[month].append(temp_f)

    return {m: sum(temps) / len(temps) for m, temps in monthly_temps.items() if temps}


def build_baseline_monthly():
    """
    Create slo_baseline_monthly.csv matching Greenfield column format:
    month, days, avg_oat_f, total_kwh, total_therms

    Uses utility bills for kWh/therms, EnergyPlus hourly for OAT.
    """
    print("Building slo_baseline_monthly.csv...")

    # Get monthly OAT from simulation
    monthly_oat = compute_monthly_oat(HOURLY_CSV)

    # Read utility data
    rows = []
    with open(UTILITY_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            oat = monthly_oat.get(i, 55.0)
            rows.append({
                'month': i,
                'days': int(row['days']),
                'avg_oat_f': round(oat, 1),
                'total_kwh': int(row['kwh']),
                'total_therms': int(row['therms']),
            })

    outpath = OUTPUT_DIR / "slo_baseline_monthly.csv"
    with open(outpath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['month', 'days', 'avg_oat_f', 'total_kwh', 'total_therms'])
        writer.writeheader()
        writer.writerows(rows)

    print(f"  -> {outpath} ({len(rows)} rows)")
    return rows


def build_sensitivity_results():
    """
    Create slo_sensitivity_results.json — pass through with added display metadata.
    """
    print("Building slo_sensitivity_results.json...")

    with open(SENSITIVITY_JSON, 'r') as f:
        raw = json.load(f)

    # Add display-friendly names and evidence sources
    param_meta = {
        'lighting_power': {
            'display_name': 'Lighting Power Density',
            'units': 'W/m²',
            'source': 'Lighting audit',
            'evidence': 'Fixture count and spot measurements',
            'confidence': 'high',
        },
        'equipment_power': {
            'display_name': 'Equipment Power Density',
            'units': 'W/m²',
            'source': 'Equipment inventory',
            'evidence': 'Nameplate survey of major equipment',
            'confidence': 'moderate',
        },
        'window_solar_transmittance': {
            'display_name': 'Window Solar Transmittance (SHGC)',
            'units': '—',
            'source': 'Window specification',
            'evidence': 'Original specs from 1980s construction drawings',
            'confidence': 'low',
        },
        'chiller_cop': {
            'display_name': 'Chiller COP',
            'units': '—',
            'source': 'Nameplate + age degradation',
            'evidence': 'Trane RTU nameplate, 15 years old, assumed 10% degradation',
            'confidence': 'moderate',
        },
        'fan_efficiency': {
            'display_name': 'Fan Total Efficiency',
            'units': '%',
            'source': 'Design documents',
            'evidence': 'Mechanical drawings, no field measurement',
            'confidence': 'moderate',
        },
        'occupancy': {
            'display_name': 'Occupancy Density',
            'units': 'people/m²',
            'source': 'HR records',
            'evidence': 'Employee headcount, assumed distribution',
            'confidence': 'moderate',
        },
        'infiltration': {
            'display_name': 'Infiltration Rate',
            'units': 'ACH',
            'source': 'Assumption',
            'evidence': 'No blower door test, typical for 1980s construction',
            'confidence': 'low',
        },
        'boiler_efficiency': {
            'display_name': 'Boiler Efficiency',
            'units': '%',
            'source': 'Not applicable',
            'evidence': 'No gas heating in model (electric reheat)',
            'confidence': 'n/a',
        },
    }

    enriched_rankings = []
    for r in raw['rankings']:
        meta = param_meta.get(r['parameter'], {})
        enriched_rankings.append({
            **r,
            **meta,
        })

    result = {
        'base_electricity_kwh': raw['base_electricity_kwh'],
        'perturbation': raw['perturbation'],
        'rankings': enriched_rankings,
        'recommendations': raw['recommendations'],
    }

    outpath = OUTPUT_DIR / "slo_sensitivity_results.json"
    with open(outpath, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"  -> {outpath}")
    return result


def build_ecm_savings(sensitivity_data):
    """
    Create slo_ecm_savings.json — project ECM savings from sensitivity deltas.

    ECM-1: LED Lighting — LPD reduction of ~35% (10.8 → 7.0 W/m²)
    ECM-2: Chiller Replacement — COP improvement of ~25% (3.2 → 4.0)
    ECM-3: VAV Box Optimization — fan efficiency improvement of ~15%
    """
    print("Building slo_ecm_savings.json...")

    base_kwh = sensitivity_data['base_electricity_kwh']

    # Find sensitivity coefficients
    sens_by_param = {r['parameter']: r for r in sensitivity_data['rankings']}

    # ECM-1: Lighting — 35% LPD reduction
    # Sensitivity says ±15% LPD → ±16.3% energy change
    # Scale: 35% / 15% = 2.33x the perturbation
    lpd_sens = sens_by_param['lighting_power']
    lpd_savings_kwh = (lpd_sens['delta_kwh'] / 2) * (35 / 15)  # half delta (just low side) × scaling

    # ECM-2: Chiller — COP from 3.2 to 4.0 (25% improvement)
    # Sensitivity says ±15% COP → 7.6% energy change (inverse)
    chiller_sens = sens_by_param['chiller_cop']
    # Higher COP = lower energy. high_kwh is at +15% COP (lower energy)
    chiller_savings_kwh = abs(chiller_sens['delta_kwh'] / 2) * (25 / 15)

    # ECM-3: VAV optimization — fan efficiency +15%
    fan_sens = sens_by_param['fan_efficiency']
    vav_savings_kwh = abs(fan_sens['delta_kwh'] / 2) * (15 / 15)

    ecms = [
        {
            'ecm_id': 1,
            'name': 'LED Lighting Retrofit',
            'description': 'Replace T8 fluorescent with LED throughout all 5 floors. LPD reduction from 10.8 to 7.0 W/m².',
            'approach': 'Retrofit isolation',
            'method': 'Key parameter measurement',
            'ipmvp': 'Option A',
            'parameter': 'lighting_power',
            'parameter_change': '-35% LPD',
            'savings_kwh': round(lpd_savings_kwh),
            'savings_pct': round(lpd_savings_kwh / base_kwh * 100, 1),
            'uncertainty_pct': 8.0,
            'uncertainty_basis': 'Sensitivity: ±15% LPD → ±16.3% energy. Fixture wattage measured (high confidence), hours stipulated (moderate).',
            'cost_savings': round(lpd_savings_kwh * 0.170),
        },
        {
            'ecm_id': 2,
            'name': 'Chiller Replacement',
            'description': 'Replace aging 15-year-old chiller with high-efficiency unit. COP improvement from 3.2 to 4.0.',
            'approach': 'Whole facility',
            'method': 'Calibrated simulation / forward model',
            'ipmvp': 'Option D',
            'parameter': 'chiller_cop',
            'parameter_change': '+25% COP',
            'savings_kwh': round(chiller_savings_kwh),
            'savings_pct': round(chiller_savings_kwh / base_kwh * 100, 1),
            'uncertainty_pct': 12.0,
            'uncertainty_basis': 'Sensitivity: ±15% COP → ±7.6% energy. COP from nameplate with degradation assumption (moderate confidence).',
            'cost_savings': round(chiller_savings_kwh * 0.170),
        },
        {
            'ecm_id': 3,
            'name': 'VAV Box Optimization',
            'description': 'Optimize VAV box minimum flow setpoints and schedules. Equivalent to ~15% fan efficiency improvement.',
            'approach': 'Whole facility',
            'method': 'Calibrated simulation / forward model',
            'ipmvp': 'Option D',
            'parameter': 'fan_efficiency',
            'parameter_change': '+15% fan efficiency',
            'savings_kwh': round(vav_savings_kwh),
            'savings_pct': round(vav_savings_kwh / base_kwh * 100, 1),
            'uncertainty_pct': 15.0,
            'uncertainty_basis': 'Sensitivity: ±15% fan efficiency → ±3.8% energy. Fan performance from design docs only (moderate confidence).',
            'cost_savings': round(vav_savings_kwh * 0.170),
        },
    ]

    total_savings = sum(e['savings_kwh'] for e in ecms)

    result = {
        'base_electricity_kwh': round(base_kwh),
        'building_sqft': 90000,
        'electric_rate': 0.170,
        'ecms': ecms,
        'total_savings_kwh': round(total_savings),
        'total_savings_pct': round(total_savings / base_kwh * 100, 1),
        'total_cost_savings': round(total_savings * 0.170),
        'note': 'Savings estimated from calibrated simulation sensitivity analysis. Individual ECM savings may not sum linearly due to interactive effects.',
    }

    outpath = OUTPUT_DIR / "slo_ecm_savings.json"
    with open(outpath, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"  -> {outpath}")
    return result


def build_calibration_summary():
    """
    Create slo_calibration_summary.json from baseline metadata.
    """
    print("Building slo_calibration_summary.json...")

    with open(BASELINE_JSON, 'r') as f:
        raw = json.load(f)

    result = {
        'building': {
            'name': 'SLO Large Office',
            'id': raw['identity']['building_id'],
            'sqft': raw['model']['floor_area_ft2'],
            'base_model': raw['model']['base_model'],
            'vintage': raw['model']['vintage'],
            'climate': 'California CZ 3C — San Luis Obispo',
            'analyst': raw['identity']['analyst'],
        },
        'diagnostics': raw['diagnostics'],
        'ashrae_g14_limits': {
            'monthly_nmbe_pct': 5.0,
            'monthly_cvrmse_pct': 15.0,
        },
        'calibration_adjustments': raw['calibration_adjustments'],
        'parameters': raw['parameters'],
        'monthly_comparison': raw['monthly_comparison'],
        'competence': raw['competence'],
        'limitations': raw['uses']['limitations'],
        'audit_trail': raw['audit_trail'],
    }

    outpath = OUTPUT_DIR / "slo_calibration_summary.json"
    with open(outpath, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"  -> {outpath}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=== SLO Large Office Data Preparation ===\n")

    build_baseline_monthly()
    sensitivity = build_sensitivity_results()
    build_ecm_savings(sensitivity)
    build_calibration_summary()

    print("\nDone! All SLO data files written to public/data/")


if __name__ == '__main__':
    main()
