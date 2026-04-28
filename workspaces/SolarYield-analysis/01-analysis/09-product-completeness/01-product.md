# 4. PRODUCT COMPLETENESS

## Score: 3 / 10

---

## 4.1 What Is Missing from the 6 Screens for Production Demo?

**Current dashboard spec** (from prior analysis):

1. Overview: KPI cards + daily yield bar chart + capacity factor trend + actual vs predicted scatter
2. Data Explorer: paginated hourly table, sortable, filterable
3. Anomaly Log: table of flagged days with residual sigma

**Missing for production-ready demo**:

| Missing Feature                    | Severity | Business Impact                                                                     |
| ---------------------------------- | -------- | ----------------------------------------------------------------------------------- |
| **User authentication**            | HIGH     | Cannot share URL without exposing all data to anyone with link                      |
| **Date range picker**              | HIGH     | Cannot compare arbitrary periods — limits analysis utility                          |
| **Site selector (multi-site)**     | CRITICAL | Single site only — no fleet view                                                    |
| **Export to CSV/PDF**              | HIGH     | Operators need to share data with banks/investors                                   |
| **PDF report generation**          | HIGH     | Bankable yield reports require formal documentation                                 |
| **Alert configuration UI**         | MEDIUM   | Currently no way to set threshold without code change                               |
| **Live data indicator**            | MEDIUM   | Is this today's data or stale? Users need to know                                   |
| **Weather overlay on yield chart** | LOW      | Helps operators understand weather–yield correlation                                |
| **Peer benchmark**                 | LOW      | "Your capacity factor vs. other Singapore sites" — even fake data drives engagement |

---

## 4.2 Minimum Viable Demo for a PE Investor in 10 Minutes

**Target**: Convince a PE investor that this is a fundable solar data business in 10 minutes.

**The 10-minute demo structure**:

**Minutes 1–2: The Problem (slide or verbal)**

- Singapore solar capacity growing 40% YoY
- C&I solar operators losing S$50K–500K/year to undetected underperformance
- Current state: Excel spreadsheets + intuition + annual inspection visits
- Pain point: No visibility into daily yield vs. expectation

**Minutes 3–5: The Product (live demo, on screen)**

1. Open dashboard → show Singapore 5MW farm, past 90 days
2. Point to the capacity factor trend line → "This is what 97% of solar operators currently see"
3. Click anomaly flag → "This red dot means yesterday's yield was 2 standard deviations below physics prediction"
4. Click anomaly detail → "We think it's a soiling event — haze from Indonesian burning season"
5. Show alert email screenshot → "We sent this to the operator at 7am, before they arrived on site"

**Minutes 6–8: The Business Model (slide)**

- Revenue: S$2,000–5,000/month per site for monitoring + anomaly alerts
- Cost to serve: S$50/month (compute + Open-Meteo API)
- Customer: C&I solar operators with 1–20 sites in Singapore
- Go-to-market: Solar EPC partnerships (Sunseap, SolarNRG, Sungevity)

**Minutes 9–10: The Ask (slide)**

- Raising S$500K seed
- Use of funds: Hire 1 ML engineer + 1 sales
- Milestone: 50 paying sites in 18 months
- Traction: [would need to fill in with real data]

**Critical prerequisite**: The anomaly alert must actually fire on real data on demo day. No fake alerts. No "I'll show you what it would look like."

---

## 4.3 How the Alert System Must Work Technically

**Alert architecture**:

```
Weather API (Open-Meteo) → Pipeline runs daily at 6am
    ↓
Compute daily yield (PVLib + actual weather)
    ↓
Compare to actual meter reading (if available) OR use anomaly detection
    ↓
If residual < -2σ for 2 consecutive days → TRIGGER ALERT
    ↓
Send via:
  - Email (SMTP or SendGrid)
  - SMS (Twilio) for critical alerts
  - Slack webhook (optional, for ops team)
```

**Alert types**:

| Level        | Condition                                                | Action                       |
| ------------ | -------------------------------------------------------- | ---------------------------- |
| **Warning**  | Residual < -1.5σ for 1 day                               | Log + email daily summary    |
| **Alert**    | Residual < -2σ for 1 day                                 | Email + SMS to operator      |
| **Critical** | Residual < -3σ for 1 day OR < -2σ for 3 consecutive days | SMS to operator + escalation |

**Threshold configuration**:

- Configurable per-site (some operators want stricter thresholds)
- Stored in database, not hardcoded
- Historical threshold changes logged

**False positive management**:

- Weather forecast errors (GHI overshoot) should NOT trigger alerts
- Use weather forecast for 1-day-ahead comparison; actual meter reading for same-day
- Alert fatigue is a real risk — minimum 24h cooldown between non-critical alerts

---

## 4.4 Multi-Site Management Database Requirements

**Current state**: Single CSV file. No database.

**Multi-site schema** (minimum viable):

```sql
-- Sites table
CREATE TABLE sites (
    id UUID PRIMARY KEY,
    name TEXT,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    system_capacity_kw FLOAT NOT NULL,
    panel_tilt FLOAT NOT NULL,
    panel_azimuth FLOAT NOT NULL,
    timezone TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Daily yield aggregation
CREATE TABLE daily_yield (
    site_id UUID REFERENCES sites(id),
    date DATE,
    actual_kwh FLOAT,
    predicted_kwh FLOAT,
    residual_kwh FLOAT,
    capacity_factor FLOAT,
    is_anomaly BOOLEAN,
    anomaly_sigma FLOAT,
    PRIMARY KEY (site_id, date)
);

-- Pipeline run log (for monitoring)
CREATE TABLE pipeline_runs (
    id UUID PRIMARY KEY,
    site_id UUID REFERENCES sites(id),
    run_at TIMESTAMP DEFAULT NOW(),
    status TEXT,  -- 'success', 'failed', 'partial'
    records_processed INT,
    error_message TEXT
);
```

**Multi-site queries needed**:

- Fleet-wide capacity factor (weighted average by site capacity)
- Anomaly count across fleet in past 30 days
- Site ranking by underperformance (worst to best)
- Per-site historical yield (downloadable)

---

## Gaps Summary

**Build tasks to close to 10/10**:

1. Add user authentication (Streamlit supports auth or deploy behind auth proxy)
2. Add date range picker to dashboard
3. Implement site selector (multi-site support)
4. Add CSV/PDF export functionality
5. Build automated alert pipeline (email + SMS via Twilio/SendGrid)
6. Implement multi-site database schema (SQLite for MVP, PostgreSQL for production)
7. Build fleet overview page (all sites at a glance)
8. Add live data freshness indicator
9. Add weather overlay on yield charts
