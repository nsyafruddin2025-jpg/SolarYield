# 6. RUBRIC GAPS — What Is Missing to Score 10/10

## Score: 3.15 / 10 overall

---

## Market and Problem (Currently 4/10 → Need 10/10)

**Evidence missing**:

| Requirement            | Current State                | Gap                                                         |
| ---------------------- | ---------------------------- | ----------------------------------------------------------- |
| Customer interviews    | 0 interviews                 | Zero actual operator conversations                          |
| Problem quantification | Assumptions                  | No verified $ pain per year per site                        |
| Competitive landscape  | Mentioned but not researched | No Solargis, Envision, AutoGrid analysis                    |
| Market sizing          | Generic SEA growth stats     | No Singapore-specific TAM/SAM/SOM calculation               |
| Regulatory analysis    | Not started                  | EMA framework, grid penalty structure not documented        |
| Customer personas      | None                         | No verified operator type, decision-maker, budget authority |

**To score 10/10**: Conduct 5 interviews, produce TAM/SAM/SOM document, produce competitive matrix, document EMA regulatory requirements.

---

## Product and Demo (Currently 3/10 → Need 10/10)

**What must work live on demo day**:

| Requirement              | Current State                      |
| ------------------------ | ---------------------------------- |
| Working web dashboard    | None (no code written)             |
| Live data                | Dashboard loads real Singapore CSV |
| Anomaly alert fires      | Not implemented                    |
| Alert delivered to email | Not implemented                    |
| Multi-site selector      | Single site only                   |
| Date range picker        | Not implemented                    |
| Export to CSV            | Not implemented                    |
| PDF report generation    | Not implemented                    |
| User authentication      | None                               |

**To score 10/10**: All of the above must be functional on demo day. No mocks. No "this is what it would look like."

---

## Business Model (Currently 2/10 → Need 10/10)

**Financial proof missing**:

| Requirement                         | Current State              |
| ----------------------------------- | -------------------------- |
| Revenue model documentation         | Hypothesised only          |
| Actual customer ROI calculation     | Generic, not site-specific |
| Unit economics (COGS per site)      | Not calculated             |
| Customer acquisition cost           | Not measured               |
| Sales cycle length                  | Not validated              |
| LOIs or paid deposits               | None                       |
| Competitor pricing                  | Not researched             |
| Financial model (3-year projection) | None                       |

**To score 10/10**: 3 signed LOIs, unit economics documented, 3-year financial model with assumptions.

---

## Team and Execution (Currently 3/10 → Need 10/10)

**Execution evidence missing from codebase**:

| Requirement                       | Current State      |
| --------------------------------- | ------------------ |
| CI/CD pipeline                    | None               |
| Automated tests                   | None               |
| Deployed production system        | None               |
| Monitoring / alerting             | None               |
| Runbook                           | None               |
| On-call rotation                  | N/A (solo)         |
| Architecture documentation        | None               |
| Code review history               | None               |
| git history showing team patterns | Single-author repo |

**To score 10/10**: GitHub Actions CI, automated tests, deployed dashboard, monitoring documentation.

---

## AI/ML Depth (Currently 4/10 → Need 10/10)

**Technical depth missing**:

| Requirement                    | Current State |
| ------------------------------ | ------------- |
| XGBoost model trained          | None          |
| CatBoost/LightGBM comparison   | None          |
| Residual hybrid architecture   | None          |
| SHAP integration               | None          |
| Bayesian hyperparameter tuning | None          |
| Temporal cross-validation      | None          |
| Automated retraining pipeline  | None          |
| MAPE drift detection           | None          |
| Model card                     | None          |
| Multi-year training data       | 1 year only   |
| Feature: clear-sky ratio       | None          |
| Feature: DNI/DHI ratio         | None          |
| Online learning                | None          |

**To score 10/10**: All of the above implemented, tested, and documented.

---

## Consolidated Gap Count

| Category         | Gap Count   | Difficulty                          |
| ---------------- | ----------- | ----------------------------------- |
| AI/ML Depth      | 13          | High (ML engineering)               |
| Product & Demo   | 9           | Medium (Streamlit + infrastructure) |
| Team & Execution | 8           | Medium (DevOps)                     |
| Market & Problem | 5           | High (customer discovery)           |
| Business Model   | 7           | Medium (sales + finance)            |
| **Total**        | **42 gaps** |                                     |

**The 5 highest-leverage gaps** (achieve greatest score improvement per hour of work):

1. **Build working Streamlit dashboard** (Product: goes from 3→5)
2. **Conduct 5 customer interviews** (Market: goes from 4→7)
3. **Implement XGBoost residual model** (ML: goes from 4→6)
4. **Add SHAP integration** (ML: goes from 6→7)
5. **Get 1 signed LOI** (Business: goes from 2→5)
