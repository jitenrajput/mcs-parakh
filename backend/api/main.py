"""MCS Parakh — Score-as-a-Service API (PoC).

FastAPI + Pydantic v2. OpenAPI at /docs is part of the demo (ULI-ready spec).
All data is SYNTHETIC (DS-42-2026.07); every mock is labeled. Consent is a
first-class object: every fetch and score carries a consent reference, every
decision lands in the audit log with version stamps (draft-MRM alignment).
"""

from __future__ import annotations

import json
import os
import sqlite3
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # backend/ on path

from adapters import AdapterRegistry, SOURCE_IDS, SOURCE_LABELS  # noqa: E402
from parakh_engine import score as engine_score, ENGINE_VERSION, SCORECARD_VERSION  # noqa: E402
from parakh_engine.monitoring import score_series, alerts_for, simulate, ACTIONS  # noqa: E402

DATA_DIR = Path(os.environ.get("PARAKH_DATA", Path(__file__).resolve().parents[2] / "data"))
DB_PATH = Path(os.environ.get("PARAKH_DB", Path(__file__).resolve().parents[1] / "parakh.db"))

app = FastAPI(
    title="MCS Parakh — MSME Financial Health API",
    version=ENGINE_VERSION,
    description="Two-sided, explainable MSME Financial Health Card for IDBI Innovate 2026. "
                "**All data is synthetic** (schema-faithful to ReBIT/GSTR conventions). "
                "Adapter layer swaps to IDBI sandbox APIs in the prototype phase — "
                "scoring code unchanged.",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

registry = AdapterRegistry(DATA_DIR)
_index_cache: dict | None = None
_portfolio_cache: list | None = None


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS consents (
        consent_id TEXT PRIMARY KEY, gstin TEXT, purpose_code TEXT, purpose_text TEXT,
        fi_types TEXT, data_range TEXT, expiry TEXT, status TEXT, created TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, gstin TEXT, consent_id TEXT,
        score INTEGER, band TEXT, confidence TEXT, coverage TEXT,
        engine_version TEXT, scorecard_version TEXT, dataset_version TEXT)""")
    return conn


def load_index() -> dict:
    global _index_cache
    if _index_cache is None:
        _index_cache = json.loads((DATA_DIR / "index.json").read_text())
    return _index_cache


def load_record(gstin: str) -> dict:
    path = DATA_DIR / "msmes" / f"{gstin}.json"
    if not path.exists():
        raise HTTPException(404, f"GSTIN {gstin} not in the synthetic dataset. "
                                 f"Try a demo persona from GET /msmes.")
    return json.loads(path.read_text())


# ---------- models ----------

class ConsentRequest(BaseModel):
    gstin: str
    purpose_code: str = Field("103", description="AA purpose: 103 one-time underwriting, 104 monitoring")
    fi_types: list[str] = ["DEPOSIT", "GSTR1_3B"]
    range_months: int = 24


class ScoreRequest(BaseModel):
    gstin: str
    consent_id: str | None = None  # minted automatically for the demo if absent


class SimulateRequest(BaseModel):
    gstin: str
    actions: list[str]


class KillSwitchRequest(BaseModel):
    source_id: str
    killed: bool


# ---------- endpoints ----------

@app.get("/", tags=["meta"])
def root():
    return dict(product="MCS Parakh", tagline="Every genuine business, recognized.",
                synthetic_data=True, docs="/docs", version="/model/version")


@app.get("/model/version", tags=["meta"])
def model_version():
    return dict(engine=ENGINE_VERSION, scorecard=SCORECARD_VERSION,
                dataset=load_index()["dataset_version"])


@app.get("/msmes", tags=["directory"])
def list_msmes():
    idx = load_index()
    return dict(synthetic=True, dataset_version=idx["dataset_version"], msmes=idx["msmes"])


@app.post("/consent", tags=["consent"])
def create_consent(req: ConsentRequest):
    """AA-style consent artefact stub (Master Direction para 6.3 fields)."""
    now = datetime.now(timezone.utc)
    consent_id = f"CNS-{uuid.uuid4().hex[:12].upper()}"
    with db() as conn:
        conn.execute("INSERT INTO consents VALUES (?,?,?,?,?,?,?,?,?)",
                     (consent_id, req.gstin, req.purpose_code,
                      "Aggregated statement for credit underwriting" if req.purpose_code == "103"
                      else "Ongoing monitoring of accounts",
                      ",".join(req.fi_types), f"last {req.range_months} months",
                      (now + timedelta(days=90)).isoformat(), "ACTIVE", now.isoformat()))
    return dict(consent_id=consent_id, status="ACTIVE", purpose_code=req.purpose_code,
                data_consumer="IDBI-Parakh-PoC (FIU)", revocable="anytime",
                note="Mock consent journey — mirrors the ReBIT consent artefact fields. "
                     "AA is data-blind; data flows encrypted FIP→FIU.")


@app.get("/consent/{consent_id}", tags=["consent"])
def get_consent(consent_id: str):
    with db() as conn:
        row = conn.execute("SELECT * FROM consents WHERE consent_id=?", (consent_id,)).fetchone()
    if not row:
        raise HTTPException(404, "consent not found")
    keys = ["consent_id", "gstin", "purpose_code", "purpose_text", "fi_types",
            "data_range", "expiry", "status", "created"]
    return dict(zip(keys, row))


@app.post("/score", tags=["scoring"])
async def score_msme(req: ScoreRequest):
    """Fan out adapters (respecting kill-switches) → score → audit. UC1/UC5."""
    consent_id = req.consent_id or create_consent(ConsentRequest(gstin=req.gstin))["consent_id"]
    record = load_record(req.gstin)  # profile only; sources come via adapters
    fetches = await registry.fetch_all(req.gstin, consent_id)
    record_for_scoring = dict(record, sources=registry.to_sources(fetches))
    result = engine_score(record_for_scoring)

    with db() as conn:
        conn.execute("INSERT INTO audit_log (ts,gstin,consent_id,score,band,confidence,"
                     "coverage,engine_version,scorecard_version,dataset_version) "
                     "VALUES (?,?,?,?,?,?,?,?,?,?)",
                     (datetime.now(timezone.utc).isoformat(), req.gstin, consent_id,
                      result.score, result.band, result.confidence,
                      json.dumps(result.coverage), *result.versions.values()))

    return dict(
        **result.to_dict(),
        consent_id=consent_id,
        fetches=[dict(source=s, label=SOURCE_LABELS[s], status=f.status,
                      error=f.error) for s, f in fetches.items()],
        synthetic=True,
    )


@app.get("/score/{gstin}", tags=["scoring"])
def get_score(gstin: str):
    """Direct score from the full record (no adapter theatre) — for deep links."""
    result = engine_score(load_record(gstin))
    return dict(**result.to_dict(), synthetic=True)


@app.get("/explain/{gstin}", tags=["scoring"])
def explain(gstin: str):
    r = engine_score(load_record(gstin))
    return dict(gstin=gstin, name=r.name, score=r.score, band=r.band,
                dimensions=r.dimensions,
                reasons_positive=r.reasons_positive, reasons_negative=r.reasons_negative,
                confidence=dict(label=r.confidence, width=r.confidence_width,
                                missing_sources=r.missing_sources,
                                note="Eligibility uses the LOWER edge of the band — "
                                     "confidence is consequential, not decorative."),
                versions=r.versions, synthetic=True)


@app.post("/simulate", tags=["kal-parakh"])
def kal_parakh(req: SimulateRequest):
    """Kal-Parakh: re-runs the REAL engine with modified inputs (FR-4.8)."""
    for a in req.actions:
        if a not in ACTIONS:
            raise HTTPException(422, f"unknown action '{a}'; see GET /simulate/actions")
    return dict(gstin=req.gstin, **simulate(load_record(req.gstin), req.actions), synthetic=True)


@app.get("/simulate/actions", tags=["kal-parakh"])
def simulate_actions():
    return dict(actions=[dict(id=k, **v) for k, v in ACTIONS.items()])


@app.get("/portfolio", tags=["portfolio"])
def portfolio(refresh: bool = False):
    """Lender book: every MSME scored + trend + Parakh Watch alerts (UC2)."""
    global _portfolio_cache
    if _portfolio_cache is None or refresh:
        rows = []
        for m in load_index()["msmes"]:
            record = load_record(m["gstin"])
            r = engine_score(record)
            series = score_series(record)
            alerts = alerts_for(record, series)
            rows.append(dict(
                gstin=m["gstin"], name=m["name"], city=m["city"],
                score=r.score, band=r.band, confidence=r.confidence,
                grade_summary={d: v["grade"] for d, v in r.dimensions.items()},
                trend=series,
                delta_1m=(series[-1]["score"] - series[-2]["score"]) if len(series) > 1 else 0,
                alerts=alerts,
                top_risk=(r.reasons_negative[0]["text"] if r.reasons_negative else None),
                demo_persona=m.get("demo_persona", False),
                watchlist=m.get("watchlist", False),
                indicative_limit=r.eligibility["indicative_limit"],
            ))
        rows.sort(key=lambda x: (len(x["alerts"]) == 0, x["delta_1m"]))
        _portfolio_cache = rows
    alerts_n = sum(1 for r in _portfolio_cache if r["alerts"])
    return dict(count=len(_portfolio_cache), with_alerts=alerts_n,
                msmes=_portfolio_cache, synthetic=True)


@app.get("/admin/killswitch", tags=["demo-control"])
def killswitch_state():
    return dict(sources=[dict(source_id=s, label=SOURCE_LABELS[s],
                              killed=s in registry.killed) for s in SOURCE_IDS],
                note="Demo control (S9): kill a source, re-score, watch the band widen.")


@app.post("/admin/killswitch", tags=["demo-control"])
def killswitch_set(req: KillSwitchRequest):
    try:
        registry.set_killed(req.source_id, req.killed)
    except KeyError:
        raise HTTPException(422, f"unknown source '{req.source_id}'")
    return killswitch_state()


@app.get("/audit/recent", tags=["governance"])
def audit_recent(limit: int = 20):
    with db() as conn:
        rows = conn.execute("SELECT ts,gstin,consent_id,score,band,confidence,"
                            "engine_version,scorecard_version,dataset_version "
                            "FROM audit_log ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    keys = ["ts", "gstin", "consent_id", "score", "band", "confidence",
            "engine_version", "scorecard_version", "dataset_version"]
    return dict(note="Every score is reconstructable: inputs coverage + consent ref + "
                     "model versions (RBI draft-MRM 2026 alignment).",
                entries=[dict(zip(keys, r)) for r in rows])
