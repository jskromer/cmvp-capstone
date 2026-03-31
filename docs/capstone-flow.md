# Counterfactual HQ — Flow Document
*The arc one building takes through the full M&V process. Design brief for the demo.*

---

## Design Intent

One building. One student. Fourteen decisions.

The demo follows a single building from first site visit to final savings report. At each stage, the student faces a real decision — not a fill-in-the-blank, not a calculation — a judgment call they must defend.

The building is simple enough to explain in two sentences. The data is purpose-built to force each judgment. The tool makes the consequences of each decision visible.

**The through-line:** Every decision either narrows or widens the uncertainty band. By the end, the student can draw a line from their first boundary decision to the width of their final confidence interval. That's M&V.

---

## The Building

**Hartwell Community Center** — 12,000 sf single-story municipal building, mid-Atlantic climate (Zone 4A). Gas heat, DX cooling, LED lighting already in lobby, T8 fluorescents in office wing. One utility account each for electric and gas.

**Two ECMs under an ESPC contract:**
- **ECM-1: LED lighting retrofit** — office wing only, 180 fixtures. Retrofit isolation approach.
- **ECM-2: HVAC controls upgrade** — new DDC controls on the RTU; optimized setpoints and scheduling. Whole facility approach (controls savings invisible at the RTU level).

**Why this building works:**
- Small enough to describe completely in one page
- Two ECMs that require *different* approaches — forces the approach selection judgment
- Gas heat + DX cooling → 5P electric model, 3P gas model
- Controls upgrade → interactive effect (better scheduling reduces both heating and cooling)
- One NRA built in: a community event space added in month 9 of reporting year
- One stipulated parameter: lighting operating hours (steady, defensible, but still a judgment)

---

## The Fourteen Steps

### STAGE 1 — CONTEXT

**Step 1: Stakeholder and Risk Map**

*What the student does:* Identify every party with a stake in the M&V outcome. Map each party to the four risk domains.

*The judgment:* Who bears performance risk? (ESCO.) Who bears financial risk? (Municipality — they financed it.) How does that allocation change what M&V rigor is required?

*What the demo shows:* A stakeholder matrix. Students fill in risk domains. The tool reveals how risk allocation maps to M&V cost — higher performance risk on the ESCO → more rigorous continuous verification required.

*Teaching moment:* The ESCO wants conservative baselines. The municipality wants aggressive savings claims. The CMVP serves neither — the CMVP serves the agreement.

---

### STAGE 2 — APPROACH SELECTION

**Step 2: Choose an Approach for Each ECM**

*What the student does:* For ECM-1 (lighting) and ECM-2 (controls), select: retrofit isolation or whole facility? If retrofit isolation: performance (stipulate) or performance/operation (continuous)?

*The judgment:*
- ECM-1: Can we isolate the savings? Yes — the lighting circuits are on a dedicated panel. Key parameter measurement is sufficient — LED wattage doesn't drift.
- ECM-2: Can we isolate controls savings from the utility meter? No — the RTU serves the whole building. Whole facility inverse model required.

*What the demo shows:* A decision tree. Students select approach; the tool explains consequences — what gets measured, what gets stipulated, what uncertainty is introduced.

*Teaching moment:* Option letters (A/B/C/D) are not the answer. The physics of the ECM is the answer.

---

### STAGE 3 — MEASUREMENT BOUNDARY

**Step 3: Draw the Boundary**

*What the student does:* Using a single-line diagram of Hartwell, identify:
- The whole-facility meter (ECM-2 boundary)
- The lighting subpanel (ECM-1 boundary)
- What's inside and outside each boundary

*The judgment:* The lobby LEDs are already installed — are they inside or outside the ECM-1 boundary? The student must decide and document the assumption.

*What the demo shows:* An annotated single-line diagram. Students click to mark meter locations and boundary lines. The tool flags ambiguous loads (lobby LEDs, exterior lighting on the same panel).

*Teaching moment:* The boundary decision is made once and governs everything that follows. A poorly drawn boundary cannot be corrected after the fact without reopening the contract.

---

### STAGE 4 — BASELINE PERIOD AND DATA

**Step 4: Select the Baseline Period**

*What the student does:* Given 24 months of pre-retrofit utility data, select the baseline period. Examine the data for anomalies.

*The judgment:*
- How long? One full year minimum (coverage factor). Two years averages out weather variation.
- Which year? Year 2 shows a spike in month 8 — the community room ran 3 summer events. Is that representative of future operations?
- If you exclude month 8, you've changed the static factors. Document it.

*What the demo shows:* Time series of 24 months of electric and gas. Students select start/end. The tool calculates coverage factor and flags anomalies. If students include the anomalous month, the model statistics degrade — they see why.

*Teaching moment:* The baseline period is not "the year before the project." It is the period that best represents expected future operations.

---

### STAGE 5 — DESCRIPTIVE STATISTICS

**Step 5: Characterize the Baseline Data**

*What the student does:* Before fitting any model, describe what they have. Mean monthly electric and gas. Standard deviation. CV. Min/max. Scatter plots.

*The judgment:* None yet — this is the deterministic step. Two students with the same data get the same answer. This is intentional.

*What the demo shows:* Auto-computed descriptive statistics table. Scatter plots (electric vs. OAT, gas vs. OAT). Students observe the shape before the model is fit.

*Teaching moment (from Kromer, 2024):* "The beauty of descriptive statistics is that any two people who apply them to a set of data should arrive at the same answer." This is the last step before judgment enters. Everything after this involves inference.

*What to look for:* The electric scatter shows a clear 5-parameter shape. The gas scatter shows a 3-parameter heating-only shape. Students identify this before fitting.

---

### STAGE 6 — BASELINE MODEL

**Step 6: Fit and Validate the Model**

*What the student does:* Fit the baseline model. Evaluate goodness-of-fit statistics. Decide whether the model is acceptable.

*The judgment:*
- Electric: 5P model fits well. But the auto-fit change points (38°F / 72°F) are mathematically optimal yet physically odd. Should the student override to ~48°F / 65°F? Watch R² drop from 0.91 to 0.87. Is that acceptable?
- Gas: 3P model. CV(RMSE) = 16.2% — above ASHRAE G14's 15% threshold. Does that make it unusable? (No — G14 is a guideline, not a code. But the student must justify keeping it.)

*What the demo shows:* Interactive scatter plot with model overlay. Change-point sliders. GoF statistics update in real time. Students see the trade-off: physically defensible vs. statistically optimal.

*Teaching moment:* Statistics tell you how well the model fits the data. Physics tells you whether the model makes sense. A model that passes every test but violates basic physics is not a good model.

---

### STAGE 7 — STATIC FACTORS AND NRA PROTOCOL

**Step 7: Document Static Factors and Set NRA Triggers**

*What the student does:* List everything the model assumes is constant. Decide what change would require a non-routine adjustment. Set measurable triggers.

*The judgment:*
- Occupancy is a static factor. But the building hosts occasional large events. At what point does a spike in occupancy require an NRA? 20% increase? Two consecutive months above threshold?
- The community room expansion (month 9) will add 1,200 sf and a new HVAC zone. This is known in advance — should it be pre-documented as a planned NRA?

*What the demo shows:* A static factor table. Students fill in the factors and trigger thresholds. The tool flags which factors are most sensitive to change based on the model's coefficients.

*Teaching moment:* Non-routine adjustments are not surprises — they are anticipated in a well-written M&V plan. The surprise is not the event; it is failing to have a protocol for it.

---

### STAGE 8 — SAMPLING (ECM-1 LIGHTING)

**Step 8: Design the Fixture Sample**

*What the student does:* There are 180 T8 fixtures to be replaced. How many need to be measured post-installation to stipulate the wattage to the full population?

*The judgment:*
- Measure all 180? Unnecessary — T8 and LED wattage is highly consistent.
- Measure 10? Is that enough to establish a defensible CV?
- The sample CV will determine the uncertainty contribution from the stipulated parameter.

*What the demo shows:* A sampling calculator. Students set sample size; the tool shows the expected CV and resulting uncertainty in the stipulated wattage. A pre-loaded dataset of 20 fixture measurements lets them see how sample size affects the confidence interval.

*Teaching moment (from Kromer, 2024):* "Two samples can return different results, even if both were collected following standard procedures. This is because sampling is inherently probabilistic." The student sees this — two random draws of n=5 from the same dataset return different means.

---

### STAGE 9 — METERING PLAN

**Step 9: Specify What Gets Metered**

*What the student does:* Build a metering specification table. For each parameter: what is it, where is the meter, what type, what interval, how long, who reads it.

*The judgment:*
- ECM-1: No ongoing metering needed — wattage is stipulated, hours are stipulated. One post-installation spot measurement per fixture sample.
- ECM-2: The whole-facility electric and gas meters are already in place — use them. But should a lighting subpanel meter be added to separate ECM-1 and ECM-2 effects? Cost: ~$800. Value: isolates interactive effects. Is it worth it?

*What the demo shows:* A metering spec table students populate. The tool calculates estimated M&V cost based on metering choices and flags whether the cost exceeds the 3–5% rule of thumb.

*Teaching moment:* M&V costs money. Every meter is a trade-off between uncertainty reduction and budget. The CMVP must justify the expenditure to all parties.

---

### STAGE 10 — THE M&V PLAN

**Step 10: Assemble the Plan**

*What the student does:* Review a checklist of required M&V plan elements. Confirm all are addressed. Identify any gaps.

*The judgment:* Is the plan specific enough to be enforced? Is it fair to both parties? Would a third-party reviewer understand it without additional explanation?

*What the demo shows:* A structured plan outline with the student's decisions from Steps 1–9 pre-populated. Gaps are flagged. Students review and finalize.

*Teaching moment:* The M&V plan is a contract document. Ambiguity in the plan becomes a dispute in the reporting period.

---

### STAGE 11 — NRA DISCOVERY

**Step 11: Detect the Non-Routine Event**

*What the student does:* Examine reporting period time series data. Identify the anomaly in month 9. Determine whether it requires an NRA.

*The judgment:*
- Is the step change large enough to matter? (Yes — ~12% increase in baseline-period-equivalent consumption.)
- Is it within the NRA trigger threshold set in Step 7? (Yes — the community room expansion was pre-documented.)
- How do you quantify the adjustment? (Engineering estimate based on the new square footage and system type.)

*What the demo shows:* Time series with model prediction overlay. The step change in month 9 is visible. Students toggle the NRA on/off and see savings bars flip from red (negative) to green (positive).

*Teaching moment:* Without the NRA, the controls upgrade appears to have failed. With it, savings are real and positive. The model didn't fail — the building changed.

---

### STAGE 12 — SAVINGS CALCULATION

**Step 12: Calculate Avoided Energy Use**

*What the student does:* Apply the adjusted baseline model to reporting period conditions. Calculate monthly avoided energy use for electric and gas separately.

*The judgment:*
- The gas went up in the reporting year. Does that mean the project failed? (No — interactive effects from the lighting retrofit reduced heat gain, increasing heating load. The controls saved gas; the lighting created a small offset.)
- Should the interactive effect be quantified separately or reported as a net?

*What the demo shows:* Monthly savings bar chart — electric and gas separately, then combined. Interactive effect prompt: "Gas went up — explain this to the building manager in one sentence."

*Teaching moment:* The counterfactual makes the gas increase legible. Without the model, the building manager sees a higher gas bill and concludes the project failed. With the model, they see exactly what happened.

---

### STAGE 13 — UNCERTAINTY

**Step 13: Quantify and Report Uncertainty**

*What the student does:* Combine uncertainty sources — model uncertainty (CV(RMSE)), metering uncertainty, sampling uncertainty (ECM-1 stipulated hours). Calculate fractional savings uncertainty.

*The judgment:* The fractional savings uncertainty is 34% at 90% confidence. That means the savings are real but statistically marginal. Do you report it? Yes — the CMVP's obligation is transparency.

*What the demo shows:* Uncertainty budget table — each source, its magnitude, its contribution to total FSU. A visualization of the savings range at 90% confidence.

*Teaching moment:* Uncertainty is not failure. A 34% FSU on a 15% savings project means the savings are likely real but not statistically certain. That's an honest result. Hiding it is not.

---

### STAGE 14 — VALUATION

**Step 14: Apply the Rate Structure**

*What the student does:* Apply the utility rate schedule to convert kWh and therms into dollars. Confront the tariff complexity.

*The judgment:*
- The electric rate has a demand charge — the controls upgrade shifted load timing, potentially reducing peak demand. Does the M&V plan account for demand savings?
- The blended rate ($0.105/kWh) is simple. The actual marginal rate varies by tier and season. Which is appropriate?
- At what point in the contract does the rate lock? What if rates increase mid-performance period?

*What the demo shows:* The cost-avoidance calculator (from `jskromer/cost-avoidance-calculator`) embedded or linked. Students compare blended-rate valuation to marginal-rate valuation. The error between them is visible and quantified.

*Teaching moment:* The counterfactual problem appears again — not just in the energy model, but in the bill. "What would the bill have been?" requires applying the correct rate to counterfactual consumption, not just multiplying savings by average rate.

---

## What the Demo Must Be

**Not:** A complex multi-tab React app with hidden state and unclear navigation.

**Yes:** A linear flow. One screen per step. Each screen shows:
1. The decision the student faces (in plain English)
2. The data or tool they need to make it (chart, table, calculator)
3. The judgment call (open-ended question, no single right answer)
4. The consequence of their choice (how it affects the next step)

The student moves forward through 14 steps. Each step builds on the last. At the end, they have a complete M&V plan and a savings report for Hartwell Community Center.

**Format options (simplest first):**
1. Static HTML — one file per step, linked in sequence. No framework. Loads instantly, works offline.
2. Single-page app with tab or accordion navigation — React or plain JS.
3. Streamlit — Python, fast to build, easy to add interactive charts.

**The data:** Twelve months of purpose-built monthly electric and gas data for Hartwell. Designed to produce a 5P electric model, a borderline 3P gas model, a visible NRA in month 9, and an interactive effect that makes gas go up. Generated analytically — no EnergyPlus required.

---

## What Gets Built First

1. **The Hartwell dataset** — 24 months baseline + 12 months reporting, as a CSV. The data IS the scenario.
2. **The scatter plots** — electric vs. OAT and gas vs. OAT. The student's first look at the building.
3. **The model fitter** — change-point sliders, live GoF statistics, the borderline gas model.
4. **The time series with NRA** — the discovery moment.

Everything else (stakeholder matrix, metering spec, plan checklist) can be paper or a simple form. The interactive tools are needed only where data visualization adds something paper cannot do.
