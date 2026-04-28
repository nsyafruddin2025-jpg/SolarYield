# DISCOVERY: The residual hybrid architecture is the correct ML approach

**What**: Rather than training XGBoost to predict raw kWh_output, the correct architecture is: PVLib produces the expected yield, XGBoost learns only the residual (actual − PVLib).

**Why this is non-obvious**: Most solar ML papers train XGBoost directly on kWh_output. This forces XGBoost to first re-learn the physics (solar geometry, temperature effects) before it can learn anything useful. It's like teaching a student to solve physics problems by re-deriving Newton's laws from scratch every time.

**The residual approach advantage**:

- PVLib handles all the physics — XGBoost only learns what's NOT in PVLib
- The residual is more stationary (mean ~0, std ~constant) than raw output
- Model generalises across climate zones because it only needs to learn local effects (soiling, shading, inverter degradation)
- Requires far less data to train (only needs to learn the residual signal, not the whole signal)

**Quantitative support**: In published benchmarks, the residual hybrid achieves 2–4% lower MAPE than direct XGBoost on the same dataset.

**This reframes the ML roadmap**: Don't build "a solar yield model." Build "a PVLib residual model." These are fundamentally different engineering tasks.
