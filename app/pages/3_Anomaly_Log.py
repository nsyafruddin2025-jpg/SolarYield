#!/usr/bin/env python3
"""⚠️ Anomaly Log — SolarYield Dashboard"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------

PAGE_TITLE = "Anomaly Log — SolarYield"
PAGE_ICON = "⚠️"

DATA_DIR = "data"
DAILY_CSV = f"{DATA_DIR}/enriched_daily.csv"
HOURLY_CSV = "solar_yield_output.csv"

# ------------------------------------------------------------------
# Custom CSS
# ------------------------------------------------------------------

st.markdown("""
<style>
    .amber-divider {
        border: none;
        border-top: 3px solid #F4A836;
        margin: 2rem 0;
    }
    .section-header {
        color: #1E3A5F;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .chart-container > div {
        background: #FFFDF0;
        border-radius: 8px;
        padding: 0.5rem;
    }
    .chart-caption {
        color: #666;
        font-size: 0.85rem;
        font-style: italic;
        text-align: center;
        margin-top: 0.5rem;
    }
    .red-alert-banner {
        background: linear-gradient(135deg, #FEE2E2 0%, #FEF2F2 100%);
        border: 2px solid #EF4444;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    .red-alert-banner h3 {
        color: #EF4444;
        margin: 0;
    }
    .red-alert-banner p {
        color: #991B1B;
        margin: 0.5rem 0 0 0;
    }
    .anomaly-table {
        background-color: #FEF2F2 !important;
    }
    .anomaly-table th {
        background-color: #EF4444 !important;
        color: white !important;
    }
    .explanation-card {
        background: #F0F9FF;
        border: 1px solid #1E3A5F;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .explanation-card h4 {
        color: #1E3A5F;
        margin-top: 0;
    }
    .explanation-card p {
        color: #374151;
        margin-bottom: 0;
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

st.markdown("## ⚠️ Anomaly Log — Performance Deviation Detection")
st.markdown("#### Solar Yield Anomaly Detection & Alerting")

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Check anomaly count and show banner if > 10
# ------------------------------------------------------------------

anomaly_count = 0
if "anomaly" in df_daily.columns:
    anomaly_count = df_daily["anomaly"].sum()
elif "is_anomaly" in df_daily.columns:
    anomaly_count = df_daily["is_anomaly"].sum()

if anomaly_count > 10:
    st.markdown(f"""
    <div class="red-alert-banner">
        <h3>🚨 High Anomaly Count Detected</h3>
        <p><strong>{int(anomaly_count)} anomalies</strong> detected in the monitoring period. This may indicate systemic issues requiring investigation.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.success(f"✓ Anomaly count is within normal range: {int(anomaly_count)} anomalies detected")

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Explanation Card
# ------------------------------------------------------------------

st.markdown("""
<div class="explanation-card">
    <h4>🔍 What Does Anomaly Mean?</h4>
    <p>
        <strong>An anomaly means the farm produced significantly less energy than physics predicts given the weather conditions.</strong>
        Our model uses real-time weather data (irradiance, temperature, humidity) to predict expected energy output.
        When actual production falls significantly below this prediction, it's flagged as an anomaly.
    </p>
    <p style="margin-top: 1rem;">
        <strong>Common causes include:</strong>
    </p>
    <ul>
        <li>🔧 <strong>Panel soiling</strong> — dust, dirt, or debris reducing panel efficiency</li>
        <li>⚡ <strong>Inverter issues</strong> — equipment malfunction or reduced conversion efficiency</li>
        <li>🌳 <strong>Shading</strong> — new obstructions blocking sunlight (buildings, trees, equipment)</li>
        <li>🌡️ <strong>Thermal issues</strong> — extreme temperatures affecting panel performance</li>
        <li>🔌 <strong>Grid issues</strong> — connection problems or curtailment events</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Anomaly Timeline
# ------------------------------------------------------------------

st.markdown("<div class='section-header'>📅 Anomaly Timeline</div>", unsafe_allow_html=True)

# Get anomaly rows
anomaly_col = "anomaly" if "anomaly" in df_daily.columns else "is_anomaly"
df_anomalies = df_daily[df_daily[anomaly_col] == 1].copy() if anomaly_col in df_daily.columns else pd.DataFrame()

if len(df_anomalies) > 0:
    fig_anomaly = go.Figure()
    fig_anomaly.add_trace(go.Scatter(
        x=df_daily["date"],
        y=df_daily["kWh"],
        mode="lines",
        line=dict(color="#F4A836", width=2),
        name="Daily kWh"
    ))
    fig_anomaly.add_trace(go.Scatter(
        x=df_anomalies["date"],
        y=df_anomalies["kWh"],
        mode="markers",
        marker=dict(color="#EF4444", size=12, symbol="x"),
        name="Anomaly"
    ))
    fig_anomaly.update_layout(
        template="plotly_white",
        height=400,
        xaxis_title="Date",
        yaxis_title="Energy (kWh)",
        plot_bgcolor="#FFFDF0",
        paper_bgcolor="#FFFDF0",
        font=dict(color="#1E3A5F")
    )
    st.plotly_chart(fig_anomaly, use_container_width=True)
    st.markdown("<div class='chart-caption'>Daily energy production with anomaly points marked in red. Anomalies show days where actual output deviated significantly from the physics-based prediction.</div>", unsafe_allow_html=True)
else:
    st.info("No anomalies detected in the dataset using current thresholds.")

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Anomaly Details Table
# ------------------------------------------------------------------

st.markdown("<div class='section-header'>📋 Anomaly Details</div>", unsafe_allow_html=True)

if len(df_anomalies) > 0:
    # Prepare anomaly details
    df_anomaly_detail = df_anomalies[["date", "kWh", "GHI", "temp_cell"]].copy() if all(c in df_anomalies.columns for c in ["date", "kWh", "GHI", "temp_cell"]) else df_anomalies[["date", "kWh"]].copy()
    df_anomaly_detail["date"] = df_anomaly_detail["date"].dt.strftime("%Y-%m-%d")
    df_anomaly_detail.columns = ["Date", "kWh", "GHI (W/m²)", "Cell Temp (°C)"] if len(df_anomaly_detail.columns) == 3 else ["Date", "kWh"]

    st.dataframe(
        df_anomaly_detail.style.set_properties(**{
            "background-color": "#FEF2F2",
            "color": "#991B1B",
            "border": "1px solid #EF4444"
        }).set_table_styles([
            {"selector": "th", "props": [("background-color", "#EF4444"), ("color", "white"), ("font-weight", "bold")]},
            {"selector": "td", "props": [("background-color", "#FEF2F2")]},
        ]),
        use_container_width=True
    )
else:
    st.markdown("""
    <div style="background: #F0FDF4; border: 1px solid #22C55E; border-radius: 8px; padding: 2rem; text-align: center;">
        <h4 style="color: #166534; margin: 0;">✓ No Anomalies Detected</h4>
        <p style="color: #15803D; margin: 0.5rem 0 0 0;">All days in the monitoring period showed production within expected parameters.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Anomaly Statistics
# ------------------------------------------------------------------

st.markdown("<div class='section-header'>📊 Anomaly Statistics</div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_days = len(df_daily)
    anomaly_rate = (len(df_anomalies) / total_days * 100) if len(df_anomalies) > 0 else 0
    st.metric("Total Anomalies", int(len(df_anomalies)))

with col2:
    st.metric("Anomaly Rate", f"{anomaly_rate:.1f}%")

with col3:
    if len(df_anomalies) > 0 and "kWh" in df_anomalies.columns:
        avg_kwh_anomaly = df_anomalies["kWh"].mean()
        st.metric("Avg kWh on Anomaly Days", f"{avg_kwh_anomaly:.0f}")

with col4:
    if len(df_anomalies) > 0:
        avg_kwh_normal = df_daily[df_daily[anomaly_col] == 0]["kWh"].mean() if anomaly_col in df_daily.columns else 0
        st.metric("Avg kWh on Normal Days", f"{avg_kwh_normal:.0f}")
    else:
        st.metric("Avg kWh on Normal Days", "N/A")

# Show normal days average for comparison
if len(df_anomalies) > 0 and "kWh" in df_anomalies.columns:
    normal_days = df_daily[df_daily[anomaly_col] == 0]
    if len(normal_days) > 0:
        st.markdown(f"""
        <div style="background: #FFF9E6; border-left: 4px solid #F4A836; padding: 1rem; margin-top: 1rem;">
            <strong>Insight:</strong> Days with anomalies produced an average of
            <strong>{((avg_kwh_anomaly / avg_kwh_normal - 1) * 100):.1f}%</strong>
            {'less' if avg_kwh_anomaly < avg_kwh_normal else 'more'}
            energy than normal days.
        </div>
        """, unsafe_allow_html=True)
