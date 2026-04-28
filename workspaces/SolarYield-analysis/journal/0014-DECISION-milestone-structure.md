---
type: DECISION
date: 2026-04-23
created_at: 2026-04-23T00:00:00Z
author: agent
session_id: current
project: SolarYield
topic: Milestone structure chosen — M1 is dashboard, M4 is business
phase: todos
tags: [milestones, roadmap, structure]
---

# DECISION: Milestone structure chosen — M1 is dashboard MVP, M4 is business validation

**What**: Organized 29 todos into 5 milestones with clear dependency order.

**Milestone 0 (Foundation)**: Spec index only — trivial, runs first.

**Milestone 1 (Dashboard MVP)**: Pre-processing (inference + daily aggregates) → 3 dashboard pages → deploy. This is the critical path. Nothing else matters until this exists.

**Milestone 2 (SHAP + Inference + Tests)**: SHAPExplainer class, prediction logging, model card, LightGBM trio, clear-sky features, temporal CV, tests. Can parallelize with M1.

**Milestone 3 (CI/CD + Operations)**: GitHub Actions CI, daily alert cron, weekly retrain cron, Playwright E2E. Can run in parallel with M1+M2.

**Milestone 4 (Business + Sustainability)**: Customer interviews, LOI, landing page, weather abstraction, drift detection, model versioning, multi-site schema, anomaly library, Solargis benchmark. The "fundable" milestone.

**Why not ML first**: The ML model is already trained (MAPE 6.10%). The product gap is bigger than the algorithm gap. Dashboard MVP produces a shareable URL — interviews and LOIs need something to show.

**Why business interviews in M4 not M1**: Because the dashboard is a better sales tool than a slide deck. Get the dashboard live first, then use it in interviews.
