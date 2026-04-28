# 7. 10-YEAR SUSTAINABILITY

## Score: 2 / 10

---

## 7.1 Data Moat Strategy — When Does It Become Defensible?

**The data moat question**: Can a well-funded competitor replicate SolarYield by simply buying Open-Meteo data and PVLib?

**Honest answer**: NO, not with current architecture. Open-Meteo is free. PVLib is open-source. The pipeline is 450 lines of Python. Any competent ML engineer replicates this in 2 weeks.

**What WOULD create a defensible moat**:

**Moat 1: Customer-specific model fine-tuning** (becomes defensible after ~20 customers)

- Each customer site has unique soiling patterns, shading, and inverter efficiency curves
- After 12 months per customer, the fine-tuned model captures site-specific physics
- A new entrant would need 12 months of data from each customer site to match this
- This is a TIME moat, not a technical moat
- Requires: per-customer ML pipelines with transfer learning

**Moat 2: Anomaly library** (accumulates defensibly after ~50 sites × 2 years)

- Over time, SolarYield accumulates a library of known anomaly patterns:
  - "This DNI + cloud cover + humidity signature = Indonesian haze event"
  - "This temperature + wind pattern = Saharan dust intrusion"
- New entrants start with zero anomaly library
- Operators value this institutional knowledge — it's the difference between "your farm underperformed" and "your farm underperformed because of haze from Indonesian burning season"
- **This is the most valuable moat and cannot be replicated without years of data**

**Moat 3: Meter/inverter integration depth** (becomes defensible after ~10 integrations)

- Deep integration with specific inverter brands (Huawei, Sungrow, SMA) captures proprietary performance data
- E.g., Huawei FusionSolar API provides inverter-level efficiency curves
- A new entrant has no equivalent integration depth

**When does the moat become real?**

- At 10 customers: nascent, easily replicable
- At 30 customers + 2 years: decent, requires 2 years to replicate
- At 100 customers + 3 years: strong — anomaly library is substantial
- At 500 customers + 5 years: very strong — data network effects compound

---

## 7.2 Geographic Expansion After Singapore

**Recommended order**:

**Phase 1 (Year 1–2): Southeast Asia**

- Malaysia (highest priority — most similar climate, large C&I market)
- Indonesia (Java — most industrialised, 2nd largest solar market in SEA)
- Thailand (strong regulatory framework, growing solar)

**Why Malaysia first**:

- Climate almost identical to Singapore (latitude 1–7°N)
- Same ASEAN regulatory framework (less advanced but harmonised)
- No local solar monitoring incumbents
- Large C&I solar market (palm oil estates converting to agrivoltaics)

**Phase 2 (Year 2–4): South Asia + Pacific**

- Philippines (strong growth, but typhoon risk requires model adaptation)
- Vietnam (fastest growing solar market in SEA)
- Australia (mature market, sophisticated buyers, but winter/summer seasonality)

**Phase 3 (Year 4+): MENA and Latin America**

- These markets have different climate regimes (desert, tropical)
- Would require model retraining from scratch
- Larger markets but lower strategic value for SEA-native operators

---

## 7.3 Biggest Technical Risk That Could Kill the Business in Year 3

**The inverter data integration trap**:

The most dangerous path is betting on inverter API integrations. Here's why:

1. **Every inverter vendor has a proprietary API**. Huawei FusionSolar, Sungrow, SMA, SolarEdge — all different.
2. **APIs change without notice**. Huawei restructured their API in 2023, breaking many third-party integrations.
3. **Some APIs require cloud-only access** (data goes to China's servers — not acceptable for Singapore government sites).
4. **Some APIs have rate limits** incompatible with daily polling.
5. **Fleet heterogeneity**: Most operators have 3–4 different inverter brands. Full coverage requires 4 integrations.

**What to do instead**: Weather-based estimation as the primary data source, inverter API as optional enrichment. Never depend on inverter APIs for the core product.

**The second biggest risk: single-point-of-failure weather data source**

Open-Meteo is free and reliable, but:

- Their API changed parameter names in 2024 (direct_radiation vs direct_normal_radiation)
- They could introduce rate limits or a paywall
- Alternative: Solcast (paid, more reliable) or ECMWF CAMS (free but complex)

**Mitigation**: Build an abstraction layer for weather data sources. If Open-Meteo fails, fall back to Solcast automatically.

---

## 7.4 How the Model Degrades Over Time — and How to Prevent It

**Model degradation mechanisms**:

**Drift type 1: Climate drift** (slow, measurable)

- Singapore's climate is relatively stable
- El Niño events cause ±10% annual yield variation
- No climate change risk in 10-year horizon for Singapore specifically

**Drift type 2: Equipment degradation** (slow, predictable)

- Solar panels degrade at 0.5–1% per year
- Inverters degrade faster: 2–3% per year
- A model trained on Year 1 data will overestimate yield in Year 3

**Drift type 3: Weather pattern shift** (medium, measurable)

- Global haze patterns changing due to Indonesian deforestation policy
- Urban heat island effect increasing around installations
- Measurable via: clear-sky ratio trend over time

**Drift type 4: Data source drift** (fast, abrupt)

- Open-Meteo API changes → data distribution changes
- Satellite orbit changes → irradiance values shift
- Measurable via: sudden jump in prediction residual mean

**Prevention strategy**:

```
Monthly: Compute rolling 30-day MAPE vs. prior 30-day MAPE
    If drift > 5% → trigger alert (human reviews)
    If drift > 15% → automatic model retrain triggered

Annual: Full model retrain on all available data
    - New Optuna hyperparameter search
    - Updated training set includes all historical data
    - New model deployed alongside old (shadow mode)
    - If shadow MAPE < production MAPE → swap
```

**The most important degradation signal to track**: `clear_sky_ratio` trend over time. If clear_sky_ratio is stable but predictions drift, the model is degrading. If clear_sky_ratio is declining, the physical plant is degrading.

---

## Gaps Summary

**Build tasks to close to 10/10**:

1. Weather data source abstraction layer (primary: Open-Meteo, fallback: Solcast)
2. Model versioning with shadow deployment
3. MAPE drift detection pipeline (monthly check + alert)
4. Annual model retrain pipeline
5. Multi-inverter integration strategy (abstraction layer, never depend on single vendor)
6. Anomaly library: document and tag every detected anomaly
7. Multi-region expansion plan (Malaysia → Thailand → Vietnam)
