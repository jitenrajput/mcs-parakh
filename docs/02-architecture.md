# 02 — Architecture

**Design principle: adapters, not integrations.** One `SourceAdapter` interface; mock implementations now (PoC), IDBI sandbox implementations in the prototype phase (G2), live rails in production. **Scoring code never changes across the three stages** — that is the entire scalability pitch, and it's true because we build it that way from commit one.

## 1. PoC architecture (what we build this week)

```
┌─────────────────┐   HTTPS    ┌────────────────────────────────────────────┐
│  React SPA       │ ────────► │  FastAPI (single container)                 │
│  (AWS Amplify)   │ ◄──────── │                                             │
│  · Lender view   │  JSON     │  ┌───────────── adapter registry ─────────┐ │
│  · MSME view     │           │  │ mock: AA-bank │ GST │ UPI │ EPFO │ CIBIL│ │
│  · Consent UX    │           │  │ each → FetchResult{status, coverage}   │ │
└─────────────────┘           │  │ kill-switch per adapter (demo moment)  │ │
                               │  └──────────────────┬─────────────────────┘ │
                               │        FeatureExtractor (per source)        │
                               │        Scorecard engine (pure module)       │
                               │          bins→points→dimensions→300-900     │
                               │          reason codes · confidence band     │
                               │        [stretch: LightGBM + SHAP lens]      │
                               │        Audit log stub (SQLite)              │
                               └────────────────────────────────────────────┘
                                     AWS App Runner (container, public URL)
        Synthetic dataset (ReBIT/GSTR1_3B-faithful JSON, watermarked SYNTHETIC)
```

**Stack:** Python 3.11 · FastAPI + Pydantic v2 · scorecard as pure stateless module · SQLite (SQLAlchemy → one-line Postgres swap) · React + Tailwind + Recharts · Docker (one `Dockerfile`, `docker compose up` runs everything).

**Working defaults (flagged, not locked):** deploy = **App Runner + Amplify** (on-brand with AWS partner; fallback Render/Railway only if App Runner stalls); model = **scorecard first, GBM stretch**; EPFO = **light labeled mock on the employer-consented path**.

## 2. Target AWS architecture (deck slide + G2 direction)

```
 Borrower / RM ── CloudFront + WAF ── S3 (React SPA) ── Cognito
                        │
              API Gateway (OpenAPI 3.1, OAuth2 + mTLS — ULI-shaped)
                        │
        FastAPI orchestrator — ECS Fargate (stateless, autoscaled)
             │                │                     │
             │                │            SageMaker endpoint (versioned model)
             │                │                     └─ SHAP reason codes
             │        SageMaker Feature Store (online DynamoDB / offline S3+Glue)
             │
   Step Functions per applicant (parallel fan-out, per-source timeout/retry/DLQ)
     ├─ λ AA/FIP adapter      ├─ λ GSTN adapter      ├─ λ UPI adapter
     ├─ λ EPFO adapter (employer-consented path)     ├─ λ Bureau adapter
     └─ λ ULI adapter         · async AA callbacks → API GW → SQS → EventBridge
                        │
   S3 raw (WORM/Object Lock) · DynamoDB scores · S3 Object Lock audit ledger
                        │
   EventBridge (schedule + fresh-signal events) → Step Functions
        → SageMaker Batch Transform (portfolio re-score = early warning)

 Cross-cutting: VPC + PrivateLink · KMS CMK per data class · Secrets Manager ·
 CloudTrail · CloudWatch/X-Ray + per-FIP health metrics · Model Registry/Monitor
```

**Named patterns for the slide:** stateless horizontal scaling · event-driven re-scoring · online feature-store caching · graceful degradation + confidence bands · idempotent fetches (dedupe keys) · circuit-breaker per adapter (one dead FIP can't stall the pipeline) · model versioning & drift monitoring (per RBI draft MRM Guidance, Jun 2026).

## 3. The adapter contract (the through-line — implement exactly this)

```python
class SourceAdapter(Protocol):
    source_id: str          # "aa.mock" | "gst.mock" | "upi.mock" | "epfo.mock" | "bureau.mock"
    async def fetch(self, subject: SubjectRef, consent: ConsentRef,
                    since: date | None = None) -> FetchResult: ...

@dataclass
class FetchResult:
    status: Literal["OK", "PARTIAL", "PENDING", "FAILED", "CONSENT_REVOKED"]
    payload: dict | None     # schema-faithful to the real rail (ReBIT deposit / GSTR1_3B / ECR / CMR)
    coverage: float          # 0.4 = only 4 of 10 requested months returned
    fetched_at: datetime
    consent_id: str
    error: str | None = None
```

Rules: **never treat PARTIAL as complete** · scoring proceeds on whatever arrived within the SLA window + a coverage vector · coverage vector → confidence band (FR-1.4) · every fetch bound to a consent ID (consent is a first-class object, DPDP/AA-native).

## 4. Data flow (PoC): GSTIN → Health Card

1. UI: user enters GSTIN → consent screen (purpose 103/104, FI types, range) → approve.
2. API: `POST /score` → adapter registry fans out (`asyncio.gather`) to 5 mock adapters.
3. Each adapter returns `FetchResult` (kill-switch may force FAILED — demo moment).
4. FeatureExtractor per source → feature dict + coverage vector.
5. Scorecard: bins → points → 5 dimension scores → weighted composite → 300–900 affine scaling.
6. Reason codes from point contributions; confidence band from coverage.
7. Audit stub row (inputs hash, coverage, engine version, timestamp, consent ref).
8. Response → card animates; flip lender/MSME; portfolio view reads precomputed monthly score series.

## 5. Repo structure (target)

```
MCS-Parakh/
├─ docs/                    ← this blueprint
├─ backend/
│  ├─ datagen/              ← synthetic data generator (upgrade to ReBIT/GSTR1_3B fidelity)
│  ├─ parakh_engine/        ← PURE scoring module: features, scorecard, reasons, confidence
│  │  └─ tests/
│  ├─ adapters/             ← SourceAdapter + 5 mocks
│  ├─ api/                  ← FastAPI app, routes, Pydantic schemas, audit stub
│  └─ requirements.txt
├─ frontend/                ← React + Tailwind + Recharts (Vite)
├─ data/                    ← generated synthetic dataset (committed; watermarked)
├─ Dockerfile · docker-compose.yml
└─ README.md                ← 2-command quickstart, architecture, demo GIF
```
