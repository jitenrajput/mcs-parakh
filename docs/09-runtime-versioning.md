# 09 — Runtime Requirements, Releases & Versioning

## 1. What the product needs to run (and what it deliberately does NOT need)

### No LLM at runtime — by design, and it's a selling point
Parakh's scoring, reason codes, and simulator are **deterministic**: scorecard arithmetic + templated sentences (+ optional LightGBM, also deterministic). Same inputs → same score, every time (NFR-6).

Why this is the right call for a credit product, and worth saying to the jury:
- **Reproducibility** — every score is auditable and re-derivable; a regulator can replay any decision (RBI draft MRM 2026 / FREE-AI alignment).
- **No hallucination risk** in rupee-value outputs; no prompt-injection surface.
- **Zero per-request AI cost and no external API dependency** — scoring works if the internet to any AI vendor is down; cost per score is effectively ₹0.
- LLM appears only on the **roadmap**: "Parakh Sahayak," a vernacular conversational assistant for MSMEs (prototype+ phase, optional, never in the scoring path).

### No GPU anywhere
Scorecard = pure arithmetic. LightGBM training on hundreds-to-thousands of rows = seconds on CPU. SHAP TreeExplainer = milliseconds per row on CPU.

### Software stack (pinned baselines)
| Layer | Requirement |
|---|---|
| Backend runtime | Python **3.11+** (dev on 3.12) |
| Backend deps | FastAPI, uvicorn, Pydantic v2, numpy, pandas, scikit-learn, **LightGBM** (stretch), shap (stretch), SQLAlchemy (SQLite → Postgres one-liner) |
| Frontend build | Node.js **20 LTS**, Vite, React 18, Tailwind, Recharts, react-i18next (EN/HI/GU) |
| Frontend runtime | Any evergreen browser; mobile Chrome/Safari (jury opens on phone) |
| Container | Docker; single image ≤ ~600 MB; `docker compose up` runs everything |

### Minimum machine — local dev / judge running the repo
- Any 64-bit laptop, **8 GB RAM**, ~2 GB free disk; Windows / macOS / Linux.
- Python 3.11+, Node 20+, Git. Docker optional (compose path) — the 2-command quickstart also works bare (`pip install + uvicorn`, `npm install + npm run dev`).
- Full dataset (60+ MSMEs × 24 months) loads in memory in < 100 MB; scoring < 2 s/MSME (NFR-1).

### Demo hosting (PoC, Jul 8–21)
| Component | Spec | Cost |
|---|---|---|
| API + engine | AWS App Runner, **1 vCPU / 2 GB**, min instances = 1 (kills cold-start risk, NFR-2) | ~$5–15 for the fortnight |
| Frontend | AWS Amplify Hosting (static build + CDN) | free tier |
| Store | SQLite inside the container (read-mostly demo data) — DynamoDB only if App Runner instance recycling proves annoying | ₹0 |
Fallback (only if App Runner burns > 3 hrs): Render/Railway, same container.

### Production sizing (deck talking point, not built this week)
Stateless scoring at ~ms per MSME on 1 vCPU → a single small Fargate task handles hundreds of scores/sec; horizontal autoscale for portfolio batch re-scoring; nightly re-score of a 1M-MSME book = embarrassingly parallel batch job. The expensive part of production is data acquisition (AA/GSP fetches), not compute — and fetches are consent-triggered + cached.

## 2. Software releases & versioning

### App versioning — SemVer, phase-aligned
`MAJOR.MINOR.PATCH` — MAJOR = hackathon phase, MINOR = feature drop, PATCH = fix.

| Series | Phase | Tags (already in 08-git-workflow.md) |
|---|---|---|
| **0.x** | Build week | `v0.1-engine` (P1 gate) · `v0.2-e2e` (P2 gate) · `v0.3-deployed` (P3 gate) |
| **1.0** | PoC submission | `v1.0-poc-submission` = the exact judged commit, Jul 9. Frozen; never force-pushed |
| 1.0.x | Jul 10–21 | README/video polish only |
| **2.x** | Prototype phase (Jul 22–31) | `v2.0-sandbox` = adapter swap live on IDBI sandbox; `v2.1` = GBM trained on IDBI data; `v2.2` = RM override |
| **3.0** | Demo Day build (Aug 21) | `v3.0-demo-day`, frozen 48 h before |

Release ritual (lightweight): gate passes → tag → deploy → persona-walkthrough smoke test → tracker update → one line in `CHANGELOG.md`.

### Model & scorecard versioning — separate from app version (governance story)
Every score response and audit row carries three stamps:
```json
{"engine_version": "1.0.0", "scorecard_version": "SC-2026.07.1", "dataset_version": "DS-42-2026.07"}
```
- **scorecard_version** (`SC-YYYY.MM.rev`): bins/points/weights config. Any weight change = new version — never edited in place. Old versions retained (draft MRM: decommissioned models retained; we mirror the principle at PoC scale).
- **dataset_version** (`DS-<seed>-YYYY.MM`): generator version + seed; regeneration = new version, stamped in `data/index.json`.
- **model artifact** (stretch GBM): serialized with metadata (train date, dataset_version, monotonic constraints, feature list); loaded at startup; `GET /model/version` endpoint exposes all three stamps.

Why the jury cares: this is RBI draft-MRM-2026 model governance (inventory, versioning, reproducibility) demonstrated at PoC scale — most teams will show a score; we show a *governed* score.

### Attribution rule (repo-wide)
All commits/co-author trailers attribute to **MCS-Labs** (`Co-Authored-By: MCS-Labs <dev@mconnectsolutions.com>`). No AI-vendor names in git history, commit messages, or release notes. (Also recorded in 08-git-workflow.md.)
