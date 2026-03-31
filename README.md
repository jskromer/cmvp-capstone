# Counterfactual HQ

A step-by-step M&V teaching demo that walks one building through the complete measurement and verification process — in sync with the CMVP course slides.

**One building. Fourteen decisions. Every step forces a judgment call.**

---

## What It Is

Counterfactual HQ is the interactive companion to the CMVP certification course. It follows a single building — Hartwell Community Center — from first site visit to final savings report.

At each stage, the student faces the same decision a practicing CMVP faces:
- What approach fits this ECM?
- How long should the baseline period be?
- Are these change points physically defensible?
- Is this model good enough?
- What triggers a non-routine adjustment?
- How do we explain a gas increase to the building owner?

The tool makes the consequences of each decision visible. The data is purpose-built to produce the right teaching moments.

---

## The Building

**Hartwell Community Center** — 12,000 sf municipal building, Zone 4A, two ECMs:
- **ECM-1:** LED lighting retrofit (retrofit isolation, key parameter measurement)
- **ECM-2:** HVAC controls upgrade (whole facility, inverse model)

---

## The Flow (14 Steps, In Sync With Slides)

| Step | Stage | Slide Section | Key Judgment |
|---|---|---|---|
| 1 | Stakeholder & risk map | Section 2 | Who bears what risk? |
| 2 | Approach selection | Sections 1, 6 | Retrofit isolation vs. whole facility |
| 3 | Measurement boundary | Section 6 | What's in, what's out |
| 4 | Baseline period | Section 4 | Is this period representative? |
| 5 | Descriptive statistics | Section 3.1 | Before inference — deterministic |
| 6 | Baseline model fitting | Sections 3.1, 5 | Physics vs. statistical optimum |
| 7 | Static factors + NRA protocol | Section 4 | What triggers an adjustment? |
| 8 | Sampling (lighting fixtures) | Section 3.1 | How many samples is enough? |
| 9 | Metering specification | Section 8 | How much M&V is enough? |
| 10 | M&V plan assembly | Section 7 | Is this plan enforceable? |
| 11 | NRA discovery | Section 4 | Anomaly or artifact? |
| 12 | Savings calculation | Section 9 | Why did gas go up? |
| 13 | Uncertainty | Sections 3.1, 5 | Transparent about limits |
| 14 | Valuation | Section 9 | Marginal rate vs. blended rate |

---

## Repository Structure

```
docs/
  capstone-flow.md        ← Full design brief, all 14 steps
  concept-map.md          ← Concept inventory from all 9 slide sections
  teaching-stories.md     ← Professional confusion case studies
  slides/                 ← CMVP course slide decks (9 sections)
  slide-extracts/         ← Markdown extracts (searchable, 313 slides)
  book/                   ← Kromer (2024), The Role of the M&V Professional
  reference/              ← Companion spreadsheets (statistics, OLS, sampling)
```

---

## Part of the GEARS Framework

Counterfactual HQ is the teaching layer of GEARS — Generic Energy Asset Risk Simulator.

**Counterfactual Designs** — Steve Kromer, PE, CMVP #1
*The Role of the Measurement and Verification Professional* (River Publishers, 2024)
