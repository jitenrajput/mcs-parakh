# 05 — Task Tracker

**This file is the single source of truth for status.** Update it in the same commit as the work (see 08-git-workflow.md). Statuses: `todo` · `doing` · `blocked` · `done` · `cut`.

Owners: **JR** Jitendra · **JT** Jayesh · **ZS** Zaid · **NP** Nirmal · **FE** frontend owner (TBD) · **CL** Claude

## P1 — Foundation (gate: personas score correctly from CLI)

| ID | Task | Req | Owner | Status |
|---|---|---|---|---|
| T-101 | Upgrade datagen to ReBIT `deposit.xsd` field fidelity (txn `mode`, `narration`, balances) | FR-2.3, NFR-8 | ZS+CL | **done** |
| T-102 | Add GSTR-1/3B filing records w/ due-date + filed-date (timeliness signal) | FR-2.3 | ZS+CL | **done** |
| T-103 | EPFO ECR mock records (UAN count, wages, contribution dates) — employer-consented path | FR-2.2 | CL | **done** |
| T-104 | Bureau mock (CMR-style; NULL for persona P2 NTC) | FR-2.2 | CL | **done** |
| T-105 | Regenerate dataset: 65 MSMEs, 24 mo, 3 personas + 2 deteriorating; SYNTHETIC watermark, DS-42-2026.07 | FR-2.3 | ZS | **done** |
| T-106 | `parakh_engine`: FeatureExtractor per source | FR-1.1 | ZS+CL | **done** |
| T-107 | Scorecard: graded bins → points → 5 dimensions → weighted composite → 300–900 affine scaling (calibrated: personas 781/691/410) | FR-1.1/1.2 | ZS+CL | **done** |
| T-108 | Reason-code generator from point contributions | FR-1.3 | CL | **done** |
| T-109 | Confidence band from coverage vector (majors/minors; lower-edge eligibility) | FR-1.4 | CL | **done** |
| T-110 | Unit tests: persona bands, determinism, degradation, monotonicity, lower-edge, version stamps — **10/10 green** | NFR-5/6 | ZS+NP | **done** |

**✅ P1 GATE PASSED (Jul 06 night): personas score 781 Prime High±15 / 691 Watch Medium±35 / 410 Critical from CLI; pytest 10/10.** *(Shipped dataset scores 781/692/409 — canon reconciled in docs/12 on Jul 7; live-verified via API.)*

## P2 — End-to-end product (gate: full flow clickable locally)

| ID | Task | Req | Owner | Status |
|---|---|---|---|---|
| T-201 | `SourceAdapter` protocol + 5 mock adapters + registry | FR-2.1/2.2 | CL | **done** |
| T-202 | Adapter kill-switch (`/admin/killswitch`) — Low confidence also drops the limit | FR-2.4 | CL | **done** |
| T-203 | FastAPI: /score, /score/{id}, /explain/{id}, /portfolio, /consent, /msmes, /simulate + OpenAPI | FR-3.1/3.2 | CL+ZS | **done** |
| T-204 | Audit log + consent store (SQLite; version stamps per row) | FR-3.3 | CL | **done** |
| T-205 | Parakh Watch: score time-series (rolling monthly) + transparent alert rules | FR-1.5/1.6 | ZS | **done** |
| T-213b | Kal-Parakh backend (`/simulate` re-runs real engine; canon verified 692→721, +₹3.9L) | FR-4.8 | CL | **done** |

**⚠️ Policy amendment pending JR confirm (docs/12): lower-edge eligibility now applies at Low confidence only; High/Medium use point band — required to keep the canonical +₹3.9L moment true (persona canon reconciled Jul 7). API tests 6/6, engine 10/10.**
| T-206 | React scaffold (Vite + Tailwind; custom SVG viz — lighter than Recharts) | FR-4.x | FE+CL | **done** |
| T-207 | Health Card (gauge + confidence halo, dimension rows, reasons, decision record) | FR-4.1 | FE+CL | **done** |
| T-208 | AA consent screen (para-6.3 fields) + DPDP notice + declined state | FR-4.2, CR-1/2 | FE+CL | **done** |
| T-209 | Lender portfolio: ranked ledger, sparklines, Parakh Watch section on top | FR-4.3 | FE+CL | **done** |
| T-210 | MSME self-view: card + plain-words reasons + readiness meter | FR-4.4 | FE+CL | **done** |
| T-211 | Flip button + watermark done; **mobile pass on real phone pending (Jul 7 QA)** | FR-4.5/4.6/4.7 | FE | doing |
| T-212 | CGTMSE flag (4-condition, circulars cited) + propensity rail | FR-1.8/1.9 | ZS+FE | **done** |
| T-213 | Kal-Parakh UI: action toggles → live re-score → +₹ delta (canon 692→721 +₹3.9L) | FR-4.8 | CL+ZS | **done** |
| T-214 | Seal-dot coverage ring + assay-stamp A–E chips | FR-4.9 | FE+CL | **done** |
| T-215 | EN/HI/GU toggle (custom i18n, one block per language) | FR-4.10 | FE+CL | **done** |
| T-216 | Demo Launcher S0: seat-picker, persona cards, 30-sec explainer | docs/10 | FE+CL | **done** |
| T-217 | Error states: consent-declined, unknown-GSTIN→persona chips, API-cold, skeletons, 404→S0, source-failed toast-equivalent | docs/10 | FE+CL+NP | **done** (NP re-test Jul 7) |
| T-218 | Tokens wired into tailwind.config.js; **copy to Slides master pending (JT)** | docs/10 | CL+JT | doing |
| T-219 | Strings EN/HI/GU live in i18n.jsx; **JR native review pending** | docs/10 | CL+JR | doing |

## P3 — Ship & tell (gate: public URL on phone; deck sourced; 2-command clone)

| ID | Task | Req | Owner | Status |
|---|---|---|---|---|
| T-301 | Dockerfile + compose; container runs full stack locally (single image 255 MB; `docker compose up` → :8000; pytest 16/16 in-container; healthcheck green) | NFR-4 | CL | **done** |
| T-302 | Deploy API — **DEFERRED (Jul 7): no AWS details; JR will host under mconnectsolutions.com when ready. Local-only until then.** Container is deploy-ready (T-301) | NFR-2 | JR+CL | blocked |
| T-303 | Deploy frontend — deferred with T-302 (single container already serves the SPA, so one host may cover both) | NFR-2 | JR+CL | blocked |
| T-304 | Phone + incognito + cold-start test | NFR-2 | NP | todo |
| T-305 | README rewritten (verified stats, Docker+bare quickstart, architecture, MIT LICENSE) + no-secrets scan clean; **demo GIF pending (after T-308 video)** | NFR-3/7, G1c | NP+CL | doing |
| T-306 | Deck: full 10-slide content draft + 250-word abstract ready (`deck-draft.md`, private) — **JT builds in IDBI template Jul 8 (needs B-4)** | G1a | JR+JT | doing |
| T-307 | Deck speaker notes: primary source per number | G1a | JT | todo |
| T-308 | 2-min demo video | G1a booster | JT | todo |
| T-309 | QA: 3 persona walkthroughs + kill-switch moment + deck-vs-demo consistency | G1 | NP | todo |
| T-310 | (Stretch) LightGBM monotonic + SHAP lens | FR-1.7 | ZS | todo |
| T-311 | Juror-rebuttal one-pager **done** (`juror-rebuttals.md`, private): 6 attacks + translation table + stat guardrails | G1a | JT+CL | **done** |
| T-312 | Logo: 4 hallmark-stamp options committed (`assets/brand/`) + preview gallery sent — **JR picks**, then path-convert + favicon/OG/banner + app header | docs/10 | CL+JR | doing |
| T-313 | Subdomain parakh.mconnectsolutions.com (CNAME + SSL on App Runner/Amplify) | docs/10 | JR+CL | todo |
| T-314 | Demo hygiene: disclaimer page, event footer, slowapi rate limit, UptimeRobot keep-warm ping | docs/10 | CL | todo |
| T-315 | Demo script **written & live-verified** (`demo-script.md`, private): 2-min video VO + 5-min walkthrough + kill-switch choreography + reset checklist. **Pending: JR voices video, pitch-roles rehearsal** | docs/10 | JT+JR | doing |
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
