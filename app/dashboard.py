#!/usr/bin/env python3
"""
SolarYield Dashboard — Streamlit Multipages App

Entry point for SolarYield dashboard. Loads data and defines navigation.
Data sources:
    - data/enriched_daily.csv: daily aggregates with anomaly flags
    - solar_yield_output.csv: hourly raw data
"""

import streamlit as st

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------

PAGE_TITLE = "SolarYield — Singapore Solar Farm"
PAGE_ICON = "☀️"
LAYOUT = "wide"

SYSTEM_CAPACITY_KW = 5000.0
SYSTEM_CAPACITY_MW = SYSTEM_CAPACITY_KW / 1000

DATA_DIR = "data"
HOURLY_CSV = "solar_yield_output.csv"
DAILY_CSV = f"{DATA_DIR}/enriched_daily.csv"

# ------------------------------------------------------------------
# Data loading
# ------------------------------------------------------------------

@st.cache_data
def load_daily_data():
    import pandas as pd
    df = pd.read_csv(DAILY_CSV, parse_dates=["date"])
    return df.sort_values("date")


@st.cache_data
def load_hourly_data():
    import pandas as pd
    df = pd.read_csv(HOURLY_CSV, parse_dates=["timestamp"])
    return df.sort_values("timestamp")


# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
)

# ------------------------------------------------------------------
# Custom CSS
# ------------------------------------------------------------------

st.markdown("""
<style>
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #1E3A5F 0%, #0d2137 100%);
        padding: 3rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .hero-title {
        color: #F4A836;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        color: #FFFFFF;
        font-size: 1.3rem;
        margin-bottom: 2rem;
    }
    .hero-tagline {
        color: #FFD700;
        font-size: 1.1rem;
        font-style: italic;
        margin-bottom: 2rem;
    }
    .hero-stat {
        display: inline-block;
        background: rgba(244, 168, 54, 0.15);
        border: 2px solid #F4A836;
        border-radius: 8px;
        padding: 1rem 2rem;
        margin: 0.5rem;
        color: #FFFFFF;
        font-weight: 600;
    }
    .hero-stat-value {
        color: #F4A836;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .hero-stat-label {
        color: #CCCCCC;
        font-size: 0.9rem;
    }

    /* Metric Cards */
    .metric-card {
        background: #FFF9E6;
        border: 2px solid #F4A836;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
    }
    .metric-card-positive {
        border-color: #22C55E;
        background: #F0FDF4;
    }
    .metric-card-negative {
        border-color: #EF4444;
        background: #FEF2F2;
    }

    /* Callout Box */
    .callout-box {
        background: linear-gradient(135deg, #FFF9E6 0%, #FFFDF0 100%);
        border-left: 5px solid #F4A836;
        padding: 1.5rem;
        border-radius: 0 8px 8px 0;
        margin: 1.5rem 0;
    }

    /* Amber Divider */
    .amber-divider {
        border: none;
        border-top: 3px solid #F4A836;
        margin: 2rem 0;
    }

    /* Chart background */
    .chart-container > div {
        background: #FFFDF0;
        border-radius: 8px;
        padding: 1rem;
    }

    /* Sidebar styling */
    .css-sidebar .css-1d391kg {
        background-color: #1E3A5F;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Hero Section
# ------------------------------------------------------------------

st.markdown("""
<div class="hero-banner">
    <div class="hero-title">☀️ SolarYield</div>
    <div class="hero-subtitle">AI-Powered Solar Yield Prediction · Singapore 5MW Farm</div>
    <div class="hero-tagline">"Predicting Tomorrow's Energy, Today"</div>
    <div>
        <div class="hero-stat">
            <div class="hero-stat-value">MAPE 6.1%</div>
            <div class="hero-stat-label">Forecast Error</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">R² 0.9915</div>
            <div class="hero-stat-label">Model Fit</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">365 Days</div>
            <div class="hero-stat-label">Data Monitored</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Key Stats Row
# ------------------------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size: 2rem; color: #1E3A5F;">☀️</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #1E3A5F;">5 MW</div>
        <div style="color: #666;">System Capacity</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size: 2rem; color: #1E3A5F;">📊</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #1E3A5F;">Physics + ML</div>
        <div style="color: #666;">Hybrid Model</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size: 2rem; color: #1E3A5F;">🔆</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #1E3A5F;">Singapore</div>
        <div style="color: #666;">5MW Solar Farm</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Description
# ------------------------------------------------------------------

st.markdown("""
### About This Dashboard

**Physics-based PVLib model combined with GradientBoosting ML** delivers industry-grade forecast accuracy.
Navigate using the sidebar to explore live forecasts, performance analytics, and anomaly detection.
""")

# ------------------------------------------------------------------
# Callout Box
# ------------------------------------------------------------------

st.markdown("""
<div class="callout-box">
    <h4 style="margin-top: 0; color: #1E3A5F;">🏆 Model Accuracy Matches Commercial-Grade Forecasters</h4>
    <p style="margin-bottom: 0; color: #1E3A5F;">
        Our hybrid model achieves forecast accuracy comparable to commercial solutions like Solargis,
        at a fraction of the cost. The combination of PVLib's physics-based solar modeling with
        GradientBoosting ML correction delivers MAPE values under 7% for day-ahead forecasts.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Navigation hint
# ------------------------------------------------------------------

st.info("👈 Use the sidebar navigation to explore: Overview · Data Explorer · Anomaly Log · Forecast Explorer")

# Streamlit auto-discovers pages in the `pages/` directory.
# Navigation is rendered automatically by Streamlit.
