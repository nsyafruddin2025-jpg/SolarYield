# Product & Demo Assessment (30%)

## Score: 3 / 10

## Evidence

### What exists

- `solar_pipeline.py` — a Python data pipeline that runs end-to-end
- `solar_yield_output.csv` — 8,760 hourly records with kWh output
- Physical validation (temperature bounds, GHI bounds, kWh ceiling)
- Retry logic (Tenacity exponential backoff)
- Configuration dataclass — partially parameterised

### What is missing

- **No user interface**: No dashboard, no web app, no API endpoint, no CLI
- **No visualization**: No charts of daily/monthly yield, capacity factor trends, or weather correlations
- **No product demo**: Cannot show to a prospective customer — it's a script that runs in a terminal
- **No delivery mechanism**: CSV on a laptop is not a product
- **No multi-site support**: Hardcoded Singapore coordinates — cannot compare multiple farms
- **No alerting/thresholds**: No way to flag anomalously low production days
- **No sharing mechanism**: Results exist only as a CSV file
- **No API**: No way for a customer or partner system to consume yield data programmatically
- **No mobile view**: Operations staff cannot check yield from the field

## Single Biggest Gap

**No shareable product artifact.** A solar farm operator cannot use `solar_pipeline.py`. They need: a dashboard showing their fleet's yield, anomaly alerts, and a way to share reports with investors or grid operators. The CSV output is an internal data artifact, not a product. The moment someone else needs to see the data, the current approach breaks down.

## What a Minimum Viable Product Demo Looks Like

A web dashboard showing:

1. Total yield (MWh) for the past 30 days
2. Capacity factor trend line
3. Today's actual vs. weather-adjusted expected yield
4. Alert banner if capacity factor drops below a threshold (e.g., <5%)

Without this, the "product" is a Python script — compelling only to other developers, not to solar farm operators or investors.
