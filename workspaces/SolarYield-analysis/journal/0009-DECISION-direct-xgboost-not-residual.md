# DECISION: Direct XGBoost training on kWh_output (not residual hybrid)

**What**: User explicitly requested direct XGBoost on kWh_output target, not the residual hybrid (PVLib → residual → XGBoost).

**Why this deviates from spec**: `specs/ml-model.md` specifies the residual hybrid as the recommended architecture. The residual hybrid has better theoretical grounding (PVLib handles physics, XGBoost learns only the residual). However, the user's explicit request overrides the spec recommendation.

**Scope decision**: The residual hybrid requires computing daily PVLib predictions first. For the current scope (direct XGBoost comparison with Random Forest baseline), the residual approach adds complexity not requested. Future todo should upgrade to residual hybrid.

**What this means for MAPE**: Direct XGBoost will learn both physics + residual effects. MAPE may be slightly higher than residual hybrid (published: 2–4% higher). With 1 year of data, MAPE of 9–14% is expected for direct approach.
