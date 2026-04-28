# 8. COMPETITIVE TECHNICAL EDGE

## Score: 3 / 10

---

## 8.1 ML Capability That Would Make SolarYield Technically Unreplicable

**The honest answer**: At the model level, nothing is unreplicable. XGBoost, PVLib, and Open-Meteo are all available to any competitor. The pipeline code is 450 lines. A well-funded competitor replicates this in 2 weeks.

**What IS hard to replicate**:

**1. The anomaly pattern library**

After 100 site-years of data, SolarYield has a library of anomalies:

- "Signature: DNI drop + humidity spike + wind from SW = Indonesian haze → 15% yield reduction for 3–7 days"
- "Signature: gradual DNI decline over 14 days + temperature spike = soiling buildup → flush panels"
- "Signature: sharp DNI drop + wind gust = dust storm → insurance claim trigger"

This library cannot be bought or built quickly. It requires: years of data + systematic anomaly tagging + domain expertise + operator feedback loops.

**How to build it**: Every anomaly detected → human review → tagged with cause → added to library. This is a systematic knowledge accumulation process.

**2. Site-specific transfer learning models**

After 12 months per customer, the fine-tuned model captures:

- Local shading patterns (nearby trees grow, buildings are constructed)
- Local soiling characteristics (nearby construction dust, agricultural burning)
- Inverter fleet-specific efficiency curves

A new entrant needs 12 months to build equivalent models for each site.

**3. Operator trust signal**

The dashboard shows: "yesterday was anomalous." Over time, the operator learns to trust or distrust the system. When SolarYield says "anomaly" and the operator confirms it ("yes, we found a faulty string"), that trust compounds. After 2 years, the operator's trust is a switching cost. This is not technical — it's relational — but it is real.

---

## 8.2 Should We Patent Any Methodology?

**Short answer: NO, for now.**

**Reasons against patenting**:

1. **Software patents are hard to enforce** — especially in Singapore and most SEA jurisdictions
2. **Patenting reveals the method** — the patent filing becomes public, letting competitors design around it
3. **The valuable IP is in data, not methods** — the anomaly library, not the specific ML algorithm
4. **Patenting takes 3–5 years** — by which time the competitive landscape has changed

**What IS worth protecting as trade secrets**:

- The anomaly pattern library (trained weights + tagged examples)
- Customer-specific model fine-tuning parameters
- The specific Optuna hyperparameter configurations for Singapore climate
- The threshold calibration methodology

**What to do instead**:

1. Document everything internally (lab notebooks, git commits)
2. Focus on speed of execution — build the moat before competitors catch up
3. If a competitor raises funding and starts copying: reassess in 18 months

**When to reconsider**: If a competitor patents the residual hybrid architecture (PVLib + XGBoost on residual) in Singapore/SEA, that could be problematic. But this architecture is described in academic literature — it's not novel.

---

## 8.3 How to Benchmark Against Solargis Publicly

**Context**: Solargis is the leading commercial solar monitoring and forecasting service. They have:

- 35+ years of solar resource data (satellite-derived)
- Global coverage (all markets SolarYield would enter)
- Institutional customers (banks, developers, utilities)
- Their Blumenstein et al. methodology is peer-reviewed

**Why benchmarking against Solargis matters for fundraising**:

- PE/institutional investors want to know: "How does SolarYield compare to the industry standard?"
- If SolarYield underperforms Solargis, the pitch is: "We're 15% cheaper and we do anomaly detection they don't."
- If SolarYield matches Solargis, the pitch is: "We're open-source-validated and 80% cheaper."

**How to do the benchmark**:

1. **Use Solargis public data portal** (limited free tier: 1 site, 1 year)
2. **Download Singapore solar data** (GHI, DNI, temperature)
3. **Run same period through SolarYield pipeline + Solargis estimates**
4. **Compute MAPE for both against actual meter data** (or against Open-Meteo reanalysis as proxy)
5. **Publish methodology on blog**: "How SolarYield compares to Solargis for Singapore C&I solar"

**What to benchmark**:

- Daily yield MAPE
- Capacity factor accuracy
- Anomaly detection precision (false positive rate)

**Important caveat**: Open-Meteo reanalysis ≠ ground truth. Any benchmark using Open-Meteo as the "actual" is flawed. The proper benchmark uses ground-level weather station data from NEA (National Environment Agency) as the reference.

---

## Gaps Summary

**Build tasks to close to 10/10**:

1. Build anomaly library: systematic tagging of every detected anomaly with cause label
2. Solargis benchmark: run same period through both pipelines, publish results
3. Weather data source abstraction layer (primary: Open-Meteo, fallback: Solcast)
4. Customer feedback loop: operator confirms/denies anomaly causes → improves library
5. Site-specific transfer learning: build fine-tuning pipeline for new customers
6. IP review: document anomaly library and model weights as trade secrets
