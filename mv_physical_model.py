"""
M&V Physical (Forward) Model Sandbox
Interactive Streamlit tool for CMVP training

Steve Kromer, P.E., CMVP #1 | Counterfactual Designs

PURPOSE:
  Students who've built statistical counterfactuals (regression on utility data)
  now experience the OTHER way to construct a counterfactual — from physics.

  In a forward model:
    - The counterfactual is built from physical parameters (U-values, COP, airflow, etc.)
    - Savings = Baseline model output − Retrofit model output
    - Uncertainty comes from parameter sensitivity, not regression residuals

  This tool lets students:
    1. Define a building (envelope, HVAC, lighting, schedules)
    2. See the physics-based energy prediction month by month
    3. Apply ECMs by changing physical parameters
    4. Compare the forward-model counterfactual to what a regression would give
    5. Explore how parameter uncertainty propagates into savings uncertainty

Run:  streamlit run mv_physical_model.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── Page Config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="M&V Physical Model Sandbox — Counterfactual Designs",
    layout="wide",
    page_icon="🏗️",
)

st.markdown("""
<style>
    .stApp { background-color: #faf6f1; }
    .stMainBlockContainer { background-color: #faf6f1; }
    section[data-testid="stSidebar"] { background-color: #f5ede3; }
    h1, h2, h3 { color: #3d3229; }
    .stMarkdown p, .stMarkdown li { color: #4a3f35; }
    .physics-card {
        background: #fff9f2;
        border-left: 4px solid #065A82;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .compare-stat { border-left-color: #2F855A; }
    .compare-phys { border-left-color: #065A82; }
    .metric-box {
        background: white;
        border-radius: 0.5rem;
        padding: 0.8rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# WEATHER DATA — Monthly degree days for a Mid-Atlantic location
# ═══════════════════════════════════════════════════════════════════════════════

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# Baltimore/DC area typical meteorological year
WEATHER = {
    "Month": MONTHS,
    "HDD65": [868, 714, 524, 238, 62, 2, 0, 0, 18, 195, 459, 772],
    "CDD65": [0, 0, 4, 22, 118, 288, 402, 372, 198, 38, 2, 0],
    "Avg_Temp_F": [33, 36, 44, 55, 65, 74, 79, 77, 70, 58, 47, 37],
    "Solar_Btu_sqft_day": [600, 800, 1050, 1300, 1500, 1600, 1550, 1400, 1150, 900, 650, 550],
}


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Building Definition
# ═══════════════════════════════════════════════════════════════════════════════

st.sidebar.header("🏗️ Building Definition")
st.sidebar.markdown("Define the building's physical properties. These are the parameters that drive the forward model.")

st.sidebar.subheader("Envelope")
floor_area = st.sidebar.number_input("Floor area (sq ft)", 10_000, 500_000, 62_000, 5_000)
num_floors = st.sidebar.slider("Number of floors", 1, 10, 2)
wall_area = st.sidebar.number_input("Gross wall area (sq ft)", 5_000, 100_000, 24_000, 1_000)
window_ratio = st.sidebar.slider("Window-to-wall ratio (%)", 10, 80, 35) / 100
roof_area = floor_area / num_floors

wall_u = st.sidebar.slider("Wall U-value (Btu/hr·ft²·°F)", 0.02, 0.30, 0.08, 0.01,
                           help="Lower = better insulated. Typical: 0.08 (insulated CMU) to 0.20 (uninsulated)")
roof_u = st.sidebar.slider("Roof U-value (Btu/hr·ft²·°F)", 0.02, 0.15, 0.04, 0.01,
                           help="Lower = better insulated. Typical: 0.03 (new) to 0.10 (old)")
window_u = st.sidebar.slider("Window U-value (Btu/hr·ft²·°F)", 0.20, 1.20, 0.55, 0.05,
                             help="Lower = better. Single pane ~1.0, double low-e ~0.30")
window_shgc = st.sidebar.slider("Window SHGC", 0.15, 0.80, 0.40, 0.05,
                                help="Solar heat gain coefficient. Lower = less solar heat admitted")

st.sidebar.subheader("HVAC")
cooling_cop = st.sidebar.slider("Cooling COP", 2.0, 7.0, 3.5, 0.1,
                                help="Coefficient of Performance. Higher = more efficient. Typical chiller: 3.0–6.0")
heating_eff = st.sidebar.slider("Heating efficiency (%)", 60, 99, 80, 1,
                                help="Gas furnace/boiler efficiency. 80% = standard, 95% = condensing")
ventilation_cfm_per_sqft = st.sidebar.slider("Ventilation (CFM/sq ft)", 0.05, 0.30, 0.12, 0.01,
                                             help="Outside air ventilation rate. ASHRAE 62.1 typical: 0.06–0.15")
fan_power_w_per_cfm = st.sidebar.slider("Fan power (W/CFM)", 0.2, 1.5, 0.65, 0.05,
                                        help="System fan efficiency. 0.3 = excellent VAV, 1.0+ = old constant volume")

st.sidebar.subheader("Internal Loads")
lpd = st.sidebar.slider("Lighting power density (W/sq ft)", 0.3, 2.0, 1.0, 0.05,
                        help="Installed lighting power. 1.0 = fluorescent, 0.5 = LED")
epd = st.sidebar.slider("Equipment power density (W/sq ft)", 0.5, 3.0, 1.2, 0.1,
                        help="Plug loads — computers, printers, etc.")
occupant_density = st.sidebar.slider("Occupant density (sq ft/person)", 100, 500, 200, 25)

st.sidebar.subheader("Schedule")
operating_hours = st.sidebar.slider("Operating hours per day", 8, 24, 12)
operating_days = st.sidebar.slider("Operating days per week", 5, 7, 5)


# ═══════════════════════════════════════════════════════════════════════════════
# PHYSICS ENGINE — Simplified monthly energy balance
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_monthly_energy(
    floor_area, num_floors, wall_area, window_ratio, roof_area,
    wall_u, roof_u, window_u, window_shgc,
    cooling_cop, heating_eff, ventilation_cfm_per_sqft, fan_power_w_per_cfm,
    lpd, epd, occupant_density, operating_hours, operating_days,
):
    """
    Simplified bin-method monthly energy calculation.

    This is a TEACHING model — not a replacement for EnergyPlus.
    It captures the key physical relationships so students can see
    how parameter changes flow through to energy predictions.
    """
    results = []
    hours_per_month = [744, 672, 744, 720, 744, 720, 744, 744, 720, 744, 720, 744]
    days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    opaque_wall_area = wall_area * (1 - window_ratio)
    glass_area = wall_area * window_ratio
    total_cfm = ventilation_cfm_per_sqft * floor_area
    num_occupants = floor_area / occupant_density

    annual_op_fraction = (operating_hours / 24) * (operating_days / 7)

    for m in range(12):
        hrs = hours_per_month[m]
        days = days_per_month[m]
        op_hrs = hrs * annual_op_fraction

        hdd = WEATHER["HDD65"][m]
        cdd = WEATHER["CDD65"][m]
        solar = WEATHER["Solar_Btu_sqft_day"][m]

        # ── Envelope losses (Btu) ──
        # UA * HDD * 24 for heating; UA * CDD * 24 for cooling
        wall_loss_heat = opaque_wall_area * wall_u * hdd * 24
        roof_loss_heat = roof_area * roof_u * hdd * 24
        window_cond_heat = glass_area * window_u * hdd * 24
        total_envelope_heat_loss = wall_loss_heat + roof_loss_heat + window_cond_heat

        wall_gain_cool = opaque_wall_area * wall_u * cdd * 24
        roof_gain_cool = roof_area * roof_u * cdd * 24
        window_cond_cool = glass_area * window_u * cdd * 24
        total_envelope_cool_gain = wall_gain_cool + roof_gain_cool + window_cond_cool

        # ── Solar gain (Btu) ──
        solar_gain = glass_area * window_shgc * solar * days

        # ── Internal gains (Btu) ──
        lighting_btu = lpd * floor_area * 3.412 * op_hrs
        equipment_btu = epd * floor_area * 3.412 * op_hrs
        people_btu = num_occupants * 450 * op_hrs  # ~450 Btu/hr sensible per person
        total_internal_gains = lighting_btu + equipment_btu + people_btu

        # ── Ventilation load (Btu) ──
        vent_heat_load = total_cfm * 1.08 * hdd * 24 * annual_op_fraction
        vent_cool_load = total_cfm * 1.08 * cdd * 24 * annual_op_fraction

        # ── Net loads ──
        # Heating: envelope loss + ventilation loss - internal gains - solar
        net_heating_btu = max(0, total_envelope_heat_loss + vent_heat_load
                              - total_internal_gains * 0.6 - solar_gain * 0.3)

        # Cooling: envelope gain + ventilation gain + internal gains + solar
        net_cooling_btu = max(0, total_envelope_cool_gain + vent_cool_load
                              + total_internal_gains * 0.7 + solar_gain * 0.7)

        # ── Convert to energy consumed ──
        heating_kwh = 0
        heating_therms = net_heating_btu / (heating_eff / 100) / 100_000  # gas heating

        cooling_kwh = net_cooling_btu / (cooling_cop * 3412)  # electric cooling

        # ── Fan energy ──
        fan_kwh = total_cfm * fan_power_w_per_cfm * op_hrs / 1000

        # ── Lighting & equipment energy ──
        lighting_kwh = lpd * floor_area * op_hrs / 1000
        equipment_kwh = epd * floor_area * op_hrs / 1000

        # ── Totals ──
        total_kwh = cooling_kwh + fan_kwh + lighting_kwh + equipment_kwh
        total_therms = heating_therms

        results.append({
            "Month": MONTHS[m],
            "Heating (therms)": round(heating_therms, 0),
            "Cooling (kWh)": round(cooling_kwh, 0),
            "Fan (kWh)": round(fan_kwh, 0),
            "Lighting (kWh)": round(lighting_kwh, 0),
            "Equipment (kWh)": round(equipment_kwh, 0),
            "Total Electric (kWh)": round(total_kwh, 0),
            "Total Gas (therms)": round(total_therms, 0),
            "Envelope Heat Loss (MBtu)": round(total_envelope_heat_loss / 1_000_000, 1),
            "Solar Gain (MBtu)": round(solar_gain / 1_000_000, 1),
            "Internal Gain (MBtu)": round(total_internal_gains / 1_000_000, 1),
        })

    return pd.DataFrame(results)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN LAYOUT
# ═══════════════════════════════════════════════════════════════════════════════

st.title("🏗️ Physical Model Sandbox")
st.caption("Counterfactual Designs — learn how a forward model constructs the counterfactual from physics, not from data.")
st.markdown(
    "*In a statistical model, the counterfactual comes from fitting a curve to historical data. "
    "In a physical model, it comes from first principles — heat transfer, thermodynamics, and "
    "engineering calculations. This tool lets you build both and compare.*"
)

# Calculate baseline energy
baseline_df = calculate_monthly_energy(
    floor_area, num_floors, wall_area, window_ratio, roof_area,
    wall_u, roof_u, window_u, window_shgc,
    cooling_cop, heating_eff, ventilation_cfm_per_sqft, fan_power_w_per_cfm,
    lpd, epd, occupant_density, operating_hours, operating_days,
)

tab1, tab2, tab_cal, tab3, tab4 = st.tabs([
    "🔬 Baseline Model",
    "🔧 Apply ECMs",
    "📐 Calibration",
    "📊 Statistical vs. Physical",
    "🎯 Sensitivity & Uncertainty",
])


# ─── TAB 1: Baseline Physical Model ──────────────────────────────────────────

with tab1:
    st.subheader("Baseline Building Energy Profile")
    st.markdown("""
    This is your **forward model baseline** — the building as it exists today,
    described entirely by physical parameters. No regression. No historical data.
    Just physics.
    """)

    annual_kwh = baseline_df["Total Electric (kWh)"].sum()
    annual_therms = baseline_df["Total Gas (therms)"].sum()
    eui_electric = annual_kwh * 3.412 / floor_area  # kBtu/sqft
    eui_gas = annual_therms * 100 / floor_area  # kBtu/sqft
    eui_total = eui_electric + eui_gas

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Annual Electric", f"{annual_kwh:,.0f} kWh")
    m2.metric("Annual Gas", f"{annual_therms:,.0f} therms")
    m3.metric("Site EUI", f"{eui_total:.1f} kBtu/ft²")
    m4.metric("Floor Area", f"{floor_area:,} ft²")

    st.divider()

    # Monthly stacked bar chart
    fig, ax = plt.subplots(figsize=(10, 4.5))
    fig.patch.set_facecolor("#faf6f1")
    ax.set_facecolor("white")

    categories = ["Cooling (kWh)", "Fan (kWh)", "Lighting (kWh)", "Equipment (kWh)"]
    colors = ["#065A82", "#1C7293", "#D4A843", "#8B6914"]
    bottom = np.zeros(12)

    for cat, color in zip(categories, colors):
        values = baseline_df[cat].values
        ax.bar(MONTHS, values, bottom=bottom, color=color, label=cat.replace(" (kWh)", ""), width=0.7)
        bottom += values

    ax.set_ylabel("Monthly kWh", fontsize=11)
    ax.set_title("Baseline Monthly Electric Consumption by End Use", fontsize=13, color="#3d3229")
    ax.legend(loc="upper right", fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"{x:,.0f}"))
    ax.grid(axis="y", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    st.pyplot(fig)
    plt.close()

    # Energy balance
    st.subheader("Monthly Energy Balance")
    st.markdown("*The numbers behind the physics. Every row traces back to a physical parameter you set in the sidebar.*")
    st.dataframe(baseline_df, use_container_width=True, hide_index=True)

    # Load component breakdown
    st.subheader("Annual Load Components")
    load_data = {
        "End Use": ["Cooling", "Fans", "Lighting", "Equipment", "Heating (gas)"],
        "Annual Energy": [
            f"{baseline_df['Cooling (kWh)'].sum():,.0f} kWh",
            f"{baseline_df['Fan (kWh)'].sum():,.0f} kWh",
            f"{baseline_df['Lighting (kWh)'].sum():,.0f} kWh",
            f"{baseline_df['Equipment (kWh)'].sum():,.0f} kWh",
            f"{annual_therms:,.0f} therms",
        ],
        "Key Parameters": [
            f"COP={cooling_cop}, Window SHGC={window_shgc}",
            f"{fan_power_w_per_cfm} W/CFM, {ventilation_cfm_per_sqft} CFM/ft²",
            f"LPD={lpd} W/ft²",
            f"EPD={epd} W/ft²",
            f"Eff={heating_eff}%, Wall U={wall_u}, Roof U={roof_u}",
        ],
    }
    st.dataframe(pd.DataFrame(load_data), use_container_width=True, hide_index=True)

    st.markdown("""
<div class="physics-card">
    <strong>Key Concept</strong><br>
    Every number in this table traces back to a physical parameter.
    If you change the wall U-value, the heating load changes. If you change the COP,
    the cooling energy changes. This is the power of a forward model —
    <strong>you can see exactly which parameter drives which load</strong>.
    In a statistical regression, all you see is a coefficient on temperature.
</div>
""", unsafe_allow_html=True)


# ─── TAB 2: Apply ECMs ───────────────────────────────────────────────────────

with tab2:
    st.subheader("Apply Energy Conservation Measures")
    st.markdown("""
    Change the physical parameters below to model your retrofit. The forward model
    recalculates energy from first principles — savings are the **difference between
    baseline and retrofit model outputs**.

    *This is how a forward model constructs the counterfactual: not by fitting data,
    but by changing the physics.*
    """)

    st.markdown("### ECM Parameters")
    st.markdown("Adjust the retrofit parameters. Compare them to your baseline values in the sidebar.")

    e1, e2 = st.columns(2)

    with e1:
        st.markdown("**Envelope Improvements**")
        ecm_roof_u = st.slider("Retrofit roof U-value", 0.02, 0.15, min(roof_u, 0.03), 0.01,
                               key="ecm_roof_u",
                               help=f"Baseline: {roof_u}")
        ecm_window_u = st.slider("Retrofit window U-value", 0.20, 1.20, min(window_u, 0.30), 0.05,
                                 key="ecm_window_u",
                                 help=f"Baseline: {window_u}")
        ecm_window_shgc = st.slider("Retrofit window SHGC", 0.15, 0.80, min(window_shgc, 0.25), 0.05,
                                    key="ecm_shgc",
                                    help=f"Baseline: {window_shgc}")

    with e2:
        st.markdown("**HVAC & Lighting Improvements**")
        ecm_cop = st.slider("Retrofit cooling COP", 2.0, 7.0, max(cooling_cop, 5.5), 0.1,
                            key="ecm_cop",
                            help=f"Baseline: {cooling_cop}")
        ecm_fan_power = st.slider("Retrofit fan power (W/CFM)", 0.2, 1.5, min(fan_power_w_per_cfm, 0.35), 0.05,
                                  key="ecm_fan",
                                  help=f"Baseline: {fan_power_w_per_cfm}")
        ecm_lpd = st.slider("Retrofit LPD (W/sq ft)", 0.3, 2.0, min(lpd, 0.45), 0.05,
                            key="ecm_lpd",
                            help=f"Baseline: {lpd}")
        ecm_heating_eff = st.slider("Retrofit heating efficiency (%)", 60, 99, max(heating_eff, 95), 1,
                                    key="ecm_heat_eff",
                                    help=f"Baseline: {heating_eff}%")

    # Calculate retrofit energy
    retrofit_df = calculate_monthly_energy(
        floor_area, num_floors, wall_area, window_ratio, roof_area,
        wall_u, ecm_roof_u, ecm_window_u, ecm_window_shgc,
        ecm_cop, ecm_heating_eff, ventilation_cfm_per_sqft, ecm_fan_power,
        ecm_lpd, epd, occupant_density, operating_hours, operating_days,
    )

    retrofit_kwh = retrofit_df["Total Electric (kWh)"].sum()
    retrofit_therms = retrofit_df["Total Gas (therms)"].sum()
    savings_kwh = annual_kwh - retrofit_kwh
    savings_therms = annual_therms - retrofit_therms
    savings_pct = savings_kwh / annual_kwh * 100 if annual_kwh > 0 else 0

    st.divider()
    st.subheader("Savings Waterfall")

    w1, w2, w3, w4 = st.columns(4)
    w1.metric("Baseline", f"{annual_kwh:,.0f} kWh")
    w2.metric("Retrofit", f"{retrofit_kwh:,.0f} kWh")
    w3.metric("Savings", f"{savings_kwh:,.0f} kWh", delta=f"{savings_pct:.1f}%")
    w4.metric("Gas Savings", f"{savings_therms:,.0f} therms")

    # Side-by-side bar chart
    fig2, ax2 = plt.subplots(figsize=(10, 4.5))
    fig2.patch.set_facecolor("#faf6f1")
    ax2.set_facecolor("white")

    x = np.arange(12)
    width = 0.35

    ax2.bar(x - width/2, baseline_df["Total Electric (kWh)"].values, width,
            label="Baseline", color="#C53030", alpha=0.7)
    ax2.bar(x + width/2, retrofit_df["Total Electric (kWh)"].values, width,
            label="Retrofit", color="#065A82", alpha=0.7)

    ax2.set_xticks(x)
    ax2.set_xticklabels(MONTHS)
    ax2.set_ylabel("Monthly kWh", fontsize=11)
    ax2.set_title("Baseline vs. Retrofit — Monthly Electric", fontsize=13, color="#3d3229")
    ax2.legend()
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"{x:,.0f}"))
    ax2.grid(axis="y", alpha=0.3)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    st.pyplot(fig2)
    plt.close()

    # ECM-by-ECM breakdown
    st.subheader("Savings by End Use")

    end_uses = ["Cooling (kWh)", "Fan (kWh)", "Lighting (kWh)", "Equipment (kWh)"]
    ecm_savings = []
    for eu in end_uses:
        base_val = baseline_df[eu].sum()
        retro_val = retrofit_df[eu].sum()
        sv = base_val - retro_val
        ecm_savings.append({
            "End Use": eu.replace(" (kWh)", ""),
            "Baseline (kWh)": f"{base_val:,.0f}",
            "Retrofit (kWh)": f"{retro_val:,.0f}",
            "Savings (kWh)": f"{sv:,.0f}",
            "Savings (%)": f"{sv/base_val*100:.1f}%" if base_val > 0 else "—",
            "Parameter Changed": {
                "Cooling": f"COP: {cooling_cop}→{ecm_cop}, SHGC: {window_shgc}→{ecm_window_shgc}",
                "Fan": f"W/CFM: {fan_power_w_per_cfm}→{ecm_fan_power}",
                "Lighting": f"LPD: {lpd}→{ecm_lpd}",
                "Equipment": "No change",
            }.get(eu.replace(" (kWh)", ""), ""),
        })

    st.dataframe(pd.DataFrame(ecm_savings), use_container_width=True, hide_index=True)

    st.markdown("""
<div class="physics-card">
    <strong>This is the forward-model counterfactual.</strong><br>
    You didn't fit a regression line. You changed physical parameters and recalculated
    from first principles. The baseline model output under reporting-period weather
    <em>is</em> the counterfactual. The difference is the savings.<br><br>
    <strong>Savings = Baseline model(reporting weather) − Retrofit model(reporting weather)</strong>
</div>
""", unsafe_allow_html=True)


# ─── TAB CAL: Calibration ─────────────────────────────────────────────────────

with tab_cal:
    st.subheader("📐 Model Calibration")
    st.markdown("""
    A physical model is only as good as its calibration. Before you can use a forward
    model as a counterfactual, you must demonstrate that **it reproduces what the building
    actually did** — that the model matches measured data within accepted tolerances.

    Without calibration, a forward model is just an opinion with equations.
    """)

    st.divider()

    # ── ASHRAE Guideline 14 Criteria ──
    st.markdown("### ASHRAE Guideline 14 Calibration Criteria")
    st.markdown("""
    | Metric | Monthly Threshold | Hourly Threshold |
    |--------|:-:|:-:|
    | **NMBE** (Normalized Mean Bias Error) | ±5% | ±10% |
    | **CV(RMSE)** (Coefficient of Variation of RMSE) | ≤15% | ≤30% |

    Both criteria must be met simultaneously. NMBE catches systematic bias (model consistently
    over- or under-predicts). CV(RMSE) catches scatter (model sometimes too high, sometimes too low).
    """)

    st.divider()

    # ── Generate "measured" data = model + noise ──
    # Simulate what real utility data looks like: the model prediction
    # plus realistic noise (weather variation, occupancy shifts, meter error)
    st.markdown("### Calibration Exercise")
    st.markdown("""
    Below is **simulated measured data** — your model's prediction with realistic noise
    added (weather variation, occupancy shifts, meter error). In a real project, this
    would be 12 months of utility bills.

    **Your task:** Adjust the sidebar parameters until the model matches the measured data
    within ASHRAE Guideline 14 tolerances. This is what calibration feels like.
    """)

    # Use a fixed seed so "measured" data doesn't change when students adjust params
    rng = np.random.RandomState(42)

    # The "true" building has slightly different parameters than the defaults
    # This creates a gap that students must close
    true_df = calculate_monthly_energy(
        floor_area=floor_area, num_floors=num_floors, wall_area=wall_area,
        window_ratio=window_ratio, roof_area=floor_area / num_floors,
        wall_u=0.09, roof_u=0.045, window_u=0.60, window_shgc=0.42,
        cooling_cop=3.2, heating_eff=78,
        ventilation_cfm_per_sqft=0.14, fan_power_w_per_cfm=0.72,
        lpd=1.05, epd=1.25, occupant_density=190,
        operating_hours=12, operating_days=5,
    )
    true_kwh = true_df["Total Electric (kWh)"].values.astype(float)
    # Add noise: ±3-8% random scatter + slight seasonal bias
    noise_pct = rng.normal(0, 0.05, 12)  # ~5% scatter
    seasonal_bias = np.array([0.02, 0.01, 0, -0.01, -0.02, 0.01,
                              0.03, 0.02, 0, -0.01, 0.01, 0.02])
    measured_kwh = true_kwh * (1 + noise_pct + seasonal_bias)

    model_kwh = baseline_df["Total Electric (kWh)"].values.astype(float)

    # ── Calculate calibration metrics ──
    residuals_cal = model_kwh - measured_kwh
    nmbe = np.sum(residuals_cal) / np.sum(measured_kwh) * 100
    cv_rmse_cal = (np.sqrt(np.mean(residuals_cal**2)) / np.mean(measured_kwh)) * 100

    nmbe_pass = abs(nmbe) <= 5
    cvrmse_pass = cv_rmse_cal <= 15
    calibrated = nmbe_pass and cvrmse_pass

    # ── Scoreboard ──
    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("NMBE", f"{nmbe:+.1f}%",
               delta="PASS ✅" if nmbe_pass else "FAIL ❌",
               delta_color="normal" if nmbe_pass else "inverse")
    sc2.metric("CV(RMSE)", f"{cv_rmse_cal:.1f}%",
               delta="PASS ✅" if cvrmse_pass else "FAIL ❌",
               delta_color="normal" if cvrmse_pass else "inverse")
    sc3.metric("Calibration Status",
               "✅ CALIBRATED" if calibrated else "❌ NOT CALIBRATED",
               delta="ASHRAE 14 monthly criteria" if calibrated else "Adjust parameters in sidebar")

    if calibrated:
        st.success("🎉 Your model meets ASHRAE Guideline 14 monthly calibration criteria! "
                   "This model can now serve as a defensible counterfactual.")
    else:
        hints = []
        if nmbe > 5:
            hints.append("Model **over-predicts** — try reducing loads (lower LPD, EPD, or operating hours) or improving efficiency (higher COP).")
        elif nmbe < -5:
            hints.append("Model **under-predicts** — try increasing loads or reducing efficiency parameters.")
        if cv_rmse_cal > 15:
            hints.append("Model has too much **scatter** — the seasonal pattern doesn't match. Try adjusting envelope parameters (U-values, SHGC) which affect heating/cooling balance.")
        for hint in hints:
            st.warning(hint)

    st.divider()

    # ── Calibration chart ──
    fig_cal, (ax_cal1, ax_cal2) = plt.subplots(1, 2, figsize=(12, 4.5))
    fig_cal.patch.set_facecolor("#faf6f1")

    # Left: Model vs Measured
    ax_cal1.set_facecolor("white")
    ax_cal1.bar(np.arange(12) - 0.18, measured_kwh, 0.35,
                label="Measured (utility bills)", color="#C53030", alpha=0.7)
    ax_cal1.bar(np.arange(12) + 0.18, model_kwh, 0.35,
                label="Model prediction", color="#065A82", alpha=0.7)
    ax_cal1.set_xticks(range(12))
    ax_cal1.set_xticklabels(MONTHS, fontsize=9)
    ax_cal1.set_ylabel("Monthly kWh", fontsize=10)
    ax_cal1.set_title("Model vs. Measured", fontsize=12, color="#3d3229")
    ax_cal1.legend(fontsize=9)
    ax_cal1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"{x:,.0f}"))
    ax_cal1.grid(axis="y", alpha=0.3)
    ax_cal1.spines["top"].set_visible(False)
    ax_cal1.spines["right"].set_visible(False)

    # Right: Residuals (% error by month)
    ax_cal2.set_facecolor("white")
    pct_errors = residuals_cal / measured_kwh * 100
    colors_res = ["#C53030" if abs(e) > 10 else "#D69E2E" if abs(e) > 5 else "#2F855A" for e in pct_errors]
    ax_cal2.bar(MONTHS, pct_errors, color=colors_res, alpha=0.8)
    ax_cal2.axhline(5, color="#D69E2E", linewidth=1, linestyle="--", alpha=0.7, label="±5% NMBE threshold")
    ax_cal2.axhline(-5, color="#D69E2E", linewidth=1, linestyle="--", alpha=0.7)
    ax_cal2.axhline(0, color="#3d3229", linewidth=0.8)
    ax_cal2.set_ylabel("Error (%)", fontsize=10)
    ax_cal2.set_title("Monthly Residuals (Model − Measured)", fontsize=12, color="#3d3229")
    ax_cal2.legend(fontsize=8, loc="upper right")
    ax_cal2.grid(axis="y", alpha=0.3)
    ax_cal2.spines["top"].set_visible(False)
    ax_cal2.spines["right"].set_visible(False)

    fig_cal.tight_layout()
    st.pyplot(fig_cal)
    plt.close()

    # ── Monthly comparison table ──
    cal_table = pd.DataFrame({
        "Month": MONTHS,
        "Measured (kWh)": [f"{v:,.0f}" for v in measured_kwh],
        "Model (kWh)": [f"{v:,.0f}" for v in model_kwh],
        "Difference (kWh)": [f"{v:+,.0f}" for v in residuals_cal],
        "Error (%)": [f"{v:+.1f}%" for v in pct_errors],
    })
    st.dataframe(cal_table, use_container_width=True, hide_index=True)

    st.divider()

    # ── Calibration process guidance ──
    st.markdown("### The Calibration Process")
    st.markdown("""
    Real-world calibration follows an iterative cycle:
    """)

    st.markdown("""
    **1. Start with design documents** — Get wall assemblies, equipment schedules, and
    nameplate data from the building's as-built drawings. Enter them in the sidebar.

    **2. Compare to measured data** — Run the model and overlay the prediction on
    12 months of utility bills. Look at the NMBE and CV(RMSE) chart above.

    **3. Identify the biggest discrepancies** — Which months are off? Summer months
    suggest cooling parameters (COP, SHGC). Winter months suggest heating parameters
    (efficiency, U-values). Flat months suggest internal loads (LPD, EPD, schedules).

    **4. Adjust parameters with physical justification** — Don't just tweak numbers
    until the error goes away. Every adjustment should have a reason: "The nameplate
    COP is 4.0 but the chiller is 15 years old, so I'm using 3.2." Document your reasoning.

    **5. Iterate until ASHRAE 14 is met** — Both NMBE ≤ ±5% and CV(RMSE) ≤ 15%
    must pass simultaneously. If you can't get there, it may indicate a missing load
    (unmeasured process equipment, after-hours use, etc.).

    **6. Document everything** — The calibration report is part of the M&V deliverable.
    It must list every parameter adjustment and its justification.
    """)

    st.divider()

    # ── Common calibration pitfalls ──
    st.markdown("### Common Calibration Pitfalls")

    p1, p2 = st.columns(2)
    with p1:
        st.markdown("""
<div class="physics-card" style="border-left-color: #C53030;">
    <strong>🚫 Pitfall: Overfitting</strong><br>
    Tweaking parameters until NMBE and CV(RMSE) are perfect, but without
    physical justification. The model "fits" the baseline data but has no
    predictive power — it fails when conditions change.<br><br>
    <strong>Symptom:</strong> Parameters far from nameplate values with no documented reason.<br>
    <strong>Fix:</strong> Every adjustment needs a physical explanation. If you can't
    explain why COP is 2.5 when nameplate says 4.0, you're overfitting.
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="physics-card" style="border-left-color: #C53030;">
    <strong>🚫 Pitfall: Missing Loads</strong><br>
    The model consistently under-predicts because there's a load you
    didn't account for — a data center, kitchen, process equipment, or
    significant after-hours usage.<br><br>
    <strong>Symptom:</strong> Negative NMBE that won't go away no matter
    what you adjust.<br>
    <strong>Fix:</strong> Walk the building. Audit the plug loads. Check for
    24/7 equipment that isn't in the model.
</div>
""", unsafe_allow_html=True)

    with p2:
        st.markdown("""
<div class="physics-card" style="border-left-color: #D69E2E;">
    <strong>⚠️ Pitfall: Wrong Weather Data</strong><br>
    Using TMY (typical year) weather instead of AMY (actual year) weather
    for the calibration period. The model can't match measured data if it's
    using the wrong temperatures.<br><br>
    <strong>Symptom:</strong> High CV(RMSE) with a seasonal pattern in the residuals.<br>
    <strong>Fix:</strong> Always calibrate against AMY weather that matches
    the utility billing period.
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="physics-card" style="border-left-color: #D69E2E;">
    <strong>⚠️ Pitfall: Compensating Errors</strong><br>
    NMBE looks great (near zero) but CV(RMSE) is high. The model over-predicts
    some months and under-predicts others by equal amounts — the errors cancel.<br><br>
    <strong>Symptom:</strong> Low NMBE but high CV(RMSE). Monthly residuals swing
    positive and negative.<br>
    <strong>Fix:</strong> Look at the residual chart. Fix the seasonal pattern
    before celebrating the low NMBE.
</div>
""", unsafe_allow_html=True)

    st.divider()

    # ── When is calibration "good enough"? ──
    st.markdown("### When Is Calibration Good Enough?")
    st.markdown("""
    This is the judgment call. ASHRAE Guideline 14 gives you thresholds, but
    meeting them is necessary, not sufficient. Ask yourself:
    """)

    st.markdown("""
    - **Do the residuals have a pattern?** Random scatter is OK. A systematic
      seasonal pattern means a missing physical relationship.
    - **Are the adjusted parameters physically defensible?** Could you explain
      every parameter to a skeptical engineer?
    - **Does the model respond correctly to perturbations?** If you increase
      cooling setpoint by 2°F, does energy go down? If not, the model structure
      may be wrong even if NMBE/CV(RMSE) pass.
    - **Is the model good enough for the savings claim?** A $50k lighting
      retrofit with 30% savings doesn't need the same calibration rigor as a
      $5M ESCO guarantee with 8% savings.
    """)

    st.info(
        "💡 **The punchline:** Calibration is where engineering judgment meets data. "
        "The numbers (NMBE, CV(RMSE)) tell you if you're in the ballpark. "
        "Your professional judgment tells you if the model is trustworthy. "
        "Both are required — neither alone is sufficient."
    )


# ─── TAB 3: Statistical vs. Physical ─────────────────────────────────────────

with tab3:
    st.subheader("Statistical vs. Physical Counterfactual")
    st.markdown("""
    Here's the key question this tool is designed to answer:
    **When should you use a statistical model, and when should you use a physical model?**

    Let's compare them side by side using your building.
    """)

    # Generate a pseudo-statistical model (regression on HDD/CDD)
    # Fit a simple regression to the forward model's own output to show the difference
    hdd = np.array(WEATHER["HDD65"])
    cdd = np.array(WEATHER["CDD65"])
    baseline_kwh_monthly = baseline_df["Total Electric (kWh)"].values

    # Simple linear fit: kWh = a + b*HDD + c*CDD
    X = np.column_stack([np.ones(12), hdd, cdd])
    coeffs, _, _, _ = np.linalg.lstsq(X, baseline_kwh_monthly, rcond=None)
    stat_predicted = X @ coeffs
    residuals = baseline_kwh_monthly - stat_predicted
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((baseline_kwh_monthly - np.mean(baseline_kwh_monthly))**2)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    cv_rmse = np.sqrt(ss_res / 12) / np.mean(baseline_kwh_monthly) * 100

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
<div class="physics-card compare-stat">
    <h3 style="color: #2F855A;">Statistical Model (Regression)</h3>
    <p><strong>How it works:</strong> Fit a line to historical data.<br>
    kWh = a + b×HDD + c×CDD</p>
    <p><strong>Strengths:</strong></p>
    <ul>
        <li>Simple — needs only utility bills + weather</li>
        <li>Empirically grounded in actual measured data</li>
        <li>Uncertainty quantified by regression diagnostics</li>
    </ul>
    <p><strong>Weaknesses:</strong></p>
    <ul>
        <li>Cannot isolate individual ECMs</li>
        <li>Cannot predict savings from a parameter change</li>
        <li>Breaks down if building use pattern changes</li>
        <li>Correlation ≠ causation</li>
    </ul>
</div>
""", unsafe_allow_html=True)

    with col_b:
        st.markdown("""
<div class="physics-card compare-phys">
    <h3 style="color: #065A82;">Physical Model (Forward)</h3>
    <p><strong>How it works:</strong> Calculate energy from first principles.<br>
    kWh = f(U-values, COP, loads, schedules, weather)</p>
    <p><strong>Strengths:</strong></p>
    <ul>
        <li>Can isolate savings per ECM</li>
        <li>Can predict savings from parameter changes</li>
        <li>Works even without historical data</li>
        <li>Captures physical interactions</li>
    </ul>
    <p><strong>Weaknesses:</strong></p>
    <ul>
        <li>Complex — many parameters to define</li>
        <li>Sensitive to assumptions (GIGO)</li>
        <li>Must be calibrated against real data</li>
        <li>More expensive to develop</li>
    </ul>
</div>
""", unsafe_allow_html=True)

    st.divider()

    # Overlay chart: physical model vs statistical model prediction
    st.subheader("Same Building, Two Models")

    fig3, ax3 = plt.subplots(figsize=(10, 4.5))
    fig3.patch.set_facecolor("#faf6f1")
    ax3.set_facecolor("white")

    ax3.plot(MONTHS, baseline_kwh_monthly, "o-", color="#065A82", linewidth=2,
             label="Physical model", markersize=7)
    ax3.plot(MONTHS, stat_predicted, "s--", color="#2F855A", linewidth=2,
             label=f"Statistical regression (R²={r_squared:.3f})", markersize=6)
    ax3.fill_between(MONTHS, stat_predicted - 2*np.std(residuals),
                     stat_predicted + 2*np.std(residuals),
                     alpha=0.15, color="#2F855A", label="±2σ regression band")

    ax3.set_ylabel("Monthly kWh", fontsize=11)
    ax3.set_title("Physical Model Output vs. Statistical Regression Fit", fontsize=13, color="#3d3229")
    ax3.legend(fontsize=9)
    ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"{x:,.0f}"))
    ax3.grid(axis="y", alpha=0.3)
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    st.pyplot(fig3)
    plt.close()

    st.markdown(f"""
    **Regression diagnostics on the physical model output:**
    R² = {r_squared:.4f} | CV(RMSE) = {cv_rmse:.1f}% | Intercept = {coeffs[0]:,.0f} | HDD coeff = {coeffs[1]:.1f} | CDD coeff = {coeffs[2]:.1f}
    """)

    st.markdown("""
<div class="physics-card">
    <strong>Notice what the regression CANNOT see:</strong><br>
    The regression model produces a single line through the data. It tells you that energy
    correlates with temperature — but it can't tell you <em>why</em>.<br><br>
    The physical model can tell you: "Cooling energy is high in July because the COP is 3.5
    and the window SHGC is 0.40 — upgrading to COP 5.5 would save X kWh specifically from
    the chiller." The regression just says "July is high."<br><br>
    <strong>This is the fundamental tradeoff:</strong> the statistical model is simpler and
    empirically grounded; the physical model is richer and explanatory.
</div>
""", unsafe_allow_html=True)

    st.divider()

    # When to use which
    st.subheader("When to Use Which?")

    st.markdown("""
| Situation | Statistical Model | Physical Model |
|-----------|:-:|:-:|
| Single whole-building retrofit, 12+ months of data | ✅ Preferred | Overkill |
| Multiple interacting ECMs | Misses interactions | ✅ Preferred |
| New construction (no baseline data) | ❌ Impossible | ✅ Only option |
| ECM-level savings attribution needed | ❌ Can't isolate | ✅ Can isolate |
| Budget is tight, deadline is tomorrow | ✅ Fast & cheap | Too expensive |
| Performance contract with guarantee | Good start | ✅ More defensible |
| Building use pattern will change (NRA risk) | ❌ Fragile | ✅ More robust |
| Simple lighting retrofit, constant load | ✅ Sufficient | Overkill |
""")


# ─── TAB 4: Sensitivity & Uncertainty ────────────────────────────────────────

with tab4:
    st.subheader("Sensitivity Analysis & Uncertainty Propagation")
    st.markdown("""
    In a **statistical model**, uncertainty comes from the regression residuals — how well
    the line fits the data (CV(RMSE), t-statistics, confidence intervals).

    In a **physical model**, uncertainty comes from **parameter uncertainty** — how well you
    know the inputs. If the COP could be 3.2 or 3.8 instead of 3.5, that range propagates
    into a range of predicted savings.

    Adjust the parameter uncertainty ranges below to see how they affect your savings estimate.
    """)

    st.markdown("### Parameter Uncertainty Ranges")
    st.markdown("*How confident are you in each parameter? Wider ranges = more uncertainty.*")

    u1, u2, u3 = st.columns(3)
    with u1:
        cop_unc = st.slider("COP uncertainty (±%)", 1, 30, 10, key="cop_unc")
        wall_u_unc = st.slider("Wall U-value uncertainty (±%)", 1, 30, 15, key="wall_unc")
    with u2:
        lpd_unc = st.slider("LPD uncertainty (±%)", 1, 20, 5, key="lpd_unc")
        fan_unc = st.slider("Fan power uncertainty (±%)", 1, 30, 10, key="fan_unc")
    with u3:
        schedule_unc = st.slider("Schedule uncertainty (±%)", 1, 25, 10, key="sched_unc")
        shgc_unc = st.slider("SHGC uncertainty (±%)", 1, 30, 15, key="shgc_unc")

    st.divider()

    # Monte Carlo sensitivity (simplified: one-at-a-time)
    st.subheader("One-at-a-Time Sensitivity")
    st.markdown("*What happens to total energy if each parameter is at its low vs. high bound?*")

    param_configs = [
        ("COP", "cooling_cop", cooling_cop, cop_unc),
        ("Wall U-value", "wall_u", wall_u, wall_u_unc),
        ("LPD", "lpd", lpd, lpd_unc),
        ("Fan W/CFM", "fan_power_w_per_cfm", fan_power_w_per_cfm, fan_unc),
        ("Operating hours", "operating_hours", operating_hours, schedule_unc),
        ("Window SHGC", "window_shgc", window_shgc, shgc_unc),
    ]

    sensitivity_results = []
    for name, param, base_val, unc_pct in param_configs:
        low_val = base_val * (1 - unc_pct / 100)
        high_val = base_val * (1 + unc_pct / 100)

        # Build kwargs with low value
        kwargs_base = dict(
            floor_area=floor_area, num_floors=num_floors, wall_area=wall_area,
            window_ratio=window_ratio, roof_area=roof_area,
            wall_u=wall_u, roof_u=roof_u, window_u=window_u, window_shgc=window_shgc,
            cooling_cop=cooling_cop, heating_eff=heating_eff,
            ventilation_cfm_per_sqft=ventilation_cfm_per_sqft,
            fan_power_w_per_cfm=fan_power_w_per_cfm,
            lpd=lpd, epd=epd, occupant_density=occupant_density,
            operating_hours=operating_hours, operating_days=operating_days,
        )

        kwargs_low = {**kwargs_base, param: low_val}
        kwargs_high = {**kwargs_base, param: high_val}

        # COP needs special handling — it's in the denominator, so low COP = more energy
        low_kwh = calculate_monthly_energy(**kwargs_low)["Total Electric (kWh)"].sum()
        high_kwh = calculate_monthly_energy(**kwargs_high)["Total Electric (kWh)"].sum()

        delta_low = low_kwh - annual_kwh
        delta_high = high_kwh - annual_kwh

        sensitivity_results.append({
            "Parameter": name,
            "Base Value": f"{base_val}",
            "Low (−{unc_pct}%)": f"{low_val:.2f}",
            "High (+{unc_pct}%)": f"{high_val:.2f}",
            "kWh at Low": f"{low_kwh:,.0f}",
            "kWh at High": f"{high_kwh:,.0f}",
            "Swing (kWh)": f"{abs(high_kwh - low_kwh):,.0f}",
            "Swing (%)": f"{abs(high_kwh - low_kwh) / annual_kwh * 100:.1f}%",
            "_swing_val": abs(high_kwh - low_kwh),
            "_delta_low": delta_low,
            "_delta_high": delta_high,
        })

    # Tornado chart
    fig4, ax4 = plt.subplots(figsize=(10, 4))
    fig4.patch.set_facecolor("#faf6f1")
    ax4.set_facecolor("white")

    sensitivity_results.sort(key=lambda x: x["_swing_val"])

    y_pos = range(len(sensitivity_results))
    names = [r["Parameter"] for r in sensitivity_results]
    lows = [r["_delta_low"] for r in sensitivity_results]
    highs = [r["_delta_high"] for r in sensitivity_results]

    for i, (name, lo, hi) in enumerate(zip(names, lows, highs)):
        left = min(lo, hi)
        width = abs(hi - lo)
        ax4.barh(i, width, left=left, color="#065A82", alpha=0.7, height=0.6)
        ax4.text(left + width + annual_kwh * 0.005, i,
                 f"±{width:,.0f} kWh ({width/annual_kwh*100:.1f}%)",
                 va="center", fontsize=9, color="#3d3229")

    ax4.set_yticks(list(y_pos))
    ax4.set_yticklabels(names)
    ax4.axvline(0, color="#C53030", linewidth=1, linestyle="--", alpha=0.5)
    ax4.set_xlabel("Change in Annual kWh from Baseline", fontsize=11)
    ax4.set_title("Tornado Chart — Parameter Sensitivity", fontsize=13, color="#3d3229")
    ax4.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"{x:+,.0f}"))
    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)
    st.pyplot(fig4)
    plt.close()

    st.dataframe(
        pd.DataFrame([{k: v for k, v in r.items() if not k.startswith("_")} for r in sensitivity_results]),
        use_container_width=True, hide_index=True,
    )

    st.divider()

    # Combined uncertainty
    total_swing = np.sqrt(sum(r["_swing_val"]**2 for r in sensitivity_results))
    combined_pct = total_swing / annual_kwh * 100

    st.subheader("Combined Uncertainty (Root-Sum-Square)")
    st.markdown(f"""
    Assuming parameter uncertainties are independent, the combined uncertainty
    is the root-sum-square of individual swings:
    """)

    st.latex(r"u_{combined} = \sqrt{\sum_{i} (\Delta E_i)^2}")

    cu1, cu2, cu3 = st.columns(3)
    cu1.metric("Combined Uncertainty", f"±{total_swing:,.0f} kWh")
    cu2.metric("As % of Baseline", f"±{combined_pct:.1f}%")
    cu3.metric("95% Confidence Range",
               f"{annual_kwh - 2*total_swing:,.0f} – {annual_kwh + 2*total_swing:,.0f} kWh")

    st.markdown("""
<div class="physics-card">
    <strong>Compare to statistical uncertainty:</strong><br>
    In a regression model, uncertainty is expressed as CV(RMSE) — a single number that
    captures how well the line fits the data. You know the <em>total</em> uncertainty
    but not <em>where it comes from</em>.<br><br>
    In the physical model, the tornado chart shows you exactly which parameter
    contributes the most uncertainty. <strong>That tells you where to invest your
    M&V budget</strong> — measure the parameter with the biggest bar, and the
    uncertainty shrinks the most per dollar spent.<br><br>
    This is the bridge between the Decision Tree (choose your design),
    the Uncertainty Budget (allocate your dollars), and this Physical Model
    (see where the uncertainty lives).
</div>
""", unsafe_allow_html=True)

    st.markdown("""
    ### Reflection Questions

    - Which parameter has the largest tornado bar? Would you prioritize measuring it?
    - If you reduced the top parameter's uncertainty from ±{0}% to ±5%, how much would combined uncertainty drop?
    - Compare the combined uncertainty ({1:.1f}%) to a typical regression CV(RMSE) of 10–15%. Which is better? Why?
    - If the building owner says "I need ±10% accuracy on savings" — can this model deliver that? What would you need to tighten?
    """.format(
        max((r for r in sensitivity_results), key=lambda r: r["_swing_val"])["Parameter"],
        combined_pct,
    ))


# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════

st.divider()
st.markdown(
    "Built on the [Counterfactual Designs](https://counterfactual-designs.com) framework "
    "by Steve Kromer, P.E., CMVP #1.  \n"
    "See also: [Decision Tree + Uncertainty Budget](https://cmvp-capstone.streamlit.app) · "
    "[Counterfactual Builder](https://mnvexample.streamlit.app) · "
    "[CfDesigns](https://cfdesigns.vercel.app)"
)
