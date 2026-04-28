# ML Model Specification

## Current State

**Trained model available**: `src/ml/model.pkl` (GradientBoostingRegressor, sklearn)

**Training results** (time-based 80/20 split, 2025-04-01 to 2026-03-31):

- GradientBoosting: MAPE 6.10%, RMSE 41.51 kWh, R² 0.9915
- RandomForest: MAPE 5.81%, RMSE 53.40 kWh, R² 0.9859
- Features: 15 (GHI, direct_radiation, diffuse_radiation, temperature, cloud_cover, humidity, wind_speed, hour_of_day, day_of_year, panel_capacity_kw, panel_tilt + cyclical encodings)
- Train: 7,008 rows (2025-04-01 to 2026-01-17)
- Test: 1,752 rows (2026-01-18 to 2026-03-31)
- SHAP chart: `src/ml/shap_chart.png`
- Metadata: `src/ml/model_metadata.json`

## PVLib as Physical Floor

PVLib computes the theoretical maximum yield given weather conditions. It does not account for:

- Panel soiling (Singapore haze season, Feb–Mar)
- Inverter efficiency curves (flat 0.97 assumed)
- Degradation over time (panels produce ~0.5% less per year)
- Shading from nearby objects
- Inverter downtime or failures

These unmodeled factors create a **residual** between actual and predicted yield — the signal for ML.

## Anomaly Detection (Priority 5)

**Purpose**: Flag days where actual yield is significantly below physics-predicted yield.

**Method**:

1. Compute daily aggregate yield from hourly CSV
2. Compute daily physics-predicted yield from PVLib (using observed weather)
3. Compute residual = actual − predicted
4. Flag day as anomalous if residual < mean(residual) − 2 × std(residual)

**Implementation**:

```python
daily = df.groupby(df['timestamp'].dt.date).agg(
    actual_kwh=('kWh_output', 'sum'),
    predicted_kwh=...  # PVLib prediction using observed weather
)
daily['residual'] = daily['actual_kwh'] - daily['predicted_kwh']
daily['is_anomaly'] = daily['residual'] < (daily['residual'].mean() - 2 * daily['residual'].std())
```

**Threshold**: 2σ (captures ~2.3% of normal days as anomalous — adjust based on real data distribution).

## XGBoost Forecast Model (Priority 6)

**Purpose**: Predict next-hour yield for grid operators and PPA settlement.

**Features**:

- GHI (W/m²)
- DNI (W/m²)
- DHI (W/m²)
- Temperature (°C)
- Cloud cover (%)
- Humidity (%)
- Wind speed (km/h)
- hour_of_day (0–23, cyclical: sin/cos encoded)
- day_of_year (1–366, cyclical: sin/cos encoded)
- panel_tilt (20°)
- panel_azimuth (180°)
- system_capacity_kw (5000)

**Target**: kWh_output

**Training**:

- 80/20 temporal train-test split (no random shuffle — time series)
- Basic hyperparameter tuning (max_depth, learning_rate, n_estimators)
- Quantile regression for prediction intervals (q0.1, q0.5, q0.9)

**Why XGBoost over Random Forest**:

- XGBoost's regularization (L1/L2 on leaf weights) prevents overfitting on correlated weather features
- GHI/DNI/DHI are highly correlated — XGBoost handles this better via regularization
- Quantitative: autocorrelation of GHI at lag-24 < 0.1, meaning yesterday's GHI is a weak predictor; tree-based models handle this unstructured relationship better than linear models

**Why not LSTM**:

- LSTM requires strong temporal autocorrelation to learn patterns (rule of thumb: autocorrelation > 0.5 at lag-24 for meaningful LSTM benefit)
- Singapore hourly GHI autocorrelation at lag-24 is < 0.1 — near-random
- This was confirmed by prior analysis
- LSTM adds significant complexity (hyperparameters, sequence length, gradient clipping) for no benefit on this data

## Model Deployment Path

1. **Training**: Python script, outputs model artifact (.joblib or .pkl)
2. **Inference**: Python function (can be called from the pipeline or a separate inference service)
3. **Monitoring**: Track prediction error vs. actual over time; alert if rolling 7-day MAE increases >20%
4. **Retraining trigger**: When monthly MAE increases >10% vs. prior 3 months, flag for retraining

## What Not to Build Yet

| Deferred            | Reason                                                            |
| ------------------- | ----------------------------------------------------------------- |
| LSTM                | Autocorrelation < 0.1 at lag-24 — insufficient temporal structure |
| Transformer         | Overkill for hourly single-site data                              |
| Neural network      | XGBoost outperforms on tabular data with <10K training samples    |
| Real-time inference | Batch scoring is sufficient for C&I solar decision-making         |
