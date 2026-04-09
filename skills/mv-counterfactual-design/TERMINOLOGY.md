# M&V Terminology Reference

## The Foundational Distinction: Evidence vs. Inference

| Category | What It Is | Examples |
|----------|-----------|---------|
| **Evidence** | What you directly observe or measure | Baseline energy bills, reporting-period meter data, OAT, fixture wattage, fan kW |
| **Inference** | What you conclude from evidence | Adjusted baseline model, the counterfactual, avoided energy use ("savings") |

**Savings are never evidence. Savings are always inference.**

You can measure baseline energy (evidence). You can measure reporting-period energy (evidence). But you can never measure what would have happened without the ECM -- that is the counterfactual, and it must be inferred.

## Factual / Counterfactual Matrix

|  | Pre-Implementation | Post-Implementation |
|--|-------------------|---------------------|
| **Evidence** (factual) | Baseline metered energy | Reporting-period metered energy |
| **Inference** (counterfactual) | -- | Adjusted baseline model -> avoided energy use |

## Primary Terminology

| Approach | Method | IPMVP Cross-Reference |
|----------|--------|-----------------------|
| Retrofit isolation | Key parameter measurement (some parameters stipulated) | cf. Option A |
| Retrofit isolation | Continuous performance verification (performance + operation over time) | cf. Option B |
| Whole facility | Statistical / inverse model (regression-based, observed data -> inferred relationships) | cf. Option C |
| Whole facility | Calibrated simulation / forward model (physics-based, physical parameters -> predicted energy) | cf. Option D |

## Performance vs. Operation -- The Retrofit Isolation Distinction

| Question | Method | What It Proves | Example |
|----------|--------|---------------|---------|
| **Does it perform?** | Key parameter measurement -- snapshot at installation, remaining parameters stipulated | ECM installed correctly and functions as designed | Lighting: measure fixture wattage, stipulate operating hours |
| **Does it keep operating?** | Continuous performance verification -- ongoing measurement through reporting period | ECM continues to deliver savings over time under varying conditions | VFDs: continuously meter fan kW, speed, airflow across seasons |

## Inverse and Forward Models -- Matched Pair

| Direction | Name | What It Does | Tools |
|-----------|------|-------------|-------|
| **Inverse** | Statistical / inverse model | Observed data -> inferred relationships | Regression, change-point models |
| **Forward** | Calibrated simulation / forward model | Physical parameters -> predicted energy | EnergyPlus, eQUEST, DOE-2 |

Both are inference methods. They run in different directions.

## Substitution Table

| Use This | Not This | Notes |
|----------|----------|-------|
| Whole facility approach | Option C | Primary label in all contexts |
| Retrofit isolation approach | Option A / Option B | Distinguish by measurement method, not letter |
| Key parameter measurement | Simplified measurement | Snapshot + stipulation |
| Continuous performance verification | All parameter measurement | Performance + operation over time |
| Inverse model | Statistical model (alone) | Emphasizes direction: observed -> inferred |
| Forward model | Physical model (alone) | Emphasizes direction: parameters -> predicted |
| Deemed savings | -- | Explicitly "not M&V"; no measurement during performance period |
| Adjusted baseline model | Counterfactual | Both acceptable; the model is the inference engine |
| Avoided energy use | Energy savings | "Avoided energy use" is technically precise; "savings" is acceptable shorthand |
| Static factor | Fixed parameter | Does not change between baseline and reporting periods |
| Dynamic factor | Variable parameter | Changes and must be modeled |
| Non-routine adjustment (NRA) | Non-routine event | The adjustment is what the CMVP does; the event triggers it |
| Evidence | Data, measurements | What you directly observe or measure |
| Inference | Estimate, prediction | What you conclude from evidence |

## Rules

1. Lead with descriptive terms in all output
2. IPMVP references appear only as parenthetical cross-references -- e.g., "(cf. IPMVP Option B)"
3. Never use Options A/B/C/D as standalone labels
4. Deemed savings is not M&V -- always distinguish
5. When the performance/operation distinction arises, surface it
6. When referencing models, use the inverse/forward pairing
