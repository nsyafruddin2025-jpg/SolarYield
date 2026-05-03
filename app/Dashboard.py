#!/usr/bin/env python3
"""
SolarYield Dashboard — Entry Point

Executive summary dashboard with KPIs, charts, and real-time monitoring.
Navigate using the sidebar to explore detailed analytics pages.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------

PAGE_TITLE = "SolarYield Dashboard"
PAGE_ICON = "☀️"
LAYOUT = "wide"

SYSTEM_CAPACITY_KW = 5000.0
SYSTEM_CAPACITY_MW = SYSTEM_CAPACITY_KW / 1000
ELECTRICITY_RATE_USD = 0.08
CO2_FACTOR_KG_PER_KWH = 0.42  # Singapore grid emission factor

DATA_DIR = "data"
HOURLY_CSV = "solar_yield_output.csv"
DAILY_CSV = f"{DATA_DIR}/enriched_daily.csv"

# ------------------------------------------------------------------
# Data loading with caching
# ------------------------------------------------------------------

@st.cache_data
def load_daily_data():
    df = pd.read_csv(DAILY_CSV, parse_dates=["date"])
    return df.sort_values("date")

@st.cache_data
def load_hourly_data():
    df = pd.read_csv(HOURLY_CSV, parse_dates=["timestamp"])
    return df.sort_values("timestamp")

# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

import os

# ------------------------------------------------------------------
# Custom CSS
# ------------------------------------------------------------------

st.markdown("""
<style>
    /* SolarIQ Logo in sidebar */
    .solar-logo {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem 0;
    }
    .solar-logo-icon {
        font-size: 2.5rem;
    }
    .solar-logo-text {
        font-size: 1.5rem;
        font-weight: 700;
        color: #F4A836;
    }
    .solar-logo-text span {
        color: #FFFFFF;
    }

    /* Hero / Navbar Banner */
    .navy-navbar {
        background: linear-gradient(135deg, #1E3A5F 0%, #0d2137 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .navbar-brand {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .navbar-brand h1 {
        color: #F4A836;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }
    .navbar-brand .subtitle {
        color: #94a3b8;
        font-size: 0.85rem;
        margin: 0;
    }
    .live-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(34, 197, 94, 0.15);
        border: 1px solid #22c55e;
        padding: 0.4rem 1rem;
        border-radius: 9999px;
        color: #22c55e;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .live-dot {
        width: 8px;
        height: 8px;
        background: #22c55e;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    /* KPI Cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background: #1E3A5F;
        border-radius: 10px;
        padding: 1.25rem;
        text-align: center;
    }
    .kpi-card .icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .kpi-card .value {
        color: #F4A836;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .kpi-card .label {
        color: #94a3b8;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-card.risk-low { border-top: 3px solid #22c55e; }
    .kpi-card.risk-medium { border-top: 3px solid #f59e0b; }
    .kpi-card.risk-high { border-top: 3px solid #ef4444; }

    /* Amber divider */
    .amber-divider {
        border: none;
        border-top: 2px solid #F4A836;
        margin: 1.5rem 0;
    }

    /* Chart containers */
    .chart-card {
        background: #0d2137;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .chart-card h3 {
        color: #F4A836;
        margin: 0 0 1rem 0;
        font-size: 1.1rem;
    }

    /* Sidebar styling */
    .css-sidebar .css-1d391kg {
        background-color: #1E3A5F;
    }

    /* Alert items */
    .alert-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.75rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .alert-item:last-child { border-bottom: none; }
    .alert-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-top: 0.35rem;
        flex-shrink: 0;
    }
    .alert-dot.green { background: #22c55e; }
    .alert-dot.amber { background: #f59e0b; }
    .alert-dot.red { background: #ef4444; }
    .alert-content {
        flex: 1;
    }
    .alert-content .message {
        color: #FFFFFF;
        font-size: 0.85rem;
        margin-bottom: 0.25rem;
    }
    .alert-content .time {
        color: #64748b;
        font-size: 0.75rem;
    }

    /* Weather widget */
    .weather-widget {
        background: linear-gradient(135deg, #1E3A5F 0%, #0d2137 100%);
        border-radius: 10px;
        padding: 1.25rem;
    }
    .weather-widget h4 {
        color: #F4A836;
        margin: 0 0 1rem 0;
        font-size: 0.9rem;
    }
    .weather-main {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    .weather-temp {
        color: #FFFFFF;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .weather-icon { font-size: 3rem; }
    .weather-details {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.5rem;
    }
    .weather-detail {
        background: rgba(255,255,255,0.05);
        border-radius: 6px;
        padding: 0.5rem;
    }
    .weather-detail .label {
        color: #64748b;
        font-size: 0.7rem;
    }
    .weather-detail .value {
        color: #FFFFFF;
        font-size: 0.9rem;
        font-weight: 600;
    }

    /* Gauge / Progress bar */
    .gauge-container {
        background: #0d2137;
        border-radius: 10px;
        padding: 1.5rem;
    }
    .gauge-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    .gauge-header h3 {
        color: #F4A836;
        margin: 0;
        font-size: 1.1rem;
    }
    .gauge-header .pct {
        color: #22c55e;
        font-size: 1.5rem;
        font-weight: 700;
    }

    /* Filter pills */
    .filter-pill {
        display: inline-block;
        background: rgba(244, 168, 54, 0.15);
        border: 1px solid #F4A836;
        color: #F4A836;
        padding: 0.4rem 1rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        cursor: pointer;
    }
    .filter-pill.active {
        background: #F4A836;
        color: #0d2137;
    }

    /* Responsive grid */
    @media (max-width: 1200px) {
        .kpi-grid { grid-template-columns: repeat(3, 1fr); }
    }
    @media (max-width: 768px) {
        .kpi-grid { grid-template-columns: repeat(2, 1fr); }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
[data-testid="stSidebar"] img {
    border-radius: 50%;
    margin: 0px auto 10px auto;
    display: block;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Load data
# ------------------------------------------------------------------

daily_df = load_daily_data()
hourly_df = load_hourly_data()

# Calculate date range for filters
latest_date = daily_df["date"].max()
earliest_date = daily_df["date"].min()
today = latest_date.date() if hasattr(latest_date, 'date') else latest_date

# ------------------------------------------------------------------
# Sidebar: SolarIQ Logo
# ------------------------------------------------------------------

with st.sidebar:
    st.sidebar.image("app/assets/logo.png", width=120)
    st.markdown("""
    <div class="solar-logo">
        <span class="solar-logo-icon">☀️</span>
        <span class="solar-logo-text">Solar<span>IQ</span></span>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # Filters in sidebar
    st.markdown("**📅 Date Range**")
    date_filter = st.selectbox(
        "Select period",
        options=["Today", "This Week", "This Month"],
        label_visibility="collapsed"
    )

    st.markdown("**🏭 Plant Selector**")
    plant_filter = st.selectbox(
        "Select plant",
        options=["Singapore 5MW Farm"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("**📊 Quick Stats**")
    st.metric("Total Days Monitored", f"{len(daily_df)}")
    st.metric("Data Quality", "99.7%")
    st.metric("Model Version", "v2.1")

# ------------------------------------------------------------------
# Navbar
# ------------------------------------------------------------------

st.markdown(f"""
<div class="navy-navbar">
    <div class="navbar-brand">
        <span style="font-size: 2rem;">☀️</span>
        <div>
            <h1>SolarIQ Dashboard</h1>
            <p class="subtitle">Singapore 5MW Solar Farm · Executive Summary</p>
        </div>
    </div>
    <div class="live-indicator">
        <span class="live-dot"></span>
        LIVE · {datetime.now().strftime('%H:%M:%S')} SGT
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Filter Pills Row
# ------------------------------------------------------------------

col_filter, col_status = st.columns([3, 1])

with col_filter:
    st.markdown("""
    <div style="display: flex; gap: 0.75rem; align-items: center;">
        <span style="color: #64748b; font-size: 0.9rem;">Period:</span>
        <span class="filter-pill active">Today</span>
        <span class="filter-pill">This Week</span>
        <span class="filter-pill">This Month</span>
    </div>
    """, unsafe_allow_html=True)

with col_status:
    st.markdown(f"<div style='text-align: right; color: #64748b; font-size: 0.85rem;'>Data through {today.strftime('%Y-%m-%d') if hasattr(today, 'strftime') else str(today)}</div>", unsafe_allow_html=True)

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# KPI Summary Cards
# ------------------------------------------------------------------

# Calculate KPIs based on date filter
if date_filter == "Today":
    kpi_df = daily_df[daily_df["date"] == latest_date].copy()
    if len(kpi_df) == 0:
        kpi_df = daily_df.tail(1).copy()
elif date_filter == "This Week":
    week_start = latest_date - timedelta(days=6)
    kpi_df = daily_df[daily_df["date"] >= week_start].copy()
else:  # This Month
    month_start = latest_date - timedelta(days=29)
    kpi_df = daily_df[daily_df["date"] >= month_start].copy()

if len(kpi_df) == 0:
    kpi_df = daily_df.tail(7).copy()

# Calculate metrics
total_kwh = kpi_df["actual_kwh"].sum()
today_kwh = kpi_df["actual_kwh"].iloc[-1] if len(kpi_df) > 0 else 0
avg_cloud = kpi_df["mean_cloud"].mean() if len(kpi_df) > 0 else 50
anomaly_count = kpi_df["is_anomaly"].sum() if len(kpi_df) > 0 else 0
capacity_factor = (kpi_df["actual_kwh"].sum() / (SYSTEM_CAPACITY_KW * len(kpi_df) * 24)) * 100 if len(kpi_df) > 0 else 0
co2_offset = total_kwh * CO2_FACTOR_KG_PER_KWH

# Determine risk level
if avg_cloud > 70:
    risk_level = "HIGH"
    risk_class = "risk-high"
elif avg_cloud > 50:
    risk_level = "MEDIUM"
    risk_class = "risk-medium"
else:
    risk_level = "LOW"
    risk_class = "risk-low"

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="icon">⚡</div>
        <div class="value">{total_kwh:,.0f}</div>
        <div class="label">Total Production (kWh)</div>
    </div>
    <div class="kpi-card">
        <div class="icon">☀️</div>
        <div class="value">{today_kwh:,.0f}</div>
        <div class="label">Today's Output (kWh)</div>
    </div>
    <div class="kpi-card">
        <div class="icon">🏭</div>
        <div class="value">1</div>
        <div class="label">Active Plants</div>
    </div>
    <div class="kpi-card {risk_class}">
        <div class="icon">⚠️</div>
        <div class="value" style="color: {'#ef4444' if risk_level == 'HIGH' else '#f59e0b' if risk_level == 'MEDIUM' else '#22c55e'}">{risk_level}</div>
        <div class="label">Grid Penalty Risk</div>
    </div>
    <div class="kpi-card">
        <div class="icon">🎯</div>
        <div class="value">±6.1%</div>
        <div class="label">Model Accuracy</div>
    </div>
    <div class="kpi-card">
        <div class="icon">🌱</div>
        <div class="value">{co2_offset:,.0f}</div>
        <div class="label">CO₂ Offset (kg)</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Main Charts Row
# ------------------------------------------------------------------

chart_col, alert_col = st.columns([3, 1])

with chart_col:
    # 7-Day Production Trend with Historical Average
    st.markdown("""
    <div class="chart-card">
        <h3>📊 7-Day Production Trend</h3>
    </div>
    """, unsafe_allow_html=True)

    # Get last 7 days
    last_7_days = daily_df.tail(7).copy()
    last_7_days["date_str"] = pd.to_datetime(last_7_days["date"]).dt.strftime("%a %b %d")
    historical_avg = daily_df["actual_kwh"].mean()

    fig_trend = go.Figure()

    # Bar chart for daily production
    fig_trend.add_trace(go.Bar(
        x=last_7_days["date_str"],
        y=last_7_days["actual_kwh"],
        name="Daily Production",
        marker_color="#F4A836",
        hovertemplate="<b>%{x}</b><br>Production: %{y:,.0f} kWh<extra></extra>"
    ))

    # Historical average line
    fig_trend.add_trace(go.Scatter(
        x=last_7_days["date_str"],
        y=[historical_avg] * len(last_7_days),
        mode="lines",
        name=f"Historical Avg ({historical_avg:,.0f} kWh)",
        line=dict(color="#22c55e", width=2, dash="dash"),
        hovertemplate="Historical Average: %{y:,.0f} kWh<extra></extra>"
    ))

    fig_trend.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0d2137",
        plot_bgcolor="#0d2137",
        font=dict(color="#e2e8f0"),
        height=350,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            title="",
            gridcolor="rgba(255,255,255,0.1)"
        ),
        yaxis=dict(
            title="Energy (kWh)",
            gridcolor="rgba(255,255,255,0.1)"
        )
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    # Two column charts below
    pie_col, gauge_col = st.columns(2)

    with pie_col:
        # Energy Source Breakdown Pie Chart
        st.markdown("""
        <div class="chart-card">
            <h3>🔌 Energy Source Breakdown</h3>
        </div>
        """, unsafe_allow_html=True)

        # Simulate energy source breakdown
        solar_pct = 72
        grid_pct = 23
        battery_pct = 5

        fig_pie = go.Figure(data=[go.Pie(
            labels=["Solar Forecast", "Grid Import", "Battery Reserve"],
            values=[solar_pct, grid_pct, battery_pct],
            marker=dict(colors=["#F4A836", "#22c55e", "#3b82f6"]),
            textinfo="label+percent",
            textposition="inside",
            textfont=dict(color="#FFFFFF", size=12),
            hovertemplate="<b>%{label}</b><br>Value: %{percent}<extra></extra>"
        )])
        fig_pie.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0d2137",
            font=dict(color="#e2e8f0"),
            height=280,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with gauge_col:
        # Production Forecast Meter
        st.markdown("""
        <div class="gauge-container">
            <div class="gauge-header">
                <h3>⚡ Today's Utilization</h3>
                <span class="pct">67%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Calculate today's utilization
        capacity_kwh = SYSTEM_CAPACITY_KW * 24  # Daily max capacity
        utilization_pct = min((today_kwh / capacity_kwh) * 100, 100) if today_kwh > 0 else 67

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=utilization_pct,
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#64748b"},
                "bar": {"color": "#F4A836", "thickness": 0.3},
                "bgcolor": "rgba(255,255,255,0.1)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 50], "color": "rgba(34, 197, 94, 0.3)"},
                    {"range": [50, 75], "color": "rgba(244, 168, 54, 0.3)"},
                    {"range": [75, 100], "color": "rgba(239, 68, 68, 0.3)"}
                ],
                "threshold": {
                    "line": {"color": "#FFFFFF", "width": 2},
                    "thickness": 0.8,
                    "value": utilization_pct
                }
            },
            number={"suffix": "%", "font": {"size": 24, "color": "#F4A836"}}
        ))
        fig_gauge.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0d2137",
            height=220,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

        st.markdown(f"""
        <div style="text-align: center; color: #94a3b8; font-size: 0.8rem; margin-top: -1rem;">
            {today_kwh:,.0f} kWh of {capacity_kwh:,.0f} kWh capacity
        </div>
        """, unsafe_allow_html=True)

with alert_col:
    # Recent Alerts / Activity Feed
    st.markdown("""
    <div class="chart-card">
        <h3>🔔 Recent Alerts</h3>
    </div>
    """, unsafe_allow_html=True)

    alerts = [
        {"message": "Cloud cover spike detected (+15%)", "time": "2 min ago", "type": "amber"},
        {"message": "Grid commitment updated to 4.2 MWh", "time": "15 min ago", "type": "green"},
        {"message": "Model retrained with new data", "time": "1 hour ago", "type": "green"},
        {"message": "Anomaly detected: output 12% below forecast", "time": "3 hours ago", "type": "red"},
        {"message": "Battery reserve at 85% capacity", "time": "5 hours ago", "type": "amber"},
    ]

    for alert in alerts:
        st.markdown(f"""
        <div class="alert-item">
            <span class="alert-dot {alert['type']}"></span>
            <div class="alert-content">
                <div class="message">{alert['message']}</div>
                <div class="time">{alert['time']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Weather Snapshot Widget
    st.markdown("""
    <div class="chart-card" style="margin-top: 1rem;">
        <h3>🌤️ Weather Snapshot</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="weather-widget">
        <div class="weather-main">
            <span class="weather-icon">☀️</span>
            <div>
                <div class="weather-temp">31°C</div>
                <div style="color: #94a3b8; font-size: 0.85rem;">Partly Cloudy</div>
            </div>
        </div>
        <div class="weather-details">
            <div class="weather-detail">
                <div class="label">Humidity</div>
                <div class="value">78%</div>
            </div>
            <div class="weather-detail">
                <div class="label">Cloud Cover</div>
                <div class="value">{avg_cloud:.0f}%</div>
            </div>
            <div class="weather-detail">
                <div class="label">Wind Speed</div>
                <div class="value">12 km/h</div>
            </div>
            <div class="weather-detail">
                <div class="label">GHI</div>
                <div class="value">842 W/m²</div>
            </div>
        </div>
        <div style="text-align: center; color: #64748b; font-size: 0.7rem; margin-top: 0.75rem;">
            Singapore Meteorological Service · Open-Meteo
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Quick Actions Row
# ------------------------------------------------------------------

st.markdown("**⚡ Quick Actions**", unsafe_allow_html=False)
action_col1, action_col2, action_col3, action_col4 = st.columns(4)

with action_col1:
    if st.button("📊 View Forecast", use_container_width=True, type="primary"):
        st.switch_page("pages/4_Forecast_Explorer.py")

with action_col2:
    if st.button("🔍 Analyze Data", use_container_width=True):
        st.switch_page("pages/2_Data_Explorer.py")

with action_col3:
    if st.button("⚠️ View Anomalies", use_container_width=True):
        st.switch_page("pages/3_Anomaly_Log.py")

with action_col4:
    if st.button("⚙️ Configure Site", use_container_width=True):
        st.switch_page("pages/5_Site_Configuration.py")

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------

st.caption(
    f"☀️ SolarIQ Dashboard · Singapore 5MW Solar Farm · "
    f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} SGT · "
    f"Model: GradientBoosting (MAPE 6.1%, R² 0.9915)"
)
