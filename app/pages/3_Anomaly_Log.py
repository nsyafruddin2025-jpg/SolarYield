#!/usr/bin/env python3
"""
SolarYield Dashboard — Anomaly Log Page

Days flagged as anomalous (actual yield >2σ below physics-predicted).
Sorted by most anomalous first.

Columns: date, actual_kWh, predicted_kWh, residual_kWh, residual_sigma
"""

import pandas as pd
import plotly.express as px
import streamlit as st

SYSTEM_CAPACITY_KW = 5000.0

st.set_page_config(page_title="Anomaly Log — SolarYield", layout="wide")

# ------------------------------------------------------------------
# Load data
# ------------------------------------------------------------------

daily = pd.read_csv("data/enriched_daily.csv", parse_dates=["date"]).sort_values("date")

# ------------------------------------------------------------------
# Anomaly table
# ------------------------------------------------------------------

st.header("⚠️ Anomaly Log")
st.markdown(
    "Days where **actual yield was more than 2 standard deviations below "
    "the physics-predicted yield**. Common causes: panel soiling, inverter failure, "
    "shading, or weather sensor errors."
)

anomalies = daily[daily["is_anomaly"] == True].copy()
anomalies["date_str"] = anomalies["date"].dt.strftime("%Y-%m-%d")
anomalies["residual_sigma_abs"] = anomalies["residual_sigma"].abs()

# Sort by most anomalous first
anomalies = anomalies.sort_values("residual_sigma").reset_index(drop=True)

# Capacity factor for anomalous days
anomalies["cap_factor"] = (anomalies["actual_kwh"] / (SYSTEM_CAPACITY_KW * 24)) * 100

st.write(f"**{len(anomalies)} anomalous days** detected out of {len(daily)} total days")

# ------------------------------------------------------------------
# Anomaly table
# ------------------------------------------------------------------

table_cols = {
    "date_str": "Date",
    "actual_kwh": "Actual (kWh)",
    "predicted_kwh": "Predicted (kWh)",
    "residual_kwh": "Residual (kWh)",
    "residual_sigma": "Sigma (σ)",
    "cap_factor": "Capacity Factor (%)",
    "mean_temp": "Avg Temp (°C)",
    "mean_cloud": "Avg Cloud (%)",
}

st.dataframe(
    anomalies[list(table_cols.keys())].rename(columns=table_cols),
    width='stretch',
    hide_index=True,
)

# ------------------------------------------------------------------
# Severity chart
# ------------------------------------------------------------------

st.divider()
st.subheader("📊 Anomaly Severity — Residual kWh Below Prediction")

anomalies_chart = anomalies.copy()
anomalies_chart["date_str"] = anomalies_chart["date"].dt.strftime("%Y-%m-%d")

fig = px.bar(
    anomalies_chart,
    x="date_str",
    y="residual_kwh",
    title="Residual (kWh) — how far below physics prediction",
    labels={"date_str": "Date", "residual_kwh": "Residual (kWh)"},
    color="residual_sigma_abs",
    color_continuous_scale="Reds",
)
fig.update_layout(height=350)
st.plotly_chart(fig, width='stretch')

# ------------------------------------------------------------------
# Monthly anomaly distribution
# ------------------------------------------------------------------

st.subheader("📅 Monthly Anomaly Count")

anomalies["month"] = anomalies["date"].dt.to_period("M")
monthly = anomalies.groupby("month").size().reset_index(name="anomaly_count")
monthly["month_str"] = monthly["month"].astype(str)

all_monthly = daily.copy()
all_monthly["month"] = all_monthly["date"].dt.to_period("M")
all_monthly = all_monthly.groupby("month").size().reset_index(name="total_days")
merged = monthly.merge(all_monthly, on="month", how="left")
merged["anomaly_pct"] = (merged["anomaly_count"] / merged["total_days"]) * 100

fig2 = px.bar(
    merged,
    x="month_str",
    y="anomaly_count",
    title="Anomalous Days per Month",
    labels={"month_str": "Month", "anomaly_count": "Anomaly Days"},
    color="anomaly_pct",
    color_continuous_scale="Reds",
)
fig2.update_layout(height=300)
st.plotly_chart(fig2, width='stretch')

# ------------------------------------------------------------------
# Explanation
# ------------------------------------------------------------------

st.divider()
st.markdown("""
### How Anomalies Are Detected

1. **Physics prediction**: PVLib computes the expected daily yield using observed weather
   (GHI, DNI, DHI, temperature, cloud cover, humidity, wind speed)
2. **Residual**: `actual_kWh − predicted_kWh` — how far below physics the actual yield was
3. **Rolling baseline**: 30-day rolling mean and standard deviation of the residual
4. **Anomaly flag**: `residual < rolling_mean − 2 × rolling_std`

This method adapts to seasonal changes in the residual baseline, so haze in February–March
is correctly attributed as anomalous relative to the Singapore baseline for that time of year.
""")
