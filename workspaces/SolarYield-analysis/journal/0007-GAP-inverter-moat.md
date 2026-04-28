# GAP: Inverter API integration is a moat trap

**What**: Deepening inverter API integrations (Huawei FusionSolar, Sungrow, SMA) is technically appealing but creates long-term fragility.

**Why it is a trap**: Each inverter vendor has proprietary APIs, no two are the same, all change without notice. A competitor (Envision Digital) has already done this work and has 500+ inverter integrations. Building another 500 integrations is not a defensible strategy.

**The right strategy**: Use weather-based estimation as the primary data source. This is:

- Free (Open-Meteo)
- Universal (works for any inverter, any location)
- Not dependent on vendor API stability

**Inverter integration as optional enrichment only**: If a customer already has SCADA/inverter API access and wants to contribute that data, accept it. But never depend on it for the core product.

**This is a strategic design decision, not a technical one**: The product architecture should be designed so that the core product never calls a single inverter API.
