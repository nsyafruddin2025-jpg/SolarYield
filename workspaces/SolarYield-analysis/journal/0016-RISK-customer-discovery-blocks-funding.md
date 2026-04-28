---
type: RISK
date: 2026-04-23
created_at: 2026-04-23T00:00:00Z
author: agent
session_id: current
project: SolarYield
topic: Customer discovery is the critical path blocker
phase: todos
tags: [customer-discovery, risk, business-model]
---

# RISK: Customer discovery is the critical path blocker

**Risk**: Todo 24 (5 customer discovery interviews) is in M4, scheduled after dashboard deployment. But if the interviews reveal the problem is different from assumed, the dashboard and ML work may be invalidated.

**Why this matters**: The project has been built for 3+ sessions with zero customer input. The entire technical architecture is based on assumptions about what solar farm operators need. If those assumptions are wrong, everything built to date is wrong.

**Origin**: Journal entry 0002-GAP-unvalidated-problem identified this as CRITICAL.

**Current mitigation**: Dashboard is built first to have something concrete to show during interviews. This is reasonable but doesn't eliminate the risk.

**Recommended approach**: Start interviews as soon as the dashboard has a URL (M1 done). Don't wait for M4. Move todo 24 to M1 or run it in parallel with M1.

**What interviews could change**:

- Target segment: C&I ground-mount (assumed) vs rooftop (different needs)
- Business model: bankable reports (assumed) vs SaaS dashboard (different product)
- Willingness to pay: could be much lower or higher than $5K-20K per report
- Decision-maker: operator vs bank vs EPC — completely different sales motion

**Risk level**: HIGH — could invalidate entire product direction.
