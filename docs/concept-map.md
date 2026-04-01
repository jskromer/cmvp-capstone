# Counterfactual HQ — Concept Map
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

**Descriptive Statistics**
The foundational insight from *The Role of the M&V Professional* (Kromer, 2024, p. 163):
> *"The beauty of descriptive statistics is that any two people who apply descriptive statistics to a set of data should arrive at the same answer."*

This is the first confidence-building step — before inference, before judgment. Descriptive statistics are deterministic.

- **Mean, median, mode** — central tendency; mean is the workhorse of M&V
- **Range, variance, standard deviation** — how spread out the data is
- **Coefficient of variation (CV)** — standard deviation ÷ mean, expressed as %; relative spread regardless of units
- **Skewness, kurtosis** — shape of the distribution; matters when normality is assumed

*Classroom example (from the book):* 10 motors, power outputs: 5.6, 4.9, 6.2, 5.8, 5.5, 4.7, 5.9, 6.1, 5.2, 5.4 kW.
Mean = 5.48 kW. Std dev = 0.459 kW. CV = 8.38%. Students compute this by hand before touching regression.

**Sampling**
From *The Role of the M&V Professional* (p. 164):
> *"Unlike descriptive statistics, sampling can lead to a range of 'answers.' Two samples can return different results, even if both were collected following standard procedures. This is because sampling is inherently probabilistic."*

- **Why we sample** — population (all fixtures, all motors) is too large to measure; a representative subset gives us a credible estimate
- **Random vs. stratified sampling** — how to make the subset representative
- **Sample size** — larger samples reduce uncertainty; at what point does cost outweigh precision gain?
- **Sampling uncertainty** — two valid samples from the same population can differ; the difference *is* the uncertainty
- **Application in M&V** — lighting fixture wattage (measure a sample, stipulate to the population); equipment inventories; multi-site programs

*Classroom example:* Take two random samples of 5 fixtures from the motor dataset above. Each sample returns a different mean. Both are correct. The spread between them is the uncertainty you carry into the savings estimate.

**Model Statistics**
- **CV(RMSE)** — how uncertain the model's predictions are; ASHRAE G14 thresholds (≤15% for monthly, ≤20–30% for less data)
- **NMBE** — normalized mean bias error; systematic over- or under-prediction; should be near zero
- **Regression** — the relationship between independent and dependent variables
- **R² (coefficient of determination)** — how much variance in energy use is explained by the model; necessary but not sufficient
- **Confidence intervals and levels** — how wide the uncertainty band is at a given probability
- **Fractional savings uncertainty (FSU)** — uncertainty in savings as a fraction of savings; "savings should be ≥ 2× RMSE"
- **Combining uncertainty** — Pythagorean: total uncertainty = √(U₁² + U₂²); example: 80 units before, 60 units after, 5% meter accuracy → 25% relative uncertainty on the 20-unit impact
- **Degrees of freedom** — each parameter estimated from the data costs one; why complex models with short baselines are risky
- **Bias vs. precision** — systematic error vs. random error; a biased model is unfair regardless of precision

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

---

## Descriptive Statistics, Sampling, and Tariffs
*From Kromer, The Role of the M&V Professional (River Publishers, 2024)*

### Descriptive Statistics

The key insight (p. 163): *"The beauty of descriptive statistics is that any two people who apply descriptive statistics to a set of data should arrive at the same answer."* This is the first confidence-building step — before inference, before judgment. Descriptive stats are deterministic.

Parameters: mean, median, mode, range, variance, standard deviation, CV, skewness, kurtosis.

**Classroom example from the book:** 10 motors, power outputs: 5.6, 4.9, 6.2, 5.8, 5.5, 4.7, 5.9, 6.1, 5.2, 5.4 kW.
Mean = 5.48 kW. Std dev = 0.459 kW. CV = 8.38%. Students compute this before touching regression.

### Sampling

Key insight (p. 164): *"Unlike descriptive statistics, sampling can lead to a range of 'answers.' Two samples can return different results, even if both were collected following standard procedures. This is because sampling is inherently probabilistic."*

- **Why we sample** — population too large to measure entirely; a representative subset gives a credible estimate
- **Sample size trade-off** — larger samples reduce uncertainty; at what point does cost outweigh precision?
- **Sampling uncertainty** — two valid samples from the same population can differ; that spread *is* the uncertainty
- **M&V application** — lighting fixture wattage (sample → stipulate to population); equipment inventories; multi-site programs

**Classroom example:** Take two random samples of 5 motors from the dataset above. Each returns a different mean. Both are valid. The spread between them is the uncertainty carried into the savings estimate.

→ JUDGMENT: How many samples are enough? When is the CV low enough to justify stipulation?

### Tariff and Valuation

The counterfactual rate problem (p. 201): *"What would the bill have been in the absence of the interventions? This requires agreement on valuation of a hypothetical baseline — complicated when energy rates are based on the amount consumed, as the marginal price may fluctuate."*

**Rate structure components:**
- **Energy charge ($/kWh)** — volumetric; what most people think of as "the rate"
- **Demand charge ($/kW-month)** — based on peak demand; can dominate commercial bills
- **Customer/fixed charge ($/month)** — immune to efficiency; high fixed charges reduce value of ECMs
- **Fuel adjustment clause** — variable adder; changes monthly
- **Blended rate** — total bill ÷ total kWh; simple but misleading for savings valuation

**Time-varying complexity:**
- **TOU rates** — a kWh saved at 4pm is worth more than one saved at 2am
- **Savings load shape** — *when* savings occur matters as much as *how much*; from the book: "the shape of the load profile before and after a retrofit can affect the value of the impact"
- **Tiered rates** — marginal rate for savings depends on which consumption tier applies
- **Duck curve / negative pricing** — in high-solar regions, midday prices can go negative; kWh metric breaks down; value shifts to peak reduction

**The high-fixed-charge problem** (p. 203): If the fixed charge is large and the energy rate is low, most of the bill is immune to efficiency action. The financial case for ECMs weakens even when the physics is clear.

**Judgment decisions in valuation:**

| Decision | What Makes It Hard |
|---|---|
| Which rate to apply to avoided energy? | Marginal rate varies by tier, time, season |
| Blended vs. time-differentiated? | Blended is wrong for TOU customers but simpler |
| How to value demand savings? | Need to know *when* peak occurs before and after |
| What emission factor? | Annual average vs. marginal vs. real-time — different stories |
| Rates change mid-contract | Counterfactual was built at old rates — must the model be revised? |

**The cost-avoidance calculator** (`jskromer/cost-avoidance-calculator`) — Streamlit tool demonstrating why naive savings × blended rate is wrong. Covers PG&E, SCE, Xcel TOU, and Hawaiian Electric flat rate. Use as the Step 14 valuation demonstration.

---

## Big Picture — What Is Energy Management, the Denominator, and Building Lifecycle
*From Kromer (2024), Sections 2.1.2–2.1.4; Section 1 slides*

### What Is Energy Management?

From *The Role of the M&V Professional* (p. xiii):
> *"Energy management is a practical means of ensuring that the costs and externalities of energy use are understood and mitigated. Common-sense energy management involves applying the fundamental laws of physics to energy systems with a goal of optimizing the value (services) produced per unit of energy consumed."*

And critically (p. xiv):
> *"M&V is the accounting system of energy management."*

Energy management is not about reducing consumption for its own sake. It is about optimizing the ratio of value produced to energy consumed. This sets up the denominator.

A better name for M&V would be **M, M & V** — measuring, modeling, and verification. The model is the most important element, not the meter.

### The Denominator Problem

From Kromer (2024), Section 2.1.3:

Every energy-consuming system exists for a reason *other* than consuming energy — to provide light, maintain comfort, manufacture goods, facilitate communications. The denominator is that reason. Energy is never the point; service is.

> *"You should consider service levels and productivity, not just raw energy inputs."*

**The core challenge:** What is the right denominator for this facility?

| Facility Type | Denominator Examples |
|---|---|
| Office building | Occupancy, conditioned area, productive hours |
| Hospital | Patient-days, air changes per hour (required by code) |
| Manufacturing | Units produced, throughput |
| Municipal building | Service hours, occupancy, public access |

**The denominator shapes the baseline.** If the facility was not meeting code or minimum service levels during the baseline period, the baseline is not fair. The only fair and relevant baseline is one where the facility operates to code and meets its intended service level.

From the book (p. 10):
> *"The only fair and relevant baseline is one where the facility meets all codes, regulations, and service requirements."*

This is a judgment call — and often a difficult one. Common situations:
- A building's lighting was below code before the retrofit. The "savings" from bringing it to code are not attributable to energy management.
- Equipment near end of life would have been replaced anyway. How much credit does the ECM get?
- COVID-19 changed outdoor air requirements mid-performance period. The baseline service level changed — the model must account for it.

**The denominator in the slides (Section 1, Slide 7):**

```
Energy / Denominator = KPI

Denominator options:
  Value
  Service
  Compliance (Code / Indoor Environment)
  Production
  Output
  Benefit
```

→ **JUDGMENT:** What is the denominator for this building, and is the baseline operating at the required service level?

### Building Lifecycle

From Kromer (2024), Section 2.1.4:

Every facility exists at a particular stage of its lifecycle. M&V decisions depend on where the building is in that lifecycle.

**Lifecycle phases:**
1. **Design** — energy model choices; new construction baselines; code compliance baseline
2. **Construction** — commissioning; installation verification
3. **Commissioning** — are systems functioning as designed?
4. **Operations** — ongoing M&V; the performance period; NRA detection
5. **Renovation / retrofit** — the moment of the ECM; baseline must be established before
6. **End of useful life** — remaining useful life (RUL) affects baseline choice; dual baseline considerations

**Why lifecycle matters for M&V:**

- **Remaining Useful Life (RUL):** If a boiler has 2 years left and would have been replaced anyway, what is the proper baseline? The "market transformation" baseline — what would the replacement have been under normal market conditions?
- **Code baselines:** If current codes require higher efficiency than the existing equipment, the baseline may be set at code-minimum, not existing conditions.
- **Dual baselines:** When the existing system would have been replaced mid-performance period regardless of the ECM, two baselines may be needed.

**From Section 1 slides — NIST Life Cycle Costing:** The financial framework for evaluating energy investments over their full life, not just the payback period. This is where M&V connects to the investment decision.

→ **JUDGMENT:** At what lifecycle stage is this facility? Does the existing baseline reflect code-compliant, service-adequate operation? If not, the baseline must be adjusted before any ECM savings can be claimed.

### How These Connect to the 14-Step Flow

These are not Step 1 — they are the stage-setting that makes Step 1 possible:

- **Before Step 1 (Context):** Understand what the building exists to do. Identify the denominator.
- **Before Step 4 (Baseline Period):** Confirm the baseline period represents code-compliant, service-adequate operation. If it doesn't, the baseline is not fair.
- **At Step 7 (Static Factors):** Lifecycle events (equipment replacement, renovation, occupancy change) are the most common triggers for non-routine adjustments.
- **At Step 14 (Valuation):** Lifecycle costing connects ECM savings to the investment decision — is the M&V result good enough to justify the capital?

The denominator and lifecycle are the **pre-conditions** for everything that follows. They are introduced first in the slides (Section 1) because without them, the counterfactual has no anchor.
