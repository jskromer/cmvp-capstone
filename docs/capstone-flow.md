# Counterfactual HQ — Flow Document
*The arc one building takes through the full M&V process. Design brief for the demo.*

---

## Design Intent

One building. One student. Sixteen decisions.

The demo follows a single building from first site visit to final savings report. At each stage, the student faces a real decision — not a fill-in-the-blank, not a calculation — a judgment call they must defend.

The building is simple enough to explain in two sentences. The data is purpose-built to force each judgment. The tool makes the consequences of each decision visible.

**The through-line:** Every decision either narrows or widens the uncertainty band. By the end, the student can draw a line from their first denominator decision to the width of their final confidence interval. That's M&V.

---

## The Building

**Counterfactual Headquarters** — 12,000 sf single-story municipal building, mid-Atlantic climate (Zone 4A). Gas heat, DX cooling, LED lighting already in lobby, T8 fluorescents in office wing. One utility account each for electric and gas.

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

## The Flow

### STAGE 0 — BEFORE THE BASELINE

These two steps happen before any data is collected. They are the pre-conditions for a fair and relevant baseline. Skip them and everything downstream is built on sand.

---

**Step 0A: What Is This Building For? (The Denominator)**

*What the student does:* Identify why the building exists. What service does it provide? What is the correct denominator for measuring energy performance?

*From Kromer (2024):* "Energy management involves applying the fundamental laws of physics to energy systems with a goal of optimizing the value (services) produced per unit of energy consumed." The denominator is that value — not the energy.

*The judgment:* For Counterfactual Headquarters, the denominator is occupied hours of public service — the building exists to serve the community. Energy per occupied hour, or energy per conditioned square foot, are both defensible. Raw kWh consumption is not a fair metric on its own.

*What the demo shows:* A denominator selection prompt. Students choose from: total energy, energy per sf, energy per occupied hour, energy per occupant. The tool shows how the choice affects how "savings" will be framed in the final report.

*Teaching moment:* The denominator is not a technical decision — it is a stakeholder agreement. The ESCO wants a denominator that makes savings look large. The municipality wants one that reflects public value. The CMVP facilitates agreement before the baseline is built.

---

**Step 0B: Lifecycle Stage and Service Level Check**

*What the student does:* Assess where the building is in its lifecycle. Verify that the baseline period represents code-compliant, service-adequate operation.

*From Kromer (2024):* "The only fair and relevant baseline is one where the facility meets all codes, regulations, and service requirements." If the baseline was not meeting code, the savings claim starts from the wrong place.

*Lifecycle stage questions:*
- How old is the building and its systems?
- What is the remaining useful life of the equipment being replaced?
- Would this equipment have been replaced anyway within the performance period? (If yes: dual baseline consideration.)
- Were any systems operating below code during the baseline period?

*For Counterfactual Headquarters:*
- The T8 lighting is 18 years old — past effective useful life, but still functioning
- Lighting levels in the office wing are at the minimum acceptable lux (borderline code compliance)
- The RTU controls are original — no economizer, no scheduling optimization
- The building was operating to code, but at the minimum

*The judgment:* The lighting was code-compliant but at the floor. The LED retrofit will increase light levels slightly. Does that improvement in service level need to be accounted for in the baseline? The student must decide — and document it.

*What the demo shows:* A lifecycle checklist. Students answer questions about equipment age, RUL, and service levels. If red flags appear (e.g., below-code operation), the tool explains why the baseline must be adjusted before any savings can be claimed.

*Teaching moment:* A building that was not meeting code during the baseline period has a different "true" baseline than the meter data suggests. The savings from bringing the building to code are not attributable to the ECM — they are the cost of catching up to where the building should have been.

---

### STAGE 1 — CONTEXT

**Step 1: Stakeholder and Risk Map**

*What the student does:* Identify every party with a stake in the M&V outcome. Map each party to the four risk domains (Technical / Commercial / Legal / Regulatory).

*The judgment:* Who bears performance risk? (ESCO.) Who bears financial risk? (Municipality — they financed it.) How does that allocation change what M&V rigor is required?

*What the demo shows:* A stakeholder matrix. Students fill in risk domains. The tool reveals how risk allocation maps to M&V cost — higher performance risk on the ESCO → more rigorous continuous verification required.

*Teaching moment:* The ESCO wants conservative baselines. The municipality wants aggressive savings claims. The CMVP serves neither — the CMVP serves the agreement.

---

### STAGE 2 — APPROACH SELECTION

**Step 2: Choose an Approach for Each ECM**

*What the student does:* For ECM-1 (lighting) and ECM-2 (controls), select: retrofit isolation or whole facility? If retrofit isolation: key parameter measurement (stipulate) or continuous performance verification (ongoing metering)?

*The judgment:*
- ECM-1: Can we isolate the savings? Yes — the lighting circuits are on a dedicated panel. Key parameter measurement is sufficient — LED wattage doesn't drift.
- ECM-2: Can we isolate controls savings from the utility meter? No — the RTU serves the whole building. Whole facility inverse model required.

*What the demo shows:* A decision tree. Students select approach; the tool explains consequences — what gets measured, what gets stipulated, what uncertainty is introduced.

*Teaching moment:* Option letters (A/B/C/D) are not the answer. The physics of the ECM is the answer.

---

### STAGE 3 — MEASUREMENT BOUNDARY

**Step 3: Draw the Boundary**

*What the student does:* Using a single-line diagram of Counterfactual Headquarters, identify:
- The whole-facility meter (ECM-2 boundary)
- The lighting subpanel (ECM-1 boundary)
- What's inside and outside each boundary

*The judgment:* The lobby LEDs are already installed — are they inside or outside the ECM-1 boundary? The student must decide and document the assumption.

*What the demo shows:* An annotated single-line diagram. Students mark meter locations and boundary lines. The tool flags ambiguous loads (lobby LEDs, exterior lighting on the same panel).

*Teaching moment:* The boundary decision is made once and governs everything that follows. A poorly drawn boundary cannot be corrected after the fact without reopening the contract.

---

### STAGE 4 — BASELINE PERIOD AND DATA

**Step 4: Select the Baseline Period**

*What the student does:* Given 24 months of pre-retrofit utility data, select the baseline period. Examine the data for anomalies. Confirm the selected period reflects the service level and lifecycle stage established in Step 0B.

*The judgment:*
- How long? One full year minimum (coverage factor). Two years averages out weather variation.
- Which year? Year 2 shows a spike in month 8 — the community room ran 3 summer events. Is that representative of future operations?
- Does the selected period reflect normal, code-compliant operation — or does it include anomalous events that distort the baseline?
- If the lighting was dimmer than code during the baseline, does the baseline need adjustment before the ECM savings can be claimed?

*What the demo shows:* Time series of 24 months of electric and gas. Students select start/end. The tool calculates coverage factor, flags anomalies, and reminds students of the service level assessment from Step 0B. If students include the anomalous month, the model statistics degrade — they see why.

*Teaching moment:* The baseline period is not "the year before the project." It is the period that best represents expected future operations — at the agreed service level.

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
- Electric: 5P model fits well. But the auto-fit change points (38°F / 72°F) are mathematically optimal yet physically odd for this climate and building type. Should the student override to ~48°F / 65°F? Watch R² drop from 0.91 to 0.87. Is that acceptable?
- Gas: 3P model. CV(RMSE) = 16.2% — above ASHRAE G14's 15% threshold. Does that make it unusable? (No — G14 is a guideline, not a code. But the student must justify keeping it.)

*What the demo shows:* Interactive scatter plot with model overlay. Change-point sliders. GoF statistics update in real time. Students see the trade-off: physically defensible vs. statistically optimal.

*Teaching moment:* Statistics tell you how well the model fits the data. Physics tells you whether the model makes sense. A model that passes every test but violates basic physics is not a good model.

---

### STAGE 7 — STATIC FACTORS AND NRA PROTOCOL

**Step 7: Document Static Factors and Set NRA Triggers**

*What the student does:* List everything the model assumes is constant during the reporting period. Set measurable triggers for non-routine adjustments. Connect back to the lifecycle assessment from Step 0B — lifecycle events are the most common NRA triggers.

*The judgment:*
- Occupancy is a static factor. But the building hosts occasional large events. At what point does an occupancy spike require an NRA? 20% increase? Two consecutive months above threshold?
- The community room expansion (month 9) adds 1,200 sf and a new HVAC zone — a lifecycle event. It was known in advance. Should it be pre-documented as a planned NRA with a pre-agreed adjustment methodology?
- Equipment at end of useful life may degrade during the performance period. Is degradation a static factor or an NRA trigger?

*What the demo shows:* A static factor table. Students fill in factors and trigger thresholds. The tool flags which factors are most sensitive based on model coefficients, and highlights any lifecycle events flagged in Step 0B.

*Teaching moment:* Non-routine adjustments are not surprises — they are anticipated in a well-written M&V plan. The community room expansion was known before the plan was signed. Failing to pre-document it is a planning failure, not a reporting surprise.

---

### STAGE 8 — SAMPLING (ECM-1 LIGHTING)

**Step 8: Design the Fixture Sample**

*What the student does:* There are 180 T8 fixtures to be replaced. How many need to be measured post-installation to stipulate the wattage to the full population?

*The judgment:*
- Measure all 180? Unnecessary — LED wattage is highly consistent.
- Measure 10? Is that enough to establish a defensible CV?
- The sample CV determines the uncertainty contribution from the stipulated parameter.

*What the demo shows:* A sampling calculator. Students set sample size; the tool shows the expected CV and resulting uncertainty in stipulated wattage. A pre-loaded dataset of 20 fixture measurements lets them see how sample size affects the confidence interval — including two random draws of n=5 that return different means.

*Teaching moment (from Kromer, 2024):* "Two samples can return different results, even if both were collected following standard procedures. This is because sampling is inherently probabilistic." The spread between them is the uncertainty you carry into the savings estimate.

---

### STAGE 9 — METERING PLAN

**Step 9: Specify What Gets Metered**

*What the student does:* Build a metering specification table. For each parameter: what, where, type, interval, duration, who reads it.

*The judgment:*
- ECM-1: No ongoing metering needed — wattage stipulated, hours stipulated. One post-installation spot measurement per fixture sample.
- ECM-2: Whole-facility meters already in place — use them. But should a lighting subpanel meter be added to isolate ECM-1 and ECM-2 effects? Cost: ~$800. Value: separates interactive effects cleanly. Is it worth it given the M&V budget?

*What the demo shows:* A metering spec table students populate. The tool calculates estimated M&V cost and flags whether it exceeds the 3–5% rule of thumb.

*Teaching moment:* M&V costs money. Every meter is a trade-off between uncertainty reduction and budget. The CMVP must justify the expenditure to all parties.

---

### STAGE 10 — THE M&V PLAN

**Step 10: Assemble the Plan**

*What the student does:* Review a checklist of required M&V plan elements. Confirm all are present. Identify gaps.

*The judgment:* Is the plan specific enough to be enforced? Is it fair to both parties? Does it account for the denominator agreement (Step 0A), the service level baseline (Step 0B), and the pre-documented NRA (Step 7)?

*What the demo shows:* A structured plan outline with the student's decisions from Steps 0–9 pre-populated. Gaps flagged. Students review and sign off.

*Teaching moment:* The M&V plan is a contract document. Ambiguity in the plan becomes a dispute in the reporting period. Everything decided in Steps 0–9 must appear in the plan — including the denominator and the service level assumption.

---

### STAGE 11 — NRA DISCOVERY

**Step 11: Detect the Non-Routine Event**

*What the student does:* Examine reporting period time series. Identify the step change in month 9. Determine whether it requires a non-routine adjustment.

*The judgment:*
- Is the step change large enough to matter? (~12% increase in baseline-equivalent consumption.)
- Is it within the NRA trigger threshold set in Step 7? (Yes — the expansion was pre-documented.)
- How is the adjustment quantified? (Engineering estimate based on new sf and system type.)

*What the demo shows:* Time series with model prediction overlay. Step change visible in month 9. Toggle NRA on/off — savings bars flip from red to green.

*Teaching moment:* Without the NRA, the controls upgrade appears to have failed. With it, savings are real and positive. The model didn't fail — the building changed. This is exactly the situation the NRA protocol exists for — and the student wrote the protocol in Step 7.

---

### STAGE 12 — SAVINGS CALCULATION

**Step 12: Calculate Avoided Energy Use**

*What the student does:* Apply the adjusted baseline model to reporting period conditions. Calculate monthly avoided energy use for electric and gas separately.

*The judgment:*
- Gas went up in the reporting year. Does that mean the project failed? (No — the lighting retrofit reduced heat gain, increasing heating load. The controls saved gas; the lighting created a partial offset.)
- Should the interactive effect be quantified separately or reported as a net?

*What the demo shows:* Monthly savings bar chart — electric and gas separately, then combined. Prompt: "Gas went up — explain this to the building manager in one sentence."

*Teaching moment:* The counterfactual makes the gas increase legible. Without the model, the building manager sees a higher gas bill and concludes the project failed. With the model, they see exactly why it happened — and why it was expected.

---

### STAGE 13 — UNCERTAINTY

**Step 13: Quantify and Report Uncertainty**

*What the student does:* Combine uncertainty sources — model uncertainty (CV(RMSE)), metering uncertainty, sampling uncertainty (ECM-1 stipulated hours). Calculate fractional savings uncertainty.

*The judgment:* The FSU is 34% at 90% confidence. The savings are likely real but statistically marginal. Do you report it? Yes — always. The CMVP's obligation is transparency.

*What the demo shows:* Uncertainty budget table — each source, its magnitude, its contribution to total FSU. Savings range visualization at 90% confidence.

*Teaching moment:* Uncertainty is not failure. Hiding it is. A 34% FSU means the savings are plausible but not certain — that is an honest result, and it is what the stakeholders agreed to accept when they signed the M&V plan.

---

### STAGE 14 — VALUATION

**Step 14: Apply the Rate Structure**

*What the student does:* Convert avoided kWh and therms to dollars. Confront rate complexity.

*The judgment:*
- The controls upgrade shifted load timing — potentially reducing peak demand. Does the M&V plan account for demand savings?
- The blended rate ($0.105/kWh) is simple. The marginal rate varies by tier and season. Which is correct?
- What happens if rates change mid-performance period? The denominator (cost avoidance) shifts without the energy savings changing.

*What the demo shows:* The cost-avoidance calculator (`jskromer/cost-avoidance-calculator`) — students compare blended-rate valuation to marginal-rate valuation and see the error quantified.

*Teaching moment:* The counterfactual problem appears again — now in the bill, not the energy model. "What would the bill have been?" requires applying the correct rate to counterfactual consumption. Savings × average rate is almost always wrong.

---

## What the Demo Must Be

**Not:** A complex multi-tab app with hidden state and unclear navigation.

**Yes:** A linear flow. One screen per step. Each screen shows:
1. The decision the student faces (plain English)
2. The data or tool needed (chart, table, calculator)
3. The judgment call (open-ended, no single right answer)
4. The consequence (how it affects the next step)

**Format options (simplest first):**
1. Static HTML — one file per step, linked in sequence. No framework. Works offline.
2. Single-page app with accordion navigation — React or plain JS.
3. Streamlit — Python, fast to build, easy interactive charts.

---

## What Gets Built First

1. **The dataset** — 24 months baseline + 12 months reporting for Counterfactual Headquarters. The data IS the scenario.
2. **The scatter plots** — electric vs. OAT and gas vs. OAT. The student's first look at the building.
3. **The model fitter** — change-point sliders, live GoF statistics, borderline gas model.
4. **The time series with NRA** — the discovery moment.

Steps 0A, 0B, 1, 2, 3, 7, 9, 10 can be paper or simple forms. Interactive tools are needed only where data visualization adds something paper cannot.
