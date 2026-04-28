#!/usr/bin/env python3
"""
Solar Yield Data Pipeline

Fetches historical weather data from Open-Meteo API for Singapore,
computes estimated kWh output using PVLib for a solar farm, and saves
results to CSV.
"""

import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pandas as pd
import requests
import pvlib
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()


# =============================================================================
# Configuration
# =============================================================================

@dataclass
class SolarConfig:
    """Solar farm configuration."""

    # Location
    latitude: float = 1.3521
    longitude: float = 103.8198
    timezone: str = "Asia/Singapore"
    altitude: float = 10  # meters

    # System parameters
    system_capacity_kw: float = 5000  # 5MW
    panel_tilt: float = 20  # degrees
    panel_azimuth: float = 180  # south-facing (180° in PVLib convention)
    module_power_w: float = 550  # typical 550W panel
    modules_per_string: int = 15
    strings_per_array: int = 607

    # Temperature coefficient for crystalline silicon (per °C)
    gamma_pdc: float = -0.004

    # Inverter efficiency (flat rate)
    inverter_efficiency: float = 0.97

    # Soiling loss factor (monthly, Singapore haze season Feb-Mar)
    soiling_factor: float = 0.98

    @property
    def total_capacity_kw(self) -> float:
        modules = self.modules_per_string * self.strings_per_array
        return (modules * self.module_power_w) / 1000


# Default configuration for Singapore 5MW farm
CONFIG = SolarConfig()

# Open-Meteo API endpoint
OPEN_METEO_URL = "https://archive-api.open-meteo.com/v1/archive"


# =============================================================================
# Data Validation
# =============================================================================

class ValidationError(Exception):
    """Raised when data fails validation."""


def validate_weather_data(df: pd.DataFrame, config: SolarConfig) -> None:
    """Validate weather data is within physical bounds."""

    issues = []

    # GHI: 0-1200 W/m² (physical limit with extreme refraction)
    if not df["GHI"].between(0, 1200).all():
        bad = df[~df["GHI"].between(0, 1200)]
        issues.append(f"GHI out of range [0, 1200]: {len(bad)} rows, max={df['GHI'].max()}")

    # Direct radiation: 0-1100 W/m²
    if not df["direct_radiation"].between(0, 1100).all():
        bad = df[~df["direct_radiation"].between(0, 1100)]
        issues.append(f"Direct radiation out of range: {len(bad)} rows")

    # Diffuse radiation: 0-800 W/m²
    if not df["diffuse_radiation"].between(0, 800).all():
        bad = df[~df["diffuse_radiation"].between(0, 800)]
        issues.append(f"Diffuse radiation out of range: {len(bad)} rows")

    # Temperature: Singapore range 20-40°C
    if not df["temperature"].between(20, 45).all():
        bad = df[~df["temperature"].between(20, 45)]
        issues.append(f"Temperature out of range [20, 45]: {len(bad)} rows")

    # Cloud cover: 0-100%
    if not df["cloud_cover"].between(0, 100).all():
        bad = df[~df["cloud_cover"].between(0, 100)]
        issues.append(f"Cloud cover out of range [0, 100]: {len(bad)} rows")

    # Humidity: 0-100%
    if not df["humidity"].between(0, 100).all():
        bad = df[~df["humidity"].between(0, 100)]
        issues.append(f"Humidity out of range [0, 100]: {len(bad)} rows")

    # Wind speed: 0-200 km/h (extreme gust)
    if not df["wind_speed"].between(0, 200).all():
        bad = df[~df["wind_speed"].between(0, 200)]
        issues.append(f"Wind speed out of range [0, 200]: {len(bad)} rows")

    if issues:
        raise ValidationError("Weather data validation failed:\n  - " + "\n  - ".join(issues))


def validate_kwh_output(df: pd.DataFrame, config: SolarConfig) -> None:
    """Validate kWh output is within physical bounds."""

    issues = []

    # kWh should never exceed system capacity per hour
    if not (df["kWh_output"] <= config.system_capacity_kw).all():
        bad = df[df["kWh_output"] > config.system_capacity_kw]
        issues.append(f"kWh output exceeds capacity ({config.system_capacity_kw}kW): {len(bad)} rows")

    # kWh should never be negative
    if not (df["kWh_output"] >= 0).all():
        bad = df[df["kWh_output"] < 0]
        issues.append(f"Negative kWh output: {len(bad)} rows")

    if issues:
        raise ValidationError("kWh output validation failed:\n  - " + "\n  - ".join(issues))


# =============================================================================
# Weather Data Fetching
# =============================================================================

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True,
)
def fetch_monthly_weather_data(
    year: int, month: int, config: SolarConfig
) -> pd.DataFrame:
    """Fetch weather data for a single month from Open-Meteo API."""

    # Build date range for the month
    start_dt = datetime(year, month, 1, tzinfo=ZoneInfo(config.timezone))
    if month == 12:
        end_dt = datetime(year + 1, 1, 1, tzinfo=ZoneInfo(config.timezone)) - timedelta(days=1)
    else:
        end_dt = datetime(year, month + 1, 1, tzinfo=ZoneInfo(config.timezone)) - timedelta(days=1)

    start_str = start_dt.strftime("%Y-%m-%d")
    end_str = end_dt.strftime("%Y-%m-%d")

    params = {
        "latitude": config.latitude,
        "longitude": config.longitude,
        "start_date": start_str,
        "end_date": end_str,
        "hourly": [
            "shortwave_radiation",  # GHI
            "direct_radiation",  # Direct radiation (not horizontal)
            "diffuse_radiation",  # Diffuse radiation
            "temperature_2m",
            "cloud_cover",
            "relative_humidity_2m",
            "wind_speed_10m",
        ],
        "timezone": config.timezone,
        "wind_speed_unit": "kmh",
    }

    response = requests.get(OPEN_METEO_URL, params=params, timeout=60)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data["hourly"])
    df["time"] = pd.to_datetime(df["time"])

    # Rename columns to match our schema
    df = df.rename(
        columns={
            "time": "timestamp",
            "shortwave_radiation": "GHI",
            "direct_radiation": "direct_radiation",
            "diffuse_radiation": "diffuse_radiation",
            "temperature_2m": "temperature",
            "relative_humidity_2m": "humidity",
            "wind_speed_10m": "wind_speed",
        }
    )

    return df


def fetch_weather_data(start_date: str, end_date: str, config: SolarConfig) -> pd.DataFrame:
    """Fetch historical weather data from Open-Meteo API (monthly chunks)."""

    print(f"Fetching weather data from {start_date} to {end_date}...")

    start_dt = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=ZoneInfo(config.timezone))
    end_dt = datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=ZoneInfo(config.timezone))

    all_data = []
    current = start_dt

    # Don't fetch future months
    now = datetime.now(ZoneInfo(config.timezone))

    while current <= end_dt:
        year = current.year
        month = current.month

        # Skip future months
        if year > now.year or (year == now.year and month > now.month):
            print(f"  Skipping {year}-{month:02d} (future)")
            current = current + timedelta(days=32)
            current = datetime(current.year, current.month, 1, tzinfo=ZoneInfo(config.timezone))
            continue

        print(f"  Fetching {year}-{month:02d}...", end=" ")

        try:
            df = fetch_monthly_weather_data(year, month, config)
            all_data.append(df)
            print(f"OK ({len(df)} records)")
        except Exception as e:
            print(f"FAILED: {e}")
            # Continue with next month instead of failing entirely
            current = current + timedelta(days=32)
            current = datetime(current.year, current.month, 1, tzinfo=ZoneInfo(config.timezone))
            continue

        # Move to next month
        current = current + timedelta(days=32)
        current = datetime(current.year, current.month, 1, tzinfo=ZoneInfo(config.timezone))

    if not all_data:
        raise ValueError("No weather data fetched")

    # Combine all months
    df = pd.concat(all_data, ignore_index=True)
    df = df.sort_values("timestamp").reset_index(drop=True)

    # Fill NaN values
    df = df.ffill().bfill()

    return df


# =============================================================================
# Solar Generation Computation
# =============================================================================

def compute_kwh_output(weather_df: pd.DataFrame, config: SolarConfig) -> pd.DataFrame:
    """Compute estimated kWh output using PVLib."""

    print("Computing solar generation with PVLib...")

    # Get location and solar position
    location = pvlib.location.Location(
        latitude=config.latitude,
        longitude=config.longitude,
        tz=config.timezone,
        altitude=config.altitude,
    )

    # Create datetime index with proper timezone
    weather_df = weather_df.copy()
    weather_df = weather_df.set_index("timestamp")

    # Get solar position for each timestamp
    solar_position = location.get_solarposition(weather_df.index)

    # Calculate POA (Plane of Array) irradiance using actual DNI/DHI
    dni = weather_df["direct_radiation"].clip(lower=0)
    dhi = weather_df["diffuse_radiation"].clip(lower=0)
    ghi = weather_df["GHI"].clip(lower=0)

    # Extraterrestrial radiation
    dni_extra = pvlib.irradiance.get_extra_radiation(weather_df.index)

    poa_irrad = pvlib.irradiance.get_total_irradiance(
        surface_tilt=config.panel_tilt,
        surface_azimuth=config.panel_azimuth,
        solar_zenith=solar_position["apparent_zenith"],
        solar_azimuth=solar_position["azimuth"],
        dni=dni,
        ghi=ghi,
        dhi=dhi,
        dni_extra=dni_extra,
        model="haydavies",
    )

    # Use POA global irradiance for calculations
    poa_global = poa_irrad["poa_global"].fillna(0).clip(lower=0)

    # Calculate temperature-corrected efficiency
    temp_model = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS["sapm"]["open_rack_glass_glass"]
    cell_temp = pvlib.temperature.sapm_cell(
        poa_global=poa_global,
        temp_air=weather_df["temperature"],
        wind_speed=weather_df["wind_speed"],
        a=temp_model["a"],
        b=temp_model["b"],
        deltaT=temp_model["deltaT"],
    )

    # Calculate DC power with temperature correction
    gamma_pdc = config.gamma_pdc
    efficiency_correction = 1 + gamma_pdc * (cell_temp - 25)

    # DC power (kW)
    dc_power_kw = config.total_capacity_kw * (poa_global / 1000) * efficiency_correction
    dc_power_kw = dc_power_kw.clip(lower=0)

    # AC power (kW) with inverter efficiency
    ac_power_kw = dc_power_kw * config.inverter_efficiency

    # Apply soiling factor
    ac_power_kw = ac_power_kw * config.soiling_factor

    # Energy (kWh) - hourly data means each interval is 1 hour
    kwh_output = ac_power_kw

    # Add kWh to dataframe
    weather_df = weather_df.reset_index()
    weather_df["kWh_output"] = kwh_output.values

    return weather_df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add hour_of_day and day_of_year columns."""

    df = df.copy()
    df["hour_of_day"] = df["timestamp"].dt.hour
    df["day_of_year"] = df["timestamp"].dt.dayofyear

    return df


def save_to_csv(df: pd.DataFrame, output_path: str) -> None:
    """Save results to CSV with specified columns."""

    columns = [
        "timestamp",
        "GHI",
        "direct_radiation",
        "diffuse_radiation",
        "temperature",
        "cloud_cover",
        "humidity",
        "wind_speed",
        "hour_of_day",
        "day_of_year",
        "kWh_output",
    ]

    df[columns].to_csv(output_path, index=False)
    print(f"Saved {len(df)} rows to {output_path}")


# =============================================================================
# Main Pipeline
# =============================================================================

def run_pipeline(config: SolarConfig, output_path: str = "solar_yield_output.csv") -> pd.DataFrame:
    """Run the complete solar yield pipeline."""

    print("=" * 60)
    print("Solar Yield Data Pipeline")
    print("=" * 60)

    # Calculate date range (past 12 months)
    end_date = datetime.now(ZoneInfo(config.timezone))
    start_date = end_date - timedelta(days=365)

    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    print(f"Location: Singapore ({config.latitude}, {config.longitude})")
    print(f"System: {config.system_capacity_kw}kW, {config.panel_tilt}° tilt, south-facing")
    print(f"Total capacity: {config.total_capacity_kw:.1f} kW")
    print()

    # Step 1: Fetch weather data
    weather_df = fetch_weather_data(start_str, end_str, config)
    print(f"Fetched {len(weather_df)} hourly records")

    # Step 2: Validate weather data
    print("Validating weather data...")
    try:
        validate_weather_data(weather_df, config)
        print("  Weather data validation passed")
    except ValidationError as e:
        print(f"  WARNING: {e}")

    # Step 3: Compute kWh output
    result_df = compute_kwh_output(weather_df, config)

    # Step 4: Validate kWh output
    print("Validating kWh output...")
    try:
        validate_kwh_output(result_df, config)
        print("  kWh output validation passed")
    except ValidationError as e:
        print(f"  WARNING: {e}")

    # Step 5: Add time features
    result_df = add_time_features(result_df)

    # Step 6: Save to CSV
    save_to_csv(result_df, output_path)

    # Print summary statistics
    print()
    print("=" * 60)
    print("Summary Statistics")
    print("=" * 60)
    print(f"Total records: {len(result_df):,}")
    print(f"Date range: {result_df['timestamp'].min()} to {result_df['timestamp'].max()}")
    print(f"Total kWh generated: {result_df['kWh_output'].sum():,.2f} kWh")
    print(f"Average hourly output: {result_df['kWh_output'].mean():.2f} kWh")
    print(f"Capacity factor: {(result_df['kWh_output'].mean() / config.system_capacity_kw) * 100:.1f}%")
    print(f"Peak output: {result_df['kWh_output'].max():.2f} kWh")
    print()

    return result_df


def main():
    """Main entry point."""

    # Singapore 5MW configuration (already set as default)
    config = SolarConfig()

    run_pipeline(config)


if __name__ == "__main__":
    main()
