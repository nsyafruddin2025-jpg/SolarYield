#!/usr/bin/env python3
"""⚙️ Site Configuration — SolarYield Dashboard"""

import streamlit as st
import pandas as pd

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------

PAGE_TITLE = "Site Configuration — SolarYield"
PAGE_ICON = "⚙️"

ELECTRICITY_RATE_USD = 0.08
PEAK_SUN_HOURS = 5.2  # Singapore average

# ------------------------------------------------------------------
# Custom CSS
# ------------------------------------------------------------------

st.markdown("""
<style>
    .amber-divider {
        border: none;
        border-top: 3px solid #F4A836;
        margin: 1.5rem 0;
    }
    .section-header {
        color: #1E3A5F;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    .navy-banner {
        background: linear-gradient(135deg, #1E3A5F 0%, #0d2137 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .navy-banner .title {
        color: #F4A836;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .navy-banner .subtitle {
        color: #FFFFFF;
        font-size: 1.1rem;
    }
    .yield-preview-box {
        background: #FFF9E6;
        border: 3px solid #F4A836;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }
    .yield-preview-box h4 {
        color: #1E3A5F;
        margin-top: 0;
        margin-bottom: 1rem;
    }
    .kpi-card {
        background: #FFFFFF;
        border: 2px solid #F4A836;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .kpi-card .value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1E3A5F;
    }
    .kpi-card .label {
        color: #666;
        font-size: 0.85rem;
    }
    .info-note {
        background: #F0F9FF;
        border-left: 4px solid #1E3A5F;
        padding: 0.75rem 1rem;
        border-radius: 0 6px 6px 0;
        color: #374151;
        font-size: 0.9rem;
    }
    .status-active {
        background: #22C55E;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-standby {
        background: #9CA3AF;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .site-table {
        width: 100%;
        border-collapse: collapse;
    }
    .site-table th {
        background: #1E3A5F;
        color: white;
        padding: 0.75rem;
        text-align: left;
    }
    .site-table td {
        padding: 0.75rem;
        border-bottom: 1px solid #E5E7EB;
    }
    .site-table tr:hover {
        background: #FFF9E6;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# ------------------------------------------------------------------
# Navy gradient banner header
# ------------------------------------------------------------------

st.markdown("""
<div class="navy-banner">
    <div class="title">⚙️ Site Configuration</div>
    <div class="subtitle">Configure your solar farm parameters for accurate yield forecasting</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# All inputs in a form to prevent reload
# ------------------------------------------------------------------

with st.form("site_config_form"):

    # ------------------------------------------------------------------
    # SECTION 1: Farm Identity
    # ------------------------------------------------------------------

    st.markdown("<div class='section-header'>🏭 Farm Identity</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        site_name = st.text_input(
            "Site Name",
            value="Singapore 5MW Farm",
            help="Display name for this solar installation"
        )

        country = st.selectbox(
            "Country",
            options=["Singapore", "Indonesia", "Philippines", "Vietnam", "Thailand", "Australia"],
            index=0
        )

    with col2:
        lat = st.number_input(
            "Latitude",
            min_value=-90.0,
            max_value=90.0,
            value=1.3521,
            step=0.0001,
            format="%.4f",
            help="Decimal degrees, positive = North"
        )

        lon = st.number_input(
            "Longitude",
            min_value=-180.0,
            max_value=180.0,
            value=103.8198,
            step=0.0001,
            format="%.4f",
            help="Decimal degrees, positive = East"
        )

    # Map centered on coordinates
    map_df = pd.DataFrame({"lat": [lat], "lon": [lon]})
    st.map(map_df, zoom=10, height=250)

    st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # SECTION 2: System Parameters
    # ------------------------------------------------------------------

    st.markdown("<div class='section-header'>☀️ System Parameters</div>", unsafe_allow_html=True)

    capacity_kw = st.slider(
        "Installed Capacity",
        min_value=100,
        max_value=50000,
        value=5000,
        step=100,
        help="Total installed capacity in kilowatts-peak (kWp)"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        panel_tilt = st.slider(
            "Panel Tilt",
            min_value=0,
            max_value=45,
            value=20,
            step=1,
            help="Angle from horizontal (0° = flat, 90° = vertical)"
        )

    with col2:
        panel_azimuth = st.selectbox(
            "Panel Azimuth",
            options=["South (180°)", "Southwest (225°)", "Southeast (135°)"],
            index=0,
            help=" compass direction panels face"
        )

    with col3:
        panel_age = st.slider(
            "Panel Age",
            min_value=0,
            max_value=25,
            value=0,
            step=1,
            help="Years since installation"
        )

    st.markdown(
        "<div class='info-note'>ℹ️ Panel efficiency degrades approximately 0.5% per year per IEC standard</div>",
        unsafe_allow_html=True
    )

    st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # SECTION 3: Instant Yield Preview
    # ------------------------------------------------------------------

    st.markdown("<div class='section-header'>📊 Instant Yield Preview</div>", unsafe_allow_html=True)

    # Calculate yield estimates
    efficiency_factor = 1 - (panel_age * 0.005)
    peak_kw = capacity_kw * 0.18 * efficiency_factor
    daily_mwh = peak_kw * PEAK_SUN_HOURS / 1000
    annual_revenue = daily_mwh * 365 * 1000 * ELECTRICITY_RATE_USD

    st.markdown(f"""
    <div class="yield-preview-box">
        <h4>📈 Estimated Output Based on Current Settings</h4>
        <div style="display: flex; gap: 1rem; justify-content: center;">
            <div class="kpi-card">
                <div class="value">{peak_kw:,.1f} kW</div>
                <div class="label">Peak Hourly Output</div>
            </div>
            <div class="kpi-card">
                <div class="value">{daily_mwh:.2f} MWh</div>
                <div class="label">Est. Daily Output</div>
            </div>
            <div class="kpi-card">
                <div class="value">${annual_revenue:,.0f}</div>
                <div class="label">Est. Annual Revenue</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # SECTION 4: Multi-Site Management
    # ------------------------------------------------------------------

    st.markdown("<div class='section-header'>🌐 Multi-Site Management</div>", unsafe_allow_html=True)

    # Pre-configured demo sites
    demo_sites = [
        {
            "Site Name": "Singapore HQ",
            "Location": "1.3521°N, 103.8198°E",
            "Capacity (kWp)": 5000,
            "Age (years)": 0,
            "Est. Daily MWh": f"{(5000 * 0.18 * 1.0 * PEAK_SUN_HOURS / 1000):.2f}",
            "Status": '<span class="status-active">Active</span>'
        },
        {
            "Site Name": "Jakarta Plant",
            "Location": "-6.2088°S, 106.8456°E",
            "Capacity (kWp)": 3000,
            "Age (years)": 2,
            "Est. Daily MWh": f"{(3000 * 0.18 * 0.99 * PEAK_SUN_HOURS / 1000):.2f}",
            "Status": '<span class="status-standby">Standby</span>'
        },
        {
            "Site Name": "Manila Farm",
            "Location": "14.5995°N, 120.9842°E",
            "Capacity (kWp)": 8000,
            "Age (years)": 1,
            "Est. Daily MWh": f"{(8000 * 0.18 * 0.995 * PEAK_SUN_HOURS / 1000):.2f}",
            "Status": '<span class="status-standby">Standby</span>'
        },
    ]

    st.markdown("""
    <table class="site-table">
        <thead>
            <tr>
                <th>Site Name</th>
                <th>Location</th>
                <th>Capacity (kWp)</th>
                <th>Age (years)</th>
                <th>Est. Daily MWh</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
    """, unsafe_allow_html=True)

    for site in demo_sites:
        st.markdown(f"""
            <tr>
                <td>{site['Site Name']}</td>
                <td>{site['Location']}</td>
                <td>{site['Capacity (kWp)']:,}</td>
                <td>{site['Age (years)']}</td>
                <td>{site['Est. Daily MWh']}</td>
                <td>{site['Status']}</td>
            </tr>
        """, unsafe_allow_html=True)

    st.markdown("""
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div class='info-note'>💡 Enterprise plan supports unlimited sites. Contact us to add your installation.</div>",
        unsafe_allow_html=True
    )

    st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # SECTION 5: Save Configuration
    # ------------------------------------------------------------------

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        submitted = st.form_submit_button("💾 Save Configuration", type="primary", width='stretch')

    if submitted:
        st.success("Configuration saved! Forecast Explorer will use these parameters.")
        # Store in session state for other pages to use
        st.session_state.site_config = {
            "site_name": site_name,
            "country": country,
            "lat": lat,
            "lon": lon,
            "capacity_kw": capacity_kw,
            "panel_tilt": panel_tilt,
            "panel_azimuth": panel_azimuth,
            "panel_age": panel_age,
            "peak_kw": peak_kw,
            "daily_mwh": daily_mwh,
            "annual_revenue": annual_revenue
        }

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------

st.caption(
    "☀️ SolarYield Site Configuration · Changes apply to yield forecasts across all pages"
)
