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

**✅ Policy amendment LOCKED by JR (Jul 7): lower-edge eligibility applies at Low confidence only; High/Medium use point band (docs/12). Demo-canon tests pin the behavior.**
| T-206 | React scaffold (Vite + Tailwind; custom SVG viz — lighter than Recharts) | FR-4.x | FE+CL | **done** |
| T-207 | Health Card (gauge + confidence halo, dimension rows, reasons, decision record). **Jul 8: each dimension row now shows its policy weight % + "weights set by credit policy" caption — explicit transparency edge vs learned-weight competitors (see `competitor-intel.md`)** | FR-4.1 | FE+CL | **done** |
| T-208 | AA consent screen (para-6.3 fields) + DPDP notice + declined state | FR-4.2, CR-1/2 | FE+CL | **done** |
| T-209 | Lender portfolio: ranked ledger, sparklines, Parakh Watch section on top | FR-4.3 | FE+CL | **done** |
| T-210 | MSME self-view: card + plain-words reasons + readiness meter | FR-4.4 | FE+CL | **done** |
| T-211 | Flip button + watermark done; **mobile pass on real phone pending (Jul 7 QA)**. **Jul 8 dev-review: browser console cleaned — React Router v7 future-flags opted in + `/favicon.ico` added → 0 errors / 0 warnings** | FR-4.5/4.6/4.7 | FE | doing |
| T-212 | CGTMSE flag (4-condition, circulars cited) + propensity rail | FR-1.8/1.9 | ZS+FE | **done** |
| T-213 | Kal-Parakh UI: action toggles → live re-score → +₹ delta (canon 692→721 +₹3.9L). **Jul 8: `/simulate` now returns full after-state (dimensions + reasons) → the WHOLE card transforms on projection, not just the number; persona-aware actions grey out no-impact levers (e.g. no-EMI business can't "refinance"); reason-sign fix (positives never shown under "holding you back"); coverage-aware "Working against" caveat when sources missing** | FR-4.8 | CL+ZS | **done** |
| T-214 | Seal-dot coverage ring + assay-stamp A–E chips | FR-4.9 | FE+CL | **done** |
| T-215 | EN/HI/GU toggle (custom i18n, one block per language) | FR-4.10 | FE+CL | **done** |
| T-216 | Demo Launcher S0: seat-picker, persona cards, 30-sec explainer | docs/10 | FE+CL | **done** |
| T-217 | Error states: consent-declined, unknown-GSTIN→persona chips, API-cold, skeletons, 404→S0, source-failed toast-equivalent | docs/10 | FE+CL+NP | **done** (NP re-test Jul 7) |
| T-218 | Tokens wired into tailwind.config.js; **copy to Slides master pending (JT)** | docs/10 | CL+JT | doing |
| T-219 | Strings EN/HI/GU in i18n.jsx — extended Jul 7 (Kal-Parakh action labels+hints, confidence words, sim note). **Jul 8: full MSME-view localization — reason codes (engine emits `vstr`; 34 HI/GU templates), 5 dimension names, score-makeup header, footer, empty-states/caveats. Review sheet: `t219-translations-review.txt`. JR native review (esp. Gujarati) pending** | docs/10 | CL+JR | doing |

## P3 — Ship & tell (gate: public URL on phone; deck sourced; 2-command clone)

| ID | Task | Req | Owner | Status |
|---|---|---|---|---|
| T-301 | Dockerfile + compose; container runs full stack locally (single image 255 MB; `docker compose up` → :8000; pytest 16/16 in-container; healthcheck green) | NFR-4 | CL | **done** |
| T-302 | Deploy API — **DEFERRED (Jul 7): no AWS details; JR will host under mconnectsolutions.com when ready. Local-only until then.** Container is deploy-ready (T-301) | NFR-2 | JR+CL | blocked |
| T-303 | Deploy frontend — deferred with T-302 (single container already serves the SPA, so one host may cover both) | NFR-2 | JR+CL | blocked |
| T-304 | Phone + incognito + cold-start test | NFR-2 | NP | todo |
| T-305 | README rewritten (verified stats, Docker+bare quickstart, architecture, MIT LICENSE) + no-secrets scan clean; **demo GIF pending (after T-308 video)** | NFR-3/7, G1c | NP+CL | doing |
| T-306 | **Deck BUILT Jul 8 by CL** (JT didn't) — 15-slide PPTX+PDF on the OFFICIAL IDBI template (cropped IDBI header band + section titles as dimmed eyebrows, our claims as headlines, ONLY our content — no leftover template prompts). Real screenshots embedded, verified numbers, QR, appendix sources. Self-QA'd render slide-by-slide. Files `MCS-Parakh_PS3_M-Connect-Labs.pptx/.pdf` (root, private; **PDF 956 KB ≤5 MB**). Built via `python-pptx` + PowerPoint-COM PDF export + poppler render-check. **Pending: JR review, confirm registered team name, QR→live URL on deploy** | G1a | CL+JR | **done** |
| T-307 | Deck speaker notes **done** — every slide carries notes with the primary source per number (in the built deck) | G1a | CL | **done** |
| T-308 | Demo video — **template allows 3 min**; script + optional extension beats in `demo-script.md`; JR voices | G1a booster | JT | todo |
| T-309 | QA: 3 persona walkthroughs + kill-switch moment + deck-vs-demo consistency | G1 | NP | todo |
| T-310 | (Stretch) LightGBM monotonic + SHAP lens | FR-1.7 | ZS | todo |
| T-311 | Juror-rebuttal one-pager **done** (`juror-rebuttals.md`, private): 6 attacks + translation table + stat guardrails | G1a | JT+CL | **done** |
| T-312 | Logo **DONE**: JR picked **B (Navy Assay)** Jul 7. Shipped: BrandMark in app headers, favicon, apple-touch icon, OG image (1200×630, meta live on deploy), README banner, mono SVG deck cuts. **Jul 8: API-docs Swagger now carries the प hallmark favicon too (branded `/docs` route, root_path-safe)** | docs/10 | CL+JR | **done** |
| T-313 | Subdomain parakh.mconnectsolutions.com (CNAME + SSL on App Runner/Amplify) | docs/10 | JR+CL | todo |
| T-314 | Demo hygiene: disclaimer page, event footer, slowapi rate limit, UptimeRobot keep-warm ping | docs/10 | CL | todo |
| T-315 | Demo script **written & live-verified** (`demo-script.md`, private): 2-min video VO + 5-min walkthrough + kill-switch choreography + reset checklist. **Pending: JR voices video, pitch-roles rehearsal** | docs/10 | JT+JR | doing |
| T-316 | PS-language mirror — deck slide 1 uses "PS3 — Financial Health Score" verbatim + slide 3 answers the template's Opportunities prompts in PS3 terms. **JR: confirm exact registered team name/leader** | pre-mortem | CL+JR | doing |
| T-317 | Template-compliance — **Jul 8: built deck IS compliant** (15 IDBI sections, official template design, PDF 956 KB ≤5 MB, links present). NP final-verify the exported PDF against `submission-form.md` | pre-mortem | NP | doing |
| T-318 | QR **created** on the Links slide — currently → public GitHub repo (safe, always-live placeholder). **Swap to live app URL (or 3-min demo video) once hosting up — JR will signal; ~10-sec regen + re-export** | pre-mortem | CL | doing |
| T-319 | **DONE (Jul 7):** terms researched (standard H2S boilerplate — IP retained, 6-mo ROFR on exclusive licenses only, MIT-compatible); JR found no separate participation agreement → **repo flipped PUBLIC** (github.com/jitenrajput/mcs-parakh) | IP | JR+CL | **done** |
| T-320 | **DONE (full form confirmed Jul 8):** only 2 required fields — **Challenges** (select "Problem Statement 3: Financial Health Score") + **PoC PPT PDF ≤5 MB**. Deployment Link & GitHub link both **optional**. No abstract field (goes inside PDF). No hidden wizard fields — single-page form. `submission-form.md` updated | dry-run | JR+CL | **done** |

## P4 — Submit

| ID | Task | Owner | Status |
|---|---|---|---|
| T-401 | Final review meeting 09:00 Jul 9 | all | todo |
| T-402 | Export PDF ≤ 5 MB; slide-1 fields; submit deck + links before noon | JR | todo |
| T-403 | Confirm Hack2Skill team formation complete | JR | todo |
| T-404 | Confirmation screenshot archived | JR | todo |

## Blockers (live)

| # | Blocker | Blocks | Owner | Raised | Status |
|---|---|---|---|---|---|
| B-1 | Frontend owner unassigned | T-206…T-212 | JR | Jul 3 | **resolved Jul 6** — CL built the frontend; NP covers QA |
| B-2 | Working defaults unconfirmed (deploy / model scope / EPFO) | T-302, T-310, T-103 | JR | Jul 6 | **resolved** — EPFO shipped; scorecard-only shipped (GBM stays stretch); deploy superseded by B-5 |
| B-3 | AWS account access not verified | T-302/303 | JR | Jul 6 | **superseded Jul 7** — no AWS; hosting = mconnectsolutions.com (B-5) |
| B-4 | IDBI template access not verified | T-306 | JT | Jul 6 | **resolved Jul 7** — template downloaded + analyzed; 15-slide structure mapped |
| B-5 | **Hosting timing on mconnectsolutions.com (JR)** — blocks deploy chain T-302/303/304/313/314/318 (QR) | deploy chain | JR | Jul 7 | **live** |
