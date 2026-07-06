# 05 — Task Tracker

**This file is the single source of truth for status.** Update it in the same commit as the work (see 08-git-workflow.md). Statuses: `todo` · `doing` · `blocked` · `done` · `cut`.

Owners: **JR** Jitendra · **JT** Jayesh · **ZS** Zaid · **NP** Nirmal · **FE** frontend owner (TBD) · **CL** Claude

## P1 — Foundation (gate: personas score correctly from CLI)

| ID | Task | Req | Owner | Status |
|---|---|---|---|---|
| T-101 | Upgrade datagen to ReBIT `deposit.xsd` field fidelity (txn `mode`, `narration`, balances) | FR-2.3, NFR-8 | ZS+CL | todo |
| T-102 | Add GSTR-1/3B filing records w/ due-date + filed-date (timeliness signal) | FR-2.3 | ZS+CL | todo |
| T-103 | EPFO ECR mock records (UAN count, wages, contribution dates) — employer-consented path | FR-2.2 | CL | todo |
| T-104 | Bureau mock (CMR-style; NULL for persona P2 NTC) | FR-2.2 | CL | todo |
| T-105 | Regenerate dataset: 60+ MSMEs, 24 mo, 3 personas + 2 deteriorating; SYNTHETIC watermark | FR-2.3 | ZS | todo |
| T-106 | `parakh_engine`: FeatureExtractor per source | FR-1.1 | ZS+CL | todo |
| T-107 | Scorecard: bins → points → 5 dimensions → weighted composite → 300–900 affine scaling | FR-1.1/1.2 | ZS+CL | todo |
| T-108 | Reason-code generator from point contributions | FR-1.3 | CL | todo |
| T-109 | Confidence band from coverage vector | FR-1.4 | CL | todo |
| T-110 | Unit tests: persona bands, monotonicity spot-checks, missing-source behavior | NFR-5/6 | ZS+NP | todo |

## P2 — End-to-end product (gate: full flow clickable locally)

| ID | Task | Req | Owner | Status |
|---|---|---|---|---|
| T-201 | `SourceAdapter` protocol + 5 mock adapters + registry | FR-2.1/2.2 | CL | todo |
| T-202 | Adapter kill-switch endpoint/toggle | FR-2.4 | CL | todo |
| T-203 | FastAPI: /score, /score/{id}, /explain/{id}, /portfolio, /consent, /msmes + OpenAPI | FR-3.1/3.2 | CL+ZS | todo |
| T-204 | Audit log stub (SQLite) | FR-3.3 | CL | todo |
| T-205 | Score time-series (rolling monthly) + alert rules | FR-1.5/1.6 | ZS | todo |
| T-206 | React scaffold (Vite + Tailwind + Recharts) | FR-4.x | FE+CL | todo |
| T-207 | Health Card component (gauge, dimensions, confidence badge, reasons) | FR-4.1 | FE+CL | todo |
| T-208 | AA consent screen + DPDP notice | FR-4.2, CR-1/2 | FE+CL | todo |
| T-209 | Lender portfolio view + early-warning list | FR-4.3 | FE+CL | todo |
| T-210 | MSME self-view + improve-actions + readiness meter | FR-4.4 | FE+CL | todo |
| T-211 | View flip + mobile responsiveness + watermark | FR-4.5/4.6/4.7 | FE | todo |
| T-212 | CGTMSE flag + propensity panel | FR-1.8/1.9 | ZS+FE | todo |
| T-213 | Improve-score simulator (re-runs engine; rupee-denominated deltas, Nayak-anchor formula) | FR-4.8 | CL+ZS | todo |
| T-214 | Coverage ring + A–E grade chips on Health Card | FR-4.9 | FE+CL | todo |
| T-215 | EN/HI/GU language toggle (react-i18next) | FR-4.10 | FE+CL | todo |
| T-216 | Demo Launcher S0 (seat-picker, persona cards, reset) — MUST | docs/10 | FE+CL | todo |
| T-217 | 7 designed error/empty states — MUST; NP tests all deliberately | docs/10 | FE+CL+NP | todo |
| T-218 | tokens.json (palette/type) wired into Tailwind + copied to Slides master | docs/10 | CL+JT | todo |
| T-219 | strings.json EN/HI/GU (~10 critical strings); JR native review Jul 7 eve | docs/10 | CL+JR | todo |

## P3 — Ship & tell (gate: public URL on phone; deck sourced; 2-command clone)

| ID | Task | Req | Owner | Status |
|---|---|---|---|---|
| T-301 | Dockerfile + compose; container runs full stack locally | NFR-4 | CL | todo |
| T-302 | Deploy API → App Runner (fallback Render after 3 hrs) | NFR-2 | JR+CL | todo |
| T-303 | Deploy frontend → Amplify | NFR-2 | JR+CL | todo |
| T-304 | Phone + incognito + cold-start test | NFR-2 | NP | todo |
| T-305 | README: quickstart, architecture diagram, demo GIF, MIT, no-secrets scan | NFR-3/7, G1c | NP+CL | todo |
| T-306 | Deck 10 slides in IDBI template — stats from research-findings §3 ONLY | G1a | JR+JT | todo |
| T-307 | Deck speaker notes: primary source per number | G1a | JT | todo |
| T-308 | 2-min demo video | G1a booster | JT | todo |
| T-309 | QA: 3 persona walkthroughs + kill-switch moment + deck-vs-demo consistency | G1 | NP | todo |
| T-310 | (Stretch) LightGBM monotonic + SHAP lens | FR-1.7 | ZS | todo |
| T-311 | Juror-rebuttal one-pager (6 attacks incl. "why your parameters" + translation table) for rehearsal | G1a | JT+CL | todo |
| T-312 | Logo SVGs (hallmark-stamp concept) → JR picks; into app header + deck + favicon + OG image | docs/10 | CL+JR | todo |
| T-313 | Subdomain parakh.mconnectsolutions.com (CNAME + SSL on App Runner/Amplify) | docs/10 | JR+CL | todo |
| T-314 | Demo hygiene: disclaimer page, event footer, slowapi rate limit, UptimeRobot keep-warm ping | docs/10 | CL | todo |
| T-315 | Demo script fitted to final screens (draft done); JR voices video; pitch-roles rehearsal | docs/10 | JT+JR | todo |
| T-316 | PS-language mirror pass: slide 4 uses PS3's exact vocabulary verbatim | pre-mortem | JT+CL | todo |
| T-317 | Template-compliance checklist (structure, slide count, PDF ≤5MB, naming) | pre-mortem | NP | todo |
| T-318 | QR code for slide 5 → parakh.mconnectsolutions.com | pre-mortem | CL | todo |
| T-319 | Read Hack2Skill/IDBI T&Cs (IP terms) BEFORE repo goes public | IP | JR+CL | todo |
| T-320 | Submission-form field screenshots (Jul 7) + pre-written answers incl. 250-word abstract | dry-run | JR+CL | todo |

## P4 — Submit

| ID | Task | Owner | Status |
|---|---|---|---|
| T-401 | Final review meeting 09:00 Jul 9 | all | todo |
| T-402 | Export PDF ≤ 5 MB; slide-1 fields; submit deck + links before noon | JR | todo |
| T-403 | Confirm Hack2Skill team formation complete | JR | todo |
| T-404 | Confirmation screenshot archived | JR | todo |

## Blockers (live)

| # | Blocker | Blocks | Owner | Raised |
|---|---|---|---|---|
| B-1 | Frontend owner unassigned | T-206…T-212 | JR | Jul 3 |
| B-2 | Working defaults unconfirmed (deploy / model scope / EPFO) — defaults adopted, flag to flip | T-302, T-310, T-103 | JR | Jul 6 |
| B-3 | AWS account + Amplify/App Runner access not yet verified | T-302/303 | JR | Jul 6 |
| B-4 | IDBI Google Slides template access (download + fonts) not verified | T-306 | JT | Jul 6 |
