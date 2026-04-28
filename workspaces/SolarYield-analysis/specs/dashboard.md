# Dashboard Specification (MVP)

## Purpose

A shareable web artifact that converts "a script on a laptop" into "a product a prospective customer can interact with."

## Tech Stack

**Streamlit** (recommended for Python-first team):

- Fastest path from Python to deployed web app
- Native support for pandas dataframes and charts
- One-file deployment
- Free hosting on Streamlit Cloud (or Railway/Render for custom domain)

**Alternative**: Flask/FastAPI + HTML/JS (if custom styling needed)

## MVP Dashboard Pages

### Page 1: Overview (Home)

**Header**: "SolarYield — Singapore Solar Farm"

**KPI Cards** (top row):

1. Total MWh (past 30 days) — large number
2. Average Capacity Factor (%) — with trend arrow vs prior 30 days
3. Number of anomaly days (yield < 2σ below physics)
4. Peak output (kWh) — past 30 days

**Chart 1**: Daily yield (MWh/day) — past 30 days, bar chart

**Chart 2**: Capacity factor trend — line chart, daily, past 90 days

**Chart 3**: Actual vs. physics-predicted yield scatter — past 30 days, with anomaly days highlighted in red

### Page 2: Data Explorer

**Table**: Paginated hourly data (last 7 days default)

- Columns: timestamp, GHI, temperature, cloud_cover, kWh_output, anomaly_flag
- Sortable by any column
- Filterable by date range

### Page 3: Anomaly Log

**Table**: Days flagged as anomalous

- Columns: date, actual*kWh, predicted_kWh, residual_kWh, residual*σ
- Sorted by most anomalous first

**Explanation text**: "Anomaly detection flags days where actual yield was more than 2 standard deviations below physics-predicted yield. Common causes: panel soiling, inverter failure, shading, or weather sensor errors."

## Data Source

For MVP: Static CSV file loaded from repository (`solar_yield_output.csv`).

For production: Python pipeline output stored in cloud storage (S3/GCS) or database.

## Deployment

1. Package Streamlit app as single Python file
2. Deploy to Streamlit Cloud (free, connects to GitHub)
3. Or deploy to Railway/Render (~$5/month, custom domain)

## Not in MVP

- User authentication (public dashboard is fine for demo)
- Multi-site support (single site only)
- Export to PDF (future: bankable report generation)
- Real-time data (daily batch is sufficient for demo)

## Success Criteria

A prospective customer can:

1. Open the URL
2. See the 4 KPI cards
3. Understand the capacity factor trend
4. See which days were anomalous
5. Form a hypothesis about what caused the anomalies

If a customer can do all five in under 2 minutes without assistance, the demo is successful.
