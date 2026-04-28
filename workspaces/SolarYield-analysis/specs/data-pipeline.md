# Data Pipeline Specification

## Overview

The SolarYield data pipeline fetches historical weather data from Open-Meteo API for Singapore, computes estimated kWh output using PVLib, and saves results to CSV.

## Data Flow

```
Open-Meteo Historical API
    → fetch_monthly_weather_data() [monthly chunks]
    → validate_weather_data() [physical bounds]
    → compute_kwh_output() [PVLib Haydavies transposition + NOCT cell temperature]
    → validate_kwh_output() [capacity ceiling + non-negative]
    → add_time_features() [hour_of_day, day_of_year]
    → save_to_csv() [timestamp, GHI, temperature, cloud_cover, humidity, wind_speed, hour_of_day, day_of_year, kWh_output]
```

## Weather Data Source

- **API**: Open-Meteo Archive API `https://archive-api.open-meteo.com/v1/archive`
- **Location**: Singapore (latitude: 1.3521, longitude: 103.8198, timezone: Asia/Singapore)
- **Resolution**: Hourly
- **Variables**:
  - `shortwave_radiation` → GHI (W/m²)
  - `direct_radiation` → Direct normal irradiance (W/m²)
  - `diffuse_radiation` → Diffuse horizontal irradiance (W/m²)
  - `temperature_2m` → Temperature (°C)
  - `cloud_cover` → Cloud cover (%)
  - `relative_humidity_2m` → Humidity (%)
  - `wind_speed_10m` → Wind speed (km/h)

## Fetching Strategy

- Fetches monthly chunks (avoiding API size limits)
- Skips future months (current year/month check)
- Retries failed months up to 3 times with exponential backoff (2–10s)
- Fills NaN values via forward-fill then backward-fill

## Physical Validation Bounds

| Variable          | Lower | Upper | Unit |
| ----------------- | ----- | ----- | ---- |
| GHI               | 0     | 1200  | W/m² |
| Direct radiation  | 0     | 1100  | W/m² |
| Diffuse radiation | 0     | 800   | W/m² |
| Temperature       | 20    | 45    | °C   |
| Cloud cover       | 0     | 100   | %    |
| Humidity          | 0     | 100   | %    |
| Wind speed        | 0     | 200   | km/h |

## PVLib Computation

- **Solar position**: `pvlib.location.Location` + `get_solarposition()`
- **POA irradiance**: `get_total_irradiance()` with Haydavies model
- **Cell temperature**: SAPM open-rack glass-glass model
- **DC power**: `total_capacity_kw × (poa_global / 1000) × (1 + γ_pdc × (T_cell - 25))`
- **AC power**: DC power × inverter_efficiency × soiling_factor
- **γ_pdc** (temperature coefficient): −0.004 / °C (crystalline silicon)
- **Inverter efficiency**: 0.97
- **Soiling factor**: 0.98

## System Configuration (Singapore 5MW)

| Parameter                   | Value               |
| --------------------------- | ------------------- |
| System capacity             | 5,000 kW            |
| Panel tilt                  | 20°                 |
| Panel azimuth               | 180° (south-facing) |
| Module power                | 550 W               |
| Modules per string          | 15                  |
| Strings per array           | 607                 |
| Total capacity (calculated) | 5,007.75 kW         |

## Output Schema

```csv
timestamp,GHI,temperature,cloud_cover,humidity,wind_speed,hour_of_day,day_of_year,kWh_output
2025-04-01 00:00:00,0.0,24.8,95,97,9.0,0,91,0.0
```

- `hour_of_day`: 0–23
- `day_of_year`: 1–366
- `kWh_output`: AC energy per hour (kWh), same value as AC power (kW) for hourly data

## kWh Validation Bounds

- `kWh_output >= 0` (never negative)
- `kWh_output <= system_capacity_kw` (5,000 kW ceiling per hour)

## Date Range

Past 12 months from current date. Future months are skipped automatically.

## Open Issues

- No real-time data support (batch only)
- No multi-site configuration (single hardcoded location)
- No automated scheduling — runs on demand
