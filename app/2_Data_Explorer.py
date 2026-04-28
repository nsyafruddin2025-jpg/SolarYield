#!/usr/bin/env python3
"""📊 Data Explorer — SolarYield Dashboard"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------

PAGE_TITLE = "Data Explorer — SolarYield"
PAGE_ICON = "📊"

DATA_DIR = "data"
HOURLY_CSV = "solar_yield_output.csv"
DAILY_CSV = f"{DATA_DIR}/enriched_daily.csv"

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
    .info-box {
        background: #FFF9E6;
        border: 1px solid #F4A836;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .dataframe-container table {
        background-color: #FFF9E6 !important;
    }
    .dataframe-container th {
        background-color: #F4A836 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Data loading
# ------------------------------------------------------------------

@st.cache_data
def load_hourly_data():
    df = pd.read_csv(HOURLY_CSV, parse_dates=["timestamp"])
    return df.sort_values("timestamp")

@st.cache_data
def load_daily_data():
    df = pd.read_csv(DAILY_CSV, parse_dates=["date"])
    return df.sort_values("date")

# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# ------------------------------------------------------------------
# Load data
# ------------------------------------------------------------------

df_hourly = load_hourly_data()
df_daily = load_daily_data()

# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------

st.markdown("## 📊 Data Explorer — Raw Data & Patterns")
st.markdown("#### Solar Yield Time Series Analysis")

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Solar Context Note
# ------------------------------------------------------------------

st.markdown("""
<div class="info-box">
    <h4 style="margin-top: 0; color: #1E3A5F;">☀️ Solar Context: Night Hours Behavior</h4>
    <p style="margin-bottom: 0; color: #1E3A5F;">
        <strong>Night hours (0-6, 18-24) show zero GHI and kWh output — this is expected solar behavior.</strong>
        Solar panels only generate electricity when sunlight hits them. During nighttime and early morning/late evening hours,
        there is insufficient solar irradiance for power generation. This pattern repeats daily and validates our
        monitoring system's data integrity.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Time Range Selection
# ------------------------------------------------------------------

st.markdown("<div class='section-header'>⏱️ Hourly Production Pattern</div>", unsafe_allow_html=True)

# Add hour column
df_hourly["hour"] = df_hourly["timestamp"].dt.hour

# Aggregate by hour across all days
hourly_pattern = df_hourly.groupby("hour").agg(
    avg_kwh=("kWh", "mean"),
    avg_ghi=("GHI", "mean") if "GHI" in df_hourly.columns else ("ghi", "mean"),
    count=("kWh", "count")
).reset_index()

fig_hourly = go.Figure()
fig_hourly.add_trace(go.Bar(
    x=hourly_pattern["hour"],
    y=hourly_pattern["avg_kwh"],
    marker_color="#F4A836",
    name="Avg kWh"
))
fig_hourly.add_trace(go.Scatter(
    x=hourly_pattern["hour"],
    y=hourly_pattern["avg_ghi"] / 100,
    mode="lines+markers",
    line=dict(color="#1E3A5F", width=2),
    yaxis="y2",
    name="GHI (scaled)"
))
fig_hourly.update_layout(
    template="plotly_white",
    height=400,
    xaxis_title="Hour of Day",
    yaxis_title="Avg Energy (kWh)",
    yaxis2=dict(title="GHI (÷100)", overlaying="y", side="right"),
    plot_bgcolor="#FFFDF0",
    paper_bgcolor="#FFFDF0",
    font=dict(color="#1E3A5F"),
    showlegend=True
)
st.plotly_chart(fig_hourly, use_container_width=True)
st.markdown("<div class='chart-caption'>Average hourly energy production pattern. Peak generation occurs between 10-14h when solar irradiance is maximum. Night hours (0-6, 18-24) show zero output as expected.</div>", unsafe_allow_html=True)

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Daily Pattern Heatmap
# ------------------------------------------------------------------

st.markdown("<div class='section-header'>🗓️ Daily Production Heatmap</div>", unsafe_allow_html=True)

# Create month-day pivot
df_hourly["month"] = df_hourly["timestamp"].dt.month
df_hourly["day"] = df_hourly["timestamp"].dt.day

# Aggregate by month and hour
daily_heatmap = df_hourly.groupby(["month", "hour"])["kWh"].mean().reset_index()
pivot_data = daily_heatmap.pivot(index="month", columns="hour", values="kWh")

fig_heatmap = px.imshow(
    pivot_data,
    labels=dict(x="Hour of Day", y="Month", color="Avg kWh"),
    color_continuous_scale="YlOrBr",
    aspect="auto"
)
fig_heatmap.update_layout(
    height=350,
    plot_bgcolor="#FFFDF0",
    paper_bgcolor="#FFFDF0",
    font=dict(color="#1E3A5F")
)
st.plotly_chart(fig_heatmap, use_container_width=True)
st.markdown("<div class='chart-caption'>Heatmap showing average hourly production by month. Darker colors indicate higher energy output during peak solar hours.</div>", unsafe_allow_html=True)

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Data Table
# ------------------------------------------------------------------

st.markdown("<div class='section-header'>📋 Raw Data Sample</div>", unsafe_allow_html=True)

# Show last 7 days of hourly data
last_date = df_hourly["timestamp"].max()
week_data = df_hourly[df_hourly["timestamp"] >= last_date - pd.Timedelta(days=7)].copy()
week_data["timestamp"] = week_data["timestamp"].dt.strftime("%Y-%m-%d %H:%M")

# Select key columns for display
display_cols = ["timestamp", "kWh", "GHI", "temp_cell", "humidity"] if all(c in week_data.columns for c in ["kWh", "GHI", "temp_cell", "humidity"]) else ["timestamp", "kWh"]
week_display = week_data[display_cols].head(50)

st.dataframe(
    week_display.style.set_properties(**{
        "background-color": "#FFF9E6",
        "color": "#1E3A5F",
        "border": "1px solid #F4A836"
    }).set_table_styles([
        {"selector": "th", "props": [("background-color", "#F4A836"), ("color", "white"), ("font-weight", "bold")]},
        {"selector": "td", "props": [("background-color", "#FFF9E6")]},
    ]),
    use_container_width=True
)

st.markdown(f"<div class='chart-caption'>Showing last {min(50, len(week_display))} records from the most recent week. Table uses amber header styling.</div>", unsafe_allow_html=True)

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Summary Statistics
# ------------------------------------------------------------------

st.markdown("<div class='section-header'>📈 Summary Statistics</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Hourly Data Summary")
    st.write(df_hourly[[c for c in df_hourly.columns if c not in ["hour", "month", "day"]]].describe())

with col2:
    st.markdown("#### Daily Data Summary")
    st.write(df_daily.describe())
