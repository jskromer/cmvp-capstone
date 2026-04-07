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

## Architecture
- Pure static HTML/JS/CSS — no framework, no build step, no npm
- All simulation data hardcoded inline (intentional — offline-capable)
- localStorage used for Checkpoint 8 → Checkpoint 9 NRA data persistence
- EnergyPlus 25.2 simulation files in simulation/
- IDF factor list: simulation/baseline_static_factors.md

## Current Build State
- Complete: Hub, Building, Checkpoints 1, 2, 5, 7, 8, 9
- Stubs (tool not built): Checkpoints 3, 4, 6
- Run docs/audit-prompt.md against the source files for full status

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
