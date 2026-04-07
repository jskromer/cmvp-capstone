# CMVP Capstone — Project Instructions

## What This Is
Interactive web capstone for CMVP/AEE course on Measurement & Verification.
Single static HTML file: docs/prototype.html
Printable handouts: docs/handouts.html
Build state: read the latest file in docs/audits/ for current status.

## Standing Rules — NON-NEGOTIABLE
1. NEVER write "measure the savings." Savings are INFERRED, ESTIMATED,
   CALCULATED, or DETERMINED. Energy is measured. Savings are a
   counterfactual inference.
2. NEVER reference IPMVP Options A, B, C, or D. Use CfD framework:
   Boundary, Model Form, Duration.
3. The IDF is the epistemological basis for all M&V decisions.
   It is the energy audit in computable form.
4. Savings are inferred from the adjusted counterfactual baseline —
   not from direct measurement.
5. Use "Checkpoint" not "Cut" — global rename completed 2026-04-07.

## Architecture
- Pure static HTML/JS/CSS — no framework, no build step, no npm
- All simulation data hardcoded inline (intentional — offline-capable)
- localStorage used for Checkpoint 6 boundary decisions and
  Checkpoint 8 → Checkpoint 9 NRA data persistence
- EnergyPlus 25.2 simulation files in simulation/
- IDF factor list: simulation/baseline_static_factors.md

## Current Build State (as of 2026-04-07 audit)
- Complete: Hub, Building, Checkpoints 1, 2, 5, 6, 7, 8, 9
- Stub (shell exists, tool not built): Checkpoints 3, 4
- Not built: Steps 0A, 0B, 1, 8, 9, 10, 12, 13, 14

### Checkpoint 6 detail
Three tools all wired and complete:
- Tool A: Boundary Decision Matrix (IDF variables → Static/Dynamic/NRA/Stipulated)
- Tool B: Sampling Calculator (n = (t × CV / precision)², 90% confidence)
- Tool C: Explain Your Answer (textarea → localStorage → feeds Step 12)

### Checkpoint 1 detail (revised 2026-04-07)
Three parts with progressive unlock gate:
- Part A: Physical boundary (3 questions — trivially whole building)
- Part B: Model boundary (5 questions — what OAT regression accounts for vs. NRA candidates)
- Part C: Who Controls? (callout connecting boundary → stipulation → NRA)

## Pending Work
- Checkpoint 3 (Scatter Plots): raw scatter viewer, Electric + Gas vs. OAT,
  NO model overlay — pre-model-fitting pedagogical step
- Checkpoint 4 (Baseline Period): 24-month time series selector,
  coverage factor, anomaly flagging
- Bug #4 Medium: Checkpoint 6 Lock button enablement logic — verify
  all selects must be filled before button activates
- Handouts: Checkpoints 5, 6, 7 missing paper handouts
- Step 12 (M&V Boundary Document): collect all localStorage inputs
  (boundary decisions, NRA pre-doc, narrative) into print-to-PDF report
- Stage 13 (Uncertainty Budget): FSU table, model + metering + sampling
- Stage 14 (Valuation): cost-avoidance calculator, blended vs. marginal rates

## CfD Framework
Three decision axes:
- Boundary: what is inside vs. outside the M&V model
- Model Form: regression type (3PC, 5P, 3PH, whole-facility vs. isolation)
- Duration: baseline period selection, reporting period length

## Key Data
- CFHQ building: 111,437 kWh/yr baseline electric, 7,590 therms/yr gas
- ECM-1 (LED lighting): -20,718 kWh/yr electric, +270 therms/yr gas
  (interactive effect — lighting heat gain removed)
- ECM-2 (night setback): -741 kWh/yr electric, -2,840 therms/yr gas
- NRA scenario: server room expansion, month 9, +420 kWh/mo electric
- Baseline year: 2025, Reporting year: 2026
