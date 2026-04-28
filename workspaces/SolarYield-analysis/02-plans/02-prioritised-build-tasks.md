# Prioritised Build Task List — All Sections

## Priority by Impact on Rubric Score + Investor Readiness

Scoring: 1 = highest priority (do immediately), 2 = second priority, etc.

### TIER 1 — Immediate (Score 9→10 on Product + Business Model)

#### 1. Build Working Streamlit Dashboard (Product: 3→5)

**Why**: No demo = no investment conversation. Every investor needs to see something live.
**Tasks**:

- [ ] Install Streamlit
- [ ] Page 1: KPI cards (total MWh, capacity factor, anomaly count, peak output)
- [ ] Page 1: Daily yield bar chart (past 30 days)
- [ ] Page 1: Capacity factor trend line (past 90 days)
- [ ] Page 2: Data explorer table (paginated hourly data, sortable, date filter)
- [ ] Page 3: Anomaly log table (date, actual, predicted, residual, sigma)
- [ ] Load real CSV data from repository
- [ ] Deploy to Streamlit Cloud (free)
      **Effort**: 1–2 days
      **Owner**: Solo developer

#### 2. Conduct 5 Customer Discovery Interviews (Market: 4→7)

**Why**: Without interviews, everything is assumptions. Investors will ask "did you talk to customers?"
**Tasks**:

- [ ] Create interview guide (10 questions on current monitoring, pain points, willingness to pay)
- [ ] Identify 10 Singapore solar farm operators via LinkedIn
- [ ] Conduct 5 interviews, document answers verbatim
- [ ] Extract: pain quantification ($/year), decision-maker, sales cycle, competitors they use
      **Effort**: 1–2 weeks
      **Owner**: Solo developer

#### 3. Get 1 Signed LOI or Deposit (Business: 2→5)

**Why**: "They paid" is the only signal that matters. Everything else is vanity.
**Tasks**:

- [ ] Create 1-page product one-pager (what it does, what it costs, what you get)
- [ ] Approach 5 operators from interviews
- [ ] Offer founding member: 6 months at S$1,000/month (discounted) = S$6,000 pre-paid
- [ ] LOI with "cancel anytime" — no legal commitment required
      **Effort**: 1–3 weeks
      **Owner**: Solo developer

---

### TIER 2 — Near-term (Score 6→8 on ML + Product)

#### 4. Implement XGBoost Residual Model

**Why**: Anomaly detection on top of PVLib is the first defensible ML feature.
**Tasks**:

- [ ] Fetch multi-year training data (2019–2025, Open-Meteo)
- [ ] Compute PVLib-predicted yield for each hour
- [ ] Compute residual = actual − predicted
- [ ] Train XGBoost on residual (features: GHI, DNI, DHI, temperature, cloud_cover, humidity, wind_speed, hour_sin, hour_cos, day_sin, day_cos)
- [ ] Implement temporal train/test split (last year = test)
- [ ] Evaluate MAPE, RMSE, MAE on test set
- [ ] Save model artifact (.joblib)
      **Effort**: 3–5 days
      **Owner**: ML engineer

#### 5. Add SHAP Integration

**Why**: Investors and enterprise customers want to understand why predictions are wrong.
**Tasks**:

- [ ] Install shap
- [ ] Compute SHAP values for daily aggregation
- [ ] Dashboard: daily SHAP waterfall (top 4 features per anomalous day)
- [ ] Dashboard: "Why was today anomalous?" explanation
- [ ] Log SHAP values to file for audit trail
      **Effort**: 2 days
      **Owner**: ML engineer

#### 6. Implement Automated Alert Pipeline

**Why**: The product needs to notify operators automatically.
**Tasks**:

- [ ] Build daily pipeline runner (GitHub Actions cron, 6am Singapore time)
- [ ] Compute daily anomaly score (residual / rolling_std)
- [ ] Alert dispatch: SendGrid email when residual < -2σ
- [ ] Alert dispatch: Twilio SMS for critical alerts (residual < -3σ)
- [ ] Alert log table (site, date, severity, dispatched_at, acknowledged)
      **Effort**: 3–4 days
      **Owner**: Backend engineer

#### 7. Implement Bayesian Hyperparameter Tuning (Optuna)

**Why**: The model needs to be tuned properly, not with defaults.
**Tasks**:

- [ ] Install optuna
- [ ] Define hyperparameter search space (max_depth, learning_rate, n_estimators, min_child_weight, subsample, colsample_bytree, reg_alpha, reg_lambda)
- [ ] Temporal CV: expanding window (train on years 1–N, test on year N+1)
- [ ] 50 Optuna trials with pruning (EarlyStoppingCallback)
- [ ] Save best hyperparameters + model
- [ ] Document best config in model card
      **Effort**: 2–3 days
      **Owner**: ML engineer

#### 8. Add Clear-Sky Ratio + DNI/DHI Ratio Features

**Why**: These are the highest-value missing features for MAPE reduction.
**Tasks**:

- [ ] Compute clear_sky_GHI using pvlib.irradiance.get_clearsky()
- [ ] Add clear_sky_ratio = GHI / clear_sky_GHI (clipped to [0, 1.5])
- [ ] Add dni_dhi_ratio = DNI / (DHI + 1) (avoid div by zero)
- [ ] Re-train XGBoost with new features
- [ ] Evaluate MAPE improvement (expect 1–3% absolute improvement)
      **Effort**: 1–2 days
      **Owner**: ML engineer

---

### TIER 3 — Mid-term (Score 8→9 on ML + Product)

#### 9. Implement Temporal Cross-Validation

**Why**: Proper CV is required for academic/institutional credibility.
**Tasks**:

- [ ] Leave-one-year-out CV (if 5+ years of data)
- [ ] Compute MAPE per fold, report mean ± std
- [ ] Report in model card
      **Effort**: 1 day
      **Owner**: ML engineer

#### 10. Build Model Card

**Why**: ISO 42001 compliance and enterprise sales require model documentation.
**Tasks**:

- [ ] Document: model version, training period, architecture description
- [ ] Document: feature list + SHAP importance ranking
- [ ] Document: performance metrics (MAPE, RMSE, MAE per CV fold)
- [ ] Document: known failure modes (nighttime, extreme weather events)
- [ ] Document: intended use and out-of-scope use cases
      **Effort**: 1 day
      **Owner**: ML engineer

#### 11. Add Date Range Picker + Site Selector

**Why**: Production demo needs these for a PE investor to explore freely.
**Tasks**:

- [ ] Add date range picker (streamlit date_input or custom component)
- [ ] Add site selector (hardcoded site for MVP)
- [ ] Export to CSV button
      **Effort**: 1 day
      **Owner**: Frontend engineer

#### 12. Weather Data Source Abstraction Layer

**Why**: Single weather source is a production risk.
**Tasks**:

- [ ] Abstract weather fetch behind a WeatherSource interface
- [ ] Primary: Open-Meteo (current)
- [ ] Fallback: Solcast API (paid, more reliable)
- [ ] Auto-fallback logic: if Open-Meteo fails 3 times in a row → switch to Solcast
      **Effort**: 2 days
      **Owner**: Backend engineer

---

### TIER 4 — Later (Score 9→10 on full rubric)

#### 13. MAPE Drift Detection Pipeline

**Why**: Model degrades silently without monitoring.
**Tasks**:

- [ ] Compute rolling 30-day MAPE vs prior 30-day MAPE
- [ ] If drift > 5% → send internal alert
- [ ] If drift > 15% → trigger model retrain automatically
- [ ] Dashboard: MAPE trend chart (past 12 months)
      **Effort**: 2 days
      **Owner**: ML engineer

#### 14. Multi-Site Database Schema

**Why**: Fleet management is required for enterprise customers.
**Tasks**:

- [ ] SQLite database (MVP) → PostgreSQL (production)
- [ ] Sites table (id, name, lat, lon, capacity, tilt, azimuth, timezone)
- [ ] Daily_yield table (site_id, date, actual, predicted, residual, capacity_factor, is_anomaly)
- [ ] Pipeline_runs table (id, site_id, run_at, status, records, error)
- [ ] Alert_config table (site_id, threshold_sigma, email, sms)
      **Effort**: 3–4 days
      **Owner**: Backend engineer

#### 15. Automated Weekly Retrain Pipeline

**Why**: Model needs to update with new data automatically.
**Tasks**:

- [ ] GitHub Actions cron: every Sunday at 2am Singapore time
- [ ] Fetch latest week's weather data
- [ ] Retrain XGBoost on all available data
- [ ] Compare new model MAPE vs. production model
- [ ] If better → deploy new model; if worse → keep production model
- [ ] Log retrain event + metrics
      **Effort**: 3 days
      **Owner**: ML engineer + DevOps

#### 16. Landing Page + Waitlist

**Why**: Customer acquisition before product is built.
**Tasks**:

- [ ] Build 1-page landing (Carrd or Webflow)
- [ ] Headline: "Know when your solar farm underperforms before your bank does."
- [ ] Form: company, email, number of sites, current monitoring method
- [ ] 20 Singapore solar operator signups = validated interest
      **Effort**: 1 day
      **Owner**: Solo developer

#### 17. Multi-Year Data Ingestion

**Why**: 1 year of data is insufficient for production ML.
**Tasks**:

- [ ] Loop through 2019–2025 for Singapore coordinates
- [ ] Open-Meteo monthly fetch for all 84 months
- [ ] Validate each month against physical bounds
- [ ] Store as Parquet (not CSV) for efficiency
      **Effort**: 1 day (runs in background)
      **Owner**: Pipeline engineer

#### 18. Anomaly Library — Systematic Tagging

**Why**: The moat is the anomaly library, not the model.
**Tasks**:

- [ ] Every anomaly → human review form (what caused it?)
- [ ] Tag taxonomy: haze, soiling, inverter_fault, shading, weather_forecast_error, sensor_error
- [ ] Store tagged anomalies in anomaly_library table
- [ ] Dashboard: anomaly history with cause labels
      **Effort**: Ongoing (accrues over time)
      **Owner**: Domain expert

---

## Master Task Summary

| #   | Task                        | Category    | Score Impact | Effort    |
| --- | --------------------------- | ----------- | ------------ | --------- |
| 1   | Streamlit dashboard         | Product     | +2           | 1–2 days  |
| 2   | Customer interviews         | Market      | +3           | 1–2 weeks |
| 3   | LOI / deposit               | Business    | +3           | 1–3 weeks |
| 4   | XGBoost residual model      | ML          | +2           | 3–5 days  |
| 5   | SHAP integration            | ML          | +1           | 2 days    |
| 6   | Alert pipeline              | Product     | +1           | 3–4 days  |
| 7   | Optuna tuning               | ML          | +1           | 2–3 days  |
| 8   | Clear-sky ratio features    | ML          | +1           | 1–2 days  |
| 9   | Temporal CV                 | ML          | +1           | 1 day     |
| 10  | Model card                  | ML/Business | +1           | 1 day     |
| 11  | Date picker + site selector | Product     | +1           | 1 day     |
| 12  | Weather abstraction         | Tech debt   | +1           | 2 days    |
| 13  | MAPE drift detection        | ML          | +1           | 2 days    |
| 14  | Multi-site DB schema        | Product     | +1           | 3–4 days  |
| 15  | Weekly retrain pipeline     | ML          | +1           | 3 days    |
| 16  | Landing page                | Business    | +1           | 1 day     |
| 17  | Multi-year data             | ML          | +1           | 1 day     |
| 18  | Anomaly library             | Competitive | +1           | Ongoing   |

**Note**: Tasks 1–3 are the immediate priority. They take 2–3 weeks but are prerequisite to any investor conversation. ML tasks (4–8) can run in parallel after that.
