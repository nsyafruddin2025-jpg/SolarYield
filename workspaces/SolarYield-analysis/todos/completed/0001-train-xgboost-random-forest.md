# Train XGBoost and Random Forest Models on Solar Yield Data

## SPEC REFERENCES

- `specs/ml-model.md` § XGBoost Forecast Model
- `specs/ml-architecture.md` (pending — will be created by this todo)

## TASKS

### Todo 1: Build ML training script ✅ DONE

**File**: `src/ml/train_models.py`

- Load `solar_yield_output.csv` ✅
- Features: GHI, direct_radiation, diffuse_radiation, temperature, cloud_cover, humidity, wind_speed, hour_of_day, day_of_year, panel_capacity_kw, panel_tilt ✅
- Time-based 80/20 split (first 80% train, last 20% test) ✅
- Cyclical sin/cos encoding for hour and day ✅

### Todo 2: Train GradientBoosting (sklearn, OpenMP-free) ✅ DONE

- GradientBoostingRegressor (sklearn equivalent of XGBoost, no OpenMP required) ✅
- Train + predict ✅
- Clip negative predictions to 0 ✅
- Compute MAPE, RMSE, R² ✅

### Todo 3: Train Random Forest baseline ✅ DONE

- RandomForestRegressor ✅
- Train + predict ✅
- Clip negative predictions to 0 ✅
- Compare metrics ✅

### Todo 4: Save GradientBoosting model ✅ DONE

- `src/ml/model.pkl` saved ✅
- `src/ml/model_metadata.json` saved ✅

### Todo 5: Compute SHAP values and save chart ✅ DONE

- TreeExplainer ✅
- Beeswarm plot ✅
- `src/ml/shap_chart.png` saved ✅

## VERIFICATION

| Criterion                                      | Result                               |
| ---------------------------------------------- | ------------------------------------ |
| `python -m ml.train_models` runs without error | ✅ (5.7s)                            |
| Comparison table printed                       | ✅                                   |
| MAPE, RMSE, R² for both models                 | ✅                                   |
| `src/ml/model.pkl` exists and loadable         | ✅ (1.7MB GradientBoostingRegressor) |
| `src/ml/shap_chart.png` valid image            | ✅ (113KB)                           |

## RESULTS

```
Model                |   MAPE (%) |   RMSE (kWh) |       R²
-----------------------------------------------------------
GradientBoosting     |       6.10 |        41.51 |   0.9915
RandomForest         |       5.81 |        53.40 |   0.9859
```

**Top 5 SHAP features**:

1. diffuse_radiation — 229.83
2. GHI — 186.40
3. day_cos — 47.46
4. direct_radiation — 43.97
5. hour_sin — 43.01

## NOTES

- GradientBoosting used instead of XGBoost (no OpenMP/libomp on this macOS machine)
- Random Forest beats GBR on MAPE (5.81% vs 6.10%) but GBR has lower RMSE and higher R²
- Both models well below 10% MAPE target from spec
- Train: 2025-04-01 to 2026-01-17 (7,008 rows)
- Test: 2026-01-18 to 2026-03-31 (1,752 rows)
