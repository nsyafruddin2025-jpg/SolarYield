# Specs Index — SolarYield

| File                | Domain   | Description                                                                   |
| ------------------- | -------- | ----------------------------------------------------------------------------- |
| `data-pipeline.md`  | Data     | Open-Meteo → PVLib → CSV pipeline, physical validation, Singapore 5MW config  |
| `ml-model.md`       | ML       | GradientBoosting/RF training, SHAP, anomaly detection, XGBoost forecast model |
| `dashboard.md`      | Product  | Streamlit 3-page dashboard (Overview, Data Explorer, Anomaly Log)             |
| `business-model.md` | Business | Three revenue models: SaaS Dashboard, Bankable Reports, API Service           |

## Brief Traceability

| Brief Requirement         | Spec File           | Section                |
| ------------------------- | ------------------- | ---------------------- |
| PVLib physical modeling   | `data-pipeline.md`  | PVLib Computation      |
| Singapore 5MW solar farm  | `data-pipeline.md`  | System Configuration   |
| GradientBoosting ML model | `ml-model.md`       | Current State          |
| SHAP explainability       | `ml-model.md`       | SHAP Analysis          |
| Anomaly detection         | `ml-model.md`       | Anomaly Detection      |
| Streamlit dashboard       | `dashboard.md`      | MVP Dashboard Pages    |
| Business model validation | `business-model.md` | Three Candidate Models |
