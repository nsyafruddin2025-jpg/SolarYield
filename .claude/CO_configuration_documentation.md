# SolarYield — CO Configuration Documentation

## How We Configured Cognitive Orchestration for This Project

### Agents Used

**analyst.md** — Used during /analyze sessions to pressure-test our
problem framing, validate market sizing, and challenge assumptions about
the Singapore solar market. Specifically used to debate whether to target
C&I building owners vs large-scale farm operators.

**ml-specialist.md** — Used to validate GradientBoosting model selection
over XGBoost (OpenMP dependency issue on Mac M-series), LSTM (data
requirements), and Linear Regression (cannot capture non-linearity of
temperature coefficient effect on crystalline silicon panels).

**frontend.md** — Used to scaffold all 6 Streamlit dashboard pages,
implement the amber/navy theme, and build the Site Configuration
multi-site management interface.

**testing.md** — Used during /redteam passes to identify the kWh column
name mismatch across pages (kWh_output vs actual_kwh), the missing
joblib dependency in requirements.txt, and the Streamlit Cloud path
resolution issue.

### Commands Used and Why

**/analyze** — Run 3 times:

1. Problem framing: validated that Singapore IPM mechanism creates
   real financial consequences for forecast inaccuracy
2. Model selection: confirmed GradientBoosting outperforms Random Forest
   by 1.7% MAPE on our dataset
3. Business model: validated 3-tier SaaS pricing against competitor
   pricing (Solcast USD 2,000+/mo vs our USD 99-499/mo)

**/todos → /implement → /redteam** cycle run for each dashboard page:

- 1_Overview.py: 3 cycles to fix column name errors and chart rendering
- 4_Forecast_Explorer.py: 4 cycles including Open-Meteo API parameter
  fix and SHAP narrative generation
- 5_Site_Configuration.py: 2 cycles for slider interactivity and map
- 6_Admin_Settings.py: 1 cycle for UI layout

**/codify** — Used to capture all 10 major decisions into COC_decision_log.md

### Domain Knowledge Loaded

The following domain knowledge was provided to COC agents:

- Singapore NEMS structure and IPM mechanism (EMA documentation)
- PVLib photovoltaic physics (irradiance, temperature coefficient, panel
  degradation at 0.5%/year per IEC standard)
- Open-Meteo API schema and parameter naming conventions
- SHAP TreeExplainer integration patterns for scikit-learn GradientBoosting
- EMA solar installation data (14,625 installations, 2,093 MWp, Q4 2025)
- Raptor Maps 2025 Global Solar Report benchmarks (5.77% industry
  average underperformance)
- Singapore NEA seasonal weather patterns (Northeast Monsoon, haze season)

### Why This Configuration Gave a 3-Person Team Enterprise Capability

COC handled all implementation complexity — Python pipeline construction,
ML training code, Streamlit dashboard scaffolding, API integrations,
HTML website, and cloud deployment configuration. The team focused
exclusively on decisions that create business value: problem framing,
model selection rationale, feature engineering strategy, UI design,
pricing architecture, and go-to-market logic.

Result: A fully functional 6-page web application + public marketing
website + trained ML model (MAPE 6.1%, R² 0.9915) + cloud deployment,
built by 3 MBA students without writing production code manually.
