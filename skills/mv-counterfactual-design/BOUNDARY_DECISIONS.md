# Boundary Decision Guide

## The Three Decision Axes

Every M&V approach is defined by three choices. These are not independent -- each constrains the others.

## Axis 1: Boundary

### Decision Tree

```
Is the ECM isolated to a single system with dedicated metering?
├── YES: Can you meter the isolated system cost-effectively?
│   ├── YES -> Retrofit isolation boundary
│   └── NO  -> Consider whole facility if savings are detectable at the meter
└── NO: Are multiple interactive ECMs being implemented?
    ├── YES -> Whole facility boundary (interactions captured automatically)
    └── NO  -> Assess: is the single ECM large enough to detect at the facility meter?
        ├── YES -> Whole facility boundary
        └── NO  -> Retrofit isolation with sub-metering
```

### Key Considerations

- **Whole facility** captures interactive effects automatically but requires savings large enough to detect above baseline noise
- **Retrofit isolation** gives cleaner attribution but misses cross-system interactions (e.g., lighting heat contributing to HVAC load)
- **Interactive effects**: When one ECM affects another system's energy use (e.g., LED retrofit reduces cooling load), whole facility boundary captures this; isolation boundary misses it unless explicitly modeled

### The IDF Connection

The IDF defines every variable in the building model. Each variable is classified as:
- **Static**: Does not change between periods (inside the boundary, held constant)
- **Dynamic**: Changes and must be modeled (the independent variables in regression)
- **NRA candidate**: May change non-routinely, requiring adjustment
- **Stipulated**: Agreed by contract rather than measured

The boundary decision determines which IDF variables fall inside vs. outside the model.

## Axis 2: Model Form

### Decision Tree

```
Do you have 12+ months of reliable utility data for the baseline?
├── YES: Is the building's energy behavior primarily weather-driven?
│   ├── YES -> Inverse model: change-point regression (3PC, 5P, 3PH)
│   │         against outdoor air temperature
│   └── NO  -> Inverse model with additional independent variables
│             (production, occupancy, etc.)
├── NO: Do you have detailed physical specifications of the building?
│   ├── YES -> Forward model: calibrated simulation (EnergyPlus, eQUEST)
│   └── NO  -> Gather more data before proceeding
└── PARTIAL: Consider hybrid approach
    - Forward model for systems without historical data
    - Inverse model for systems with good metered history
```

### Model Form Reference

| Form | Input | Output | Best For |
|------|-------|--------|----------|
| 3-Parameter Cooling (3PC) | OAT | kWh | Cooling-dominated buildings |
| 5-Parameter (5P) | OAT | kWh or therms | Buildings with both heating and cooling |
| 3-Parameter Heating (3PH) | OAT | therms | Heating-dominated buildings |
| Mean model | None | kWh or therms | Baseload-only (no weather sensitivity) |
| Multivariate | OAT + others | kWh | Buildings with significant non-weather drivers |
| Forward simulation | Physical params | kWh + therms | New construction, complex retrofits, no baseline data |

## Axis 3: Duration

### Baseline Period

```
What data is available?
├── 12 months minimum (captures full seasonal cycle)
│   ├── Data is clean and representative -> Use 12 months
│   └── Anomalies present -> Extend to 24 months, flag and exclude anomalous periods
├── 24 months available
│   ├── Both years consistent -> Use most recent 12 months
│   └── Years differ significantly -> Investigate cause; use the representative year
└── Less than 12 months
    └── Insufficient for weather-normalized regression
        -> Consider forward model or defer until data accumulates
```

### Reporting Period

- Must be long enough to verify savings persistence under varying conditions
- Minimum: one full seasonal cycle (12 months) for weather-dependent ECMs
- Shorter acceptable for non-weather-dependent ECMs (e.g., lighting) if performance verification is the goal
- Consider: does the contract specify a reporting duration?

### Coverage Factor

The fraction of the baseline period represented by valid data points. Target > 0.9 (90% coverage). Gaps from meter failures, data quality issues, or operational anomalies reduce coverage and increase model uncertainty.

## Interaction Map

| Boundary | Model Form | Duration Implication |
|----------|-----------|---------------------|
| Whole facility | Inverse (regression) | Need 12+ months baseline; NRAs critical |
| Whole facility | Forward (simulation) | Can use shorter baseline if calibration data exists |
| Retrofit isolation | Key parameter measurement | Baseline can be short (pre/post snapshot) |
| Retrofit isolation | Continuous verification | Reporting period must cover seasonal variation |
