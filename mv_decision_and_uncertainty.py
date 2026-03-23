"""
M&V Decision Tree + Uncertainty Budget
Combined Streamlit Application

Steve Kromer, P.E., CMVP #1 | Counterfactual Designs

Two tools in one app:
  Tab 1 — Decision Tree: Choose your M&V counterfactual design (Boundary, Model Form, Duration)
  Tab 2 — Uncertainty Budget: See where your M&V dollars go and why
  Tab 3 — Combined View: Your design recommendation WITH its uncertainty profile

Run:  streamlit run mv_decision_and_uncertainty.py
"""

import streamlit as st
import graphviz
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── Page Config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="M&V Design + Uncertainty Budget — Counterfactual Designs",
    layout="wide",
    page_icon="⚖️",
)

# ── Warm Cream Theme (matches CfDesigns branding) ───────────────────────────

st.markdown("""
<style>
    .stApp { background-color: #faf6f1; }
    .stMainBlockContainer { background-color: #faf6f1; }
    section[data-testid="stSidebar"] { background-color: #f5ede3; }
    h1, h2, h3 { color: #3d3229; }
    .stMarkdown p, .stMarkdown li { color: #4a3f35; }
    .design-card {
        background: #fff9f2;
        border-left: 4px solid #b8860b;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .uncertainty-high { color: #C53030; font-weight: 700; }
    .uncertainty-med  { color: #D69E2E; font-weight: 700; }
    .uncertainty-low  { color: #2F855A; font-weight: 700; }
    .metric-card {
        background: white;
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        text-align: center;
    }
    .metric-card h3 { font-size: 2rem; margin: 0; }
    .metric-card p { font-size: 0.85rem; color: #64748B; margin: 0; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Project Context Inputs (shared by all tabs)
# ═══════════════════════════════════════════════════════════════════════════════

st.sidebar.header("Project Context")
st.sidebar.markdown("Answer these questions to receive a counterfactual design *and* an uncertainty budget recommendation.")

num_ecms = st.sidebar.radio(
    "How many energy conservation measures (ECMs)?",
    ["Single ECM", "Multiple ECMs with interactive effects"],
)

boundary_access = st.sidebar.radio(
    "Measurement boundary access?",
    [
        "Sub-meter available on affected equipment/system",
        "Whole-building meter only (utility bills)",
        "Calibrated simulation model available or feasible",
    ],
)

load_variability = st.sidebar.radio(
    "Load variability of affected system?",
    [
        "Constant or near-constant load (e.g., lighting, base-load motors)",
        "Variable — depends on weather, occupancy, or production",
    ],
)

baseline_data = st.sidebar.selectbox(
    "Baseline data availability?",
    [
        "12+ months of interval or monthly data",
        "3–11 months of data",
        "Little or no pre-intervention data",
    ],
)

independent_vars = st.sidebar.radio(
    "Key independent variables?",
    [
        "None — flat load profile",
        "Single variable (e.g., outdoor air temperature)",
        "Multiple variables (temperature, occupancy, production, etc.)",
    ],
)

savings_signal = st.sidebar.radio(
    "Expected savings relative to baseline noise?",
    [
        "Large — savings clearly exceed baseline variability (>20%)",
        "Moderate — detectable with good model (10–20%)",
        "Small — may be difficult to distinguish from noise (<10%)",
    ],
)

budget_accuracy = st.sidebar.radio(
    "Budget / accuracy priority?",
    [
        "Minimize cost — stipulated values acceptable where defensible",
        "Balanced — reasonable accuracy within practical budget",
        "High accuracy required (e.g., performance contract, ESCO guarantee)",
    ],
)

st.sidebar.divider()
annual_savings_kwh = st.sidebar.number_input(
    "Estimated annual savings (kWh)", min_value=1_000, max_value=50_000_000,
    value=122_390, step=10_000,
    help="Used for uncertainty budget calculations"
)
rate_per_kwh = st.sidebar.number_input(
    "Blended energy rate ($/kWh)", min_value=0.01, max_value=1.00,
    value=0.12, step=0.01,
)
mv_budget = st.sidebar.number_input(
    "Total M&V budget ($)", min_value=500, max_value=500_000,
    value=18_000, step=1_000,
)


# ═══════════════════════════════════════════════════════════════════════════════
# DECISION LOGIC (from mv-decision-tree)
# ═══════════════════════════════════════════════════════════════════════════════

def build_recommendation():
    """Return (boundary, model_form, duration, rationale_bullets) tuple."""

    # --- Boundary ---
    if boundary_access == "Calibrated simulation model available or feasible":
        boundary = "Whole-building (simulation-defined boundary)"
        boundary_note = (
            "A calibrated simulation defines the counterfactual across the entire "
            "building, even when physical sub-metering isn't practical."
        )
    elif boundary_access == "Whole-building meter only (utility bills)":
        boundary = "Whole-building meter"
        boundary_note = (
            "Only whole-building meters are available, so the measurement boundary "
            "encompasses the entire facility."
        )
    elif num_ecms == "Multiple ECMs with interactive effects":
        boundary = "Whole-building meter"
        boundary_note = (
            "Multiple interacting ECMs make equipment-level isolation impractical. "
            "A whole-building boundary captures net interactive effects."
        )
    else:
        boundary = "Equipment / system level"
        boundary_note = (
            "A single ECM with sub-metering available — draw the boundary tightly "
            "around the affected equipment to isolate savings."
        )

    # --- Model Form ---
    if (boundary_access == "Calibrated simulation model available or feasible"
            or baseline_data == "Little or no pre-intervention data"):
        model_form = "Engineering / physical simulation model"
        if boundary_access == "Calibrated simulation model available or feasible":
            model_note = (
                "Construct the counterfactual using a calibrated energy simulation "
                "(e.g., EnergyPlus, eQUEST). The model represents physics-based "
                "relationships and can handle complex interactions."
            )
        else:
            model_note = (
                "Without pre-intervention data, a statistical counterfactual has no "
                "foundation. A calibrated simulation is the recommended path."
            )
        if baseline_data == "Little or no pre-intervention data" and boundary != "Whole-building (simulation-defined boundary)":
            boundary = "Whole-building (simulation-defined boundary)"
            boundary_note = (
                "Insufficient baseline data requires a simulation-based counterfactual. "
                "The simulation defines the measurement boundary across the building."
            )
    elif load_variability == "Constant or near-constant load (e.g., lighting, base-load motors)":
        if budget_accuracy == "Minimize cost — stipulated values acceptable where defensible":
            model_form = "Stipulated key-parameter model"
            model_note = (
                "For constant-load equipment, the counterfactual can be constructed by "
                "measuring the key operating parameter and stipulating stable parameters."
            )
        else:
            model_form = "Direct measurement (metered before/after comparison)"
            model_note = (
                "Constant-load equipment with sub-metering — continuously meter energy "
                "use before and after the intervention."
            )
    elif independent_vars == "Multiple variables (temperature, occupancy, production, etc.)":
        if (num_ecms == "Multiple ECMs with interactive effects"
                or boundary == "Whole-building meter"):
            model_form = "Multivariable statistical regression or hybrid model"
            model_note = (
                "Multiple independent variables drive energy use. Use a multivariable "
                "regression or hybrid approach to construct the counterfactual."
            )
        else:
            model_form = "Multivariable statistical regression"
            model_note = (
                "Energy use depends on multiple independent variables. A multivariable "
                "regression at the equipment level constructs the counterfactual."
            )
    else:
        model_form = "Single-variable statistical regression"
        model_note = (
            "Energy use varies with a single dominant independent variable. "
            "A regression model predicts baseline energy under reporting-period conditions."
        )

    # --- Duration ---
    if baseline_data == "12+ months of interval or monthly data":
        duration = "12+ month baseline, 12+ month reporting period recommended"
        duration_note = (
            "A full year of baseline data captures seasonal patterns. Match with "
            "at least 12 months of reporting-period data."
        )
    elif baseline_data == "3–11 months of data":
        duration = "Partial baseline — extend reporting period for confidence"
        duration_note = (
            "Less than a full year of baseline data means seasonal gaps. Extend the "
            "reporting period or use engineering judgment to fill gaps."
        )
    else:
        duration = "Simulation-derived baseline — reporting period data validates model"
        duration_note = (
            "With no measured baseline, the simulation model defines the counterfactual. "
            "Use reporting-period data to validate model calibration."
        )

    # --- Signal-to-noise ---
    signal_note = None
    if savings_signal == "Small — may be difficult to distinguish from noise (<10%)":
        if boundary == "Whole-building meter":
            signal_note = (
                "**Signal-to-noise warning:** Small savings at the whole-building level "
                "may be statistically indistinguishable from model noise. Consider "
                "tightening the boundary or extending the reporting period."
            )
        else:
            signal_note = (
                "**Signal-to-noise note:** Small expected savings — ensure prediction "
                "uncertainty is smaller than the expected savings."
            )

    rationale = []
    rationale.append(f"**Boundary:** {boundary_note}")
    rationale.append(f"**Model form:** {model_note}")
    rationale.append(f"**Duration:** {duration_note}")
    if signal_note:
        rationale.append(signal_note)

    return boundary, model_form, duration, rationale


boundary_rec, model_rec, duration_rec, rationale_bullets = build_recommendation()


# ═══════════════════════════════════════════════════════════════════════════════
# UNCERTAINTY BUDGET ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def build_uncertainty_budget():
    """Generate an uncertainty budget table based on the design recommendation."""

    annual_savings_dollars = annual_savings_kwh * rate_per_kwh

    # Build M&V actions based on the recommended design
    actions = []

    # Always recommended: baseline model
    if "regression" in model_rec.lower() or "statistical" in model_rec.lower():
        actions.append({
            "action": "Collect & clean baseline data (12-month utility bills or interval data)",
            "type": "Aleatory",
            "est_cost": int(mv_budget * 0.08),
            "uncertainty_reduction": 15,
            "rationale": "Seasonal data reduces aleatory (random) uncertainty in the regression model."
        })
        actions.append({
            "action": "Fit & validate regression model (goodness-of-fit diagnostics)",
            "type": "Aleatory",
            "est_cost": int(mv_budget * 0.10),
            "uncertainty_reduction": 20,
            "rationale": "Model selection and validation are the biggest levers for reducing model-form uncertainty."
        })

    if "stipulated" in model_rec.lower():
        actions.append({
            "action": "Spot-measure key parameters (wattage, runtime, flow rates)",
            "type": "Epistemic",
            "est_cost": int(mv_budget * 0.12),
            "uncertainty_reduction": 25,
            "rationale": "Replaces stipulated values with measured values — directly reduces epistemic uncertainty."
        })

    if "simulation" in model_rec.lower():
        actions.append({
            "action": "Build & calibrate energy simulation model",
            "type": "Epistemic",
            "est_cost": int(mv_budget * 0.35),
            "uncertainty_reduction": 30,
            "rationale": "Physics-based model captures interactions that statistical models miss."
        })
        actions.append({
            "action": "Validate simulation against reporting-period metered data",
            "type": "Aleatory",
            "est_cost": int(mv_budget * 0.10),
            "uncertainty_reduction": 15,
            "rationale": "Validation confirms the model tracks reality — reduces both aleatory and epistemic risk."
        })

    if "direct" in model_rec.lower() or "metered" in model_rec.lower():
        actions.append({
            "action": "Install continuous sub-metering on affected equipment",
            "type": "Epistemic",
            "est_cost": int(mv_budget * 0.30),
            "uncertainty_reduction": 30,
            "rationale": "Continuous measurement eliminates estimation — the gold standard for epistemic reduction."
        })

    # Universal actions
    if boundary_rec == "Whole-building meter" or "whole" in boundary_rec.lower():
        actions.append({
            "action": "Non-routine adjustment (NRA) protocol for known changes",
            "type": "Ontological",
            "est_cost": int(mv_budget * 0.12),
            "uncertainty_reduction": 20,
            "rationale": "Without NRA, real-world changes (occupancy, schedules, expansions) mask true savings."
        })

    if num_ecms == "Multiple ECMs with interactive effects":
        actions.append({
            "action": "Interactive effects analysis (engineering calculation or simulation)",
            "type": "Epistemic",
            "est_cost": int(mv_budget * 0.08),
            "uncertainty_reduction": 10,
            "rationale": "Quantifies how ECMs affect each other — prevents double-counting or under-counting."
        })

    if savings_signal == "Small — may be difficult to distinguish from noise (<10%)":
        actions.append({
            "action": "Extended reporting period (24+ months) for small-signal detection",
            "type": "Aleatory",
            "est_cost": int(mv_budget * 0.05),
            "uncertainty_reduction": 10,
            "rationale": "More data points improve statistical power to detect small savings signals."
        })

    # Always: QA/QC and reporting
    actions.append({
        "action": "QA/QC review and final savings report",
        "type": "Epistemic",
        "est_cost": int(mv_budget * 0.08),
        "uncertainty_reduction": 5,
        "rationale": "Independent review catches errors — small cost, significant credibility gain."
    })

    # Sort by benefit/cost ratio
    for a in actions:
        a["ratio"] = a["uncertainty_reduction"] / max(a["est_cost"], 1) * 1000

    actions.sort(key=lambda a: a["ratio"], reverse=True)

    # Assign priorities
    for i, a in enumerate(actions):
        a["priority"] = i + 1

    return actions


def build_diminishing_returns_data(actions):
    """Build cumulative spend vs uncertainty reduction curve."""
    spend = [0]
    remaining = [100]

    running_spend = 0
    running_remaining = 100

    for a in actions:
        running_spend += a["est_cost"]
        running_remaining = max(5, running_remaining - a["uncertainty_reduction"])
        spend.append(running_spend)
        remaining.append(running_remaining)

    return spend, remaining


# ═══════════════════════════════════════════════════════════════════════════════
# GRAPHVIZ DECISION TREE
# ═══════════════════════════════════════════════════════════════════════════════

def build_decision_tree_diagram():
    dot = graphviz.Digraph(comment="CfD Decision Tree", format="svg")
    dot.attr(rankdir="TB", fontname="Helvetica", bgcolor="transparent")
    dot.attr("node", fontname="Helvetica", fontsize="11", style="filled", shape="box",
             color="#5c4a3a", fontcolor="white")
    dot.attr("edge", fontname="Helvetica", fontsize="10", color="#8b7355")

    q_color = "#6b4226"
    term_boundary = "#b8860b"

    questions = [
        ("Q1", "What measurement boundary\nis accessible?"),
        ("Q2", "Is the load constant\nor variable?"),
        ("Q3", "How many independent\nvariables drive energy use?"),
        ("Q4", "Are savings large enough\nto detect at this boundary?"),
        ("Q5", "How much baseline\ndata is available?"),
    ]
    for nid, label in questions:
        dot.node(nid, label, fillcolor=q_color, shape="diamond", width="3", height="1.2")

    terminals = [
        ("T_SIM", "Engineering / Physical\nSimulation Counterfactual\n(simulation-defined boundary)"),
        ("T_STIP", "Equipment-Level\nStipulated Key-Parameter\nCounterfactual"),
        ("T_DIRECT", "Equipment-Level\nDirect Measurement\nCounterfactual"),
        ("T_EQ_REG", "Equipment-Level\nStatistical Regression\nCounterfactual"),
        ("T_WB_REG", "Whole-Building\nStatistical Regression\nCounterfactual"),
        ("T_WB_MULTI", "Whole-Building\nMultivariable / Hybrid\nCounterfactual"),
        ("T_NARROW", "Consider Tightening\nBoundary to Equipment\n(small signal at WB level)"),
    ]
    for nid, label in terminals:
        dot.node(nid, label, fillcolor=term_boundary, shape="box",
                 style="filled,rounded", width="2.5", height="1")

    dot.edge("Q1", "T_SIM", label="Simulation model\navailable")
    dot.edge("Q1", "Q4", label="Whole-building\nmeter only")
    dot.edge("Q1", "Q2", label="Sub-meter on\naffected equipment")
    dot.edge("Q2", "T_STIP", label="Constant load\n(budget-constrained)")
    dot.edge("Q2", "T_DIRECT", label="Constant load\n(accuracy priority)")
    dot.edge("Q2", "Q3", label="Variable load")
    dot.edge("Q3", "T_EQ_REG", label="Single variable\n(e.g., temperature)")
    dot.edge("Q3", "Q5", label="Multiple variables")
    dot.edge("Q4", "T_WB_REG", label="Yes — savings\ndetectable")
    dot.edge("Q4", "T_NARROW", label="No — signal\ntoo small")
    dot.edge("Q5", "T_WB_MULTI", label="12+ months\navailable")
    dot.edge("Q5", "T_EQ_REG", label="Limited data —\nsimplify model")
    dot.edge("Q5", "T_SIM", label="No baseline data —\nuse simulation")

    # Highlight recommended terminal
    highlight_map = {
        "Engineering / physical simulation model": "T_SIM",
        "Stipulated key-parameter model": "T_STIP",
        "Direct measurement (metered before/after comparison)": "T_DIRECT",
        "Single-variable statistical regression": "T_EQ_REG",
        "Multivariable statistical regression": "T_EQ_REG",
        "Multivariable statistical regression or hybrid model": "T_WB_MULTI",
    }
    highlight_id = highlight_map.get(model_rec)
    if boundary_rec == "Whole-building meter" and model_rec == "Single-variable statistical regression":
        highlight_id = "T_WB_REG"
    if highlight_id:
        for nid, label in terminals:
            if nid == highlight_id:
                dot.node(nid, label, fillcolor=term_boundary, shape="box",
                         style="filled,rounded,bold", width="2.5", height="1",
                         penwidth="4", color="#facc15")
                break

    return dot


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN LAYOUT — Three Tabs
# ═══════════════════════════════════════════════════════════════════════════════

st.title("M&V Design + Uncertainty Budget")
st.caption(
    "Counterfactual Designs framework — design your M&V approach, "
    "then see where every dollar should go."
)
st.markdown(
    "*The core question: What would energy use have been without the intervention — "
    "and how confident are you in the answer?*"
)

tab1, tab2, tab3, tab4 = st.tabs([
    "🌳 Decision Tree",
    "💰 Uncertainty Budget",
    "🧪 Judgment Lab",
    "⚖️ Combined View",
])


# ─── TAB 1: Decision Tree ────────────────────────────────────────────────────

with tab1:
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Decision Tree")
        dot = build_decision_tree_diagram()
        st.graphviz_chart(dot, use_container_width=True)

    with col2:
        st.subheader("Your Counterfactual Design")
        st.markdown("*Based on your project context:*")
        st.markdown(f"**Boundary:** {boundary_rec}")
        st.markdown(f"**Model Form:** {model_rec}")
        st.markdown(f"**Duration:** {duration_rec}")
        st.divider()
        st.markdown("#### Why this design?")
        for bullet in rationale_bullets:
            st.markdown(bullet)
        st.divider()
        st.markdown(
            "**Savings =** Counterfactual prediction under reporting-period conditions "
            "**minus** measured reporting-period energy use."
        )

    # Three Dimensions Reference
    st.subheader("The Three Design Dimensions")
    st.markdown("""
Every M&V counterfactual design is defined by three choices:

| Dimension | Question | Options |
|-----------|----------|---------|
| **Boundary** | What do you draw the measurement boundary around? | Equipment/system, whole building, campus/portfolio |
| **Model Form** | How do you construct the counterfactual? | Stipulated parameters, statistical regression, engineering simulation, hybrid |
| **Duration** | How much data do you need? | Baseline period length, reporting period length, data granularity |

These three dimensions replace protocol labels (A, B, C, D) with **explicit design choices**.
""")


# ─── TAB 2: Uncertainty Budget ───────────────────────────────────────────────

with tab2:
    actions = build_uncertainty_budget()
    annual_dollars = annual_savings_kwh * rate_per_kwh

    st.subheader("The Uncertainty Budget Algorithm")
    st.markdown("""
    Every M&V dollar should buy the maximum reduction in risk. The algorithm:

    **1. Identify** all sources of uncertainty (aleatory, epistemic, ontological)
    → **2. Quantify** the cost and benefit of each reduction action
    → **3. Optimize** — allocate where marginal risk reduction is greatest
    → **4. Implement** meters, models, and protocols
    → **5. Iterate** as new data arrives
    """)

    # Headline metrics
    total_cost = sum(a["est_cost"] for a in actions)
    total_reduction = min(95, sum(a["uncertainty_reduction"] for a in actions))
    at_risk = annual_dollars * (1 - total_reduction / 100)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Annual Savings", f"${annual_dollars:,.0f}")
    c2.metric("M&V Budget", f"${mv_budget:,.0f}")
    c3.metric("Budget Actions Cost", f"${total_cost:,.0f}")
    c4.metric("Uncertainty Reduced", f"{total_reduction}%")

    st.divider()

    # Budget allocation table
    st.subheader("Prioritized M&V Actions")

    type_colors = {"Aleatory": "🔵", "Epistemic": "🟢", "Ontological": "🔴"}

    df = pd.DataFrame([{
        "Priority": f"#{a['priority']}",
        "M&V Action": a["action"],
        "Type": f"{type_colors.get(a['type'], '')} {a['type']}",
        "Est. Cost": f"${a['est_cost']:,}",
        "Uncertainty Reduction": f"{a['uncertainty_reduction']}%",
        "Rationale": a["rationale"],
    } for a in actions])

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    # Diminishing returns chart
    st.subheader("Diminishing Returns — Where to Stop")

    spend, remaining = build_diminishing_returns_data(actions)

    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor("#faf6f1")
    ax.set_facecolor("#ffffff")

    ax.plot(spend, remaining, color="#065A82", linewidth=2.5, marker="o", markersize=6)
    ax.fill_between(spend, remaining, alpha=0.08, color="#065A82")

    # Annotate each action
    for i, a in enumerate(actions):
        ax.annotate(
            f"{a['action'][:30]}...",
            xy=(spend[i + 1], remaining[i + 1]),
            xytext=(10, 10), textcoords="offset points",
            fontsize=7, color="#4a3f35", alpha=0.8,
            arrowprops=dict(arrowstyle="-", color="#8b7355", lw=0.5),
        )

    ax.set_xlabel("Cumulative M&V Spend ($)", fontsize=11, color="#3d3229")
    ax.set_ylabel("Uncertainty Remaining (%)", fontsize=11, color="#3d3229")
    ax.set_ylim(0, 105)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"${x:,.0f}"))
    ax.grid(axis="y", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    st.pyplot(fig)
    plt.close()

    st.divider()

    # Three uncertainty types
    st.subheader("Three Uncertainty Types → Three Investment Strategies")

    t1, t2, t3 = st.columns(3)

    with t1:
        st.markdown("#### 🔵 Aleatory")
        st.markdown("*Irreducible randomness*")
        st.markdown("""
        **Strategy:** More data points. Longer baselines. Better statistical models.

        **Actions:** Baseline data collection, regression model fitting, extended reporting periods.

        **What it buys:** Tighter confidence intervals around the counterfactual prediction.
        """)

    with t2:
        st.markdown("#### 🟢 Epistemic")
        st.markdown("*Reducible by better knowledge*")
        st.markdown("""
        **Strategy:** Better instruments. Submetering. Bayesian updating. Expert analysis.

        **Actions:** Spot measurements, continuous metering, simulation calibration, QA/QC.

        **What it buys:** Replaces assumptions with measurements — directly shrinks the uncertainty band.
        """)

    with t3:
        st.markdown("#### 🔴 Ontological")
        st.markdown("*The world doesn't fit your model*")
        st.markdown("""
        **Strategy:** NRA protocols. Scenario planning. Contingency reserves. Professional judgment.

        **Actions:** Non-routine adjustment protocols, interactive effects analysis, change monitoring.

        **What it buys:** Protection against real-world changes that would otherwise mask or inflate savings.
        """)


# ─── TAB 3: Judgment Lab ──────────────────────────────────────────────────────

with tab3:
    st.subheader("🧪 The Judgment Lab")
    st.markdown("""
    *M&V is not a flowchart — it's a series of judgment calls under uncertainty.*

    In real projects, you don't get to collect all the data you want. You have a finite
    budget, a skeptical stakeholder, and a deadline. The question is never "what's the
    best M&V plan?" — it's **"what's the best plan I can defend with the resources I have?"**

    Use this lab to explore the tradeoffs. Toggle actions on and off, watch the
    uncertainty move, and develop your instinct for when *enough is enough*.
    """)

    st.divider()

    # Get all possible actions
    all_actions = build_uncertainty_budget()

    st.markdown("### Your M&V Menu")
    st.markdown("Check the actions you'd include in your plan. Watch the budget and uncertainty respond.")

    # Interactive checkboxes for each action
    selected_actions = []
    running_cost = 0

    for i, a in enumerate(all_actions):
        type_icon = {"Aleatory": "🔵", "Epistemic": "🟢", "Ontological": "🔴"}.get(a["type"], "⚪")

        col_check, col_desc, col_cost, col_reduction = st.columns([0.5, 4, 1.2, 1.2])
        with col_check:
            include = st.checkbox("", value=True, key=f"action_{i}")
        with col_desc:
            st.markdown(f"{type_icon} **{a['action']}**")
        with col_cost:
            st.markdown(f"${a['est_cost']:,}")
        with col_reduction:
            st.markdown(f"−{a['uncertainty_reduction']}% unc.")

        if include:
            selected_actions.append(a)
            running_cost += a["est_cost"]

    st.divider()

    # Live scoreboard
    selected_reduction = min(95, sum(a["uncertainty_reduction"] for a in selected_actions))
    remaining_unc = 100 - selected_reduction
    over_budget = running_cost > mv_budget

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Your Plan Cost", f"${running_cost:,}",
              delta=f"{'OVER' if over_budget else 'Under'} by ${abs(mv_budget - running_cost):,}",
              delta_color="inverse" if over_budget else "normal")
    s2.metric("Uncertainty Reduced", f"{selected_reduction}%")
    s3.metric("Uncertainty Remaining", f"{remaining_unc}%")

    savings_at_risk = annual_savings_kwh * rate_per_kwh * remaining_unc / 100
    s4.metric("Savings at Risk", f"${savings_at_risk:,.0f}",
              help="The dollar value of savings that remain uncertain — the cost of NOT measuring.")

    if over_budget:
        st.warning(f"⚠️ Your plan costs ${running_cost:,} but your budget is ${mv_budget:,}. "
                   "What would you cut? That's the judgment call.")

    st.divider()

    # The hard questions
    st.markdown("### Reflection Questions")
    st.markdown("""
    These are the questions a CMVP should be able to answer about their plan:
    """)

    questions = [
        "Which action gives you the most uncertainty reduction per dollar? Is it in your plan?",
        "If you had to cut one action to stay on budget, which would it be and why?",
        f"Your remaining uncertainty is {remaining_unc}%. Is that acceptable for this project? What would the stakeholder say?",
        "Are you spending on the right *type* of uncertainty? (If the real risk is ontological, more meters won't help.)",
        f"${savings_at_risk:,.0f} of savings are still at risk. Is that number small enough to defend?",
        "Could you make a cheaper plan that covers 80% of the uncertainty? (The 80/20 rule applies here.)",
    ]
    for q in questions:
        st.markdown(f"- {q}")

    st.divider()

    # Scenario comparison
    st.markdown("### Quick Scenarios")
    st.markdown("*How would different budgets change your plan?*")

    scenarios = [
        ("Shoestring ($5k)", 5000),
        ("Balanced ($15k)", 15000),
        ("High-confidence ($30k)", 30000),
        ("Performance contract ($50k)", 50000),
    ]

    scenario_cols = st.columns(len(scenarios))
    for col, (name, budget) in zip(scenario_cols, scenarios):
        with col:
            # Pick actions that fit within this budget
            fitted = []
            budget_left = budget
            for a in all_actions:  # already sorted by ratio
                if a["est_cost"] <= budget_left:
                    fitted.append(a)
                    budget_left -= a["est_cost"]
            red = min(95, sum(a["uncertainty_reduction"] for a in fitted))
            cost = sum(a["est_cost"] for a in fitted)
            risk = annual_savings_kwh * rate_per_kwh * (100 - red) / 100

            st.markdown(f"**{name}**")
            st.markdown(f"Actions: {len(fitted)} of {len(all_actions)}")
            st.markdown(f"Spend: ${cost:,}")
            st.markdown(f"Uncertainty: {100 - red}% remaining")
            st.markdown(f"Risk: ${risk:,.0f}")

    st.info(
        "💡 **The punchline:** Notice how the $5k plan still covers a lot of ground? "
        "And the jump from $30k to $50k barely moves the needle? "
        "That's diminishing returns — the most important concept in M&V budgeting."
    )


# ─── TAB 4: Combined View ────────────────────────────────────────────────────

with tab4:
    actions = build_uncertainty_budget()

    st.subheader("Your M&V Design + Uncertainty Budget")
    st.markdown("*Your counterfactual design determines which uncertainty sources matter most — "
                "and where your M&V dollars should go.*")

    # Design summary card
    st.markdown(f"""
<div class="design-card">
    <strong>Recommended Design:</strong><br>
    <strong>Boundary:</strong> {boundary_rec}<br>
    <strong>Model Form:</strong> {model_rec}<br>
    <strong>Duration:</strong> {duration_rec}
</div>
""", unsafe_allow_html=True)

    # Uncertainty profile by type
    aleatory_pct = sum(a["uncertainty_reduction"] for a in actions if a["type"] == "Aleatory")
    epistemic_pct = sum(a["uncertainty_reduction"] for a in actions if a["type"] == "Epistemic")
    ontological_pct = sum(a["uncertainty_reduction"] for a in actions if a["type"] == "Ontological")

    aleatory_cost = sum(a["est_cost"] for a in actions if a["type"] == "Aleatory")
    epistemic_cost = sum(a["est_cost"] for a in actions if a["type"] == "Epistemic")
    ontological_cost = sum(a["est_cost"] for a in actions if a["type"] == "Ontological")

    st.markdown("### Uncertainty Profile by Type")

    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown(f"""
<div class="metric-card">
    <p>🔵 Aleatory (random)</p>
    <h3>{aleatory_pct}%</h3>
    <p>reduction · ${aleatory_cost:,} spend</p>
</div>
""", unsafe_allow_html=True)

    with p2:
        st.markdown(f"""
<div class="metric-card">
    <p>🟢 Epistemic (knowledge)</p>
    <h3>{epistemic_pct}%</h3>
    <p>reduction · ${epistemic_cost:,} spend</p>
</div>
""", unsafe_allow_html=True)

    with p3:
        st.markdown(f"""
<div class="metric-card">
    <p>🔴 Ontological (world-change)</p>
    <h3>{ontological_pct}%</h3>
    <p>reduction · ${ontological_cost:,} spend</p>
</div>
""", unsafe_allow_html=True)

    st.divider()

    # Stacked bar: spend by type
    st.markdown("### Budget Allocation by Uncertainty Type")

    fig2, ax2 = plt.subplots(figsize=(8, 2.5))
    fig2.patch.set_facecolor("#faf6f1")
    ax2.set_facecolor("#faf6f1")

    bar_data = [
        ("Aleatory", aleatory_cost, "#065A82"),
        ("Epistemic", epistemic_cost, "#2F855A"),
        ("Ontological", ontological_cost, "#C53030"),
    ]

    left = 0
    for label, cost, color in bar_data:
        if cost > 0:
            ax2.barh(0, cost, left=left, color=color, height=0.5, label=f"{label}: ${cost:,}")
            ax2.text(left + cost / 2, 0, f"${cost:,}\n{label}", ha="center", va="center",
                     fontsize=9, color="white", fontweight="bold")
            left += cost

    unspent = max(0, mv_budget - left)
    if unspent > 0:
        ax2.barh(0, unspent, left=left, color="#E2E8F0", height=0.5, label=f"Unallocated: ${unspent:,}")
        ax2.text(left + unspent / 2, 0, f"${unspent:,}\nUnallocated", ha="center", va="center",
                 fontsize=9, color="#64748B")

    ax2.set_xlim(0, max(mv_budget, left) * 1.05)
    ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"${x:,.0f}"))
    ax2.set_yticks([])
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_visible(False)

    st.pyplot(fig2)
    plt.close()

    st.divider()

    # Decision tree + budget side by side
    st.markdown("### Design ↔ Budget Connection")
    st.markdown("""
    Your **design choices** (Boundary, Model Form, Duration) determine which uncertainty
    sources dominate — and therefore where your M&V dollars have the most impact:
    """)

    connection_data = []
    if "regression" in model_rec.lower() or "statistical" in model_rec.lower():
        connection_data.append(("**Statistical regression** model form", "Aleatory uncertainty dominates → invest in more/better data points and model diagnostics"))
    if "stipulated" in model_rec.lower():
        connection_data.append(("**Stipulated parameter** model form", "Epistemic uncertainty dominates → invest in spot measurements to validate assumptions"))
    if "simulation" in model_rec.lower():
        connection_data.append(("**Simulation** model form", "Epistemic uncertainty dominates → invest in calibration and validation against metered data"))
    if "direct" in model_rec.lower():
        connection_data.append(("**Direct measurement** model form", "Continuous metering minimizes both aleatory and epistemic → budget goes to meter installation"))
    if "whole" in boundary_rec.lower():
        connection_data.append(("**Whole-building** boundary", "Ontological risk is high → invest in NRA protocols and change monitoring"))
    if savings_signal == "Small — may be difficult to distinguish from noise (<10%)":
        connection_data.append(("**Small savings signal**", "Aleatory risk is critical → invest in extended reporting period and tighter model"))

    for design_choice, implication in connection_data:
        st.markdown(f"- {design_choice} → {implication}")

    st.divider()
    st.markdown("### Key Takeaways")
    st.markdown(f"""
1. **Diminishing returns are real.** The first ${int(sum(a['est_cost'] for a in actions[:3])):,} of your M&V budget eliminates ~{sum(a['uncertainty_reduction'] for a in actions[:3])}% of uncertainty.

2. **Prioritize by marginal benefit-to-cost ratio**, not by ECM size. The highest-ratio action in your budget is: *{actions[0]['action']}*

3. **Match investment to uncertainty type.** Don't spend on better meters when the real risk is ontological (the world changing on you).

4. **The counterfactual is a designed artifact.** Your M&V budget of ${mv_budget:,} is the construction budget for that artifact.
""")


# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════

st.divider()
st.markdown(
    "Built on the [Counterfactual Designs](https://counterfactual-designs.com) framework "
    "by Steve Kromer, P.E., CMVP #1.  \n"
    "See also: [CfDesigns interactive platform](https://cfdesigns.vercel.app) · "
    "[Counterfactual Builder](https://mnvexample.streamlit.app) · "
    "[IPMVP-aligned course](https://mv-course.vercel.app)"
)
