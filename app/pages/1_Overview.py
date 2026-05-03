#!/usr/bin/env python3
"""🔆 Overview — SolarYield Dashboard"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------

PAGE_TITLE = "Overview — SolarYield"
PAGE_ICON = "🔆"

SYSTEM_CAPACITY_KW = 5000.0
SYSTEM_CAPACITY_MW = SYSTEM_CAPACITY_KW / 1000
DATA_DIR = "data"
DAILY_CSV = f"{DATA_DIR}/enriched_daily.csv"
HOURLY_CSV = "solar_yield_output.csv"

# ------------------------------------------------------------------
# Custom CSS
# ------------------------------------------------------------------

st.markdown("""
<style>
    .metric-card {
        background: #FFF9E6;
        border: 2px solid #F4A836;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
    }
    .metric-card .value {
        font-size: 2rem;
        font-weight: 700;
        color: #1E3A5F;
    }
    .metric-card .label {
        color: #666;
        font-size: 0.9rem;
    }
    .metric-card .delta-positive {
        color: #22C55E;
        font-weight: 600;
    }
    .metric-card .delta-negative {
        color: #EF4444;
        font-weight: 600;
    }
    .amber-divider {
        border: none;
        border-top: 3px solid #F4A836;
        margin: 2rem 0;
    }
    .chart-container > div {
        background: #FFFDF0;
        border-radius: 8px;
        padding: 0.5rem;
    }
    .section-header {
        color: #1E3A5F;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .chart-caption {
        color: #666;
        font-size: 0.85rem;
        font-style: italic;
        text-align: center;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Data loading
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

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# ------------------------------------------------------------------
# Load data
# ------------------------------------------------------------------

df_daily = load_daily_data()
df_hourly = load_hourly_data()

# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------

st.markdown("## ☀️ Overview — Solar Yield Analytics")
st.markdown("#### Singapore 5MW Solar Farm Performance Dashboard")

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# KPI Cards
# ------------------------------------------------------------------

# Calculate key metrics
total_days = len(df_daily)
total_energy_mwh = df_daily["kWh"].sum() / 1000
avg_daily_kwh = df_daily["kWh"].mean()
capacity_factor = (df_daily["kWh"].sum() / 1000) / (SYSTEM_CAPACITY_MW * total_days * 24) * 100

# Get latest values
latest_date = df_daily["date"].max()
latest_row = df_daily[df_daily["date"] == latest_date].iloc[0]
yesterday_idx = df_daily[df_daily["date"] == (latest_date - timedelta(days=1))]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="value">{total_energy_mwh:.1f} MWh</div>
        <div class="label">Total Energy Generated</div>
        <div class="delta-positive">↑ Lifetime</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="value">{avg_daily_kwh:.0f} kWh</div>
        <div class="label">Avg Daily Production</div>
        <div class="delta-positive">↑ Per Day</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="value">{capacity_factor:.1f}%</div>
        <div class="label">Capacity Factor</div>
        <div class="delta-positive">↑ Industry Avg: 15-20%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    anomaly_count = df_daily["anomaly"].sum() if "anomaly" in df_daily.columns else 0
    delta_str = f'<div class="delta-negative">⚠️ {int(anomaly_count)} Anomalies</div>' if anomaly_count > 0 else '<div class="delta-positive">✓ No Anomalies</div>'
    st.markdown(f"""
    <div class="metric-card">
        <div class="value">{int(anomaly_count)}</div>
        <div class="label">Total Anomalies</div>
        {delta_str}
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Daily Yield Chart
# ------------------------------------------------------------------

st.markdown("<div class='section-header'>📈 Daily Energy Production</div>", unsafe_allow_html=True)

fig_daily = go.Figure()
fig_daily.add_trace(go.Bar(
    x=df_daily["date"],
    y=df_daily["kWh"],
    marker_color="#F4A836",
    name="Daily kWh"
))
fig_daily.update_layout(
    template="plotly_white",
    height=400,
    xaxis_title="Date",
    yaxis_title="Energy (kWh)",
    plot_bgcolor="#FFFDF0",
    paper_bgcolor="#FFFDF0",
    font=dict(color="#1E3A5F")
)
st.plotly_chart(fig_daily, use_container_width=True)
st.markdown("<div class='chart-caption'>Daily energy production in kWh over the monitoring period. Peak days indicate optimal solar irradiance conditions.</div>", unsafe_allow_html=True)

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Capacity Factor Over Time
# ------------------------------------------------------------------

st.markdown("<div class='section-header'>⚡ Capacity Factor Trend</div>", unsafe_allow_html=True)

df_daily["capacity_factor"] = (df_daily["kWh"] / (SYSTEM_CAPACITY_KW * 24)) * 100

fig_cf = go.Figure()
fig_cf.add_trace(go.Scatter(
    x=df_daily["date"],
    y=df_daily["capacity_factor"],
    mode="lines",
    line=dict(color="#1E3A5F", width=2),
    fill="tozeroy",
    fillcolor="rgba(244, 168, 54, 0.3)",
    name="Capacity Factor %"
))
fig_cf.update_layout(
    template="plotly_white",
    height=350,
    xaxis_title="Date",
    yaxis_title="Capacity Factor (%)",
    plot_bgcolor="#FFFDF0",
    paper_bgcolor="#FFFDF0",
    font=dict(color="#1E3A5F")
)
st.plotly_chart(fig_cf, use_container_width=True)
st.markdown("<div class='chart-caption'>Capacity factor shows how efficiently the solar farm converts its theoretical maximum output into actual energy production.</div>", unsafe_allow_html=True)

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Irradiance vs Production Correlation
# ------------------------------------------------------------------

st.markdown("<div class='section-header'>☀️ Irradiance vs Energy Output</div>", unsafe_allow_html=True)

if "GHI" in df_daily.columns:
    fig_corr = px.scatter(
        df_daily,
        x="GHI",
        y="kWh",
        trendline="ols",
        color_discrete_sequence=["#F4A836"]
    )
    fig_corr.update_layout(
        template="plotly_white",
        height=400,
        plot_bgcolor="#FFFDF0",
        paper_bgcolor="#FFFDF0",
        font=dict(color="#1E3A5F"),
        xaxis_title="Global Horizontal Irradiance (GHI) W/m²",
        yaxis_title="Energy Production (kWh)"
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    st.markdown("<div class='chart-caption'>Strong correlation between solar irradiance (GHI) and energy output validates the PVLib physics model accuracy.</div>", unsafe_allow_html=True)
else:
    st.info("GHI data not available in daily dataset for correlation analysis.")

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Monthly Summary
# ------------------------------------------------------------------

st.markdown("<div class='section-header'>📅 Monthly Energy Summary</div>", unsafe_allow_html=True)

df_daily["month"] = df_daily["date"].dt.to_period("M")
monthly = df_daily.groupby("month").agg(
    total_kwh=("kWh", "sum"),
    avg_kwh=("kWh", "mean"),
    max_kwh=("kWh", "max"),
    days=("kWh", "count")
).reset_index()
monthly["month"] = monthly["month"].astype(str)

fig_monthly = go.Figure()
fig_monthly.add_trace(go.Bar(
    x=monthly["month"],
    y=monthly["total_kwh"] / 1000,
    marker_color="#F4A836",
    name="Monthly MWh"
))
fig_monthly.update_layout(
    template="plotly_white",
    height=400,
    xaxis_title="Month",
    yaxis_title="Total Energy (MWh)",
    plot_bgcolor="#FFFDF0",
    paper_bgcolor="#FFFDF0",
    font=dict(color="#1E3A5F")
)
st.plotly_chart(fig_monthly, use_container_width=True)
st.markdown("<div class='chart-caption'>Monthly aggregated energy production. Singapore's consistent solar irradiance enables year-round generation with minor seasonal variation.</div>", unsafe_allow_html=True)
