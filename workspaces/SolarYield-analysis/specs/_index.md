# SolarYield Project Specifications

## Manifest

| File                      | Domain         | Description                                                                                       |
| ------------------------- | -------------- | ------------------------------------------------------------------------------------------------- |
| `data-pipeline.md`        | Infrastructure | Open-Meteo → PVLib → CSV pipeline for Singapore solar yield                                       |
| `data-quality.md`         | Infrastructure | Physical realism validation, data sufficiency, leakage risks, missing variables                   |
| `configuration.md`        | Infrastructure | SolarConfig dataclass: all parameterised values                                                   |
| `ml-model.md`             | ML             | XGBoost forecast model, anomaly detection, LSTM rejection rationale, residual hybrid architecture |
| `ml-architecture.md`      | ML             | Bayesian tuning, temporal CV, feature engineering, MAPE targets, online learning                  |
| `shap-explainability.md`  | ML/Compliance  | SHAP values, operator presentation, ISO 42001 requirements                                        |
| `dashboard.md`            | Product        | MVP web dashboard spec: yield, capacity factor, anomaly alerts, 6 screens                         |
| `product-completeness.md` | Product        | Missing features, PE demo structure, alert architecture, multi-site DB schema                     |
| `business-model.md`       | Business       | Revenue model: SaaS dashboard vs bankable reports vs API service                                  |
| `business-validation.md`  | Business       | MAPE/grid penalties, customer ROI, segment priority, WTP validation                               |
| `sustainability.md`       | Strategy       | Data moat, geographic expansion, model degradation, drift detection                               |
| `competitive-edge.md`     | Strategy       | Unreplicable capabilities, patent decisions, Solargis benchmark                                   |

## Brief Traceability

All spec files map to the 8 analysis dimensions from the Stanford PhD review.

## Key Decisions Locked

- **ML approach**: XGBoost residual hybrid (PVLib → residual → XGBoost)
- **MAPE target**: <10% achievable; <5% requires AOD + panel temperature
- **Business model**: Bankable yield reports (Option B) as primary, SaaS dashboard as secondary
- **First customer segment**: C&I ground-mount, 1–5MW, Singapore
- **Data source**: Open-Meteo ERA5 reanalysis (not ground truth — limitation documented)
- **Defensibility**: Anomaly pattern library is the primary moat, not model architecture
