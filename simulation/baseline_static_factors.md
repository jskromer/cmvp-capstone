# Counterfactual Headquarters — Baseline Static Factor List

**Source:** `cfhq_baseline.idf`
**Purpose:** Fixed parameters defining the pre-retrofit counterfactual model
**IPMVP Context:** Static factors are quantities held constant in the baseline model because they are not expected to change during the performance period (or are contractually fixed). Any deviation triggers a baseline adjustment.

---

## 1. Building Geometry & Envelope

| Factor | Value | IDF Object | Notes |
|--------|-------|------------|-------|
| Gross floor area | 12,000 sf (1,115 m²) | Zone | OFFICE 8,000 sf + LOBBY 4,000 sf |
| Ceiling height | 10 ft (3.048 m) | Zone | Both zones |
| OFFICE volume | 2,265 m³ | Zone | 743.22 m² x 3.048 m |
| LOBBY volume | 1,134 m³ | Zone | 371.61 m² x 3.048 m |
| Building orientation | 0° (long axis E-W) | Building | North axis = 0 |
| Terrain | City | Building | — |

### Envelope Constructions

| Component | Construction | R-value / U-factor | Material |
|-----------|-------------|-------------------|----------|
| Roof | Roof Construction | ~R-25 (US) | Metal deck + polyiso insulation (0.090 m, k=0.022) |
| Exterior walls | Exterior Wall | ~R-7.5 ci | 8" CMU (0.200 m, k=0.51) + polyiso ci (0.033 m, k=0.022) |
| Interior wall | Interior Wall | — | Drywall partition (0.013 m, k=0.16) |
| Floor slab | Floor Slab | — | 6" concrete slab-on-grade (0.150 m, k=1.73) |
| Windows | Window Construction | U=2.047 W/m²K, SHGC=0.40 | Double-pane low-E, VT=0.60 |

### Fenestration

| Window | Host Wall | Aperture (m) | Area (m²) |
|--------|-----------|-------------|-----------|
| OFFICE:Win:South | OFFICE:Wall:South | 12.384 x 1.200 | 14.86 |
| OFFICE:Win:North | OFFICE:Wall:North | 15.616 x 1.200 | 18.74 |
| OFFICE:Win:West | OFFICE:Wall:West | 14.48 x 1.200 | 17.38 |
| LOBBY:Win:East | LOBBY:Wall:East | 9.00 x 1.800 | 16.20 |
| LOBBY:Win:South | LOBBY:Wall:South | 6.192 x 1.800 | 11.15 |

---

## 2. Location & Climate

| Factor | Value | Notes |
|--------|-------|-------|
| Location | Washington Dulles Intl Airport, VA | ASHRAE Zone 4A |
| Latitude | 38.98° N | — |
| Longitude | -77.47° W | — |
| Elevation | 82 m | — |
| Time zone | GMT -5 | — |
| Weather file | USA_VA_Sterling-Washington.Dulles.Intl.AP.724030_TMY3.epw | TMY3 |
| Winter design day | -11.8°C DB (99.6% heating) | Jan 21 |
| Summer design day | 32.7°C DB / 23.5°C WB (1% cooling) | Jul 21 |
| Envelope standard | ASHRAE 90.1-2004 | Zone 4A compliance |

---

## 3. Internal Loads

### Occupancy

| Zone | Density | Method | Activity Level |
|------|---------|--------|---------------|
| OFFICE | 0.054 person/m² (5/1000 sf) | People/Area | 120 W/person |
| LOBBY | 0.108 person/m² (10/1000 sf) | People/Area | 120 W/person |

### Lighting — BASELINE (T8 Fluorescent)

| Zone | LPD | Lamp Type | Return Air Frac | Radiant Frac | Visible Frac |
|------|-----|-----------|----------------|-------------|-------------|
| OFFICE | 16.15 W/m² (1.5 W/sf) | T8 fluorescent | 0.42 | 0.09 | 0.18 |
| LOBBY | 10.76 W/m² (1.0 W/sf) | Existing (not retrofitted) | 0.32 | 0.09 | 0.18 |

*ECM-1 target: OFFICE LED at 0.75 W/sf (50% reduction)*

### Plug Loads

| Zone | EPD | Method |
|------|-----|--------|
| OFFICE | 10.76 W/m² (1.0 W/sf) | Watts/Area |
| LOBBY | 5.38 W/m² (0.5 W/sf) | Watts/Area |

### Infiltration

| Zone | Rate | Method |
|------|------|--------|
| OFFICE | 0.000305 m³/s-m² (0.06 cfm/sf EWA) | Flow/ExteriorArea |
| LOBBY | 0.000305 m³/s-m² (0.06 cfm/sf EWA) | Flow/ExteriorArea |

---

## 4. HVAC Systems

### System Type: Packaged Rooftop Unit (PSZ-AC) — One per Zone

| Parameter | OFFICE RTU | LOBBY RTU |
|-----------|-----------|----------|
| Cooling coil | SingleSpeedDX | SingleSpeedDX |
| Cooling COP | 3.50 | 3.50 |
| Cooling SAT | 12.8°C (55°F) | 12.8°C (55°F) |
| Heating coil | Gas furnace | Gas furnace |
| Gas efficiency | 0.80 | 0.80 |
| Heating SAT | 50.0°C (122°F) | 50.0°C (122°F) |
| Fan total efficiency | 0.70 | 0.70 |
| Fan delta pressure | 745 Pa | 745 Pa |
| Fan motor efficiency | 0.90 | 0.90 |
| Fan placement | Blow-through | Blow-through |
| Economizer | None | None |
| Night cycle control | StayOff | StayOff |
| Heat recovery | None | None |
| Outdoor air method | Flow/Person | Flow/Person |
| OA per person | 0.00944 m³/s (20 cfm) | 0.00944 m³/s (20 cfm) |

---

## 5. Thermostat Setpoints — BASELINE (Fixed, No Setback)

| Zone | Heating Setpoint | Cooling Setpoint | Schedule |
|------|-----------------|-----------------|----------|
| OFFICE | 21.1°C (70°F) constant | 23.9°C (75°F) constant | 24/7, no setback |
| LOBBY | 20.0°C (68°F) constant | 25.0°C (77°F) constant | 24/7, no setback |

*ECM-2 target: night setback/setup and optimal scheduling*

---

## 6. Operating Schedules

| Schedule | Weekday Profile | Weekend Profile |
|----------|----------------|-----------------|
| OFFICE occupancy | 7a-8a ramp (25%), 8a-5p full, 5p-6p (50%), night 5% | Sat 8a-1p (20%), Sun off |
| LOBBY occupancy | 7a-6p (75%), 6p-9p (40%), night 5% | 9a-6p (35%), night 5% |
| OFFICE lighting | 7a-6p on (100%), night 5% security | Sat 8a-2p (50%), Sun 5% |
| LOBBY lighting | 6a-7a (60%), 7a-9p (100%), 9p-10p (60%), night 20% | Same all days |
| OFFICE equipment | 7a-8a (50%), 8a-5p (100%), 5p-6p (50%), night 10% | 10% all day |
| LOBBY equipment | 7a-9p (60%), night 10% | 20% all day |
| HVAC availability | Always on (1.0) — no scheduling optimization | Same |
| Infiltration | Occupied: 0.25 (pressurized), Unoccupied: 1.0 | 1.0 all day |

---

## 7. Ground Temperatures (Monthly, °C)

| Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 12.8 | 11.1 | 11.7 | 13.3 | 15.6 | 18.3 | 20.6 | 21.7 | 21.1 | 19.4 | 16.1 | 13.9 |

---

## 8. ECM Summary (What Changes, What Stays Fixed)

| ECM | What Changes | Static Factors Affected |
|-----|-------------|----------------------|
| ECM-1: LED Retrofit | OFFICE LPD: 16.15 → 8.07 W/m² | Lighting heat fractions change (Return Air, Radiant, Visible) |
| ECM-2: DDC Controls | Thermostat schedules, HVAC availability | Setpoints become scheduled (setback/setup); fan mode changes |
| Neither ECM | Envelope, geometry, weather, plug loads, occupancy, LOBBY lighting | All remain at baseline values above |

---

*Generated from `cfhq_baseline.idf` — Counterfactual Headquarters capstone model*
*Counterfactual Designs / Steve Kromer PE CMVP*
