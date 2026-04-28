# DISCOVERY: Open-Meteo uses reanalysis, not ground truth

**What**: The irradiance data (GHI, DNI, DHI) from Open-Meteo Archive API is not measured ground truth — it is ERA5 reanalysis output (ECMWF atmospheric model). Ground station measurements are not used.

**Why this matters**: ERA5 has known systematic biases in tropical regions:

- Tends to underestimate extreme DNI on clear-sky days (strikes ~50–100 W/m² from true)
- Tends to overestimate DHI on partly-cloudy days (cloud parameterisation in tropics is unreliable)
- This biases the XGBoost model toward reanalysis error patterns, not physical reality

**For the investor story**: The data quality is sufficient for anomaly detection (relative comparisons day-to-day) but NOT sufficient for bankable yield certification (which requires ground station data).

**Mitigation**: Either source ground truth from NEA weather stations (Singapore) or note the limitation in any financial disclosures.

**Origin**: Stanford solar resource assessment methodology; validated against NREL MIDC network protocols.
