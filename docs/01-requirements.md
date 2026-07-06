# 01 — System Requirements

Each requirement carries an ID (used in commits, tracker, and PRs), a priority, and the goal it serves.
**MUST** = demo breaks without it. **SHOULD** = strong shortlist signal. **COULD** = stretch, cut first.

## 1. Functional requirements

### FR-1 Scoring engine (goal: G1a/G1b — the product core)
| ID | Requirement | Priority |
|---|---|---|
| FR-1.1 | Compute 5 dimension scores (0–100): Cash-Flow Strength, Compliance Discipline, Growth Trajectory, Obligation Load, Business Stability — via transparent binned-points scorecard | MUST |
| FR-1.2 | Composite score on **300–900 band** (CIBIL-like), affine log-odds scaling (PDO method), config-driven weights (30/20/15/20/15) visible in UI | MUST |
| FR-1.3 | Reason codes: top ± contributors per dimension from scorecard points, human sentences ("GST filed 14 days late → −12 Compliance points") | MUST |
| FR-1.4 | Confidence band from source-coverage vector: High ±15 / Medium ±35 / Low ±60; missing source → neutral prior + wider band, never zero | MUST |
| FR-1.5 | Score history on rolling monthly windows → trend series per MSME | MUST |
| FR-1.6 | Deterioration alerts: drop >40 pts/month OR negative slope 3 consecutive months OR dimension trip-wires (bounce↑, GST lapse, EMI/inflow threshold) | MUST |
| FR-1.7 | Monotonic LightGBM "risk lens" + SHAP corroborating reason codes | COULD (stretch Jul 8) |
| FR-1.8 | CGTMSE eligibility flag: Micro/Small only + ≤₹10 cr + collateral-free + MLI (4-condition logic, Circular 250) | SHOULD |
| FR-1.9 | Product propensity: volatility→OD, steady→Term Loan, cross-border→Trade Finance, payroll debits→Salary Account | SHOULD |

### FR-2 Data & adapters (goal: G2 — the scale story made real)
| ID | Requirement | Priority |
|---|---|---|
| FR-2.1 | `SourceAdapter` interface: `fetch(subject, consent) → FetchResult{status: OK/PARTIAL/PENDING/FAILED/CONSENT_REVOKED, payload, coverage, consent_id}` | MUST |
| FR-2.2 | Mock adapters: AA-bank (ReBIT `deposit.xsd` field-faithful), GST (`GSTR1_3B`), UPI (via AA txn `mode=UPI`), EPFO (separate employer-consented path — NOT via AA), bureau (CMR-style, nullable for NTC persona) | MUST |
| FR-2.3 | Synthetic dataset: ~60+ MSMEs, 24 months history, 3 scripted personas + ≥2 deteriorating accounts; every record watermarked SYNTHETIC | MUST |
| FR-2.4 | Adapter kill-switch (API/UI toggle) to demo graceful degradation live | MUST |

### FR-3 API (goal: G1b/G2)
| ID | Requirement | Priority |
|---|---|---|
| FR-3.1 | FastAPI + Pydantic v2: `POST /score`, `GET /score/{msme_id}`, `GET /explain/{msme_id}`, `GET /portfolio`, `POST /consent`, `GET /msmes` | MUST |
| FR-3.2 | Auto-generated OpenAPI docs at `/docs` (ULI-ready spec = a demo tab) | MUST |
| FR-3.3 | Decision/audit log stub: inputs + coverage + model version + timestamp + consent ref per score | SHOULD |

### FR-4 Frontend (goal: G1a screenshots + G1b wow-factor)
| ID | Requirement | Priority |
|---|---|---|
| FR-4.1 | Health Card: animated composite gauge (300–900) + 5 dimension bars + confidence badge + reason codes | MUST |
| FR-4.2 | AA-style 7-step consent screen (purpose code 103/104, FI types, data range, duration, approve/revoke) + DPDP plain-language notice | MUST |
| FR-4.3 | Lender view: portfolio list ranked by health trend, early-warning alerts with reasons, propensity + CGTMSE panel | MUST |
| FR-4.4 | MSME view: own card, plain-language strengths/risks, "improve your score" actions, loan-readiness meter | MUST |
| FR-4.5 | Lender/MSME view flip on one card | MUST |
| FR-4.6 | Mobile-responsive (jury will open the link on a phone) | MUST |
| FR-4.7 | Synthetic-data watermark visible on every screen | MUST |

## 2. Non-functional requirements

| ID | Requirement | Priority |
|---|---|---|
| NFR-1 | Score computation < 2 s per MSME end-to-end in demo | MUST |
| NFR-2 | Deployed URLs live from Jul 8 through at least Jul 21 (shortlist date) — no sleeping free-tier that cold-starts > 30 s | MUST |
| NFR-3 | Zero secrets/PII in repo; MIT license; public-safe | MUST |
| NFR-4 | Fresh clone → running locally in 2 commands | SHOULD |
| NFR-5 | Scoring engine = pure stateless module, framework-free, unit-tested (the "swap FastAPI→SageMaker" credibility) | MUST |
| NFR-6 | Deterministic demo: same inputs → same score, no randomness at request time | MUST |
| NFR-7 | Honest-mock rule: every mock labeled in UI, deck, and README | MUST |
| NFR-8 | Schema fidelity: synthetic data uses real ReBIT/GST field names (adapter-ready for IDBI sandbox in G2) | SHOULD |

## 3. Compliance requirements (deck + demo signals; see research-findings.md §4)

| ID | Requirement |
|---|---|
| CR-1 | Consent flow mirrors RBI AA Master Direction para 6.3 journey |
| CR-2 | DPDP Rules 2025 language: purpose limitation, data-minimization list, "withdraw as easily as given" |
| CR-3 | Explainability labeled "aligned with RBI FREE-AI (Aug 2025) + draft MRM Guidance (Jun 2026)" |
| CR-4 | Data-used vs data-available contrast shown (minimization) |
| CR-5 | CGTMSE flag logic cites Circular 250 (₹10 cr) / 241 (75–90% cover) |

## 4. Out of scope this week (explicitly)

Real AA/GSTN/bureau integrations · authentication beyond a demo token · multi-tenancy · real AWS pipeline (Step Functions/SageMaker — slides only) · Hindi localization (tagline only) · admin panels · notifications.
