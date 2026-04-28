# CONNECTION: PVLib is the floor, ML is the signal

**What**: PVLib computes the physics-predicted yield (the maximum possible given weather). The residual (actual − predicted) is where ML provides value — it captures unmodeled factors (soiling, degradation, inverter inefficiency, shading).

**Why non-obvious**: Many solar ML projects try to predict yield directly (PVLib + ML as a combined model), which means the ML has to first undo PVLib's physics before adding signal. The correct architecture is: use PVLib as a fixed floor, then train ML on the residual.

**Implication**: Anomaly detection (flag days where actual << PVLib prediction) is the highest-value, lowest-risk ML feature. No model training required — just statistical thresholds on the residual.

**This insight reframes the MVP**: Build PVLib pipeline → compute daily residuals → flag anomalies → surface in dashboard. This is the minimum defensible ML product.
