# SolarYield Project State Assessment — All 8 Dimensions

## Overall Score: 3.73 / 10

---

## 1. Data Quality & Pipeline — 7/10 ✅ SOLID

**Production-ready:**

- `solar_pipeline.py` — Complete PVLib pipeline: fetch → validate → compute → save
  - Open-Meteo API integration with retry logic (tenacity, 3 attempts, exponential backoff)
  - Physical validation bounds on all weather variables
  - PVLib Haydavies transposition + SAPM cell temperature + temperature-corrected DC/AC power
  - `solar_yield_output.csv` — 1 year of hourly data (2025-04 to 2026-03), ~8,760 rows
- `specs/data-pipeline.md` — Complete specification

**Weak (not broken):**

- Single-year training data — insufficient for multi-year degradation modeling
- Open-Meteo is reanalysis data, not ground truth from site sensors
- No AOD (aerosol optical depth) variable — important for Singapore haze
- No weather source abstraction — single point of failure

**Missing entirely:**

- Multi-site configuration (hardcoded Singapore coordinates)
- No real-time data support (batch only)

---

## 2. Machine Learning Architecture — 6/10 ✅ DECENT

**Production-ready:**

- `src/ml/train_models.py` — GradientBoosting + RandomForest training script
- `src/ml/model.pkl` — Trained GradientBoostingRegressor (MAPE 6.10%, R² 0.9915)
- `src/ml/model_metadata.json` — Model metadata (features, train/test dates, metrics)
- Time-based 80/20 split (no data leakage)
- Cyclical encoding for hour/day features

**Weak:**

- GradientBoosting used instead of LightGBM (per user request, documented in journal)
- No temporal cross-validation (walk-forward)
- No residual hybrid architecture (PVLib → XGBoost on residual) despite spec recommending it
- No model comparison trio (only 2 of 3 models trained — missing LightGBM)

**Missing entirely:**

- No inference script (`predict.py` does not exist)
- No SHAP at inference time (SHAP computed only during training, lines 211-236 of `train_models.py`)
- No prediction logging
- No model versioning

---

## 3. SHAP Explainability — 4/10 ⚠️ WEAK

**Production-ready:**

- `src/ml/shap_chart.png` — SHAP beeswarm plot generated at training time
- SHAP values computed via `shap.TreeExplainer` on 500-sample test set

**Weak:**

- SHAP is a one-off chart, not integrated into the product
- No `src/ml/explainer.py` — no `SHAPExplainer` class for per-prediction explanations
- No `predict_with_shap()` function in the pipeline
- No model card (spec requires: training data, architecture, performance, SHAP importance, limitations, intended use)

**Missing entirely:**

- Decision logging (no CSV/table recording predictions with SHAP explanations)
- ISO 42001 compliance documentation
- Anomaly explanation with SHAP waterfall plots

---

## 4. Product Completeness — 3/10 ❌ MOSTLY MISSING

**Production-ready:**

- `specs/dashboard.md` — Detailed Streamlit dashboard specification (3 pages, KPIs, charts, anomaly log)
- `src/ml/shap_chart.png` — SHAP chart available for embedding

**Weak:**

- Dashboard is not built — zero lines of code written
- The CSV lacks columns the dashboard spec requires:
  - No `anomaly_flag` column
  - No `predicted_kWh` column (model predictions not run on full dataset)
  - No `residual_kWh` column
  - No `residual_σ` column
  - Data is hourly; dashboard spec requires daily aggregates

**Missing entirely:**

- `app/dashboard.py` or any dashboard code
- Alerting system
- Multi-site support
- User authentication
- CI/CD pipeline

---

## 5. Business Model Validation — 2/10 ❌ UNVALIDATED

**Production-ready:**

- `specs/business-model.md` — Three business models documented (SaaS Dashboard, Bankable Reports, API Service)
- `workspaces/SolarYield-analysis/journal/` — 11 journal entries documenting analysis decisions

**Weak:**

- No customer interviews conducted
- No LOIs signed
- No pricing validated with real prospects
- No unit economics with real data

**Missing entirely:**

- Any customer contact
- Landing page or sales collateral
- Revenue or signed agreements

---

## 6. Rubric Gaps — 3/10 ❌ MANY GAPS

**Production-ready:**

- Partial specs exist (data-pipeline, ml-model, dashboard, business-model)
- 11 journal entries capturing decisions

**Weak:**

- `specs/_index.md` does not exist at project root
- No complete spec index linking requirements to implementation files
- 42 documented gaps across categories (from scorecard)
- No CI/CD pipeline

**Missing entirely:**

- `specs/` at project root (exists only in `workspaces/SolarYield-analysis/specs/`)
- Full traceability from brief requirements to spec files to implementation
- Deployment automation

---

## 7. 10-Year Sustainability — 2/10 ❌ FRAGILE

**Production-ready:**

- `solar_pipeline.py` can be re-run to fetch new data

**Weak:**

- No model versioning (no git tag, no model registry)
- No automated retraining trigger
- Single-year dataset

**Missing entirely:**

- Weather source abstraction (no fallback if Open-Meteo changes API or pricing)
- Model versioning with SHAP artifact archival
- Monthly MAPE drift alert
- SHAP feature drift detection
- Degradation tracking over multi-year period

---

## 8. Competitive Technical Edge — 3/10 ⚠️ WEAK

**Production-ready:**

- GradientBoosting MAPE of 6.10% is competitive (published range for direct XGBoost: 9-14%)
- PVLib physics floor well-implemented
- SHAP analysis done

**Weak:**

- No anomaly pattern library (the moat — spec acknowledges it but hasn't been built)
- No benchmark against Solargis or other commercial products
- Nothing proprietary yet

**Missing entirely:**

- Systematic anomaly tagging library
- Solargis benchmark comparison
- Inverter-specific efficiency curves
- Panel degradation tracking

---

## Summary: What Is Production-Ready, Broken, Missing

| Category             | Status                                                                                    | Details                                                                        |
| -------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **Production-Ready** | Pipeline, ML training, SHAP chart, model artifacts, specs                                 | `solar_pipeline.py`, `src/ml/model.pkl`, `src/ml/shap_chart.png`, 4 spec files |
| **Broken**           | Nothing is broken — everything that exists works                                          | No runtime errors, no failed tests                                             |
| **Missing Entirely** | Dashboard app, inference pipeline, SHAP integration, alerting, CI/CD, customer validation | ~8 major product gaps                                                          |

---

## Critical Path to 8/10

1. **Pre-processing script** — run inference on full CSV, compute daily aggregates + anomaly flags
2. **Streamlit dashboard** — implement `specs/dashboard.md`
3. **SHAP explainer class** — `src/ml/explainer.py`
4. **Model card** — `src/ml/model_card.md`
5. **5 customer interviews** — validate business model
6. **LightGBM + model trio** — complete ML comparison
7. **Weather abstraction** — Open-Meteo + Solcast fallback
8. **Model versioning + drift detection** — sustainability infrastructure
