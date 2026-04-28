---
type: DISCOVERY
date: 2026-04-23
created_at: 2026-04-23T00:00:00Z
author: agent
session_id: current
session_turn: 1
project: SolarYield
topic: Dashboard is the critical path to 8/10
phase: analyze
tags: [roadmap, dashboard, product, business-model]
---

# DISCOVERY: Dashboard is the critical path to raising the score from 3.73 to 8/10

**What**: The Streamlit dashboard is the single highest-leverage item. It is the connective tissue across 5 of 8 dimensions and is the prerequisite for every downstream proof point (investor demo, SHAP explainability, anomaly alerts, CSV export for bank reports).

**Why this is non-obvious**: The scorecard shows 8 dimensions needing improvement. The natural impulse is to spread effort across all 8. But the dashboard is blocked by nothing -- it just needs to be built. Meanwhile it unblocks: business model validation (demo for investors), SHAP explainability (SHAP charts visible to operators), ML architecture (model comparison trio), and product completeness (the spec exists, just not built).

**Key insight**: The project has more ML than product. The pipeline works, models are trained (MAPE 6.10%), SHAP was computed. What it lacks is a product a customer can interact with.

## Top 3 highest-leverage improvements

| #   | Improvement                     | Dimensions moved              | Difficulty |
| --- | ------------------------------- | ----------------------------- | ---------- |
| 1   | Build Streamlit dashboard       | Product 3→7, SHAP 4→5, ML 6→7 | Medium     |
| 2   | Conduct 5 customer interviews   | Business 2→5, Competitive 3→5 | Medium     |
| 3   | Add LightGBM + model comparison | ML 6→8, SHAP 4→5              | Easy       |

## Prerequisites discovered

The dashboard spec (specs/dashboard.md) requires `anomaly_flag`, `predicted_kWh`, `residual_kWh` columns in the CSV -- none of which exist. The dashboard cannot simply load the current CSV. A pre-processing step is needed first.

## Score projection

- Phase 1 (dashboard built): 3.73 → ~5.0
- Phase 2 (interviews + LightGBM): ~5.0 → ~6.5
- Phase 3 (LOI, weather abstraction, SHAP model card, drift detection): ~6.5 → 8.0+
