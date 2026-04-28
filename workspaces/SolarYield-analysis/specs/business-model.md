# Business Model Specification

## Three Candidate Models

### Option A: SaaS Dashboard (C&I Solar Fleet Operators)

**Description**: Multi-site solar yield monitoring dashboard, subscription-based.

**Target customer**: Commercial & industrial solar farm operators with 5–50 sites
**Revenue**: $500–2,000/month per site
**Example**: Operator with 10 sites pays $10,000–20,000/month

**Value proposition**: "See all your sites at a glance. Know immediately when a panel is underperforming."

**What this requires**:

- Multi-site data model (currently single-site)
- User authentication and authorization
- Web dashboard with site-level drill-down
- Alerting and notification system
- 99.5%+ uptime SLA

**Go-to-market**: Direct sales + solar EPC channel partners

### Option B: Bankable Yield Report Service (Solar Project Finance)

**Description**: Audit-ready yield reports for banks and investors financing solar projects.

**Target customer**: Solar developers seeking project financing; banks approving solar loans
**Revenue**: $5,000–20,000 per report; annual validation: $2,000–5,000/year
**Example**: 5MW project, bank requires independent yield assessment → $15,000 report

**Value proposition**: "Bank-ready yield analysis backed by physical modeling and ML anomaly detection. Accepted by [major bank] and [major bank]."

**What this requires**:

- Methodology documentation (bank regulators want to understand the model)
- Uncertainty quantification (prediction intervals, not just point estimates)
- Independent validation / third-party audit trail
- Historical track record (past performance is predictor of future)
- Legal review of liability framework

**Go-to-market**: Direct sales to solar developers; partnership with banks' energy finance teams

**Why this may be the strongest fit**:

- Singapore's highly regulated banking sector requires documented, independently-verified yield analysis
- C&I solar developers in Singapore typically need bank financing (capital-intensive)
- Existing incumbents (Envision, DNV) charge $50K+ for reports
- A validated, lower-cost alternative could capture significant share

### Option C: API Service (Solar Data Integrators)

**Description**: API providing solar yield data for energy management systems.

**Target customer**: Energy management system (EMS) vendors, demand response aggregators, grid operators
**Revenue**: Per-MWh reported ($0.10–0.50/MWh) or per-site annual key ($1,000–5,000/year)
**Example**: EMS vendor integrating yield data for 100 sites → $50,000–500,000/year

**Value proposition**: "Plug-and-play solar yield data for your energy management system."

**What this requires**:

- REST API with proper authentication (API keys, rate limiting)
- SLAs (99.9%+ uptime)
- Real-time or near-real-time data (current pipeline is daily batch)
- Geographic expansion (Singapore → Southeast Asia)

**Go-to-market**: Self-service developer portal; integration partnerships with major EMS vendors

---

## Recommendation

**Pursue Option B first** (bankable yield reports) given:

1. Aligns with technical strength (accurate PVLib physical modeling)
2. Singapore's regulatory environment creates natural demand
3. High ticket size per report ($5K–20K) enables fast revenue
4. Lower product complexity than SaaS dashboard (no auth, no multi-site, no alerting)
5. No ML model required for initial MVP (PVLib + documentation is sufficient)

**Validated path**: Interview 3 solar developers and 2 bank energy finance teams to validate pain and willingness to pay.

---

## Unit Economics (Illustrative)

Assuming Option B (bankable reports):

| Item                          | Cost                                           |
| ----------------------------- | ---------------------------------------------- |
| Pipeline compute (daily)      | ~$0.10/day (Open-Meteo free tier, PVLib local) |
| Report generation (manual)    | 2–4 hours analyst time                         |
| Annual hosting                | ~$100/year (static hosting for report PDFs)    |
| Customer acquisition (direct) | ~$2,000 per deal (sales time)                  |

**Implied break-even**: 1 report per quarter covers costs. First paying customer makes this profitable.
