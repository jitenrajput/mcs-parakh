"""API smoke tests — the demo flow end-to-end (P2 backend half).

Run from backend/:  python -m pytest api/tests -q
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from fastapi.testclient import TestClient  # noqa: E402

from api.main import app, registry  # noqa: E402

client = TestClient(app)

MEENA = "24AABCT9876K1Z3"
DINESH = "24AADCM4321P1Z8"


def teardown_function():
    registry.killed.clear()


def test_demo_flow_consent_then_score():
    consent = client.post("/consent", json={"gstin": MEENA, "purpose_code": "103"}).json()
    assert consent["consent_id"].startswith("CNS-")
    r = client.post("/score", json={"gstin": MEENA, "consent_id": consent["consent_id"]}).json()
    assert 680 <= r["score"] <= 700 and r["band"] == "Watch"
    assert r["synthetic"] is True and r["consent_id"] == consent["consent_id"]
    statuses = {f["source"]: f["status"] for f in r["fetches"]}
    assert statuses["aa_deposit"] == "OK" and statuses["gst_returns"] == "OK"


def test_killswitch_widens_band():
    base = client.post("/score", json={"gstin": DINESH}).json()
    client.post("/admin/killswitch", json={"source_id": "gst_returns", "killed": True})
    degraded = client.post("/score", json={"gstin": DINESH}).json()
    assert degraded["confidence_width"] > base["confidence_width"]
    assert any(f["source"] == "gst_returns" and f["status"] == "FAILED"
               for f in degraded["fetches"])


def test_kal_parakh_meena_crosses_to_good():
    """The canonical wow: GST discipline lifts Meena into the Good band."""
    sim = client.post("/simulate", json={
        "gstin": MEENA, "actions": ["gst_on_time_3m", "gst_on_time_6m"]}).json()
    assert sim["delta_score"] > 0
    assert sim["after"]["band"] in ("Good", "Prime")
    assert sim["delta_limit"] > 0  # rupee-denominated outcome (UX hard rule)


def test_portfolio_has_alerts_and_personas():
    p = client.get("/portfolio").json()
    assert p["count"] >= 60 and p["with_alerts"] >= 2
    flagged = [m for m in p["msmes"] if m["watchlist"]]
    assert all(m["alerts"] for m in flagged), "watchlist accounts must fire alerts"
    assert any(m["demo_persona"] for m in p["msmes"])


def test_unknown_gstin_is_designed_error():
    r = client.post("/score", json={"gstin": "24ZZZZZ9999Z9Z9"})
    assert r.status_code == 404 and "persona" in r.json()["detail"]


def test_audit_and_versions():
    client.post("/score", json={"gstin": MEENA})
    audit = client.get("/audit/recent").json()
    assert audit["entries"] and audit["entries"][0]["scorecard_version"].startswith("SC-")
    v = client.get("/model/version").json()
    assert v["dataset"].startswith("DS-")
