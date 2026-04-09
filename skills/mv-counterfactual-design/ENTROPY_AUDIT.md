# Entropy Audit Template

## Purpose

An entropy audit is a structured accounting of where uncertainty lives in an M&V plan, who owns it, and whether it is being honestly represented. Conduct this audit before finalizing any M&V approach.

**Guiding principle:** Before arguing about price, audit where the entropy lives.

## The Three Entropy Sources

### 1. Physical Entropy

**Source:** Weather, occupant behavior, load variation, equipment degradation.
**Owner:** Nobody -- this is the irreducible uncertainty of the physical world.

| Assessment Question | Low | Medium | High |
|---|---|---|---|
| How weather-sensitive is the building? | Baseload-dominated | Mixed heating/cooling | Extreme climate, high OAT sensitivity |
| How variable is occupancy? | Fixed schedule, stable tenant | Some variation, predictable | Highly variable, multi-tenant turnover |
| How stable are internal loads? | Constant process loads | Seasonal variation | Unpredictable equipment changes |
| Equipment degradation risk? | New equipment, warranty | Mid-life, maintained | Aging systems, deferred maintenance |

**Physical entropy determines the floor of achievable model accuracy.** No model can do better than the physical noise in the system.

### 2. Model Entropy

**Source:** Baseline period selection, variable selection, functional form, over/under-fitting.
**Owner:** The CMVP / M&V designer.

| Assessment Question | Low | Medium | High |
|---|---|---|---|
| Is the baseline period representative? | 12+ months, no anomalies | Minor gaps or anomalies | Short period, significant anomalies |
| Are the right independent variables included? | OAT + known drivers, validated | OAT only, reasonable fit | Missing known drivers, poor fit |
| Is the model form appropriate? | Change-point matches physical behavior | Adequate but simplified | Wrong functional form for the system |
| Is the model over-fit or under-fit? | CV(RMSE) within thresholds, residuals clean | Marginal statistics | Fails diagnostic checks |
| Are stipulated values defensible? | Measured or industry-standard | Reasonable but unverified | Arbitrary or favorable to one party |

**Model entropy is the CMVP's responsibility.** Overfitting, baseline sculpting, and aggressive variable selection are not just bad practice -- they are unaudited information injection.

### 3. Governance Entropy

**Source:** Change protocols, adjustment triggers, dispute resolution mechanisms, contract ambiguity.
**Owner:** The contract / institutional framework.

| Assessment Question | Low | Medium | High |
|---|---|---|---|
| Are NRA triggers clearly defined? | Written protocol with thresholds | General guidance exists | Undefined -- decided ad hoc |
| Is there a dispute resolution process? | Third-party review mechanism | Informal process | No mechanism |
| Are adjustment methods pre-agreed? | Calculation methods specified | Methods referenced but not detailed | Left to future negotiation |
| Who decides if conditions have changed? | Joint review with defined criteria | One party decides, other can appeal | No defined process |
| Are reporting requirements clear? | Format, frequency, content specified | General requirements | Undefined |

**Governance entropy determines whether the M&V plan survives contact with reality.** A technically perfect model with ambiguous governance will generate disputes.

## Conducting the Audit

### Step 1: Rate Each Source
For each entropy source, rate overall as Low / Medium / High based on the assessment questions above.

### Step 2: Identify the Dominant Source
Which entropy source contributes most to total uncertainty? This determines where effort should be focused.

| Dominant Source | Action |
|---|---|
| Physical | Accept it. Widen confidence intervals. Do not over-model. |
| Model | Improve the model. Extend baseline, add variables, validate functional form. |
| Governance | Strengthen the contract. Define NRA protocols, dispute mechanisms, reporting requirements. |

### Step 3: Document the Audit

```
PROJECT: [name]
DATE: [date]
AUDITOR: [name]

PHYSICAL ENTROPY:  [Low / Medium / High]
  Key driver: [description]
  Implication: [what this means for model accuracy]

MODEL ENTROPY:     [Low / Medium / High]
  Key driver: [description]
  Implication: [what this means for baseline reliability]

GOVERNANCE ENTROPY: [Low / Medium / High]
  Key driver: [description]
  Implication: [what this means for plan durability]

DOMINANT SOURCE: [Physical / Model / Governance]
RECOMMENDED ACTION: [specific next step]
```

### Step 4: Maximum Entropy Check

**The maximum entropy principle as an ethical rule:** Do not inject unaudited assumptions. Ask:

- Are any stipulated values suspiciously favorable to one party?
- Does the model complexity exceed what the data can support?
- Are adjustment methods designed to minimize reported savings uncertainty, or to honestly represent it?

If the answer to any of these is concerning, the plan needs revision before proceeding.
