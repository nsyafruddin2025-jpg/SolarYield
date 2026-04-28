# Verification: M1 Pre-processing — inference + daily aggregates + anomaly flags

## Plan Reference

Todo 1: "Load src/ml/model.pkl, run inference on solar_yield_output.csv (all 8,760 rows), compute daily aggregates (date, actual_kwh, predicted_kwh, residual_kwh, residual_sigma, is_anomaly). Output enriched_daily.csv."

## What Was Built

- `src/ml/preprocess.py` — pre-processing script
- `data/enriched_daily.csv` — enriched daily data (365 rows)

## Verification

### Output CSV columns match spec

```
['date', 'actual_kwh', 'predicted_kwh', 'residual_kwh', 'residual_sigma', 'is_anomaly', 'mean_temp', 'mean_cloud', 'mean_humidity', 'max_ghi']
```

✅ All required columns present: date, actual_kwh, predicted_kwh, residual_kwh, residual_sigma, is_anomaly

### Anomaly detection working

- 13 anomalous days flagged out of 365 (3.6%)
- Most anomalous: 2026-01-18 at -4.33σ (actual=8205, predicted=8306 kWh)
- Sorted by residual_sigma ascending (most anomalous first)
  ✅ Anomaly threshold: residual < rolling_mean - 2σ

### Data range

- Date range: 2025-04-01 to 2026-03-31 (365 days)
- Hourly rows processed: 8,760
  ✅ All data processed

### Model inference

- GradientBoostingRegressor loaded from src/ml/model.pkl
- Predictions clipped to >= 0
- Mean predicted: 341.99 kWh/hour, Max: 3311.80 kWh/hour
  ✅ Inference runs correctly

## Journal constraints addressed

- Journal 0013: "The gap is productization" — pre-processed data now exists for dashboard to consume
- Journal 0012: "Dashboard is the critical path" — pre-processing was prerequisite for dashboard

## Status: COMPLETE
