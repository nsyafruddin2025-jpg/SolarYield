# SolarYield — Todo Milestones

## How to Read This File

Todos are organized into 5 milestones. Each todo is atomic — one person, one session, one deliverable. Dependencies are noted in each todo.

**Execution order within milestone:** Todos can run in parallel if they have no dependencies. Build vs Wire are ALWAYS separate todos.

---

## M0: Foundation (run first — no dependencies)

- [ ] **Todo 26**: Create project root `specs/_index.md` — spec index with traceability

---

## M1: Dashboard MVP (biggest score multiplier — 3→7 on Product)

**Prerequisite: todo 1 (enriched_daily.csv must exist before dashboard pages)**

- [ ] **Todo 1**: Pre-processing — run inference on full CSV, compute daily aggregates + anomaly flags → `data/enriched_daily.csv`
- [ ] **Todo 5**: Build Streamlit dashboard — Page 1: Overview (KPIs + 3 charts)
- [ ] **Todo 4**: Build Streamlit dashboard — Page 2: Data Explorer (sortable table)
- [ ] **Todo 2**: Build Streamlit dashboard — Page 3: Anomaly Log
- [ ] **Todo 3**: Deploy Streamlit dashboard to Streamlit Cloud

**After M1 complete:** Dashboard URL exists, customer can interact with real Singapore data.

---

## M2: SHAP + Inference + Tests (completes ML Architecture + SHAP dimensions)

**Can start after M1 page 3 is built (todo 2) for wiring SHAP into dashboard**

- [ ] **Todo 6**: Build `src/ml/explainer.py` — SHAPExplainer class (standalone, no dashboard dependency)
- [ ] **Todo 8**: Build `src/ml/log_prediction.py` — prediction logging to CSV
- [ ] **Todo 9**: Build `src/ml/predict.py` — inference script for batch scoring
- [ ] **Todo 10**: Create `src/ml/model_card.md` — model documentation
- [ ] **Todo 13**: Add LightGBM to model comparison trio (GB + RF + LGB)
- [ ] **Todo 14**: Add clear-sky ratio + DNI/DHI ratio features
- [ ] **Todo 11**: Add temporal walk-forward cross-validation
- [ ] **Todo 30**: Write tests — `tests/test_ml_pipeline.py` (pytest)
- [ ] **Todo 15**: Write tests — `tests/test_solar_pipeline.py` (pytest)
- [ ] **Todo 7**: Wire SHAP into dashboard Page 3 — anomalous day explanations
- [ ] **Todo 31**: Add Page 4 to dashboard — SHAP full explainability view

**After M2 complete:** SHAP is in the product, not just a static chart. Model is competitive (3-model comparison).

---

## M3: CI/CD + Operations (raises Sustainability from 2→5)

**Independent of M1/M2 — can run in parallel**

- [ ] **Todo 12**: Set up GitHub Actions CI — validate CSV schema + physics bounds on push
- [ ] **Todo 17**: Daily alert pipeline — GitHub Actions cron (6am SG), anomaly → SendGrid email
- [ ] **Todo 29**: Weekly model retrain pipeline — GitHub Actions cron (Sunday 2am SG)
- [ ] **Todo 32**: Write Playwright E2E tests for dashboard (runs in CI on push to main)

**After M3 complete:** Pipeline runs automatically. Alerts fire on anomalies.

---

## M4: Business + Sustainability (raises Business from 2→7, Sustainability 2→5)

**Independent of M1-M3 — can run in parallel**

- [ ] **Todo 24**: Conduct 5 customer discovery interviews (CRITICAL GAP — blocks everything)
- [ ] **Todo 19**: Build landing page — `apps/landing/index.html`
- [ ] **Todo 22**: Obtain signed LOI from first customer (depends on: interviews + deployed dashboard)
- [ ] **Todo 18**: Build ISO 42001 compliance documentation — `docs/iso-42001-compliance.md`
- [ ] **Todo 20**: Implement weather source abstraction — Open-Meteo + Solcast fallback
- [ ] **Todo 16**: Implement monthly MAPE drift detection — `src/ml/monitor.py`
- [ ] **Todo 23**: Implement model versioning — `models/` registry
- [ ] **Todo 21**: Design multi-site database schema — `src/db/schema.sql`
- [ ] **Todo 27**: Build anomaly pattern library — systematic tagging (THE MOAT)
- [ ] **Todo 28**: Ingest multi-year training data (2019–2025)
- [ ] **Todo 25**: Run Solargis benchmark comparison — `docs/solargis-comparison.pdf`

**After M4 complete:** Fundable MVP reached. Score should be ~8/10 across all dimensions.

---

## Score Impact by Milestone

| Milestone                     | Score Change | Dimensions Moved                                  |
| ----------------------------- | ------------ | ------------------------------------------------- |
| M0: Foundation                | +0.1         | Compliance (Rubric Gaps 3→4)                      |
| M1: Dashboard MVP             | +2.4         | Product 3→7, SHAP 4→5, ML 6→7, Business 2→3       |
| M2: SHAP + Inference          | +1.5         | ML 6→8, SHAP 4→6, Product 3→5                     |
| M3: CI/CD + Operations        | +0.8         | Sustainability 2→5, Product 3→5                   |
| M4: Business + Sustainability | +2.0         | Business 2→7, Sustainability 2→5, Competitive 3→6 |
| **Total**                     | **~6.8→8.0** |                                                   |
