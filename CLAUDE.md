# CLAUDE.md — CMVP Capstone Project

## Project Owner
Steve Kromer — author of *The Role of the Measurement and Verification Professional* (River Publishers, 2024), former Chair of IPMVP, CMVP course instructor for AEE.

## Overview
Build a progressive capstone project for the CMVP certification training course. Students build a complete M&V plan for a realistic building across three phases, combining written deliverables with interactive workbench tools. The capstone must touch all 9 CMVP exam domains.

---

## The Scenario: Greenfield Municipal Center
A 62,000 sq ft mixed-use government facility (mid-Atlantic climate, Zone 4A) with 4 ECMs under an ESPC contract:
- **ECM-1:** LED lighting + controls (Wings A & B) — retrofit isolation / stipulated
- **ECM-2:** Chiller/DX replacement (all units) — student decides approach
- **ECM-3:** Building envelope / roof insulation (R-15 → R-30) — whole facility
- **ECM-4:** VFDs on AHU supply fans (AHU-1, 2, 3) — retrofit isolation / continuous performance verification

### Building Wings
| Wing | Use | Area | HVAC | Schedule |
|------|-----|------|------|----------|
| A | Office (open + private) | 35,000 sf | AHU-1: Gas furnace, DX cool, 15 HP fan | M-F 7am–6pm |
| B | Public library | 15,000 sf | AHU-2: Heat pump, DX cool, 10 HP fan | M-Sat 8am–9pm, Sun 12–5pm |
| C | Data center / IT | 2,000 sf | CRAC-1: 5-ton DX, 24/7 | 24/7 |
| Common | Lobby, corridors, mech. | 10,000 sf | AHU-3: Gas furnace, DX cool, 5 HP fan | M-F 6am–10pm |

### Key Data (from EnergyPlus simulation)
- **Baseline annual electric:** 1,162,628 kWh (64.0 kBtu/ft² electric EUI)
- **Baseline annual gas:** 5,800 therms (9.4 kBtu/ft² gas EUI)
- **Combined EUI:** 73.4 kBtu/ft²
- **Combined ECM savings:** 122,390 kWh (10.5%)
- **Gas change:** +358 therms (+6.2%) — interactive effects from reduced lighting heat
- **NRA event:** Data center expansion month 8 adds +93,984 kWh (months 8–12)

### Utility Rates
- **Electric:** $0.090/kWh energy + $0.015/kWh fuel adj. = $0.105/kWh blended; Demand: $12.50/kW-month; Customer: $125/month
- **Gas:** $1.03/therm + $0.12/therm transport = $1.15/therm blended; Customer: $45/month
- **Emission factors:** Electric 0.92 lb CO₂/kWh (PJM grid); Gas 11.7 lb CO₂/therm

---

## Three-Phase Arc (flexible pacing — not tied to specific days)

- **Phase 1:** Context, boundaries, approach selection (Modules 0–3)
- **Phase 2:** Modeling, baselines, NRAs, retrofit isolation (Modules 4–6)
- **Phase 3:** Planning, metering, reporting, defense (Modules 7–9)

Phases are decoupled from calendar days. Instructor controls pacing based on group needs.

## Exam Domain Coverage
| Domain | Weight | Primary Capstone Touchpoint |
|--------|--------|---------------------------|
| 1. Basis for Adjustments | 10–16% | Boundaries, baseline, NRA protocol |
| 2. Fundamental Approaches | 9–13% | Approach selection per ECM |
| 3. Retrofit Isolation | 11–17% | ECM-4 VFD metering plan |
| 4. Whole Facility | 10–16% | Workbench model fitting |
| 5. M&V Planning | 12–18% | Complete M&V plan document |
| 6. Savings Reporting | 6–10% | Savings calc + annual report |
| 7. Metering | 6–8% | Metering specification table |
| 8. Modeling Concepts | 9–13% | Model validation, uncertainty |
| 9. Contextual Considerations | 6–10% | Stakeholder/risk matrix |

---

## Terminology Convention — CRITICAL

This course uses its own descriptive terminology as the primary working vocabulary. IPMVP Options A–D are referenced only as cross-references, never as the primary labels. The IPMVP trademark disclaimer ("IPMVP is a registered trademark of EVO. AEE is using the term 'IPMVP' only to refer to the protocol.") appears in the slides whenever IPMVP is mentioned.

### Evidence and Inference — The Conceptual Foundation

Everything in M&V falls into one of two categories:

| Category | What It Is | Examples | How You Get It |
|----------|-----------|----------|---------------|
| **Evidence** | What you can directly observe or measure | Baseline energy bills, reporting period meter data, outdoor air temperature, fixture wattage, fan kW | Measurement, observation, metering |
| **Inference** | What you conclude from the evidence | The adjusted baseline model, the counterfactual, avoided energy use ("savings") | Modeling, calculation, professional judgment |

**Savings are never evidence. Savings are always inference.**

You can measure baseline energy (evidence). You can measure reporting period energy (evidence). But you can never measure what *would have happened* without the ECM — that's the counterfactual, and it must be inferred. The adjusted baseline model is the inference engine that bridges the gap.

This maps directly to the course's factual/counterfactual framework:

|  | Pre-Implementation | Post-Implementation |
|--|-------------------|---------------------|
| **Evidence** (factual) | Baseline metered energy | Reporting period metered energy |
| **Inference** (counterfactual) | — | Adjusted baseline model → avoided energy use |

The evidence/inference distinction drives every major decision in the capstone:

- **Model selection** (inverse vs. forward) = choosing your inference method
- **Metering plan** = deciding what evidence to collect
- **Uncertainty analysis** = quantifying how much you trust your inference
- **Key parameter measurement vs. continuous performance verification** = how much evidence you need before you're willing to infer the rest
- **Stipulation** = replacing evidence with professional judgment (a weaker form of inference) — acceptable when the parameter is stable and the cost of measuring outweighs the value
- **Non-routine adjustments** = correcting your inference when new evidence (a changed static factor) invalidates the original model assumptions

### Primary Terms (use these in all UI labels, templates, and instructions)

| Approach | Method | IPMVP Cross-Reference |
|----------|--------|-----------------------|
| Retrofit isolation | Key parameter measurement (some parameters stipulated) | cf. Option A |
| Retrofit isolation | Continuous performance verification (performance + operation over time) | cf. Option B |
| Whole facility | Statistical / inverse model (regression-based, observed data → inferred relationships) | cf. Option C |
| Whole facility | Calibrated simulation / forward model (physics-based, physical parameters → predicted energy) | cf. Option D |

### The Performance vs. Operation Distinction — Teachable Moment

The two retrofit isolation methods map to two fundamentally different questions:

| Question | Method | What It Proves | Example |
|----------|--------|---------------|---------|
| **Does it perform?** | Key parameter measurement — snapshot/spot measurement at installation, remaining parameters stipulated | The ECM was installed correctly and functions as designed | Lighting: measure fixture wattage, stipulate operating hours |
| **Does it keep operating?** | Continuous performance verification — ongoing measurement through the reporting period, no stipulated values | The ECM continues to deliver savings over time under varying conditions | VFDs: continuously meter fan kW, speed, and airflow across seasons |

The original concept behind what became "Option B" was this two-part idea: **performance** (functional verification at installation) AND **operation** (continuous confirmation over time). The term "all parameter measurement" (used in some protocols) flattens this into a metering specification and loses the intent.

The capstone forces the distinction through ECM-1 vs. ECM-4:
- **ECM-1 (Lighting):** Key parameter measurement is sufficient — LED wattage doesn't drift
- **ECM-4 (VFDs):** Continuous performance verification is required — fan power varies with load, speed, and conditions

### Inverse and Forward Models — Matched Pair

| Direction | Name | What It Does | Tools |
|-----------|------|-------------|-------|
| **Inverse** | Statistical / inverse model | Observed data → inferred relationships | Regression, change-point models, ASHRAE G14 methods |
| **Forward** | Calibrated simulation / forward model | Physical parameters → predicted energy | EnergyPlus, eQUEST, DOE-2 |

Both are inference methods — they run in different directions. The Greenfield dataset was generated by a forward model (EnergyPlus), but students work with the inverse model approach.

### Additional Terminology

| Use This | Not This | Notes |
|----------|----------|-------|
| Whole facility approach | Option C | Primary label in all UI and templates |
| Retrofit isolation approach | Option A / Option B | Distinguish by measurement method, not letter |
| Key parameter measurement | Simplified measurement | Snapshot + stipulation |
| Continuous performance verification | All parameter measurement | Performance + operation over time |
| Inverse model | Statistical model (alone) | Emphasizes direction: observed data → inferred relationships |
| Forward model | Physical model (alone) | Emphasizes direction: physical parameters → predicted energy |
| Deemed savings | — | Explicitly "not M&V" (Module 3); no measurement during performance period |
| Adjusted baseline model | Counterfactual | Both acceptable; the model is the inference engine |
| Avoided energy use | Energy savings | "Avoided energy use" is technically precise; "savings" is common shorthand |
| Static factor | Fixed parameter | Course term |
| Significant parameter | Key variable | Course term |
| Non-routine adjustment (NRA) | Non-routine event | The adjustment is what the CMVP does; the event triggers it |
| Evidence | Data, measurements | What you directly observe or measure |
| Inference | Estimate, prediction | What you conclude from evidence |

### Terminology Rules for the App

1. **All dropdown menus, table headers, form labels, and instruction text** use the primary course terms
2. **IPMVP references appear only in parenthetical cross-references** — e.g., "Retrofit isolation: continuous performance verification (cf. IPMVP Option B)"
3. **Never use Options A/B/C/D as standalone labels** — always pair with the descriptive term
4. **The approach selection table** should have columns: ECM | Approach | Method | Justification | (cf. IPMVP)
5. **Deemed savings** should be clearly distinguished from M&V
6. **When the performance/operation distinction arises**, surface it as a teaching moment
7. **When referencing models**, use the inverse/forward pairing

### Capstone ECM Approach Mapping (Expected Student Decisions)

| ECM | Expected Approach | Expected Method | cf. IPMVP | Key Teaching Point |
|-----|------------------|-----------------|-----------|-------------------|
| ECM-1 Lighting | Retrofit isolation | Key parameter measurement (stipulated hours, measured watts) | Option A | Why stipulation is sufficient — LED wattage doesn't drift |
| ECM-2 Chiller | Student decides | Student decides | — | Professional judgment — could argue whole facility or retrofit isolation |
| ECM-3 Envelope | Whole facility | Statistical / inverse model | Option C | Cannot isolate envelope savings with metering |
| ECM-4 VFDs | Retrofit isolation | Continuous performance verification (ongoing fan kW metering) | Option B | Why continuous verification is needed — fan power varies with load |

---

## Delivery Model — Design for Paper First

The course is delivered via Zoom or in-person (sometimes without student laptops). The capstone must work in all modes.

### Two Deliverables, Two Audiences

| Component | Purpose | Who Uses It |
|-----------|---------|-------------|
| **Paper packet** (PDF, 13 pages) | Student's personal M&V plan workbook. Fill in by hand or on screen. Progressive across 3 phases. | Every student, every delivery mode |
| **Web app** (cmvp-capstone.vercel.app) | Instructor's projection tool + student self-paced explorer (when laptops available). Scatter plots, model fitting, time series, savings calculator. | Instructor always; students when they have browsers |

### How They Work Together

| Capstone Component | With Computer | Without Computer |
|---|---|---|
| Scatter plot exploration | Student's own browser | Instructor projects; students observe and discuss |
| Model fitting / validation | Student's own browser | Instructor projects; students call out decisions, record stats on worksheet |
| Stakeholder/risk matrix | Fill in web form | Fill in printed worksheet |
| Approach selection table | Fill in web form | Fill in printed worksheet |
| Lighting stipulation calc | Interactive calculator in browser | Calculator + printed worksheet |
| Metering specification | Fill in web form | Fill in printed worksheet |
| M&V plan assembly | Fill in web template | Fill in printed template |
| Savings report | Web calculator | Instructor projects; students record numbers on worksheet |

### Paper Packet Structure (14 pages)

| Item | Description | Phase |
|------|-------------|-------|
| Cover page | Student name, date, building elevation graphic, TOC | — |
| Scenario Brief (2 pp) | Building, wings, ECMs, stakeholders, rates, floor plan, single line diagram | Reference |
| Worksheet 1A | Stakeholder & Risk Matrix | Phase 1 |
| Worksheet 1B | Measurement Boundaries | Phase 1 |
| Worksheet 1C | Approach Selection | Phase 1 |
| Worksheet 2A | Baseline Data Analysis | Phase 2 |
| Worksheet 2B | Static Factors & NRA Protocol | Phase 2 |
| Worksheet 2C | ECM-1 Lighting Stipulation (9 spaces, 740 fixtures) | Phase 2 |
| Worksheet 2D | ECM-4 VFD Metering Plan | Phase 2 |
| Worksheet 3A | M&V Plan Assembly | Phase 3 |
| Worksheet 3B | Savings Calculation & Reporting | Phase 3 |
| Worksheet 3C | Plan Defense Preparation | Phase 3 |

**PDF source:** `scripts/build_packet.py` generates the packet from reportlab. Diagrams are SVG (`docs/greenfield/greenfield-floor-plan.svg`, `docs/greenfield/greenfield-single-line.svg`, `docs/greenfield/greenfield-elevation.svg`).

---

## Companion Spreadsheets — Calculation Aids

These spreadsheets support specific capstone exercises. They can be used by the instructor on the projected screen, or distributed to students who have laptops. They are teaching tools, not required for completing the paper worksheets.

| Spreadsheet | Capstone Phase | Exercise | How It Helps |
|-------------|---------------|----------|-------------|
| `Statistics_Exercise.xlsm` | Phase 1 (Interlude 3.1) | Statistics foundation before model fitting | 4 tabs: population simulation, random sampling, descriptive stats, sample size calculator. Builds intuition for variance, CV, confidence intervals before students encounter model GoF statistics in Phase 2. |
| `Descriptive_Stats_Step_1.xlsx` | Phase 2 (Worksheet 2C) | ECM-1 lighting stipulation | Sample of 12 fixture wattages → calculate mean, variance, CV → extrapolate to 1,000 fixtures. Teaches why we sample instead of measuring every fixture, and how sample statistics propagate into savings uncertainty. |
| `Least_Squares_Matrix_Formula.xlsx` | Phase 2 (Worksheet 2A) | "Inside the model" companion to workbench | Matrix algebra walkthrough of OLS regression: X'X, (X'X)⁻¹, X'Y → β₀, β₁. Shows what the model fitting engine actually does. Validated against LINEST. Project alongside workbench model fitting. |
| `OEH_M_V_planning_tool.xlsx` | Phase 3 (Worksheet 3A) | M&V plan structure reference | 9-tab professional M&V planning workbook (Australian OEH). Sections: project background, requirements, M&V design, budget, tasks, timing (Gantt), results. Use as structural reference for the M&V plan template — adapt field labels to course terminology. |

### When to Surface Each Spreadsheet (instructor notes)

- **Before Phase 2 model fitting:** Project `Least_Squares_Matrix_Formula.xlsx` to demystify what regression does. Students who understand matrix multiplication will have better intuition for why change-point models need grid search.
- **During Phase 2 lighting stipulation:** Project `Descriptive_Stats_Step_1.xlsx` alongside Worksheet 2C. Students see that the fixture wattage sample mean is their stipulated value, and the CV tells them how much uncertainty that introduces.
- **During Phase 1 statistics interlude:** `Statistics_Exercise.xlsm` is a hands-on exercise if students have laptops, or a projected walkthrough if they don't. The sample size calculator directly connects to metering decisions — "how many data points do you need?"
- **During Phase 3 plan assembly:** Show `OEH_M_V_planning_tool.xlsx` structure as an example of a professional M&V plan. Students compare it to their Worksheet 3A checklist.

---

## Web App — Instructor Projection + Student Explorer

**Deployed:** https://cmvp-capstone.vercel.app/
**Repo:** https://github.com/jskromer/cmvp-capstone

### Design Principles for the Web App

1. **Large-screen readability** — designed for projection. Big fonts on axes, clear colors, no tiny controls
2. **No answer giveaways** — instructions ask open-ended questions ("What patterns do you observe?") not leading ones ("This should show 5P behavior")
3. **Warm cream theme** — consistent with CFdesigns branding (#f5f0e8 background)
4. **NRA is a discovery** — the Overview tab should NOT reveal the data center expansion. Students discover it in Phase 2/3 when they compare baseline model to reporting data
5. **Terminology convention** applies to all labels (see above)

### Tab Structure (current — 7 tabs)

| Tab | Phase | Components | Key Interactions |
|-----|-------|-----------|------------------|
| **Overview** | Phase 1 | `BuildingGraphic.jsx`, wing cards, ECM cards, `SummaryTable.jsx` | SVG building elevation with ECM markers, answer-key toggle, ecosystem links |
| **Scatter Plots** | Phase 2 | `ScatterPlot.jsx` | Electric vs OAT (5P), Gas vs OAT (3P), month labels. Fit line + change-point diamonds overlay after model fitting. |
| **Model Fitting** | Phase 2 | `ModelFitter.jsx` | Auto-fit + manual change-point sliders, side-by-side fit scatter plots, stats tables (NMBE, CV(RMSE), R²), residual diagnostics. Gas CV(RMSE) intentionally fails G14 → teaching prompt. |
| **Lighting Stipulation** | Phase 2 | `LightingStipulation.jsx` | 9 spaces, 740 fixtures matching paper packet. Editable hours, auto-calculated kWh, T8→LED graphic, interactive effects prompt. |
| **VFD Analysis** | Phase 2 | `FanAnalysis.jsx` | 672 hourly points, 3 AHUs. Speed vs Power (fan law cubic), Power vs OAT, pre/post comparison, VFD graphic, summary cards. |
| **Time Series** | Phase 2–3 | `TimeSeriesPlot.jsx` | Electric/Gas selector, model prediction overlay (purple dotted), NRA discovery. Gas prompt: "Gas went up — does retrofit make things worse?" |
| **Savings Calculator** | Phase 3 | `SavingsCalculator.jsx` | Monthly table, NRA controls (toggle/start/magnitude), per-bar coloring (green=savings, red=negative), cost/CO₂ valuation, uncertainty, "Compare another model" link. |

### Source Files

```
src/
├── App.jsx, App.css, index.css, main.jsx
├── components/
│   ├── BuildingGraphic.jsx          # SVG building elevation (800×340)
│   ├── FanAnalysis.jsx              # ECM-4 VFD pre/post analysis
│   ├── LightingStipulation.jsx      # ECM-1 fixture inventory calculator
│   ├── ModelFitter.jsx              # Change-point model fitting + residuals
│   ├── SavingsCalculator.jsx        # Monthly savings, NRA, valuation
│   ├── ScatterPlot.jsx              # Energy vs OAT scatter plots
│   ├── SummaryTable.jsx             # Annual energy summary
│   └── TimeSeriesPlot.jsx           # Monthly time series with model overlay
└── utils/
    ├── dataLoader.js                # CSV parsing
    └── statistics.js                # Regression, GoF, change-point search
```

### Teaching Moments Built Into the UI

1. **5P change points (35/71°F):** Mathematically optimal but physically unrealistic. Manual sliders let students drag to ~48/63°F and watch R² drop. Physics vs. statistics tradeoff.
2. **Gas CV(RMSE) fails G14:** 16.13% vs 15% limit. "Does that mean it's unusable?"
3. **NRA discovery:** Time series August step change → savings calculator red bars → toggle NRA on → bars flip green.
4. **Interactive effects:** Lighting stipulation total ≠ whole-facility savings. Less lighting heat → less cooling, more heating.
5. **Fan law cubic:** 35% speed reduction → ~73% power reduction. Why continuous verification matters.
6. **Gas went up:** Reporting year gas > baseline. Model prediction reveals the counterfactual truth.

### Future Additions

- M&V plan builder template — interactive version of Worksheet 3A
- Single line diagram with interactive metering point placement
- Stakeholder/risk matrix tool
- i18n/es.json for Spanish-language delivery

---

## Tech Stack & Deployment

- **Framework:** Vite + React (JSX), same as CFdesigns and mv-course
- **Charts:** Recharts + Plotly (for scatter/model fitting)
- **Hosting:** Vercel (auto-deploys from GitHub `main` branch)
- **Repo:** https://github.com/jskromer/cmvp-capstone
- **Workflow:** Claude pushes directly to GitHub using Steve's PAT (provided per session, never stored)
- **Branch note:** Vercel deploys from `main`. If local work is on `master`, use `git push --force origin master:main`.

### Data Files (in `public/data/`)
| File | Rows | Description |
|------|------|-------------|
| `greenfield_baseline_monthly.csv` | 12 | Monthly electric (kWh), gas (therms), OAT (°F) — baseline year |
| `greenfield_reporting_monthly.csv` | 12 | Same fields — reporting year (with NRA from month 8) |
| `greenfield_reporting_no_nra_monthly.csv` | 12 | Same fields — reporting year without NRA (answer key) |
| `greenfield_baseline_hourly.csv` | 8,760 | Hourly electric, gas, OAT — baseline year |
| `greenfield_reporting_hourly.csv` | 8,760 | Hourly — reporting year with NRA |
| `greenfield_ecm4_fan_data.csv` | 672 | Hourly fan kW, speed (%), airflow (CFM), OAT for 4 weeks pre/post |

### Companion Sites
- **CFdesigns:** https://cfdesigns.vercel.app — Counterfactual Designs course
- **mv-course:** https://mv-course.vercel.app — IPMVP-aligned course
- **Central resource:** https://counterfactual-designs.com

### Reusable Components (from CFdesigns/mv-course)
- `Workbench.jsx` — dataset selection, model fitting, validation, savings
- `Fundamentals.jsx` — scatter vs time series, linear models, residuals, GoF
- `CaseStudies.jsx` — NRA case studies (reporting period + baseline)

---

## Pedagogical Features Embedded in the Data

The EnergyPlus simulation was designed to create six specific teaching moments:

1. **5P change-point shape (electric):** Heating leg + deadband + cooling leg. Students must identify the correct model type.
2. **Interactive effects (gas increase):** Reduced lighting heat → more gas heating needed. Gas goes UP after retrofit. Students must explain this to the building owner.
3. **NRA detection:** Data center expansion in month 8 masks true savings. Students must detect and adjust.
4. **Seasonal asymmetry:** Heating savings ≠ cooling savings due to different HVAC systems (gas furnace vs DX).
5. **Borderline uncertainty:** Fractional savings uncertainty near the 50% threshold — forces discussion of statistical significance.
6. **Gas model validation:** Gas 3P model may fail CV(RMSE) at 15% threshold while passing R² — students must grapple with a model that partially passes.

---

## Project Knowledge Files

- `capstone-design.md` — Full design document with scenario, domain mapping, tool requirements
- `CMVP_Scheme_2-0_v1-2.pdf` — Exam blueprint with domain weights and specific tasks
- `CMVP_Body-of-Knowledge_2-0_v1-2-1.pdf` — BoK topics and references
- `CMVP_v2_0_Section-*.pptx` (12 files) — Complete slide decks for Modules 0–9 plus interludes
- `slide-extracts/` — Markdown text extractions of all slide decks

---

## Design Principles

1. **Every decision maps to an exam domain** — no busywork
2. **Progressive construction** — Phase 1 deliverables feed into Phase 2, Phase 2 into Phase 3
3. **Paper first, web is a bonus** — capstone works without student laptops
4. **Interactive + written** — workbench tools for analysis, structured templates for documentation
5. **Professional judgment emphasis** — no single "right answer"; students must justify choices
6. **Realistic complexity** — multiple ECMs, mixed approaches, NRA events, interactive effects
7. **Warm cream theme** — consistent with CFdesigns branding
8. **Flexible pacing** — phases, not days; instructor controls timing

## Key Design Decisions

- Standalone site (not embedded in CFdesigns) to avoid mixing audiences
- Scenario is government/ESPC to naturally engage all 4 contextual domains (technical, commercial, legal, regulatory)
- 5P change-point model for whole-facility to match existing workbench capabilities
- Built-in NRA event (data center expansion) to force non-routine adjustment exercise
- Capstone deliverable is a structured M&V plan document, not just interactive exploration
- Paper packet is the student's artifact; web app is the instructor's projection tool
- Companion spreadsheets support specific calculation exercises but are not required
