# Teaching Stories — Common Professional Confusions in M&V

These stories illustrate the conceptual errors that IPMVP's letter-based terminology enables. Each uses a common dataset from CMVP v2.0 Section 1.0 (Fundamental Concepts), slide 29.

**Instructor note (slide 29):** The regression-based adjusted baseline applies mainly to *counterfactual methods* — whole-facility approaches where you must construct what *would have happened*. Performance verification (retrofit isolation) doesn't do this; it verifies the ECM itself.

---

## The Dataset

| Days | HDD (15.5°C) | Gas (Mcf) |
|------|-----|-------------|
| 29 | 650 | 210,692 |
| 33 | 440 | 208,664 |
| 29 | 220 | 157,886 |
| 30 | 150 | 120,793 |
| 32 | 50 | 116,508 |
| 31 | 20 | 107,272 |
| 29 | 14 | 95,411 |
| 31 | 29 | 126,423 |
| 31 | 125 | 149,253 |
| 28 | 275 | 166,202 |
| 33 | 590 | 221,160 |
| 30 | 723 | 224,958 |

Regression: **y = 173.08x + 111,372** (R² = 0.9193)

This regression *is* the inference engine. It is the adjusted baseline model. Without it, the 12 rows of HDD and gas consumption are just evidence sitting in a table.

---

## The Foundational Framework: Evidence vs. Inference

| Category | What It Is | Examples |
|----------|-----------|---------|
| **Evidence** | What you directly observe or measure | Baseline energy bills, reporting-period meter data, OAT, fixture wattage, fan kW |
| **Inference** | What you conclude from evidence | Adjusted baseline model, the counterfactual, avoided energy use ("savings") |

**Savings are never evidence. Savings are always inference.**

### Factual / Counterfactual Matrix

|  | Pre-Implementation | Post-Implementation |
|--|-------------------|---------------------|
| **Evidence** (factual) | Baseline metered energy | Reporting-period metered energy |
| **Inference** (counterfactual) | — | Adjusted baseline model → avoided energy use |

---

## Story 1: "We're Doing Option B" — Measuring Everything, Concluding Nothing

A controls contractor wins a performance contract to replace three aging boilers at a 60,000 sf municipal building. The M&V plan says: "Option B — all parameters measured."

The engineer installs gas meters on each boiler, temperature sensors on every supply and return loop, a weather station on the roof, and flow meters on the hydronic piping. Twenty-two measurement points. The data acquisition system costs $44,000. Monthly reports run fifty pages.

Eight months in, the building owner asks: "Are the new boilers saving gas?"

The engineer pulls up a spreadsheet. Thousands of hourly readings. But no model. No adjusted baseline. No counterfactual.

Imagine he had the dataset above — 12 months of baseline HDD and gas consumption. He could see that in a month with 450 HDD, the old boilers consumed 210,692 therms. In the reporting period, a month with similar HDD shows lower consumption. But *how much lower than expected?* Without the regression — y = 173.08x + 111,372 — he has no way to answer. The model is what translates "450 HDD" into "the old system *would have used* 189,258 therms." The difference between 189,258 and what the meter actually read is the avoided energy use.

He has *evidence* — mountains of it. What he doesn't have is *inference*. He can tell you the lead boiler consumed 847 therms at 2 PM on February 12th. He cannot tell you what the old boiler *would have consumed* under those same conditions.

**What went wrong:** He read "all parameter measurement" as a hardware procurement list. He missed the two questions that retrofit isolation actually asks:

- **Does it perform?** (At commissioning — do the new boilers hit rated efficiency at design conditions?)
- **Does it keep operating?** (Across seasons — does efficiency hold as load varies from 14 HDD in July to 723 HDD in January?)

The first question needed a commissioning test. The second needed a model — even a simple relationship between boiler output and heating load — that creates a counterfactual against which to compare reporting-period performance.

The $44,000 in sensors could have been $8,000 in targeted metering with an analytical plan: meter gas input and heat output continuously, verify rated efficiency at commissioning, model the efficiency-vs-load relationship, compare reporting period to the modeled baseline.

**The confusion:** "Continuous performance verification" was reduced to "continuous measurement." Verification requires a counterfactual. Measurement alone is monitoring.

---

## Story 2: "We Have to Comply with IPMVP"

A state energy office issues an RFP for M&V services on 200 school buildings. The RFP says: "All M&V shall comply with IPMVP."

Two firms submit plans that read like compliance checklists. Every section header is a clause reference. The approach selection table has four rows: Option A, Option B, Option C, Option D. One firm proposes Option C for every building — not because a whole-facility inverse model fits every case, but because it's the only approach their software supports and the protocol doesn't say they can't.

A third firm submits something different. For each school cluster, they describe the ECMs and select the approach that fits the physics:

- **Lighting-only retrofits** → retrofit isolation with key parameter measurement. LED wattage doesn't drift. Stipulated hours. No regression needed — you don't need to model y = 173.08x + 111,372 to verify that a fixture draws 12 watts instead of 32.
- **Boiler replacements** → whole-facility inverse model. *This* is where the regression matters — you need the adjusted baseline to construct a counterfactual, because you can't isolate boiler savings from the gas meter without one.
- **The one school with a ground-source heat pump conversion** → calibrated simulation (forward model). The system interactions are too complex for a regression — a change in heating source changes the electric and gas signatures simultaneously in ways that confound a simple HDD model.

Their plan never mentions "Option A" or "Option C" in a heading. IPMVP appears in a methodology crosswalk appendix.

The state energy office scores the third firm highest. The program manager explains: "The first two firms showed me they could read a document. The third showed me they understood the buildings."

**What went wrong:** IPMVP is a *protocol* — a framework for structuring M&V decisions. It is not a building code. It has no mandatory provisions. There is no IPMVP inspector. You cannot "violate" it.

When practitioners treat it as a compliance document, they optimize for audit defensibility instead of analytical quality. They pick the Option that's easiest to justify on paper rather than the approach that matches the physics. The letters become a shield against professional judgment.

---

## Story 3: "Option C Is Regression, Option D Is Simulation"

An ESCO's M&V lead reviews approach selection for a university campus — central plant optimization, envelope upgrades, and a controls retrofit across 14 buildings.

The junior engineer's table:

| ECM | Option | Justification |
|-----|--------|--------------|
| Central plant | D | "Complex system, need simulation" |
| Envelope | C | "Whole building, use regression" |
| Controls | C | "Whole building, use regression" |

The senior engineer asks: "Why regression for the controls?"

"Whole facility means Option C. Option C means regression."

"Pull up the baseline gas data." The scatter plot appears — HDD vs. gas consumption, y = 173.08x + 111,372, R² = 0.9193. "This regression captures the relationship between weather and gas use. It works because heating load drives gas consumption in a predictable way. Now — the controls retrofit changes *when* the system runs, not *how much energy it uses per degree-day*. The slope doesn't change. The change points don't move. The schedules shift. What does the regression see?"

"...Nothing?"

"Exactly. The savings are real but invisible to an inverse model. The energy signature looks the same pre and post. You need a forward model — a simulation — that can represent the schedule changes and calculate the difference."

The letters created a false binary. "C" = regression, "D" = simulation. In reality, there's a spectrum:

| ← Data-driven | | | Physics-driven → |
|---|---|---|---|
| Simple linear regression | Change-point models (like the 173.08x + 111,372 HDD model) | Hybrid/gray-box models | Calibrated simulation |
| Minimal physics needed | Physical intuition (break points, slopes) | Physics structure + data fitting | Full physical description |
| Fast, cheap, transparent | Moderate effort | Specialized expertise | Expensive, time-consuming |
| Fails when savings are invisible to the meter | Works when energy signature changes shape | Bridges the gap | Works for any mechanism |

The campus project used a forward model for both the central plant and controls (physics drove the counterfactual) and a change-point regression for envelope (the heating slope shift was detectable — you could see it in the 173.08 coefficient dropping). No one needed to say "D, D, C." They needed to say: "Here's the inference method that produces a credible counterfactual for each ECM, and here's why."

---

## Story 4: "We Measured the Savings"

A utility program administrator presents results to the public utilities commission. The slide says: **"Measured savings: 12.4 GWh."**

A commissioner asks: "How do you measure savings?"

Consider the gas dataset above. Baseline year: 12 months of HDD and gas consumption. Reporting year: 12 more months, after the boiler retrofit. The administrator subtracted reporting-year totals from baseline-year totals and reported the difference as "measured savings."

But January in the baseline year had 723 HDD. January in the reporting year had 580 HDD. Of course gas went down — it was warmer. That's not savings, that's weather.

What the M&V professional actually did (or should have done):

1. **Measured** baseline gas consumption — the 12 rows in the table (evidence)
2. **Measured** reporting-period gas consumption (evidence)
3. **Built the regression** — y = 173.08x + 111,372 — from baseline data (inference)
4. **Fed reporting-period HDD into the model** to calculate what the old boilers *would have consumed* under reporting-period weather — the counterfactual (inference)
5. **Subtracted** actual from adjusted baseline to estimate avoided energy use (inference)

Steps 1 and 2 are measurement. Steps 3 through 5 are inference. The reported number is not a measured quantity — it's the output of a model. It depends on which variables were included (just HDD? or HDD + occupancy?), how the model was specified (linear? change-point?), and what professional judgments were made.

For a month with 580 HDD in the reporting period, the model predicts: 173.08 × 580 + 111,372 = **211,758 therms**. If the new boilers actually consumed 185,000 therms, the avoided energy use is 26,758 therms. That number came from the model, not from a meter.

**Why it matters:** When savings are called "measured," they inherit the authority of physical measurement. But savings have model uncertainty, parameter uncertainty, and specification uncertainty stacked on top of metering accuracy. Calling them "measured" closes the door on the question that matters most: *how confident are we in this number, and what would change it?*

The precise term is **avoided energy use**. "Savings" is fine as shorthand. "Measured savings" is not.
