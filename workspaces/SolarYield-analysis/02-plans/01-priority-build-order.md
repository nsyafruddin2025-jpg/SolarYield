# Priority Build Order

## Weighted Scores Summary

| Category         | Weight | Score | Weighted      |
| ---------------- | ------ | ----- | ------------- |
| Market & Problem | 25%    | 4     | 1.00          |
| Product & Demo   | 30%    | 3     | 0.90          |
| Business Model   | 20%    | 2     | 0.40          |
| Team & Execution | 15%    | 3     | 0.45          |
| AI/ML Depth      | 10%    | 4     | 0.40          |
| **Total**        |        |       | **3.15 / 10** |

---

## Priority 1: Validate the Problem (blocks everything)

**Why first**: Building without customer validation is the highest-risk bet. If the problem is wrong, every hour of engineering is wasted.

**Action**: Conduct 3–5 customer discovery interviews with:

- Solar farm operators in Singapore (C&I scale: 100kW – 5MW)
- Solar EPCs (Engineering, Procurement, Construction companies)
- Bankers or credit analysts who finance solar projects

**Deliverable**: Validated problem statement with quantified pain (hours lost per week, dollars at risk per year, decision blocked by missing data).

---

## Priority 2: Define the Business Model (MVP scope depends on this)

**Why second**: Business model determines product scope. "Bankable yield reports for solar financing" requires audit-ready documentation. "Fleet monitoring dashboard" requires multi-site support. These are different products.

**Action**: Choose one:

- **Option A**: SaaS dashboard for C&I solar fleet operators (subscription, $500–2,000/month per site)
- **Option B**: Bankable yield report service for solar project financing (per-report fee, $5,000–20,000 per report)
- **Option C**: API service for solar data integrators / energy management systems (per-MWh or per-site API key)

**Deliverable**: Revenue model, target customer segment, pricing, and the top 3 features that serve this model.

---

## Priority 3: Build the MVP Product Demo (makes the sale)

**Why third**: No customer can evaluate the current product. A dashboard converts "a script on a laptop" into "a product I can show my boss."

**Action**: Build a minimal web dashboard (can be a single HTML page + Python API):

- Total MWh generated (past 30 days)
- Capacity factor trend chart
- Expected vs. actual yield (anomaly signal)
- Alert banner for capacity factor <5%

**Tech**: Streamlit or Dash (Python-first, fastest path to a working dashboard) or a simple Flask/FastAPI + HTML/JS frontend.

**Deliverable**: A URL a prospective customer can visit and interact with, using real Singapore solar data.

---

## Priority 4: Operational Infrastructure (makes it a real business)

**Why fourth**: A product that requires manual intervention to run is not a business — it's a consulting engagement.

**Actions** (in order):

1. GitHub Actions CI: validate CSV output on every push (schema checks, physics bounds)
2. Scheduled daily pipeline run (GitHub Actions cron or external scheduler)
3. Alert on validation failure (email/Slack webhook)
4. Data quality monitor: daily capacity factor % posted to a Slack channel

**Deliverable**: Pipeline that runs automatically and signals when it breaks.

---

## Priority 5: ML Model — Anomaly Detection (first defensible ML feature)

**Why fifth**: PVLib is the floor (what physics predicts). Anomaly detection is the first ML layer on top — flagging days where actual yield deviates from physics predictions identifies real operational problems (soiling, inverter failure, shading).

**Action**:

1. Compute daily aggregate yield from the CSV pipeline
2. Compute physics-predicted daily yield from PVLib (using weather data)
3. Flag days where actual < predicted - 2σ (standard deviation of residual)

**Deliverable**: Anomaly score per day, surfaced in the dashboard as an alert or red flag.

---

## Priority 6: XGBoost Forecast Model (next ML feature)

**Why sixth**: The XGBoost recommendation from the prior analysis should be implemented — hourly yield forecast for grid operators and PPA settlement.

**Action**: Train XGBoost model using features (GHI, DNI, DHI, temperature, cloud_cover, hour_of_day, day_of_year, panel_tilt, system_capacity_kw) → target (kWh_output). Use 80/20 train-test split, tune basic hyperparameters.

**Deliverable**: A prediction endpoint (or function) that returns next-hour yield estimate with a prediction interval (quantile regression or multiple quantile outputs).

---

## What NOT to build yet (and why)

| Deferred Item                | Reason                                                                                                              |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| LSTM model                   | Rejected by prior analysis — autocorrelation too low. Revisit only if residual series shows long-range dependencies |
| Multi-site support           | Premature without validated business model                                                                          |
| Real-time data ingestion     | Batch is sufficient for C&I solar; real-time adds significant complexity                                            |
| Mobile app                   | Web dashboard covers 80% of use cases                                                                               |
| Detailed financial model     | Validate problem and product first                                                                                  |
| API for external integrators | Premature without paying customers                                                                                  |

---

## Sequencing Summary

```
Week 1–2: Customer discovery interviews → validated problem + business model
Week 3–4: MVP dashboard (Streamlit) → shareable product artifact
Week 5–6: GitHub Actions CI/CD → operational reliability
Week 7–8: Anomaly detection → first ML feature
Week 9–10: XGBoost forecast → second ML feature
```

Each phase should validate before proceeding to the next. If discovery reveals the problem is different from assumed, pivot before building.
