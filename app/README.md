# SolarYield Dashboard — Deployment

## Local Development

```bash
cd app
uv sync
uv run streamlit run dashboard.py --server.port 8501
```

## Deploy to Streamlit Cloud (free)

1. Push this repository to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your GitHub repository
4. Set:
   - **Repository**: `your-username/SolarYield`
   - **Branch**: `main`
   - **Main file path**: `app/dashboard.py`
   - **App URL**: choose a subdomain (e.g., `solaryield`)
5. Click **Deploy**

Streamlit Cloud will automatically install dependencies from `app/requirements.txt`.

## Data Files

The dashboard loads two CSV files:

| File                      | Location     | Description                         |
| ------------------------- | ------------ | ----------------------------------- |
| `data/enriched_daily.csv` | Project root | Daily aggregates with anomaly flags |
| `solar_yield_output.csv`  | Project root | Hourly raw weather + yield data     |

For Streamlit Cloud deployment, these files must be in the repository root (they are).

## Requirements

```
streamlit>=1.40.0
pandas>=2.0.0
plotly>=5.0.0
```

## Configuration

No API keys required. The dashboard is fully static.

## Multi-page Navigation

The app uses Streamlit's multipage structure:

- `dashboard.py` — entry point
- `pages/1_Overview.py` — KPI cards + 3 charts
- `pages/2_Data_Explorer.py` — hourly data table
- `pages/3_Anomaly_Log.py` — anomalous days log
