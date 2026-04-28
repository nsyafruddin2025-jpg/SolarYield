#!/usr/bin/env python3
"""
Train GradientBoosting (scikit-learn, XGBoost-equivalent without OpenMP dependency)
and Random Forest models on solar yield data.
Time-based 80/20 split. Features: GHI, DNI, DHI, temperature,
cloud_cover, humidity, wind_speed, hour_of_day, day_of_year,
panel_capacity_kw, panel_tilt. Target: kWh_output.
"""

import json
import math
import pathlib
import warnings
from datetime import datetime

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor

warnings.filterwarnings("ignore")

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------

DATA_PATH = pathlib.Path(__file__).parent.parent.parent / "solar_yield_output.csv"
MODEL_OUT = pathlib.Path(__file__).parent / "model.pkl"
SHAP_OUT = pathlib.Path(__file__).parent / "shap_chart.png"
METADATA_OUT = pathlib.Path(__file__).parent / "model_metadata.json"

FEATURES = [
    "GHI",
    "direct_radiation",  # DNI
    "diffuse_radiation",  # DHI
    "temperature",
    "cloud_cover",
    "humidity",
    "wind_speed",
    "hour_of_day",
    "day_of_year",
    "panel_capacity_kw",
    "panel_tilt",
]
TARGET = "kWh_output"

# System constants (from SolarConfig)
SYSTEM_CAPACITY_KW = 5000.0
PANEL_TILT = 20.0

# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Absolute Percentage Error, ignoring zero targets."""
    mask = y_true > 0
    if mask.sum() == 0:
        return float("nan")
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100)


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    if ss_tot == 0:
        return float("nan")
    return float(1 - ss_res / ss_tot)


def cyclical_encode(series: pd.Series, period: int) -> tuple[pd.Series, pd.Series]:
    return np.sin(2 * math.pi * series / period), np.cos(2 * math.pi * series / period)


def print_comparison(results: list[dict]) -> None:
    header = f"{'Model':<20} | {'MAPE (%)':>10} | {'RMSE (kWh)':>12} | {'R²':>8}"
    print(header)
    print("-" * len(header))
    for r in results:
        print(f"{r['name']:<20} | {r['mape']:>10.2f} | {r['rmse']:>12.2f} | {r['r2']:>8.4f}")
    print()


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

def main() -> None:
    t0 = datetime.now()
    print("=" * 60)
    print("Solar Yield ML Training")
    print("=" * 60)

    # 1. Load data
    print(f"\n[1] Loading data from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH, parse_dates=["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    print(f"    Rows: {len(df):,}  |  Date range: {df['timestamp'].min()} → {df['timestamp'].max()}")

    # 2. Engineer features
    print("\n[2] Engineering features...")

    # Add constant config features
    df["panel_capacity_kw"] = SYSTEM_CAPACITY_KW
    df["panel_tilt"] = PANEL_TILT

    # Cyclical encoding for hour and day
    df["hour_sin"], df["hour_cos"] = cyclical_encode(df["hour_of_day"], 24)
    df["day_sin"], df["day_cos"] = cyclical_encode(df["day_of_year"], 365)

    # All features including cyclical variants
    all_features = FEATURES + ["hour_sin", "hour_cos", "day_sin", "day_cos"]

    # Drop rows with NaN in key columns
    n_before = len(df)
    df = df.dropna(subset=FEATURES + [TARGET])
    n_after = len(df)
    if n_after < n_before:
        print(f"    Dropped {n_before - n_after} rows with NaN")

    # 3. Time-based train/test split (80/20)
    print("\n[3] Time-based 80/20 split...")
    split_idx = int(len(df) * 0.80)
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]

    X_train = train_df[all_features].values
    y_train = train_df[TARGET].values
    X_test = test_df[all_features].values
    y_test = test_df[TARGET].values

    print(f"    Train: {len(train_df):,} rows  |  {train_df['timestamp'].min()} → {train_df['timestamp'].max()}")
    print(f"    Test:  {len(test_df):,} rows  |  {test_df['timestamp'].min()} → {test_df['timestamp'].max()}")

    # 4. Train GradientBoosting (sklearn, OpenMP-free equivalent to XGBoost)
    print("\n[4] Training GradientBoosting (sklearn)...")
    gbr = GradientBoostingRegressor(
        max_depth=6,
        learning_rate=0.1,
        n_estimators=300,
        subsample=0.8,
        min_samples_leaf=5,
        random_state=42,
    )
    gbr.fit(X_train, y_train)
    y_pred_gbr = gbr.predict(X_test)
    y_pred_gbr = np.clip(y_pred_gbr, 0, None)

    gbr_results = {
        "name": "GradientBoosting",
        "mape": mape(y_test, y_pred_gbr),
        "rmse": rmse(y_test, y_pred_gbr),
        "r2": r2(y_test, y_pred_gbr),
    }
    print(f"    GBR  — MAPE: {gbr_results['mape']:.2f}%  RMSE: {gbr_results['rmse']:.2f}  R²: {gbr_results['r2']:.4f}")

    # 5. Train Random Forest
    print("\n[5] Training Random Forest...")
    rf = RandomForestRegressor(
        n_estimators=300,
        max_depth=15,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    y_pred_rf = np.clip(y_pred_rf, 0, None)

    rf_results = {
        "name": "RandomForest",
        "mape": mape(y_test, y_pred_rf),
        "rmse": rmse(y_test, y_pred_rf),
        "r2": r2(y_test, y_pred_rf),
    }
    print(f"    RF   — MAPE: {rf_results['mape']:.2f}%  RMSE: {rf_results['rmse']:.2f}  R²: {rf_results['r2']:.4f}")

    # 6. Comparison table
    print("\n[6] Comparison Table")
    print_comparison([gbr_results, rf_results])

    # 7. Save GradientBoosting model
    print(f"[7] Saving GradientBoosting model to {MODEL_OUT}...")
    joblib.dump(gbr, MODEL_OUT)
    metadata = {
        "model_type": "GradientBoostingRegressor (sklearn)",
        "features": all_features,
        "feature_count": len(all_features),
        "n_train": len(train_df),
        "n_test": len(test_df),
        "train_date_range": [str(train_df["timestamp"].min()), str(train_df["timestamp"].max())],
        "test_date_range": [str(test_df["timestamp"].min()), str(test_df["timestamp"].max())],
        "system_capacity_kw": SYSTEM_CAPACITY_KW,
        "panel_tilt": PANEL_TILT,
        "metrics": {
            "MAPE_pct": round(gbr_results["mape"], 2),
            "RMSE_kWh": round(gbr_results["rmse"], 2),
            "R2": round(gbr_results["r2"], 4),
        },
    }
    with open(METADATA_OUT, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"    Metadata saved to {METADATA_OUT}")

    # 8. SHAP analysis
    print(f"\n[8] Computing SHAP values (TreeExplainer)...")
    explainer = shap.TreeExplainer(gbr)
    sample_size = min(500, len(X_test))
    X_sample = X_test[:sample_size]
    shap_values = explainer.shap_values(X_sample)

    # Feature importance by mean |SHAP|
    shap_abs_mean = np.abs(shap_values).mean(axis=0)
    importance_df = pd.DataFrame({
        "feature": all_features,
        "mean_abs_shap": shap_abs_mean,
    }).sort_values("mean_abs_shap", ascending=False)

    print("\n    Top 5 features by mean |SHAP|:")
    for _, row in importance_df.head(5).iterrows():
        print(f"      {row['feature']:<20} {row['mean_abs_shap']:.4f}")

    # 9. Beeswarm plot
    print(f"\n[9] Saving SHAP beeswarm to {SHAP_OUT}...")
    plt.figure(figsize=(10, 8))
    shap.summary_plot(shap_values, features=X_sample, feature_names=all_features, show=False)
    plt.tight_layout()
    plt.savefig(SHAP_OUT, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"    SHAP chart saved")

    elapsed = (datetime.now() - t0).total_seconds()
    print(f"\n{'=' * 60}")
    print(f"Done in {elapsed:.1f}s")
    print(f"  model:  {MODEL_OUT}")
    print(f"  chart:  {SHAP_OUT}")
    print(f"  meta:   {METADATA_OUT}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
