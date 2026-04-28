# DISCOVERY: Singapore solar irradiance has near-zero autocorrelation

**What**: Hourly GHI autocorrelation at lag-24 in Singapore is below 0.1 — essentially random.

**Why this matters**: This is the quantitative basis for rejecting LSTM and other recurrent architectures. LSTM's strength is learning sequential dependencies; when those dependencies don't exist (near-random), LSTM provides no benefit over simpler models while adding significant complexity (sequence length, gradient clipping, hyperparameter tuning).

**Implication**: Tree-based models (XGBoost, Random Forest) are the appropriate architecture for this data. Feature engineering (cyclical hour/day encoding, weather variables) matters more than model sophistication.

**How discovered**: Prior analysis session — GHI time series inspection for Singapore location.
