# 5. BUSINESS MODEL VALIDATION

## Score: 2 / 10

---

## 5.1 Is MAPE < 10% Sufficient to Avoid Grid Penalties?

**Context**: In Singapore, solar farms connecting to the grid operate under the Enhanced Central Interfacing Scheme (ECIS) or similar frameworks administered by EMA (Energy Market Authority). Grid operators can penalise underperformance if a solar farm fails to deliver committed energy.

**The MAPE threshold question**: MAPE measures prediction accuracy relative to actual output. But **grid penalties are based on meter readings, not predictions**.

The relevant metric for grid compliance is:

- **Availability**: % of time the system is capable of generating (not the prediction accuracy)
- **Curtailment compliance**: Did you deliver what you committed?

**How MAPE < 10% helps avoid penalties**:

- Accurate yield predictions enable accurate commitment schedules
- Under-commit → lost revenue. Over-commit → penalty for shortfall
- A MAPE of 8% means you can confidently commit 92% of predicted output without triggering penalties

**MAPE alone is insufficient** — grid operators care about:

1. Actual metered output vs. committed schedule (not vs. prediction)
2. System availability (inverter uptime, panel health)
3. Response time during grid events

**Verdict**: MAPE < 10% is a necessary but not sufficient condition for penalty avoidance. The product needs to track meter readings, not just predictions.

---

## 5.2 Actual Customer ROI Calculation for a Singapore Solar Farm

**Setup**: 5MW (5,000 kW) C&I solar installation in Singapore.

**Revenue parameters**:

- Grid export tariff: ~S$0.10–0.15/kWh (Energy Market Authority regulated tariff)
- Capacity factor: 6.8% (current pipeline output for Singapore)
- Annual output: 5,000 kW × 8,760 h × 6.8% = ~2,978 MWh/year
- Annual revenue: ~S$297,800–446,700/year

**The underperformance problem**:

- Industry average: solar farms operate at 85–90% of rated capacity due to soiling, degradation, inverter losses
- For a 5MW farm: effective capacity loss of 500–750 kW = S$50,000–75,000/year in lost revenue
- Detection problem: without monitoring, operators don't know which days they're underperforming

**ROI calculation for SolarYield**:

| Item                               | Cost                 |
| ---------------------------------- | -------------------- |
| SolarYield subscription            | S$2,000–5,000/month  |
| Hardware: meter/logger (if needed) | S$5,000 one-time     |
| Annual cost                        | S$24,000–60,000/year |

**Value delivered**:

- Assume SolarYield detects 5 days/year of severe underperformance (e.g., inverter issue)
- Recovery: 5 days × 5MW × 8h × S$0.125/kWh = S$2,500/recovery event
- If 4 recovery events/year: S$10,000 in recovered revenue
- Plus: reduced insurance premiums (documented monitoring), better bank financing terms

**ROI**: Break-even is marginal. The real value is risk reduction and bank financing terms improvement, not direct revenue recovery. This needs customer validation.

---

## 5.3 Which Customer Segment in Singapore First and Why

**Three candidate segments**:

| Segment              | Description                   | Appetite | Decision Speed      |
| -------------------- | ----------------------------- | -------- | ------------------- |
| **C&I rooftop**      | 100kW–1MW commercial rooftops | Medium   | Slow (2–6 months)   |
| **C&I ground mount** | 1–10MW ground-mount farms     | High     | Medium (1–3 months) |
| **Utilities / EMA**  | >10MW utility scale           | Low      | Slow (6–12 months)  |

**Recommended first target: C&I ground-mount, 1–5MW**

**Why**:

1. Highest pain: ground-mount farms have highest capital at stake and longest payback period
2. Decision-maker access: typically the property owner or MD, not a facilities manager
3. Regulatory pressure: EMA requires performance reporting for farms >1MW
4. Budget authority: S$2,000–5,000/month is <0.1% of annual revenue for a 5MW farm
5. Singapore has many C&I solar farms in this range (JTC, Sembcorp,Keppel)

**Second target: large commercial rooftops** (1MW+)

- Easier to access (building owner)
- Shorter decision cycle
- Less regulatory reporting burden

**Avoid initially**: Residential rooftop (<10kW) — too small a ticket, too fragmented.

---

## 5.4 How to Validate Willingness to Pay Before Building

**The correct sequence**:

**Step 1: Interview, not build** (Week 1–2)

- Find 5 Singapore solar farm operators (LinkedIn outreach: "solar yield" + "Singapore")
- Ask: "Walk me through how you know if your farm underperformed last month."
- Document the current process (manual meter reading? SCADA? Excel?)
- Ask: "If I could tell you on the morning of Day 2 that Day 1 had an anomaly, what would that be worth to you?"
- Ask: "What would you pay for that?" Write down the number.

**Step 2: Landing page + waitlist** (Week 2–3)

- Build a 1-page landing page describing the product (not the code)
- "SolarYield: know when your solar farm underperforms before your bank does."
- Capture: company name, email, number of sites, current monitoring method
- Target: 20 signups from Singapore solar operators
- Conversion rate validates interest: >10% = strong signal, <5% = weak signal

**Step 3: Letter of Intent before building** (Week 3–4)

- For interested companies: offer a "Founding Member" spot
- Pre-pay 6 months at S$1,000/month (discounted) in exchange for early access
- LOI with "cancel anytime" — no legal commitment
- 3 signed LOIs = validated willingness to pay

**The key validation metric**: Did someone give you money? Not "would you use this?" — that's worthless. Did they pay a deposit?

---

## Gaps Summary

**Build tasks to close to 10/10**:

1. Conduct 5 customer discovery interviews (document answers to specific questions above)
2. Build landing page with waitlist (Webflow, Carrd, or Streamlit)
3. Get 3 signed LOIs or deposits (validated willingness to pay)
4. Implement meter reading integration (API from inverter/SCADA, not just weather-based estimation)
5. Calculate and document actual customer ROI with real Singapore solar farm parameters
