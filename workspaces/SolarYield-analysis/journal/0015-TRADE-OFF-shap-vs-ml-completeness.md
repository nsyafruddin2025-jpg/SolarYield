---
type: TRADE-OFF
date: 2026-04-23
created_at: 2026-04-23T00:00:00Z
author: agent
session_id: current
project: SolarYield
topic: SHAP integration vs ML completeness trade-off
phase: todos
tags: [shap, ml, trade-off]
---

# TRADE-OFF: SHAP integration vs. ML completeness — chose SHAP-first

**Trade-off**: M2 could either (A) complete all ML improvements first (LightGBM, clear-sky features, temporal CV) then add SHAP, or (B) add SHAP integration immediately so it appears in the dashboard.

**Chosen**: Option B — SHAP first.

**Rationale**:

- SHAP in the dashboard is user-visible and investor-visible. LightGBM is not.
- The dashboard spec was written with SHAP as a key feature. Without it, the dashboard is incomplete.
- SHAPExplainer class (todo 6) is a prerequisite for both the dashboard wiring (todo 7) and the SHAP page (todo 31), both in M2.
- LightGBM comparison (todo 13) can be done after SHAP — it changes model selection, not user experience.

**Risk**: If LightGBM beats GradientBoosting significantly, the SHAP explanations would be on the suboptimal model. Mitigation: after todo 13, if LightGBM wins, re-run SHAP on the new best model.
