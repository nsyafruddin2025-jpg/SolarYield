# AI/ML Depth Assessment (10%)

## Score: 4 / 10

## Evidence

### What exists

- PVLib physical model (well-established, industry-standard)
- Actual DNI/DHI from Open-Meteo API (not estimated)
- Physical validation (GHI bounds, temperature bounds, kWh capacity ceiling)
- Retry logic with exponential backoff
- Configuration dataclass with parameterisation
- XGBoost vs Random Forest analysis done (conclusion: XGBoost wins)
- LSTM rejection based on quantitative autocorrelation analysis (lag-24h GHI autocorrelation < 0.1)
- Time features (hour_of_day, day_of_year) engineered

### What is missing

- **No ML model trained or deployed**: XGBoost analysis was theoretical, no actual model
- **No feature pipeline**: No real-time or batch ML inference infrastructure
- **No training data pipeline**: Historical CSV is not an ML training pipeline
- **No model registry**: No way to version, compare, or roll back models
- **No drift monitoring**: No concept of model staleness, data drift, or prediction confidence
- **No retraining trigger**: When does the model update? Manually?
- **No uncertainty quantification**: Point estimate only — no prediction intervals
- **No ensemble**: Single model, no uncertainty bounds from multiple models
- **No hyperparameter tuning**: No validation set, no cross-validation, no grid search
- **No error analysis**: No decomposition of prediction errors by weather condition

## Single Biggest Gap

**No actual ML model in production.** The project has the scaffolding for ML (XGBoost recommendation, LSTM rejection rationale, feature engineering) but zero ML code has been written, trained, or deployed. The physical PVLib model is excellent, but the step from "weather → kWh output" (already solved by PVLib) to "weather + historical patterns → next-hour yield forecast" (the ML value-add) has not been built.

## Why This Matters

PVLib gives you the physical maximum yield. The ML value is in predicting:

1. **Anomaly detection**: Is today's yield below what physics predicts? (panel soiling, inverter failure)
2. **Forecasting**: What will tomorrow's yield be? (for grid operators, PPA settlement)
3. **Degradation tracking**: Is the system producing 2% less per year than expected?

These are the use cases that make a solar yield product defensible and valuable. PVLib alone cannot provide any of these.

## Recommended ML Path

1. **Short-term (MVP)**: Build anomaly detection on top of PVLib — flag days where actual yield is >2 standard deviations below physics-predicted yield
2. **Medium-term**: XGBoost hourly forecast model (GHI, DNI, DHI, temperature, cloud_cover, hour, day_of_year as features) predicting kWh_output for the next hour
3. **Long-term**: LSTM or Transformer for multi-day lookahead (only if autocorrelation analysis shows LSTM-appropriate patterns in actual residual data)
