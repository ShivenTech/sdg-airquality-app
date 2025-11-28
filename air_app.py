# air_app.py

import streamlit as st
from air_logic import overall_health_risk

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Healthy Cities – Air Quality Risk",
    page_icon="🌱",
    layout="wide",
)

# ---------- GLOBAL STYLES ----------
st.markdown(
    """
    <style>
    /* Overall background */
    .stApp {
        background-color: #f3f4f6;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    /* Main container width + centering */
    .main-block {
        max-width: 1100px;
        margin: 0 auto;
        padding-bottom: 2rem;
    }

    /* Title / subtitle */
    .big-title {
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: 0.2rem;
    }
    .tagline {
        font-size: 15px;
        color: #4b5563;
        margin-bottom: 0.8rem;
    }

    /* Info / note box */
    .note-box {
        padding: 0.9rem 1.1rem;
        border-radius: 0.9rem;
        background: #ecfdf5;
        border: 1px solid #6ee7b7;
        font-size: 13px;
        color: #064e3b;
        margin-bottom: 1.2rem;
    }

    /* Cards */
    .card {
        padding: 1.25rem 1.4rem;
        border-radius: 0.9rem;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
    }

    /* Section headings */
    .section-title {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 0.6rem;
        color: #111827;
    }

    /* Small caption */
    .caption-small {
        font-size: 12px;
        color: #6b7280;
    }

    /* Streamlit button styling */
    .stButton>button {
        width: 100%;
        border-radius: 999px;
        background: linear-gradient(135deg, #22c55e, #16a34a);
        color: white;
        border: none;
        padding: 0.55rem 1rem;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #16a34a, #15803d);
    }

    /* Metric cards tweaks */
    div[data-testid="stMetricValue"] {
        font-size: 20px;
        font-weight: 700;
        color: #111827;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 11px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- SIDEBAR (INPUTS) ----------
st.sidebar.markdown("### 🌱 Air Quality Inputs")
st.sidebar.write("Enter air pollution readings for the area you want to analyse.")

location = st.sidebar.text_input(
    "Location / Area",
    placeholder="e.g. KL City Centre, Petaling Jaya, Penang",
)

pm25 = st.sidebar.slider(
    "PM2.5 (µg/m³)",
    min_value=0.0,
    max_value=300.0,
    value=35.0,
    step=1.0,
    help="Fine particulate matter ≤ 2.5 µm. Main factor for health risk.",
)

pm10 = st.sidebar.slider(
    "PM10 (µg/m³)",
    min_value=0.0,
    max_value=400.0,
    value=80.0,
    step=1.0,
    help="Coarse particulate matter ≤ 10 µm. Used to refine overall risk.",
)

analyse = st.sidebar.button("🔍 Analyse Health Risk")

st.sidebar.markdown("---")
st.sidebar.caption(
    "Tip: Use sensor or open data from DOE Malaysia / OpenAQ for real locations."
)

# ---------- MAIN CONTENT ----------
st.markdown('<div class="main-block">', unsafe_allow_html=True)

# Header
st.markdown(
    """
    <div>
        <div class="big-title">Healthy Cities – Air Quality Risk Assistant</div>
        <div class="tagline">
            SDG 3: Good Health & Well-Being · Subtopic: <b>Air Quality & Health Risks</b>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Note box
st.markdown(
    """
    <div class="note-box">
        <b>How this prototype works:</b><br/>
        • You input current PM2.5 and (optionally) PM10 readings from sensors or open datasets.<br/>
        • The system classifies air quality into categories (Good → Hazardous) based on guideline ranges.<br/>
        • It generates a simple health risk level and recommended actions for city residents.<br/>
        <br/>
        <span class="caption-small">
        ⚠️ This is an educational prototype. For serious health decisions, always follow official health & environmental advisories.
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Layout: summary + details
top_col1, top_col2 = st.columns([1.1, 1.2])

# --- SUMMARY CARD ---
with top_col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Air Quality Summary</div>', unsafe_allow_html=True)

    if analyse:
        category, risk_score, description = overall_health_risk(pm25, pm10)

        # risk badge
        if risk_score == 0:
            st.success(f"✅ Overall Air Quality: **{category}**")
        elif risk_score == 1:
            st.info(f"ℹ️ Overall Air Quality: **{category}**")
        elif risk_score == 2:
            st.warning(f"⚠️ Overall Air Quality: **{category}**")
        else:
            st.error(f"🚨 Overall Air Quality: **{category}**")

        if location:
            st.write(f"📍 *Location analysed:* **{location}**")

        # metrics row
        m1, m2 = st.columns(2)
        with m1:
            st.metric("PM2.5 (µg/m³)", f"{pm25:.1f}")
        with m2:
            st.metric("PM10 (µg/m³)", f"{pm10:.1f}")

    else:
        st.write("Use the controls on the **left sidebar** to enter pollution data, then click **Analyse Health Risk**.")
        st.caption("No data analysed yet.")

    st.markdown('</div>', unsafe_allow_html=True)

# --- HEALTH IMPACT CARD ---
with top_col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🩺 Health Impact & Recommended Actions</div>', unsafe_allow_html=True)

    if analyse:
        _, risk_score, description = overall_health_risk(pm25, pm10)

        st.write("**What this level means:**")
        st.write(description)

        st.markdown("**Recommended actions:**")

        if risk_score <= 1:
            st.write(
                "- Outdoor activities are generally **safe** for most people.\n"
                "- Sensitive groups (asthma, children, elderly) should still stay informed.\n"
                "- Keep monitoring air quality if there are nearby construction or forest fires."
            )
        elif risk_score == 2:
            st.write(
                "- People with asthma, children and elderly should **limit long outdoor activities**.\n"
                "- Consider wearing a **mask** during outdoor exposure.\n"
                "- Keep windows closed during peak pollution hours."
            )
        elif risk_score == 3:
            st.write(
                "- Everyone should **reduce outdoor activities**, especially exercise.\n"
                "- High-risk groups should **stay indoors** where air is cleaner.\n"
                "- Use **air purifiers / masks** if available and avoid busy roads."
            )
        else:
            st.write(
                "- **Avoid going outdoors** unless absolutely necessary.\n"
                "- Keep doors and windows **closed**.\n"
                "- Follow local government alerts and seek medical help if symptoms worsen."
            )
    else:
        st.write("Health impact and advice will appear here after you run an analysis.")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")  # spacing

# --- EXPLAINER / FOR JUDGES ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📘 For judges & educators: how the scoring works</div>', unsafe_allow_html=True)
st.write(
    """
    - Inputs: PM2.5 and PM10 readings (manually entered or from open datasets).
    - PM2.5 is classified using guideline-style ranges into:  
      **Good, Moderate, Unhealthy for Sensitive Groups, Unhealthy, Very Unhealthy, Hazardous.**
    - PM10 is classified similarly; the system takes the **worse category** between PM2.5 and PM10.
    - Each category is mapped to a risk score (0–5) that controls:
      - the colour and icon of the alert banner,
      - and which health recommendations are displayed.
    - This rule-based model can later be upgraded with:
      - live data streams from OpenAQ / DOE Malaysia,
      - and machine learning models trained on historical health outcomes.
    """
)
st.caption("Prototype for SDG XI Hackathon 2025 – Track: Healthy Cities · Subtopic: Air Quality & Health Risks.")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # end main-block
