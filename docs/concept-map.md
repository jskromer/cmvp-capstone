# CMVP Concept Map — All Sections
*Derived from slide extracts, Sections 1.0–9.0. Scaffold for building scenario design.*

---

## The Central Spine

Every concept in the course connects back to one question:

> **"How do we know what WOULD have happened?"**

The answer is always: we cannot measure it. We must infer it.
That inference — the adjusted baseline model — is the counterfactual.
Everything else is either how we build it, how we govern it, or how we communicate it.

---

## Concept Inventory by Section

### Section 1 — Fundamental Concepts
- **The counterfactual** — the world that didn't happen; the baseline adjusted to reporting conditions
- **Evidence vs. inference** — baseline data is evidence; savings are always inference
- **Statistical model (inverse)** — observed data → inferred relationships; runs backward from data
- **Physical model (forward)** — physical parameters → predicted energy; runs forward from inputs
- **Avoided energy use** — the output of the inference; not "measured savings"
- **KPIs** — what the project is actually optimizing for (energy, cost, carbon, comfort)
- **Professional judgment** — present from the first decision; cannot be eliminated

### Section 2 — Contextual Considerations
- **Four risk domains** — Technical / Commercial / Legal / Regulatory; every project has all four
- **ESPC** — Energy Savings Performance Contract; the ESCO finances, building owner repays from savings
- **Guaranteed vs. shared savings** — who bears performance risk; shapes every M&V decision
- **Stakeholder map** — owner, ESCO, regulator, utility, lender, occupants; all have different needs
- **Guiding principles** — Accurate, Complete, Conservative, Consistent, Relevant, Transparent
- **Communication as the master principle** — protocols are secondary to mutual understanding
- **Risk and cost** — M&V cost is directly proportional to risk allocation; more risk = more rigor
- **M&V 2.0** — AMI data + automated analytics; changes what's feasible but not what's required
- **Utility programs vs. ESPCs** — different risk structures, different reporting requirements

### Section 3.1 — Statistics Foundation
- **Descriptive statistics** — mean, variance, standard deviation, CV; describe what you have
- **CV(RMSE)** — how uncertain the model's predictions are; ASHRAE G14 sets thresholds
- **NMBE** — normalized mean bias error; whether the model systematically over- or under-predicts
- **Sampling** — why we don't measure everything; trade-off between cost and precision
- **Regression** — the relationship between independent and dependent variables
- **R² (coefficient of determination)** — how much variance is explained by the model
- **Confidence intervals and levels** — how wide the uncertainty band is at a given probability
- **Fractional savings uncertainty (FSU)** — uncertainty in savings as a fraction of savings; the key risk metric
- **Combining uncertainty** — Pythagorean: total uncertainty = √(U₁² + U₂²)
- **Degrees of freedom** — what constrains the model; why more parameters cost you
- **Bias vs. precision** — systematic error vs. random error; both matter, differently

### Section 4 — Baseline and Adjustments
- **Three distinct "baseline" concepts** — period (when), data (what was measured), model (the inference engine)
- **Coverage factor** — the model must cover the full range of expected operating conditions (ASHRAE: ≥90%)
- **Independent variable** — what drives energy use (OAT, HDD, occupancy, production)
- **Static factor** — what the model assumes is constant and won't change during reporting period
- **Routine adjustment** — expected changes to independent variables (weather, season); built into the model
- **Non-routine adjustment (NRA)** — unexpected change to a static factor; requires explicit correction
- **Avoided energy use** — adjusted baseline minus actual reporting period consumption
- **Normalized savings** — both periods adjusted to "typical" conditions; useful for long-term comparison
- **Backcasting** — rare; reporting period model applied to baseline conditions; used when baseline data is weak
- **Remaining/Effective Useful Life (RUL/EUL)** — affects whether a "dual baseline" is appropriate
- **Code baseline** — what "should have happened" under current standards; relevant for new construction
- **Realization rate** — actual impact vs. estimated impact; ex-ante vs. ex-post comparison

### Section 5 — Whole Facility Approaches
- **Whole facility** — the utility meter is the measurement boundary; captures all ECM effects simultaneously
- **Statistical / inverse model** — regression-based; fits curves to observed data
- **Physical / forward model** — simulation-based; encodes engineering first principles
- **Significant parameters** — variables that meaningfully drive energy use; must be identified before modeling
- **Proxy variable** — a measurable stand-in for a significant parameter that's hard to measure directly
- **Stepwise analysis / parameter sweep** — systematic tests to find which inputs matter most
- **Sensitivity analysis** — rank inputs by their influence on output; guides where to spend metering budget
- **Interactive effects** — one ECM changes the energy signature of another (lighting → cooling load)
- **Fractional savings uncertainty** — ratio of savings uncertainty to total savings; "savings should be ≥ 2× RMSE"
- **Load shape** — distribution of energy use over time; matters for TOU rates and demand charges

### Section 6 — Retrofit Isolation
- **Measurement boundary** — drawn around the specific equipment or system being evaluated
- **Single line diagram** — the map; shows where power flows and where meters can go
- **Performance approach** — snapshot measurement of key parameters at installation; rest stipulated (cf. Option A)
- **Performance/operation approach** — continuous measurement of all key parameters through reporting period (cf. Option B)
- **Significant parameter** — must be measured (or justified if estimated)
- **Estimable parameter** — can be stipulated if stable, justifiable, and auditable
- **Stipulation** — replacing measurement with professional judgment; acceptable when parameter is stable and cost of measuring outweighs value
- **Interactive effects** — lighting reduces heat gain, which reduces cooling load; must account for or consciously ignore
- **Savings attribution** — with multiple ECMs on one system, which ECM gets credit?
- **Field skills** — site visits, single-line reading, meter placement, safety; M&V is physical work

### Section 7 — Planning
- **M&V plan** — the agreement; must be signed before implementation; governs the entire performance period
- **Operational verification** — confirming ECMs were installed and are functioning as designed
- **Commissioning** — broader process of verifying systems perform to design intent
- **Post-installation report** — documents what was actually installed vs. what was planned
- **Annual report** — reports savings for the year; triggers payment in performance contracts
- **Risk and responsibility matrix** — who owns what risk; who does what, when
- **Cost-benefit of M&V** — industry rule of thumb: 3–5% of project cost; more complex ECMs warrant more
- **Stakeholder agreement** — the plan is only as good as the consensus around it

### Section 8 — Metering Considerations
- **Meter types** — billing meters, sub-meters, portable meters, BMS/SCADA data points
- **Calibration** — meters drift; calibration frequency depends on accuracy requirements
- **Measurement accuracy** — what the meter claims; vs. what it actually delivers in the field
- **Data acquisition** — how data gets from the meter to the analyst; gaps, corruption, transmission errors
- **Sampling vs. continuous** — when is a short measurement campaign sufficient vs. ongoing monitoring required
- **Metering duration** — must capture the full range of operating conditions (coverage factor)
- **Data quality and cleaning** — outlier identification, gap filling, plausibility checks; judgment-heavy
- **BMS/SCADA** — existing building data infrastructure; often already collecting useful parameters

### Section 9 — Reporting
- **Savings calculation** — apply the adjusted baseline model; report avoided energy use
- **Valuation** — convert kWh/therms to dollars and/or CO₂; apply correct rate structures
- **Transparency** — show your work; the model, the inputs, the assumptions, the uncertainty
- **Operational verification reporting** — confirm ongoing ECM function, not just savings
- **Dispute resolution** — what happens when parties disagree on the model or the adjustment
- **Audit trail** — every number traceable to its source; the CMVP's professional protection

---

## Technical vs. Judgment — The Full Map

This is the most important distinction in the course.
From Steve Kromer's *The Role of the M&V Professional* (River Publishers, 2024): the CMVP's value is not in running calculations — it is in making defensible decisions that others will rely on and, when necessary, contest.

### Technical (Procedural — can be learned from a manual)
| Task | Where It Appears |
|---|---|
| Running regression calculations | Section 3.1, 5 |
| Computing R², NMBE, CV(RMSE) | Section 3.1, 5 |
| Applying routine adjustments (weather normalization) | Section 4 |
| Calculating avoided energy use (model minus actual) | Sections 4, 9 |
| Combining uncertainty with Pythagorean method | Section 3.1 |
| Installing and reading meters | Section 8 |
| Applying rate structures to get cost savings | Section 9 |
| Building a regression in Excel or software | Sections 3.1, 5 |

### Judgment (Professional — requires experience, context, and accountability)
| Decision | Where It Appears | What Makes It Hard |
|---|---|---|
| **How long should the baseline period be?** | Section 4 | Must cover full range of conditions; too short = unrepresentative |
| **Which approach — retrofit isolation or whole facility?** | Sections 5, 6 | Depends on ECM physics, metering access, contractual risk |
| **Which parameters are "significant"?** | Sections 5, 6 | Requires engineering understanding of how the system works |
| **What can be stipulated vs. must be measured?** | Section 6 | Balance between cost, risk, and defensibility |
| **What model form — 3P, 5P, linear, physical?** | Sections 3.1, 5 | The data won't tell you; physics and professional judgment do |
| **Where to set change points?** | Sections 3.1, 5 | Math gives optimal; physics gives defensible — they differ |
| **When is a model "good enough"?** | Sections 3.1, 5 | G14 thresholds exist but judgment is always required for borderline cases |
| **What are the static factors?** | Sections 4, 5 | Requires knowing the building, the contract, and what's likely to change |
| **What triggers a non-routine adjustment?** | Section 4 | Requires monitoring, engineering judgment, and contractual clarity |
| **Are interactive effects significant enough to measure?** | Sections 5, 6 | Cost-benefit judgment; physics estimate vs. metering expense |
| **How long must we meter?** | Sections 6, 8 | Coverage factor vs. cost; seasonal systems need full-cycle data |
| **What is the measurement boundary?** | Sections 4, 5, 6 | Sets the scope of every calculation that follows |
| **How do we communicate uncertainty to a non-technical client?** | Sections 1, 2, 9 | Requires translation between statistical and contractual language |
| **Is this NRA permanent or temporary?** | Section 4 | Changes whether you adjust the baseline or just the reporting period |
| **When does a dispute warrant third-party review?** | Sections 2, 9 | Risk management, relationship management, and professional ethics |

---

## The Step-by-Step Journey of One Building

This is the arc every capstone scenario should follow:

```
1. CONTEXT
   Who are the stakeholders? What type of contract?
   What are the four risk domains for this project?
   → JUDGMENT: Who bears what risk? What does that imply for M&V rigor?

2. APPROACH SELECTION
   What ECMs? Can they be isolated or not?
   → JUDGMENT: Retrofit isolation vs. whole facility for each ECM

3. MEASUREMENT BOUNDARY
   Where does the measurement begin and end?
   Single line diagram: where are the meters?
   → JUDGMENT: What's in, what's out, what are we ignoring?

4. BASELINE PERIOD AND DATA
   How long? Which period? Any anomalies?
   → JUDGMENT: Is this period representative of future operations?

5. SIGNIFICANT PARAMETERS AND STATIC FACTORS
   What drives energy use in this building?
   What will stay constant during the reporting period?
   → JUDGMENT: What to model, what to stipulate, what to monitor

6. BASELINE MODEL
   Build the model. Evaluate GoF statistics.
   → TECHNICAL: Regression, R², NMBE, CV(RMSE)
   → JUDGMENT: Is this model defensible? Are the change points physical?

7. NON-ROUTINE ADJUSTMENT PROTOCOL
   What could change during the reporting period?
   How will we detect and quantify it?
   → JUDGMENT: What thresholds trigger an adjustment?

8. METERING PLAN
   What gets metered? Where? What type? How long?
   → JUDGMENT: How much M&V is enough for this level of risk?

9. M&V PLAN (THE AGREEMENT)
   Write it. Get sign-off before implementation.
   → JUDGMENT: Is this plan fair to all parties?

10. IMPLEMENTATION AND OPERATIONAL VERIFICATION
    Were the ECMs installed as designed?
    → TECHNICAL: Commissioning checks, post-installation report

11. REPORTING PERIOD DATA COLLECTION
    Collect data. Clean it. Watch for NRAs.
    → TECHNICAL: Data management, meter reading
    → JUDGMENT: Is this data plausible? Are there anomalies?

12. SAVINGS CALCULATION
    Apply adjusted baseline model.
    Calculate avoided energy use.
    → TECHNICAL: Model × reporting conditions - actual consumption
    → JUDGMENT: Does this number make physical sense?

13. VALUATION AND REPORTING
    Convert to dollars and CO₂.
    Document uncertainty.
    Communicate to all stakeholders.
    → TECHNICAL: Rate application, uncertainty propagation
    → JUDGMENT: How do we explain this to a county manager?

14. DISPUTE RESOLUTION (IF NEEDED)
    Who is right? What does the contract say?
    → JUDGMENT: Professional ethics, transparency, third-party role
```

---

## What the Simpler Building Must Demonstrate

The building scenario doesn't need to be complex.
It needs to force each judgment decision above.

**Minimum requirements:**
- At least two ECMs — one isolable (lighting or VFD), one not (envelope or whole HVAC system)
- Monthly utility data — electric and gas, 12 months baseline + 12 months reporting
- A visible change-point shape in the electric data (5P or 3P)
- A gas model that's borderline on CV(RMSE) — teaches "good enough" judgment
- One non-routine adjustment event — something changed mid-reporting period
- An interactive effect — one ECM affects the other's energy signature
- One stipulated parameter — forces the "measure vs. estimate" judgment

**The building can be small.** The data does the teaching.
