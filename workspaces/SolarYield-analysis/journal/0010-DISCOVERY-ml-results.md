# DISCOVERY: GradientBoosting MAPE 6.10%, Random Forest MAPE 5.81% on Singapore solar data

**What**: Both models achieved MAPE well under the 10% target. GradientBoosting achieved R²=0.9915.

**Key findings**:

- Random Forest beats GradientBoosting on MAPE (5.81% vs 6.10%) but GBR has lower RMSE (41.51 vs 53.40 kWh) and higher R² (0.9915 vs 0.9859)
- The MAPE of 5.81% is at the optimistic edge of the expected 5-8% range for direct XGBoost on this dataset
- The test period (Jan-Mar 2026) includes Singapore haze season (Feb-Mar) — good stress test

**Top SHAP features**: diffuse_radiation dominates (229.83 mean |SHAP|), followed by GHI (186.40), then day_cos (47.46), direct_radiation (43.97), hour_sin (43.01).

**Why this matters**: The models are performing well above the <10% MAPE threshold. The residual hybrid (PVLib → XGBoost on residual) was NOT implemented — direct GradientBoosting was used as requested. The residual approach could push MAPE lower (to 4-7% based on literature), but current results are already investor-ready.
