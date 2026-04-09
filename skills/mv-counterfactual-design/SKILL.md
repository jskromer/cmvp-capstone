---
name: mv-counterfactual-design
description: >
  Measurement & Verification using the Counterfactual Design (CfD) framework.
  Use when analyzing energy savings, evaluating M&V plans, designing baselines,
  assessing retrofit performance, or working with energy conservation measures.
  Replaces IPMVP Options A-D with descriptive terminology organized around
  three decision axes: boundary, model form, duration.
---

# M&V as Counterfactual Design

## Core Principles

1. **Savings are inferred, never measured.** Energy consumption is measured. Savings are the difference between measured reporting-period energy and the adjusted counterfactual baseline -- a quantity that does not exist in the physical world. Never say "measure the savings."

2. **The IDF is the epistemological basis.** The Input Data File (energy audit in computable form) defines what is known, what is assumed, and what must be observed. Every M&V decision traces back to the IDF.

3. **Three decision axes define every M&V approach:**
   - **Boundary** -- what is inside vs. outside the M&V model
   - **Model Form** -- regression type (inverse/statistical) or simulation (forward/physical)
   - **Duration** -- baseline period selection, reporting period length

## The CfD Decision Framework

### Boundary
- **Whole facility**: The meter is the boundary. All loads included. Model accounts for weather and occupancy; everything else becomes a potential non-routine adjustment.
- **Retrofit isolation**: Only the affected system is inside the boundary. Requires sub-metering or engineering calculations for the isolated system.

### Model Form
- **Inverse model (statistical)**: Observed data yields inferred relationships. Change-point regression, degree-day models. Works backward from bills to behavior.
- **Forward model (calibrated simulation)**: Physical parameters yield predicted energy. EnergyPlus, eQUEST. Works forward from physics to consumption.

### Duration
- **Baseline period**: Must be long enough to capture seasonal variation (typically 12+ months). Must be free of anomalies.
- **Reporting period**: Must cover enough post-implementation time to verify persistence under varying conditions.

For detailed decision trees, see [BOUNDARY_DECISIONS.md](BOUNDARY_DECISIONS.md).

## Terminology Rules

**Always lead with descriptive terms.** IPMVP Options A-D appear only as parenthetical cross-references.

| Approach | Method | Cross-Reference |
|----------|--------|-----------------|
| Retrofit isolation | Key parameter measurement | cf. IPMVP Option A |
| Retrofit isolation | Continuous performance verification | cf. IPMVP Option B |
| Whole facility | Inverse / statistical model | cf. IPMVP Option C |
| Whole facility | Forward / calibrated simulation | cf. IPMVP Option D |

For the full substitution table, see [TERMINOLOGY.md](TERMINOLOGY.md).

## Evidence vs. Inference

|  | Pre-Implementation | Post-Implementation |
|--|-------------------|---------------------|
| **Evidence** (factual) | Baseline metered energy | Reporting-period metered energy |
| **Inference** (counterfactual) | -- | Adjusted baseline model -> avoided energy use |

Savings live in the inference row. They are never evidence.

## Working with Baselines

- A baseline is a **model of behavior**, not a historical record. It must be adjusted to reporting-period conditions before comparison.
- **Static factors**: Parameters that do not change between baseline and reporting periods (e.g., building envelope, lighting fixture type after retrofit).
- **Dynamic factors**: Parameters that change and must be accounted for in the model (e.g., outdoor air temperature, occupancy schedules).
- **Non-routine adjustments (NRAs)**: Corrections for changes outside normal operation that the model cannot predict (e.g., new server room, major tenant change). The adjustment is what the CMVP does; the event triggers it.
- **Stipulated values**: Parameters agreed upon by contract rather than measured. Must be defensible and documented.

## Entropy Audit

Every M&V plan carries three types of uncertainty:

| Type | Source | Owner |
|------|--------|-------|
| **Physical** | Weather, loads, occupancy | Nobody -- it is the world |
| **Model** | Variable selection, functional form, baseline duration | The CMVP / designer |
| **Governance** | Change protocols, adjustment triggers, dispute resolution | The contract |

Before arguing about price, audit where the entropy lives. See [ENTROPY_AUDIT.md](ENTROPY_AUDIT.md) for the structured audit template.

## Regression Guidance

When working with inverse models, validate:
- **CV(RMSE)** < 25% for monthly, < 35% for daily models
- **R-squared** appropriate for model complexity (not the sole criterion)
- **t-statistics** > 2.0 for all model coefficients
- **Sample size**: n = (t x CV / precision)^2 at 90% confidence

Use `scripts/regression_check.py` to validate regression inputs programmatically.
