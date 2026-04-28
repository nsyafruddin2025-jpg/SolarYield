#!/usr/bin/env python3
"""
SolarYield Dashboard — Data Explorer Page

Paginated hourly data table (last 7 days default),
sortable by any column, filterable by date range.

Columns: timestamp, GHI, temperature, cloud_cover, kWh_output, anomaly_flag
"""

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Data Explorer — SolarYield", layout="wide")

# ------------------------------------------------------------------
# Load data
# ------------------------------------------------------------------

hourly = pd.read_csv("solar_yield_output.csv", parse_dates=["timestamp"]).sort_values("timestamp")
daily = pd.read_csv("data/enriched_daily.csv", parse_dates=["date"]).sort_values("date")

# Merge anomaly_flag from daily onto hourly
hourly["date"] = hourly["timestamp"].dt.date
daily["date"] = daily["date"].dt.date
hourly = hourly.merge(daily[["date", "is_anomaly", "residual_kwh"]], on="date", how="left")
hourly["is_anomaly"] = hourly["is_anomaly"].fillna(False).astype(bool)

# ------------------------------------------------------------------
# Filters
# ------------------------------------------------------------------

st.header("🔍 Data Explorer — Hourly Solar Data")

col_date1, col_date2 = st.columns(2)

with col_date1:
    start_date = st.date_input(
        "Start date",
        value=hourly["timestamp"].dt.date.max() - pd.Timedelta(days=7),
    )

with col_date2:
    end_date = st.date_input(
        "End date",
        value=hourly["timestamp"].dt.date.max(),
    )

# Filter by date range
mask = (
    (hourly["timestamp"].dt.date >= start_date) &
    (hourly["timestamp"].dt.date <= end_date)
)
filtered = hourly[mask].copy()

st.write(f"Showing **{len(filtered):,} rows** ({start_date} to {end_date})")

# ------------------------------------------------------------------
# Data table
# ------------------------------------------------------------------

display_cols = [
    "timestamp",
    "GHI",
    "direct_radiation",
    "diffuse_radiation",
    "temperature",
    "cloud_cover",
    "humidity",
    "wind_speed",
    "kWh_output",
    "is_anomaly",
]

st.dataframe(
    filtered[display_cols],
    width='stretch',
    hide_index=False,
)

# ------------------------------------------------------------------
# Summary stats for filtered period
# ------------------------------------------------------------------

st.divider()
st.subheader("📋 Summary Statistics")

summary_cols = ["GHI", "temperature", "cloud_cover", "humidity", "kWh_output"]
stats = filtered[summary_cols].describe().T
stats["missing"] = filtered[summary_cols].isnull().sum()
st.dataframe(stats, width='stretch')

# ------------------------------------------------------------------
# Export to CSV
# ------------------------------------------------------------------

csv = filtered[display_cols].to_csv(index=False)
st.download_button(
    "📥 Download filtered data as CSV",
    data=csv,
    file_name=f"solar_data_{start_date}_{end_date}.csv",
    mime="text/csv",
)
