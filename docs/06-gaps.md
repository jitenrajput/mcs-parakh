# 06 — Gaps, Risks & Open Decisions

## 1. Current gaps (state vs end goal)

| # | Gap | Impact on goal | Closing action | When |
|---|---|---|---|---|
| G-1 | **No scoring engine yet** — the product core doesn't exist | G1b impossible | P1 (T-106…T-110) | Jul 6–7 |
| G-2 | **No frontend at all**, and no owner assigned | G1b wow-factor at risk; single biggest schedule risk | Assign owner today; Claude generates components so it's integrate-not-build | Jul 6 |
| G-3 | Synthetic data not schema-faithful (current 63 MSMEs predate ReBIT/GSTR1_3B decision) | NFR-8, G2 adapter-readiness claim would be hollow | T-101…T-105 regeneration | Jul 6–7 |
| G-4 | No deployment pipeline; AWS account/access unverified | NFR-2; B-3 | Verify AWS access before Jul 8; App Runner + Amplify dry-run | Jul 7 |
| G-5 | Deck not started; IDBI template access unverified | G1a (the only MANDATORY item) | T-306/307; verify template download today | Jul 6 → 8 |
| G-6 | `solution-design.md` still contains stale stats + "UdyamPulse" name | Risk of stale numbers leaking into deck | Scrub after user confirms; research-findings.md §3 is authoritative meanwhile | Jul 7 |
| G-7 | Team formation completion on Hack2Skill unconfirmed (closes Jul 9 too) | Hard fail if missed | JR verifies independently of submission | Jul 7 |
| G-8 | No demo script/narration written | Demo Day + video quality | 1-pager after P2 gate | Jul 8 |

## 2. Risk register

| # | Risk | L×I | Mitigation | Trigger → fallback |
|---|---|---|---|---|
| R-1 | Frontend slips (owner gap) | H×H | Claude generates all components Jul 7 AM regardless; owner integrates | No owner by Jul 7 noon → Claude builds UI end-to-end, JT does visual QA |
| R-2 | App Runner/Amplify friction burns Jul 8 | M×H | Dry-run Jul 7 eve; container is platform-agnostic | >3 hrs stuck → Render/Railway (architecture slide unchanged) |
| R-3 | Jury challenges a stat | M×H | research-findings §3 twice-verified; primary source per number in speaker notes | — |
| R-4 | "ML is circular" challenge | M×M | Scorecard leads; data-limit stated openly; GBM framed as scale path | — |
| R-5 | "Just another bureau score / FIT Rank clone" | M×H | Slide 7 differentiation: two-sided coaching loop + bank-native continuity vs lender-side point-in-time rank (Dec 2022) | — |
| R-6 | Scope creep vs 3-day runway | H×M | MUST/SHOULD/COULD tags; pre-agreed cut list below | Gate at risk → cut in order |
| R-7 | Demo cold-start > 30 s in front of jury | L×H | NFR-2; keep-warm ping; T-304 cold-start test | — |
| R-8 | Team member unavailable (weekday — day jobs) | M×M | Claude covers any stream; tracker keeps work resumable | — |

**Pre-agreed cut list (in order):** 1. GBM+SHAP lens (T-310) → 2. demo video (T-308) → 3. propensity panel (T-212 propensity half) → 4. audit stub UI exposure (keep backend row) → 5. score animations. **Never cut:** consent screen, reason codes, confidence band/kill-switch, mobile responsiveness, watermark.

## 3. Open decisions — working defaults adopted (flip = one line in this file + tracker update)

| # | Decision | Working default (adopted Jul 6) | Status |
|---|---|---|---|
| D-1 | Model scope | Scorecard = critical path; GBM+SHAP = stretch T-310 | ⚠️ awaiting JR confirm |
| D-2 | Deploy target | AWS App Runner + Amplify; Render/Railway fallback | ⚠️ awaiting JR confirm |
| D-3 | EPFO handling | Light labeled mock, employer-consented path (never AA) | ⚠️ awaiting JR confirm |
| D-4 | Frontend owner | — none — | 🔴 BLOCKING, JR to assign |
| D-5 | Scrub UdyamPulse from solution-design.md | Yes, pending confirm | ⚠️ awaiting JR confirm |
| D-6 | Audit ledger on target-architecture slide | S3 Object Lock (not QLDB — AWS de-emphasized) | adopted (slide-only) |
| D-7 | Production serving on slide | SageMaker endpoint (governance story) | adopted (slide-only) |

Per team rule: defaults are **working assumptions, not locked decisions** — JR confirms or flips; we proceed meanwhile so the deadline doesn't slip.
