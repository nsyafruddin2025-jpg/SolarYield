# SolarYield COC Decision Log
Team Project | MGMT 655 | SMU MBA 2024/2025

---

## Decision 1: Data Pipeline Design
Date: April 2025
Options considered: GHI only vs GHI + DNI/DHI
Decision: Use actual DNI/DHI from Open-Meteo direct parameters
Reason: GHI alone introduces systematic error in PVLib, not just noise. 
Affects MAPE directly. AI recommendation accepted after review.
Deferred: Loss factors (Phase 2), structured logging (Phase 2)

---

## Decision 2: DNI/DHI Fix Impact Validation
Date: April 2025
Before: 1,678,525 kWh total (GHI used as DNI - incorrect)
After: 2,991,171 kWh total (actual DNI/DHI from Open-Meteo)
Decision: Accept new numbers as ground truth for model training
Reason: Lower peak output (3,331 kWh vs 4,835 kWh) is physically 
realistic. Original model was overestimating due to incorrect 
irradiance inputs.

---

## Decision 3: Redteam Triage
Date: April 2025
Fix now: DNI/DHI fetch, retry backoff, output validation, parameterize config
Defer: Loss factors, structured logging
Reason: Deferred items do not affect MVP accuracy or demo reliability.
Customer impact of fixing them is low at this stage.

---