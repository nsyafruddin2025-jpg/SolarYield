#!/usr/bin/env python3
"""
Pre-processing script for SolarYield dashboard.

Loads the trained GradientBoosting model, runs inference on the full
solar_yield_output.csv, computes daily aggregates, and flags anomalies.

Outputs data/enriched_daily.csv with columns:
    date, actual_kwh, predicted_kwh, residual_kwh, residual_sigma, is_anomaly
"""

import json
import math
import pathlib
import sys

import joblib
import numpy as np
import pandas as pd

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------

DATA_DIR = pathlib.Path(__file__).parent.parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

CSV_IN = pathlib.Path(__file__).parent.parent.parent / "solar_yield_output.csv"
MODEL_IN = pathlib.Path(__file__).parent / "model.pkl"
OUTPUT_OUT = DATA_DIR / "enriched_daily.csv"

# Model features (same as train_models.py)
FEATURES = [
    "GHI",
    "direct_radiation",
    "diffuse_radiation",
    "temperature",
    "cloud_cover",
    "humidity",
    "wind_speed",
    "hour_of_day",
    "day_of_year",
    "panel_capacity_kw",
    "panel_tilt",
]
CYCLICAL_FEATURES = ["hour_sin", "hour_cos", "day_sin", "day_cos"]
ALL_FEATURES = FEATURES + CYCLICAL_FEATURES

# System constants (from SolarConfig)
SYSTEM_CAPACITY_KW = 5000.0
PANEL_TILT = 20.0

# Anomaly threshold (standard deviations below mean residual)
ANOMALY_SIGMA = 2.0


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def cyclical_encode(series: pd.Series, period: int) -> tuple[pd.Series, pd.Series]:
    return np.sin(2 * math.pi * series / period), np.cos(2 * math.pi * series / period)


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add model-required features that aren't in the raw CSV."""
    df = df.copy()
    df["panel_capacity_kw"] = SYSTEM_CAPACITY_KW
    df["panel_tilt"] = PANEL_TILT
    df["hour_sin"], df["hour_cos"] = cyclical_encode(df["hour_of_day"], 24)
    df["day_sin"], df["day_cos"] = cyclical_encode(df["day_of_year"], 365)
    return df


def load_model() -> object:
    """Load the trained GradientBoosting model."""
    if not MODEL_IN.exists():
        sys.exit(f"Model not found at {MODEL_IN}. Run src/ml/train_models.py first.")
    return joblib.load(MODEL_IN)


def run_inference(df: pd.DataFrame, model: object) -> np.ndarray:
    """Run model predictions on the dataframe."""
    X = df[ALL_FEATURES].values
    preds = model.predict(X)
    return np.clip(preds, 0, None)


def compute_daily_aggregates(
    hourly_df: pd.DataFrame, predictions: np.ndarray
) -> pd.DataFrame:
    """Aggregate hourly data to daily and merge with predictions."""
    df = hourly_df.copy()
    df["predicted_kwh"] = predictions

    # Add date column (date only, no time)
    df["date"] = df["timestamp"].dt.date

    # Group by date and aggregate
    daily = df.groupby("date").agg(
        actual_kwh=("kWh_output", "sum"),
        predicted_kwh=("predicted_kwh", "sum"),
        mean_temp=("temperature", "mean"),
        mean_cloud=("cloud_cover", "mean"),
        mean_humidity=("humidity", "mean"),
        max_ghi=("GHI", "max"),
    )

    daily = daily.reset_index()
    daily["date"] = pd.to_datetime(daily["date"])

    return daily


def flag_anomalies(daily_df: pd.DataFrame) -> pd.DataFrame:
    """Flag anomalous days using rolling residual statistics."""
    df = daily_df.copy()

    # Residual = actual - predicted
    df["residual_kwh"] = df["actual_kwh"] - df["predicted_kwh"]

    # Rolling residual statistics (30-day window, require at least 7 days of data)
    df["residual_mean"] = df["residual_kwh"].rolling(window=30, min_periods=7).mean()
    df["residual_std"] = df["residual_kwh"].rolling(window=30, min_periods=7).std()

    # Flag anomaly if residual < mean - 2*std (significant underperformance)
    threshold = df["residual_mean"] - ANOMALY_SIGMA * df["residual_std"]
    df["is_anomaly"] = df["residual_kwh"] < threshold

    # Number of sigmas below (for sorting — negative = anomalous)
    df["residual_sigma"] = (df["residual_kwh"] - df["residual_mean"]) / df["residual_std"]

    return df


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("SolarYield Pre-processing — Dashboard Data Enrichment")
    print("=" * 60)

    # 1. Load data
    print(f"\n[1] Loading data from {CSV_IN}...")
    df = pd.read_csv(CSV_IN, parse_dates=["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    print(f"    Rows: {len(df):,} | {df['timestamp'].min()} → {df['timestamp'].max()}")

    # 2. Engineer features
    print("\n[2] Engineering features...")
    df = engineer_features(df)
    print(f"    Features: {ALL_FEATURES}")

    # 3. Run inference
    print("\n[3] Loading model from {MODEL_IN}...")
    model = load_model()
    print(f"    Model: {type(model).__name__}")

    print("\n[4] Running inference...")
    predictions = run_inference(df, model)
    print(f"    Predictions: {len(predictions):,} rows")
    print(f"    Mean predicted kWh/hour: {predictions.mean():.2f}")
    print(f"    Max predicted kWh/hour: {predictions.max():.2f}")

    # 5. Compute daily aggregates
    print("\n[5] Computing daily aggregates...")
    daily = compute_daily_aggregates(df, predictions)
    print(f"    Days: {len(daily)}")

    # 6. Flag anomalies
    print(f"\n[6] Flagging anomalies (>{ANOMALY_SIGMA}σ below rolling mean)...")
    daily = flag_anomalies(daily)
    anomaly_count = daily["is_anomaly"].sum()
    print(f"    Anomalous days: {anomaly_count}")

    # 7. Select and order output columns
    output_cols = [
        "date",
        "actual_kwh",
        "predicted_kwh",
        "residual_kwh",
        "residual_sigma",
        "is_anomaly",
        "mean_temp",
        "mean_cloud",
        "mean_humidity",
        "max_ghi",
    ]
    daily = daily[output_cols].copy()

    # Sort by most anomalous first (lowest residual_sigma)
    daily = daily.sort_values("residual_sigma").reset_index(drop=True)

    # 8. Save
    print(f"\n[7] Saving to {OUTPUT_OUT}...")
    daily.to_csv(OUTPUT_OUT, index=False)
    print(f"    Rows: {len(daily)} | {daily['date'].min()} → {daily['date'].max()}")

    # 9. Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Total days:          {len(daily)}")
    print(f"Anomalous days:      {anomaly_count} ({100*anomaly_count/len(daily):.1f}%)")
    print(f"Mean actual kWh/day: {daily['actual_kwh'].mean():.1f}")
    print(f"Mean predicted kWh/day: {daily['predicted_kwh'].mean():.1f}")
    print(f"Mean residual kWh/day: {daily['residual_kwh'].mean():.1f}")
    print(f"Capacity factor (actual): {(daily['actual_kwh'].sum() / (len(daily) * SYSTEM_CAPACITY_KW) * 100):.1f}%")
    print(f"Output: {OUTPUT_OUT}")
    print("=" * 60)


if __name__ == "__main__":
    main()
