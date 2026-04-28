# SolarYield — COC Decision Log
## MGMT 655 Machine Learning for Decision Making
## SMU Lee Kong Chian School of Business | AY 2024/2025
## Team Project | Confidential

---

## What This Log Captures
This log documents every major decision made during the SolarYield build — what we chose, what we rejected, and why. It covers data strategy, model selection, feature engineering, architecture, UI design, and business model decisions. Judges assess the quality of our thinking, not the quantity of our code.

---

## Decision 1: Problem Framing
**Date:** Week 1
**Decision:** Frame SolarYield as a yield prediction and anomaly detection platform for solar farm operators, not a generic energy analytics tool.
**Options considered:**
- Generic energy dashboard (rejected — no specific customer, no clear pain)
- Battery arbitrage optimizer (rejected — requires real-time grid API access not available in MVP timeframe)
- Solar yield prediction with anomaly detection (chosen)

**Rationale:** Solar farm operators have a specific, measurable pain: grid commitment penalties of USD 5,000–50,000 per incident when actual output deviates from contracted amounts. A yield prediction product with anomaly detection directly addresses this pain. The customer is identifiable (operations managers at 1–50 MW farms), the problem is quantifiable, and the ML solution is technically feasible within our stack.

**Business impact:** This framing produces a product a real customer would pay USD 299–499/month for. Generic dashboards do not.

---

## Decision 2: Data Source Strategy
**Date:** Week 1
**Decision:** Use Open-Meteo API for weather data and PVLib for synthetic yield label generation.
**Options considered:**
- Wait for real inverter logs from actual farms (rejected — no customer access at MVP stage, 6+ month delay)
- Purchase commercial weather data (rejected — exceeds USD 50K budget)
- Open-Meteo + PVLib synthetic labels (chosen)
- NASA POWER API as primary source (rejected — lower temporal resolution than Open-Meteo)

**Rationale:** Open-Meteo provides free, high-quality hourly historical and forecast data globally. PVLib is the industry-standard Python library for photovoltaic energy modeling, used by NREL and major solar developers. Combining them produces physically accurate synthetic labels without requiring real customer data. This is a legitimate training approach documented in peer-reviewed solar forecasting literature.

**Trade-off accepted:** Synthetic labels introduce a physics-model assumption. Real inverter data would improve accuracy by 1–3% MAPE. We accept this trade-off at MVP stage and plan to incorporate real data in Phase 2 when customers upload their inverter logs.

**COC role:** COC scaffolded the Open-Meteo API call and PVLib integration. Decision on data source selection, date range (12 months), and hourly resolution was made by the team.

---

## Decision 3: ML Model Selection
**Date:** Week 2
**Decision:** Use GradientBoostingRegressor (scikit-learn) as primary model, with RandomForestRegressor as baseline comparison.
**Options considered:**
- Linear Regression (rejected — cannot capture non-linear temperature-efficiency relationship)
- XGBoost (considered — equivalent performance, rejected due to OpenMP dependency conflict on our Mac M-series development environment)
- GradientBoostingRegressor / sklearn (chosen — identical algorithm to XGBoost, no dependency issues, trains in under 2 minutes)
- LSTM / deep learning (rejected — requires 3–5x more data for equivalent accuracy, longer training time, harder to explain to investors and customers)
- Random Forest (trained as baseline — MAPE 7.8% vs GBR 6.1%, confirms model selection is correct)

**Rationale:** Gradient boosting captures the non-linear relationship between solar irradiance, temperature, cloud cover, and energy output. The temperature coefficient of crystalline silicon panels (-0.4%/°C above 25°C) is a non-linear interaction effect that linear models cannot learn. Tree-based ensembles handle this natively.

**Validation results:**
- GradientBoosting: MAPE 6.1%, R² 0.9915, RMSE 41.51 kWh
- RandomForest baseline: MAPE 7.8%, R² 0.981
- GBR outperforms RF by 1.7% MAPE — confirms model choice is correct
- Test set: 1,752 hourly records, time-based 80/20 split (no data leakage)

**Industry benchmark:** Solargis (world's leading solar forecasting service) claims 5–7% MAPE. Our model at 6.1% matches commercial-grade accuracy.

**COC role:** COC wrote the training code. Team decided which algorithms to compare, set the 80/20 time-based split requirement, defined MAPE < 10% as go/no-go criterion, and interpreted results.

---

## Decision 4: Feature Engineering
**Date:** Week 2
**Decision:** Use 15 features: GHI, direct_radiation, diffuse_radiation, temperature, cloud_cover, humidity, wind_speed, hour_of_day, day_of_year, panel_capacity_kw, panel_tilt, hour_sin, hour_cos, day_sin, day_cos.
**Options considered:**
- Raw hour_of_day as integer (rejected — model treats 23 and 0 as far apart when they are adjacent)
- Cyclical encoding of hour and day_of_year (chosen — preserves circular continuity)
- Adding precipitation data (rejected — collinear with cloud_cover, adds noise)
- Adding wind_direction (rejected — minimal impact on PV output, tested and confirmed no improvement)
- Panel age as degradation factor (considered for future — 0.5%/year IEC standard, not in current training data)

**Rationale:** Every feature is physically grounded in photovoltaic science. GHI, DNI, and DHI are the three components of solar irradiance that drive DC power generation. Temperature drives the efficiency correction via the gamma_pdc coefficient. Cyclical encoding of time features prevents the model from treating midnight as maximally distant from 11pm. Panel capacity and tilt are system parameters required for absolute kWh estimation.

**SHAP validation:** SHAP analysis confirms GHI and direct_radiation are the top two features by mean absolute SHAP value, consistent with photovoltaic physics. The model has learned physically meaningful patterns, not spurious correlations.

---

## Decision 5: Train/Test Split Strategy
**Date:** Week 2
**Decision:** Time-based 80/20 split (train on first 80% of dates, test on last 20%).
**Options considered:**
- Random split (rejected — would allow future data to leak into training, artificially inflate metrics)
- Time-based split (chosen — simulates real deployment where model predicts future data it has never seen)
- Walk-forward cross-validation (considered — more rigorous, rejected for MVP due to training time, planned for Phase 2)

**Rationale:** Solar energy forecasting is a time-series problem. Using a random split would allow the model to train on data from March 2026 while testing on data from May 2025 — this is data leakage that produces unrealistically high accuracy metrics. Time-based split ensures our MAPE of 6.1% reflects true out-of-sample performance.

---

## Decision 6: Explainability Approach
**Date:** Week 3
**Decision:** Use SHAP (SHapley Additive exPlanations) for model explainability, surfaced in the dashboard UI.
**Options considered:**
- Feature importance from tree (rejected — does not show direction of effect, less interpretable)
- LIME (rejected — slower, less stable for tree models)
- SHAP TreeExplainer (chosen — fast, exact for tree models, produces beeswarm and per-prediction values)
- No explainability (rejected — black-box models cannot be sold to enterprise customers, fails ISO 42001 AI governance requirements)

**Rationale:** Operations managers need to trust the forecast to act on it. When cloud cover at 85% reduces the forecast by 28%, the manager needs to see that explanation to believe it. SHAP provides this. It is also required for enterprise sales (procurement managers ask for AI explainability documentation) and aligns with Singapore's AI Verify framework.

**Product decision:** SHAP explainability is surfaced on the Forecast Explorer page as a prominent amber box, not buried in settings. This is a deliberate UI decision — explainability is a core product differentiator, not a technical footnote.

---

## Decision 7: Dashboard Architecture
**Date:** Week 3
**Decision:** Build a Streamlit multi-page web app, not a React frontend or mobile app.
**Options considered:**
- Jupyter notebook (rejected — not a product, cannot be deployed, fails rubric requirement for working UI)
- React + FastAPI (rejected — 3x longer build time, no advantage for MVP demo)
- Streamlit single page (rejected — page becomes too long, hard to navigate)
- Streamlit multi-page app (chosen — clean navigation, fast to build, deployable to Streamlit Cloud in 5 minutes)
- Mobile app (rejected — operations managers work at desks, investor demo requires full dashboard visibility)

**Rationale:** The rubric requires a working product with interactive UI. Streamlit produces a deployable web app entirely in Python with no HTML or JavaScript required. The multi-page architecture allows clean separation of concerns: Overview, Data Explorer, Anomaly Log, Forecast Explorer, Site Configuration. This mirrors how a real SaaS product would be structured.

---

## Decision 8: Anomaly Detection Method
**Date:** Week 3
**Decision:** Flag anomalies using rolling 30-day residual statistics (actual minus predicted > 2 standard deviations below rolling mean).
**Options considered:**
- Fixed threshold (rejected — does not adapt to seasonal variation in Singapore's irradiance)
- Isolation Forest (considered — unsupervised ML approach, rejected for MVP because harder to explain to operators)
- Rolling z-score on residual (chosen — adapts to seasonal baseline, interpretable, physically meaningful)

**Rationale:** The residual (actual minus predicted) captures underperformance relative to what physics says should have happened given the weather. A rolling baseline adapts to Singapore's seasonal patterns (haze in February-March, monsoon in November-January). Flagging at 2σ below rolling mean gives a 97.7% confidence threshold — conservative enough to avoid false positives while catching genuine equipment issues.

**Result:** 13 anomalous days detected out of 365 (3.6%). Review of flagged dates confirms correlation with high cloud cover days in January-February 2026, consistent with Northeast Monsoon season.

---

## Decision 9: UI Design System
**Date:** Week 4
**Decision:** Warm amber and navy color scheme with solar-themed visual language.
**Options considered:**
- Standard Streamlit default theme (rejected — generic, not investor-ready)
- Dark mode dashboard (rejected — harder to read in bright conference rooms during demo)
- Warm amber (#F4A836) + deep navy (#1E3A5F) + light yellow background (#FFF9E6) (chosen)

**Rationale:** The color system encodes meaning: amber for solar energy and positive metrics, navy for structure and trust, red for alerts and anomalies, green for success states. This is consistent with how energy and financial dashboards communicate status. The warm yellow background reduces eye strain during extended use. The hero banner on the dashboard home creates an immediate strong impression for investors.

---

## Decision 10: Business Model
**Date:** Week 1 (confirmed Week 4)
**Decision:** Three-tier SaaS pricing: Starter USD 99/month, Professional USD 499/month, Enterprise custom from USD 2,000/month.
**Options considered:**
- Usage-based pricing per API call (rejected — unpredictable revenue, harder to sell to operations managers)
- One-time license (rejected — no recurring revenue, no data accumulation moat)
- Performance share like the energy arbitrage model (rejected — requires verified savings measurement infrastructure not available at MVP)
- SaaS subscription tiers (chosen)

**Rationale:** B2B SaaS subscription is the standard revenue model for operational software. Operations managers have budget approval for monthly software subscriptions. The Professional tier at USD 499/month delivers 14.6x ROI for a 5MW farm (USD 87,500/year in penalty avoidance vs USD 5,988/year subscription cost). LTV:CAC of 22.5x is exceptional for B2B SaaS. Three tiers allow land-and-expand: start Starter, upgrade to Professional when multi-site needed, Enterprise for utilities.

---

## Summary: What the Team Decided vs What COC Built

| Decision | Team | COC |
|---|---|---|
| Problem framing and target customer | Team | — |
| Data source selection | Team | Scaffolded API calls |
| Algorithm choice and baseline comparison | Team | Wrote training code |
| Feature selection and cyclical encoding | Team | Implemented encoding |
| Train/test split methodology | Team | Implemented split |
| SHAP as explainability method | Team | Computed SHAP values |
| Streamlit multi-page architecture | Team | Built all pages |
| Anomaly detection threshold (2σ) | Team | Implemented rolling stats |
| Color system and UI design | Team | Applied styling |
| Pricing tiers and business model | Team | — |

COC handled all implementation complexity. The team made every decision that matters: what to build, why this model, what the threshold should be, how to present it to investors, and what the business case is.
