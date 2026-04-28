# SolarYield — Complete Assessment Across All 8 Dimensions

## Overall Score: 3.73 / 10

| Dimension                        | Score | Status            |
| -------------------------------- | ----- | ----------------- |
| 1. Data Quality & Pipeline       | 7/10  | ✅ Solid          |
| 2. Machine Learning Architecture | 6/10  | ✅ Decent         |
| 3. SHAP Explainability           | 4/10  | ⚠️ Weak           |
| 4. Product Completeness          | 3/10  | ❌ Mostly missing |
| 5. Business Model Validation     | 2/10  | ❌ Unvalidated    |
| 6. Rubric Gaps                   | 3/10  | ❌ Many gaps      |
| 7. 10-Year Sustainability        | 2/10  | ❌ Fragile        |
| 8. Competitive Technical Edge    | 3/10  | ⚠️ Weak           |

---

## Dimension 1: Data Quality & Pipeline — 7/10 ✅ SOLID

**File: `solar_pipeline.py`**

The pipeline is complete and functional. It fetches weather data from Open-Meteo, runs it through PVLib's physical models, validates inputs/outputs, and produces a CSV.

**What works:**

- `fetch_monthly_weather_data()` — monthly chunk fetching with retry (tenacity, 3 attempts, exponential backoff 2-10s)
- `validate_weather_data()` — physical bounds on all 7 weather variables
- `compute_kwh_output()` — PVLib Haydavies POA irradiance + SAPM cell temperature + temperature-corrected DC/AC power
- `validate_kwh_output()` — capacity ceiling + non-negative checks
- `solar_yield_output.csv` — 8,760 hourly rows (Apr 2025 – Mar 2026)

**What's weak (not broken):**

- Single-year data — insufficient for degradation modeling over 25-year panel lifetime
- Open-Meteo is reanalysis data, not ground-truth from site sensors
- No AOD (aerosol optical depth) variable — important for Singapore's haze season
- No weather source abstraction — no fallback if Open-Meteo changes API/pricing

**What's missing entirely:**

- Multi-site configuration (hardcoded Singapore coordinates in `SolarConfig`)
- Real-time data (batch only)
- No pipeline scheduling — runs on demand only

**Spec:** `workspaces/SolarYield-analysis/specs/data-pipeline.md` ✅ Complete

---

## Dimension 2: Machine Learning Architecture — 6/10 ✅ DECENT

**Files: `src/ml/train_models.py`, `src/ml/model.pkl`, `src/ml/model_metadata.json`**

**What works:**

- `train_models.py` — GradientBoosting + RandomForest training with 80/20 time-based split
- `model.pkl` — Trained GradientBoostingRegressor (MAPE 6.10%, RMSE 41.51 kWh, R² 0.9915)
- `model_metadata.json` — features, train/test dates, metrics
- Cyclical encoding (hour_sin/cos, day_sin/cos)
- No data leakage (temporal split, not random)

**What's weak:**

- GradientBoosting used instead of LightGBM per user request (journal: `0011-DECISION-gradientboosting-not-xgboost.md`)
- No temporal cross-validation (walk-forward validation not implemented)
- No residual hybrid architecture despite spec recommending it
- Only 2 of 3 models trained — LightGBM missing

**What's missing entirely:**

- Inference script (`predict.py` does not exist — no way to run the model on new data)
- SHAP at inference time (SHAP computed only at training, line 213 of `train_models.py`)
- Prediction logging
- Model versioning

**Spec:** `workspaces/SolarYield-analysis/specs/ml-model.md` ✅ Mostly complete

---

## Dimension 3: SHAP Explainability — 4/10 ⚠️ WEAK

**Files: `src/ml/shap_chart.png`, `src/ml/train_models.py` (lines 211-236)**

**What works:**

- `shap_chart.png` — SHAP beeswarm plot generated at training time
- `shap.TreeExplainer` used correctly on 500-sample test set

**What's weak:**

- SHAP is a static chart saved to disk — not integrated into the product
- No `src/ml/explainer.py` — no `SHAPExplainer` class for per-prediction explanations
- No `predict_with_shap()` function in the pipeline
- No model card (spec requires: training data period, model architecture, SHAP importance, limitations, intended use)

**What's missing entirely:**

- Decision logging (no CSV/table recording predictions with SHAP explanations)
- ISO 42001 compliance documentation
- Anomaly explanation with SHAP waterfall plots for flagged days
- Model card file

---

## Dimension 4: Product Completeness — 3/10 ❌ MOSTLY MISSING

**Files: `specs/dashboard.md` (NOT BUILT), `solar_yield_output.csv`**

This is the biggest gap. The dashboard spec exists but zero lines of code were written.

**What works:**

- `specs/dashboard.md` — detailed 3-page Streamlit specification (Overview KPIs, Data Explorer, Anomaly Log)
- `src/ml/shap_chart.png` — available for embedding

**What's broken / missing:**

1. **Dashboard app not built** — `app/dashboard.py` does not exist
2. **The CSV lacks columns the spec requires:**
   - No `anomaly_flag` column
   - No `predicted_kWh` column (model never run on full dataset)
   - No `residual_kWh` column
   - No `residual_σ` column
3. **Data granularity mismatch** — CSV is hourly; dashboard spec requires daily aggregates
4. **No alerting system**
5. **No multi-site support**
6. **No user authentication**

**To build the dashboard, you must first build:**

- Pre-processing script that runs inference on full CSV and adds anomaly/prediction columns
- Daily aggregation layer

---

## Dimension 5: Business Model Validation — 2/10 ❌ UNVALIDATED

**File: `workspaces/SolarYield-analysis/specs/business-model.md`**

**What works:**

- Three business models documented: SaaS Dashboard, Bankable Reports, API Service
- Recommendation: pursue Option B (bankable yield reports) first
- Unit economics illustrated (hypothetical, not validated)

**What's weak:**

- No customer interviews conducted
- No pricing validated with real prospects
- No LOIs signed
- Unit economics are illustrative, not derived from real data

**What's missing entirely:**

- Any customer contact
- Landing page or sales collateral
- Revenue, signed agreements, letters of intent

---

## Dimension 6: Rubric Gaps — 3/10 ❌ 42 GAPS

**Files: `workspaces/SolarYield-analysis/01-analysis/00-master-scorecard.md`**

**What works:**

- Partial specs exist (4 of ~8 spec files)
- 11 journal entries capturing decisions

**What's broken:**

- `specs/_index.md` missing from workspace (no complete spec index)
- No project root `specs/` directory (specs live only in `workspaces/SolarYield-analysis/specs/`)
- 42 documented gaps across all dimensions
- No CI/CD pipeline

**What's missing entirely:**

- Full spec-to-implementation traceability
- Deployment automation

---

## Dimension 7: 10-Year Sustainability — 2/10 ❌ FRAGILE

**Files: `solar_pipeline.py`**

**What works:**

- Pipeline can be re-run manually to fetch new data

**What's broken:**

- No model versioning (no git tag, no model registry entry)
- No automated retraining trigger
- Single-year dataset (insufficient for degradation modeling)

**What's missing entirely:**

- Weather source abstraction (no fallback if Open-Meteo changes)
- Model versioning with SHAP artifact archival
- Monthly MAPE drift alert
- SHAP feature drift detection
- Multi-year degradation tracking

---

## Dimension 8: Competitive Technical Edge — 3/10 ⚠️ WEAK

**Files: `src/ml/model.pkl`, `src/ml/shap_chart.png`**

**What works:**

- GradientBoosting MAPE 6.10% — competitive (literature for direct XGBoost: 9-14%)
- PVLib physics floor well-implemented
- SHAP analysis completed

**What's weak:**

- No anomaly pattern library despite spec identifying it as the moat
- No benchmark against Solargis or commercial alternatives
- Nothing proprietary yet

**What's missing entirely:**

- Systematic anomaly tagging library
- Solargis benchmark comparison
- Inverter-specific efficiency curves
- Panel degradation tracking over multi-year data

---

## Production-Ready vs. Broken vs. Missing

|                      | Count | Items                                                                                                                                     |
| -------------------- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **Production-ready** | 6     | Pipeline, trained model, SHAP chart, CSV data, specs (partial), journal                                                                   |
| **Broken**           | 0     | Nothing is broken — everything that exists works                                                                                          |
| **Missing entirely** | 8+    | Dashboard app, inference script, SHAP integration, alerting, model card, CI/CD, customer interviews, weather abstraction, anomaly library |

---

## Top 3 Actions to Reach 8/10

1. **Pre-processing + Dashboard** — Run inference on full CSV → build Streamlit app
2. **SHAP integration** — `explainer.py` + model card + decision logging
3. **5 customer interviews** — validate bankable report business model
