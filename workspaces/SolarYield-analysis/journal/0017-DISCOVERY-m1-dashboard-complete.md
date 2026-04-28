---
type: DISCOVERY
date: 2026-04-23
created_at: 2026-04-23T00:00:00Z
author: agent
session_id: current
project: SolarYield
topic: M1 dashboard complete — 13 anomalies found, dashboard runs
phase: implement
tags: [m1, dashboard, anomaly-detection, deployment]
---

# DISCOVERY: M1 dashboard complete — 13 anomalies found, Streamlit app runs

**What**: M1 (pre-processing + dashboard) is complete.

**Key findings from pre-processing run**:

- 365 days of data processed (2025-04-01 to 2026-03-31)
- 13 anomalous days flagged (3.6%) — reasonable for Singapore haze season (Feb-Mar)
- Most anomalous day: 2026-01-18 at -4.33σ (actual 8,205 kWh vs predicted 8,306 kWh — barely underperforming, just anomalous relative to recent trend)
- Mean residual: -12.7 kWh/day (model slightly overpredicts on average)
- The anomaly detection method is conservative — flagging days that deviate from recent rolling baseline, not days with low absolute output

**Dashboard status**:

- All 3 pages built and tested
- Streamlit Cloud deployment requires manual step (push to GitHub, connect to streamlit.io)
- Dashboard runs locally via `uv run streamlit run app/dashboard.py`

**Remaining for M1 deployment**: User must push to GitHub and deploy to Streamlit Cloud.
