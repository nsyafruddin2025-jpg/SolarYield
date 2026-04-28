---
type: DISCOVERY
date: 2026-04-23
created_at: 2026-04-23T00:00:00Z
author: agent
session_id: current
project: SolarYield
topic: Pipeline and ML exist but product does not
phase: analyze
tags: [production-ready, dashboard, inference, shap]
---

# DISCOVERY: Production pipeline and ML exist; product does not

**What**: The project has a complete, working data pipeline and trained ML model. Nothing downstream exists.

**What exists (working)**:

- `solar_pipeline.py` — full PVLib pipeline, validated
- `src/ml/model.pkl` — trained GradientBoosting, MAPE 6.10%
- `src/ml/shap_chart.png` — SHAP beeswarm generated
- `solar_yield_output.csv` — 8,760 hourly rows, validated

**What doesn't exist**:

- No inference script (`predict.py` missing)
- No dashboard code (`app/dashboard.py` missing)
- SHAP not integrated into pipeline — computed once at training, saved to disk
- CSV lacks columns dashboard spec requires (anomaly_flag, predicted_kWh, residual_kWh)
- No CI/CD, no tests for the pipeline or ML code

**Why this matters**: The project was scored on algorithmic maturity (pipeline, ML) but not on productization. Raising the score requires product work, not algorithm work. The algorithms are ready; the product is a blank screen.
