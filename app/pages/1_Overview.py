#!/usr/bin/env python3
"""
SolarYield Dashboard — Overview Page

KPI cards + 3 charts:
    1. Daily yield bar chart (past 30 days)
    2. Capacity factor trend (past 90 days)
    3. Actual vs predicted scatter (past 30 days, anomalies in red)
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

SYSTEM_CAPACITY_KW = 5000.0

st.set_page_config(page_title="Overview — SolarYield", layout="wide")

# ------------------------------------------------------------------
# Load data
# ------------------------------------------------------------------

daily = pd.read_csv("data/enriched_daily.csv", parse_dates=["date"]).sort_values("date")
hourly = pd.read_csv("solar_yield_output.csv", parse_dates=["timestamp"]).sort_values("timestamp")

# ------------------------------------------------------------------
# KPI calculations
# ------------------------------------------------------------------

today = daily["date"].max()
last_30d = daily[daily["date"] > today - pd.Timedelta(days=30)]
last_90d = daily[daily["date"] > today - pd.Timedelta(days=90)]

# Total MWh (past 30 days)
total_mwh_30d = last_30d["actual_kwh"].sum() / 1000

# Capacity factor (past 30 days) — actual kWh / (capacity_kW * hours in period)
hours_30d = len(last_30d) * 24
cap_factor_30d = (last_30d["actual_kwh"].sum() / (SYSTEM_CAPACITY_KW * hours_30d)) * 100

# Prior period for trend
prior_30d = daily[
    (daily["date"] > today - pd.Timedelta(days=60)) &
    (daily["date"] <= today - pd.Timedelta(days=30))
]
prior_cap_factor = (prior_30d["actual_kwh"].sum() / (SYSTEM_CAPACITY_KW * len(prior_30d) * 24)) * 100
cap_factor_trend = cap_factor_30d - prior_cap_factor

# Anomaly days (past 30 days)
anomaly_days_30d = last_30d["is_anomaly"].sum()

# Peak output (past 30 days)
peak_kwh_30d = last_30d["actual_kwh"].max()

# ------------------------------------------------------------------
# KPI Cards
# ------------------------------------------------------------------

st.header("📊 Key Performance Indicators — Past 30 Days")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Generation",
    f"{total_mwh_30d:.1f} MWh",
    help="Total kWh generated in the past 30 days",
)
col2.metric(
    "Capacity Factor",
    f"{cap_factor_30d:.1f}%",
    f"{cap_factor_trend:+.1f}% vs prior 30d",
    help="Actual output ÷ theoretical maximum (capacity × hours)",
)
col3.metric(
    "Anomaly Days",
    f"{int(anomaly_days_30d)}",
    help="Days where actual yield was >2σ below physics-predicted yield",
)
col4.metric(
    "Peak Daily Output",
    f"{peak_kwh_30d:,.0f} kWh",
    help="Maximum daily yield in the past 30 days",
)

st.divider()

# ------------------------------------------------------------------
# Chart 1: Daily Yield Bar Chart (past 30 days)
# ------------------------------------------------------------------

st.subheader("📈 Daily Yield — Past 30 Days")

chart_30d = last_30d.copy()
chart_30d["date_str"] = chart_30d["date"].dt.strftime("%Y-%m-%d")

fig_bar = px.bar(
    chart_30d,
    x="date_str",
    y="actual_kwh",
    title="Daily Yield (kWh)",
    labels={"date_str": "Date", "actual_kwh": "Yield (kWh)"},
    color="is_anomaly",
    color_discrete_map={True: "#ef4444", False: "#3b82f6"},
)
fig_bar.update_layout(showlegend=False, height=350)
st.plotly_chart(fig_bar, use_container_width=True)

# ------------------------------------------------------------------
# Chart 2: Capacity Factor Trend (past 90 days)
# ------------------------------------------------------------------

st.subheader("📉 Capacity Factor Trend — Past 90 Days")

chart_90d = last_90d.copy()
chart_90d["date_str"] = chart_90d["date"].dt.strftime("%Y-%m-%d")
chart_90d["cap_factor"] = (chart_90d["actual_kwh"] / (SYSTEM_CAPACITY_KW * 24)) * 100

fig_line = px.line(
    chart_90d,
    x="date_str",
    y="cap_factor",
    title="Daily Capacity Factor (%)",
    labels={"date_str": "Date", "cap_factor": "Capacity Factor (%)"},
    markers=True,
)
fig_line.update_layout(height=350)
st.plotly_chart(fig_line, use_container_width=True)

# ------------------------------------------------------------------
# Chart 3: Actual vs Predicted Scatter (past 30 days)
# ------------------------------------------------------------------

st.subheader("🔴 Actual vs Physics-Predicted Yield — Past 30 Days")

scatter_df = last_30d.copy()
scatter_df["date_str"] = scatter_df["date"].dt.strftime("%Y-%m-%d")
scatter_df["residual_label"] = scatter_df["is_anomaly"].map(
    {True: "Anomaly", False: "Normal"}
)

fig_scatter = px.scatter(
    scatter_df,
    x="predicted_kwh",
    y="actual_kwh",
    color="is_anomaly",
    color_discrete_map={True: "#ef4444", False: "#3b82f6"},
    hover_data=["date_str", "residual_kwh", "residual_sigma"],
    labels={
        "predicted_kwh": "Physics-Predicted Yield (kWh)",
        "actual_kwh": "Actual Yield (kWh)",
        "is_anomaly": "Status",
    },
)
# Add diagonal reference line (perfect prediction)
max_val = max(scatter_df["predicted_kwh"].max(), scatter_df["actual_kwh"].max())
fig_scatter.add_trace(go.Scatter(
    x=[0, max_val],
    y=[0, max_val],
    mode="lines",
    name="Perfect",
    line=dict(color="gray", dash="dash"),
    hoverinfo="skip",
))
fig_scatter.update_layout(height=400)
st.plotly_chart(fig_scatter, use_container_width=True)

# ------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------

st.caption(
    "SolarYield Dashboard · Singapore 5MW Solar Farm · "
    f"Data through {today.strftime('%Y-%m-%d')} · "
    "Anomaly detection: residual < rolling mean − 2σ"
)
