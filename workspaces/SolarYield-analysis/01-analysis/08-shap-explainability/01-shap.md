# 3. SHAP EXPLAINABILITY

## Score: 4 / 10

---

## 3.1 Which Features Will Dominate SHAP Values in Singapore?

**Expected dominant features** (by decreasing importance):

1. **GHI** — The single strongest predictor. SHAP dominance: 40–55% of total explainability. Clear physical intuition: more irradiance → more power.

2. **Cloud cover** — Second strongest. In Singapore's humid tropical climate, cloud cover is the primary day-to-day variability driver (not seasonal variation). SHAP dominance: 15–25%.

3. **Hour of day** — Strong non-linear effect. SHAP shows bell curve centred on solar noon. SHAP dominance: 8–12%.

4. **Temperature** — Non-linear (efficiency degrades above 25°C). SHAP dominance: 5–10%.

5. **DNI** — Only when sky is clear; zero at night. Sparse but high-impact when non-zero. SHAP dominance: 3–8%.

6. **Humidity** — Affects panel efficiency and atmospheric clarity. Secondary. SHAP dominance: 2–5%.

**Less important**: Wind speed, day of year (Singapore has minimal seasonal solar angle variation).

---

## 3.2 Presenting SHAP to a Non-Technical Solar Farm Operator

**Analogy to use**: "Like a doctor reading a patient's vital signs — each feature contributes to the overall 'health score' of your solar output."

**Dashboard presentation approach**:

```
┌─────────────────────────────────────────────────────┐
│  WHY DID YOUR SYSTEM PRODUCE 3,240 kWh TODAY?     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  GHI was HIGH         ████████████████████ +620 kWh  │
│  Cloud cover was LOW  ████████████████    +280 kWh  │
│  It was 2PM          ██████████████      +190 kWh  │
│  Temperature was HIGH ████████            -120 kWh  │
│  ─────────────────────────────────────────────────  │
│  PREDICTED: 4,210 kWh   ACTUAL: 4,180 kWh          │
│  ▲ 0.7% below prediction (within normal range)     │
└─────────────────────────────────────────────────────┘
```

**Key design principles for operator presentation**:

- Always show direction: "+" means helped output, "−" means hurt output
- Use absolute kWh, not normalised units — operators think in MWh/kWh
- Keep to top 4–5 features — more is cognitive overload
- Show comparison to prediction, not raw model output

**SHAP waterfall for daily anomaly explanation**:

- When a day is anomalous, show: which features caused the deviation
- "Your yield was 800 kWh below prediction because: cloud cover was 40% higher than forecasted (+500 kWh difference) and GHI was 15% below model average"

---

## 3.3 Explainability Requirements for Enterprise Compliance (ISO 42001)

**ISO 42001 (AI Management System) — relevant sections**:

- **Section 7.2.4**: Organisations must document how AI systems make decisions that affect individuals — solar operators are not individuals, but enterprise contracts may require this
- **Section 9.4**: Must monitor AI system outputs and flag anomalous decisions
- **Section 10.2**: Must provide meaningful explanations for AI-influenced outcomes

**What this means for SolarYield**:

1. **Model cards**: Required. Must document: training data period, model architecture, performance metrics, known failure modes, intended use.

2. **Decision logging**: Every prediction must be logged with: timestamp, input features, prediction output, SHAP explanation.

3. **Anomaly explanation**: When yield deviates >2σ from prediction, the system must explain WHY — which weather variable caused it.

4. **Audit trail**: Model updates must be versioned. If a model is retrained, the previous version's predictions remain explainable by the old SHAP values.

5. **Human-in-the-loop threshold**: For yield reports used in financial contracts, a human must review and sign off on any prediction used for bank reporting.

**Currently implemented**: None of the above. The pipeline has no logging, no model cards, no SHAP integration.

---

## Gaps Summary

**Build tasks to close to 10/10**:

1. Integrate SHAP (`shap.TreeExplainer`) into pipeline output
2. Build daily SHAP summary dashboard (top 4 features per day)
3. Build anomaly SHAP waterfall (why was today anomalous?)
4. Generate model card (model version, training period, performance metrics, known limitations)
5. Implement decision logging (append predictions + SHAP to a log table)
6. Document ISO 42001 compliance path with legal review
