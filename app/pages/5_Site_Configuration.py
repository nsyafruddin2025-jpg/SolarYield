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

# City database with irradiance-derived peak sun hours
CITIES = {
    "Singapore":    {"lat": 1.3521,  "lon": 103.8198, "peak_sun_hours": 5.2},
    "Jakarta":       {"lat": -6.2088, "lon": 106.8456, "peak_sun_hours": 4.8},
    "Manila":        {"lat": 14.5995, "lon": 120.9842, "peak_sun_hours": 5.0},
    "Bangkok":       {"lat": 13.7563, "lon": 100.5018, "peak_sun_hours": 4.9},
    "Kuala Lumpur":  {"lat": 3.1390,  "lon": 101.6869, "peak_sun_hours": 5.1},
    "Hanoi":         {"lat": 21.0285, "lon": 105.8542, "peak_sun_hours": 4.5},
    "Ho Chi Minh":   {"lat": 10.8231, "lon": 106.6297, "peak_sun_hours": 4.7},
    "Sydney":        {"lat": -33.8688,"lon": 151.2093, "peak_sun_hours": 5.5},
    "Melbourne":     {"lat": -37.8136,"lon": 144.9631, "peak_sun_hours": 4.8},
    "Brisbane":      {"lat": -27.4698,"lon": 153.0251, "peak_sun_hours": 5.7},
    "Perth":         {"lat": -31.9505,"lon": 115.8605, "peak_sun_hours": 6.0},
    "London":        {"lat": 51.5074,  "lon": -0.1278,  "peak_sun_hours": 2.9},
    "Manchester":    {"lat": 53.4808,  "lon": -2.2426,  "peak_sun_hours": 2.7},
    "New York":      {"lat": 40.7128,  "lon": -74.0060, "peak_sun_hours": 4.3},
    "Los Angeles":   {"lat": 34.0522,  "lon": -118.2437,"peak_sun_hours": 6.1},
    "Miami":         {"lat": 25.7617,  "lon": -80.1918, "peak_sun_hours": 5.4},
    "Dubai":         {"lat": 25.2048,  "lon": 55.2708,  "peak_sun_hours": 6.5},
    "Riyadh":        {"lat": 24.7136,  "lon": 46.6753,  "peak_sun_hours": 6.8},
    "Mumbai":        {"lat": 19.0760,  "lon": 72.8777,  "peak_sun_hours": 5.5},
    "Delhi":         {"lat": 28.6139,  "lon": 77.2090,  "peak_sun_hours": 5.2},
    "Tokyo":         {"lat": 35.6762,  "lon": 139.6503,  "peak_sun_hours": 4.2},
    "São Paulo":     {"lat": -23.5505, "lon": -46.6333, "peak_sun_hours": 5.1},
    "Mexico City":   {"lat": 19.4326,  "lon": -99.1332, "peak_sun_hours": 5.8},
    "Lagos":         {"lat": 6.5244,   "lon": 3.3792,   "peak_sun_hours": 5.3},
    "Nairobi":       {"lat": -1.2921,  "lon": 36.8219,  "peak_sun_hours": 5.9},
}


def calculate_dynamic_yield(capacity_kw, panel_tilt, panel_azimuth, panel_age, lat, peak_sun_hours):
    """
    Compute daily yield and revenue using location-aware optimal tilt/azimuth.

    - optimal_tilt  = abs(lat) * 0.87
    - optimal_azimuth = 180 if lat >= 0 else 0
    - Tilt loss   = 0.3% per degree deviation from optimal_tilt
    - Azimuth loss = 0.2% per degree deviation from optimal_azimuth
    - Age degradation = 0.5% per year (IEC standard)
    """
    optimal_tilt = abs(lat) * 0.87
    optimal_azimuth = 180.0 if lat >= 0 else 0.0

    # Parse panel_azimuth degrees
    az_map = {
        "South (180°)": 180, "Southwest (225°)": 225,
        "Southeast (135°)": 135, "East (90°)": 90,
        "West (270°)": 270, "North (0°)": 0,
    }
    panel_az_deg = az_map.get(panel_azimuth, 180)

    tilt_loss_pct = abs(panel_tilt - optimal_tilt) * 0.3
    az_loss_pct   = abs(panel_az_deg - optimal_azimuth) * 0.2
    age_loss_pct  = panel_age * 0.5

    total_loss = tilt_loss_pct + az_loss_pct + age_loss_pct
    efficiency_factor = max(0.0, (100 - total_loss) / 100)

    peak_kw     = capacity_kw * 0.18 * efficiency_factor
    daily_mwh   = peak_kw * peak_sun_hours / 1000
    annual_rev  = daily_mwh * 365 * 1000 * ELECTRICITY_RATE_USD

    return {
        "optimal_tilt":     optimal_tilt,
        "optimal_azimuth":  optimal_azimuth,
        "tilt_loss_pct":   tilt_loss_pct,
        "az_loss_pct":     az_loss_pct,
        "age_loss_pct":    age_loss_pct,
        "total_loss_pct":  total_loss,
        "efficiency_factor": efficiency_factor,
        "peak_kw":         peak_kw,
        "daily_mwh":       daily_mwh,
        "annual_revenue":  annual_rev,
    }

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

st.sidebar.image("app/assets/logo.png", width=120)

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
# Session state defaults (must exist before any widget uses them)
# ------------------------------------------------------------------

if "selected_city" not in st.session_state:
    st.session_state.selected_city = "Singapore"
if "lat_input" not in st.session_state:
    st.session_state.lat_input = CITIES["Singapore"]["lat"]
if "lon_input" not in st.session_state:
    st.session_state.lon_input = CITIES["Singapore"]["lon"]

# ------------------------------------------------------------------
# Multi-site base data — initialized once; user-added rows persist in
# session_state.multi_site_extra_rows (list of dicts, rebuilt below)
# ------------------------------------------------------------------
if "multi_site_extra_rows" not in st.session_state:
    st.session_state.multi_site_extra_rows = []

# Safely default site_name so row 0 never shows blank
_site_name_input = site_name if site_name and site_name.strip() else "Solar Farm"

# ------------------------------------------------------------------
# SECTION 1: Farm Identity
# ------------------------------------------------------------------

st.markdown("<div class='section-header'>🏭 Farm Identity</div>", unsafe_allow_html=True)

city_names = list(CITIES.keys())
default_idx = city_names.index(st.session_state.selected_city)

col1, col2 = st.columns(2)

with col1:
    site_name = st.text_input(
        "Site Name",
        value="Solar Farm",
        help="Display name for this solar installation"
    )

    selected_city = st.selectbox(
        "City",
        options=city_names,
        index=default_idx,
        key="city_selector",
        help="Select a city to auto-fill coordinates and irradiance data"
    )

    # Sync lat/lon when city changes
    if selected_city != st.session_state.selected_city:
        st.session_state.selected_city = selected_city
        st.session_state.lat_input = CITIES[selected_city]["lat"]
        st.session_state.lon_input = CITIES[selected_city]["lon"]
        st.rerun()

with col2:
    lat = st.number_input(
        "Latitude",
        min_value=-90.0,
        max_value=90.0,
        value=st.session_state.lat_input,
        step=0.0001,
        format="%.4f",
        key="lat_input",
        help="Decimal degrees, positive = North"
    )

    lon = st.number_input(
        "Longitude",
        min_value=-180.0,
        max_value=180.0,
        value=st.session_state.lon_input,
        step=0.0001,
        format="%.4f",
        key="lon_input",
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
    key="capacity_kw",
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
        key="panel_tilt",
        help="Angle from horizontal (0° = flat, 90° = vertical)"
    )

with col2:
    panel_azimuth = st.selectbox(
        "Panel Azimuth",
        options=["South (180°)", "Southwest (225°)", "Southeast (135°)"],
        index=0,
        key="panel_azimuth",
        help="compass direction panels face"
    )

with col3:
    panel_age = st.slider(
        "Panel Age",
        min_value=0,
        max_value=25,
        value=0,
        step=1,
        key="panel_age",
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

city = st.session_state.selected_city
peak_sun_hours = CITIES[city]["peak_sun_hours"]

# Compute optimal yield (no tilt/azimuth/age losses)
optimal_peak_kw    = capacity_kw * 0.18
optimal_daily_mwh  = optimal_peak_kw * peak_sun_hours / 1000
optimal_annual_rev = optimal_daily_mwh * 365 * 1000 * ELECTRICITY_RATE_USD

# Compute actual yield with dynamic losses
y = calculate_dynamic_yield(capacity_kw, panel_tilt, panel_azimuth, panel_age, lat, peak_sun_hours)

tilt_pct   = y["tilt_loss_pct"]
az_pct     = y["az_loss_pct"]
age_pct    = y["age_loss_pct"]
total_loss = y["total_loss_pct"]

st.markdown(f"""
<div class="yield-preview-box">
    <h4>📈 Yield Estimates — {city}</h4>
    <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
        <div class="kpi-card">
            <div class="value" style="color:#22C55E;">{optimal_peak_kw:,.1f} kW</div>
            <div class="label">★ Optimal Peak Output</div>
            <div class="label" style="font-size:0.75rem;">tilt={y["optimal_tilt"]:.1f}° · az={y["optimal_azimuth"]:.0f}°</div>
        </div>
        <div class="kpi-card">
            <div class="value" style="color:#F4A836;">{y["peak_kw"]:,.1f} kW</div>
            <div class="label">⚡ Actual Peak Output</div>
            <div class="label" style="font-size:0.75rem;">-{total_loss:.1f}% total loss</div>
        </div>
        <div class="kpi-card">
            <div class="value" style="color:#22C55E;">{optimal_daily_mwh:.2f} MWh</div>
            <div class="label">★ Optimal Daily Yield</div>
        </div>
        <div class="kpi-card">
            <div class="value" style="color:#F4A836;">{y["daily_mwh"]:.2f} MWh</div>
            <div class="label">⚡ Actual Daily Yield</div>
        </div>
        <div class="kpi-card">
            <div class="value" style="color:#22C55E;">${optimal_annual_rev:,.0f}</div>
            <div class="label">★ Optimal Annual Revenue</div>
        </div>
        <div class="kpi-card">
            <div class="value" style="color:#F4A836;">${y["annual_revenue"]:,.0f}</div>
            <div class="label">⚡ Actual Annual Revenue</div>
        </div>
    </div>
    <div style="margin-top:1rem; font-size:0.85rem; color:#555;">
        <strong>Loss Breakdown:</strong>
        Tilt: -{tilt_pct:.1f}% &nbsp;|&nbsp;
        Azimuth: -{az_pct:.1f}% &nbsp;|&nbsp;
        Age: -{age_pct:.1f}% &nbsp;|&nbsp;
        <strong>Total: -{total_loss:.1f}%</strong>
        &nbsp;&nbsp;|&nbsp;&nbsp;
        <strong>Eff:</strong> {y["efficiency_factor"]*100:.1f}%
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="info-note">
    ℹ️ Optimal tilt = |{lat:.2f}°| × 0.87 = <strong>{y["optimal_tilt"]:.1f}°</strong> ·
    Optimal azimuth = <strong>{y["optimal_azimuth"]:.0f}°</strong> ({city} is in the {'Northern' if lat >= 0 else 'Southern'} hemisphere) ·
    Peak sun hours for {city}: <strong>{peak_sun_hours}</strong>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# SECTION 4: Multi-Site Management
# ------------------------------------------------------------------

st.markdown("<div class='section-header'>🌐 Multi-Site Management</div>", unsafe_allow_html=True)

# --- Build sites_df: static base rows (Jakarta, Manila) stored in session ---
if "sites_df" not in st.session_state:
    st.session_state.sites_df = pd.DataFrame({
        "Site Name":       ["Jakarta Plant", "Manila Farm"],
        "Location":        ["-6.2088°, 106.8456°", "14.5995°, 120.9842°"],
        "Capacity (kWp)": [3000, 8000],
        "Age (years)":     [2, 1],
        "Est. Daily MWh":  [
            f"{3000 * 0.18 * 0.99 * CITIES['Jakarta']['peak_sun_hours'] / 1000:.2f}",
            f"{8000 * 0.18 * 0.995 * CITIES['Manila']['peak_sun_hours'] / 1000:.2f}",
        ],
        "Status":          ["Standby", "Standby"],
    })

# Safely default site_name to prevent blank cells
_display_name = site_name.strip() if site_name and site_name.strip() else "Solar Farm"

# --- Build display_df: Row 0 synced from Farm Identity + user-added rows ---
primary_row = pd.DataFrame([{
    "Site Name":       _display_name,
    "Location":        f"{lat:.4f}°, {lon:.4f}°",
    "Capacity (kWp)":  capacity_kw,
    "Age (years)":     panel_age,
    "Est. Daily MWh":  f"{y['daily_mwh']:.2f}",
    "Status":          "Active",
}])

# Restore user-added rows from prior session
user_added_rows = st.session_state.multi_site_extra_rows
if user_added_rows:
    user_df = pd.DataFrame(user_added_rows)
else:
    user_df = pd.DataFrame(columns=st.session_state.sites_df.columns)

display_df = pd.concat([primary_row, st.session_state.sites_df, user_df], ignore_index=True)

# --- Column config ---
col_config = {
    "Site Name": st.column_config.TextColumn(
        "Site Name",
        help="★ Row 0 (Primary Site) is auto-synced from Farm Identity above",
        width="medium",
    ),
    "Location": st.column_config.TextColumn(
        "Location",
        help="★ Row 0 is auto-synced from Farm Identity above",
        width="medium",
    ),
    "Capacity (kWp)": st.column_config.NumberColumn(
        "Capacity (kWp)", min_value=0, max_value=500000, format="%,.0f", width="small",
    ),
    "Age (years)": st.column_config.NumberColumn(
        "Age (years)", min_value=0, max_value=50, format="%d", width="small",
    ),
    "Est. Daily MWh": st.column_config.TextColumn("Est. Daily MWh", width="small"),
    "Status": st.column_config.SelectboxColumn(
        "Status", options=["Active", "Standby", "Decommissioned"], width="small",
    ),
}

# --- Render data_editor ---
result = st.data_editor(
    display_df,
    column_config=col_config,
    use_container_width=True,
    hide_index=False,
    num_rows="dynamic",
    key="main_site_editor",
)

# --- Capture edits: rebuild extra rows (rows 3+) and persist ---
total_static = 1 + len(st.session_state.sites_df)  # 1 primary + N base rows
if len(result) > total_static:
    extra = result.iloc[total_static:].copy()
    extra.loc[:, "Capacity (kWp)"] = extra["Capacity (kWp)"].astype(int)
    extra.loc[:, "Age (years)"] = extra["Age (years)"].astype(int)
    st.session_state.multi_site_extra_rows = extra.to_dict("records")
else:
    st.session_state.multi_site_extra_rows = []

st.markdown(
    "<div class='info-note'>💡 Row 0 (★ Primary Site) syncs from Farm Identity above — "
    "edits to row 0 are not saved. Rows 1+ are fully editable. Use + to add sites.</div>",
    unsafe_allow_html=True
)

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# SECTION 5: Save Configuration — wrapped in a minimal form
# ------------------------------------------------------------------

with st.form("save_form"):
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        submitted = st.form_submit_button(
            "💾 Save Configuration",
            type="primary",
            use_container_width=True
        )

    if submitted:
        st.success("Configuration saved! Forecast Explorer will use these parameters.")
        st.session_state.site_config = {
            "site_name":        site_name,
            "city":             city,
            "lat":              lat,
            "lon":              lon,
            "capacity_kw":      capacity_kw,
            "panel_tilt":       panel_tilt,
            "panel_azimuth":    panel_azimuth,
            "panel_age":        panel_age,
            "peak_kw":          y["peak_kw"],
            "daily_mwh":        y["daily_mwh"],
            "annual_revenue":   y["annual_revenue"],
        }

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------

st.caption(
    "☀️ SolarYield Site Configuration · Changes apply to yield forecasts across all pages"
)
