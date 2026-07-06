# 12 — Score Policy & Demo Personas (LOCKED Jul 06)

Single source of truth for the numbers. Datagen, engine, UI, script, and deck all quote THESE values — any change happens here first.

## Dimension weights (config-driven; shown in UI)
Cash-Flow Strength **30%** · Compliance Discipline **20%** · Obligation Load **20%** · Growth Trajectory **15%** · Business Stability **15%**.
Defense: a credit memo's question order — can they repay (30), are they disciplined (20), how burdened already (20); growth/stability modulate.

## Bands, multipliers, action gates (300–900 scale)

| Band | Range | Band multiplier (× Nayak ceiling = 20% of annual turnover) | RM action gate |
|---|---|---|---|
| **Prime** | 780–900 | 100% | Pre-qualified lead; straight-through to sanction prep |
| **Good** | 720–779 | 80% | Sanctionable, standard checks |
| **Watch** | 600–719 | 60% | Manual review; MSME side pushes improvement path |
| **Weak** | 480–599 | 30% | Not now — coaching mode, re-assess 90 days |
| **Critical** | 300–479 | 0% | Existing borrower → Parakh Watch alert; new → decline + rehab path |

- **Confidence-conservative rule (AMENDED Jul 06 night — ⚠️ pending JR confirm):** at **Low** confidence (±60), eligibility is banded at the lower edge (score − 60); at High/Medium the **point band** applies and the ± range is always displayed. *Why amended: the original strict lower-edge rule contradicted this doc's own canonical numbers — 720 − 35 = 685 = still Watch, which would have made Meena's +₹3.8L moment +₹0. The amendment preserves every canonical number, keeps confidence consequential (kill a source → Low → the limit visibly drops — a better kill-switch beat), and matches how the worked example below was always computed.*
- Multipliers apply everywhere (today's readiness meter AND Kal-Parakh projections) — they are band properties, not simulator properties.
- Everything labeled: "indicative — bank credit policy owns final sanction."
- Calibration target on synthetic population: p10 ≈ 450, p90 ≈ 800.

## Naming note
**Parakh** = umbrella product; **Parakh Score** = the number; **Kal-Parakh** (कल = tomorrow, "tomorrow's assay") = the simulator that re-runs the real engine with hypothetical inputs; **Parakh Watch** = early-warning alerts. Fallback UI label for Kal-Parakh if needed: "Score Simulator".

## Demo personas (canonical numbers — no drift allowed)

| | P1 Prime | P2 Hero (NTC) | P3 Warning |
|---|---|---|---|
| Business | Shree Ganesh Auto Components, Rajkot | TrendKart Online, Surat | Maruti Trading Co, Ahmedabad |
| Owner | Rameshbhai Patel, 52 | Meena Shah, 29 | Dineshbhai Soni, 47 |
| GSTIN (fixed) | 24AAACS1234F1Z5 | 24AABCT9876K1Z3 | 24AADCM4321P1Z8 |
| Profile | 12 yrs vintage, 18 employees, OEM supplier, 8-mo growth streak | Ethnic wear, marketplaces + Instagram, 3 yrs GST, **no bureau file**, 80% UPI inflows | Textiles trader, 9 yrs; inflows sliding 6 mo; 3 NACH bounces; GST late 2× (21 days) |
| Turnover | ₹24L/mo | **₹8L/mo → ₹96L/yr → ceiling ₹19.2L** | ₹11L/mo, falling |
| Key ratios | EMI/inflow 6% | EMI/inflow ~0 (no loans) | EMI/inflow 28% |
| Score | **780, High conf.** (Prime) | **690 ± 35, Medium** (no bureau, no EPFO) | **410** (Critical), alert −55 in 2 mo |
| Demo beat | ₹75L collateral-free term loan, CGTMSE-covered expansion lead | Kal-Parakh: 3 on-time GSTR-3B → 720 (Good) → ₹11.5L → ₹15.4L (**+₹3.8L**) | Parakh Watch fires; MSME side shows rehab path |

Consistency check built in: Meena 690 = Watch (60% × 19.2 = 11.5L on lower-edge basis) → 720 = Good (80% = 15.4L). Story and policy agree by construction.

Plus ≥2 non-persona "watchlist" MSMEs seeded with clear 6-month deterioration so the portfolio alert list is never empty.
