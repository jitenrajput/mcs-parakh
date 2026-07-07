"""Demo-canon regression — the exact numbers the demo script and deck promise.

Canon per docs/12-score-policy.md (reconciled Jul 07, 2026):
781 / 692 ± 35 → 721 (+₹3.9L) / 409, kill-switch staircase 781 → 768 → 759 → Low.
If any assertion here fails, a demo beat is broken: fix the regression, or
re-verify live and amend docs/12 + every downstream doc BEFORE filming/demo day.

Run from backend/:  python -m pytest api/tests/test_demo_canon.py -q
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from fastapi.testclient import TestClient  # noqa: E402

from api.main import app, registry  # noqa: E402

client = TestClient(app)

RAMESH, MEENA, DINESH = "24AAACS1234F1Z5", "24AABCT9876K1Z3", "24AADCM4321P1Z8"


def teardown_function():
    registry.killed.clear()


def score(gstin):
    return client.post("/score", json={"gstin": gstin}).json()


def test_persona_canon():
    r = score(RAMESH)
    assert (r["score"], r["band"], r["confidence"], r["confidence_width"]) == (781, "Prime", "High", 15)
    assert r["eligibility"]["indicative_limit"] == 7_523_135  # the ₹75.2L CGTMSE lead

    m = score(MEENA)
    assert (m["score"], m["band"], m["confidence"], m["confidence_width"]) == (692, "Watch", "Medium", 35)

    d = score(DINESH)
    assert (d["score"], d["band"]) == (409, "Critical")
    assert d["eligibility"]["indicative_limit"] == 0  # Critical band multiplier = 0%


def test_dinesh_alert_text_matches_script():
    p = client.get("/portfolio").json()
    row = next(x for x in p["msmes"] if x["gstin"] == DINESH)
    assert any("EMI burden 93% of inflows" in a["text"] for a in row["alerts"])


def test_kal_parakh_canonical_moment():
    sim = client.post("/simulate", json={"gstin": MEENA, "actions": ["gst_on_time_3m"]}).json()
    assert sim["before"]["score"] == 692 and sim["after"]["score"] == 721
    assert sim["after"]["band"] == "Good"
    assert sim["delta_limit"] == 386_503  # +₹3.9L — THE moment


def test_killswitch_staircase_and_exact_restore():
    assert score(RAMESH)["score"] == 781

    client.post("/admin/killswitch", json={"source_id": "bureau", "killed": True})
    s1 = score(RAMESH)
    assert (s1["score"], s1["band"], s1["confidence"]) == (768, "Good", "Medium")
    assert s1["eligibility"]["indicative_limit"] == 6_018_508  # ₹60.2L — limit visibly drops

    client.post("/admin/killswitch", json={"source_id": "epfo_ecr", "killed": True})
    s2 = score(RAMESH)
    assert (s2["score"], s2["confidence"]) == (759, "Medium")

    client.post("/admin/killswitch", json={"source_id": "upi_months", "killed": True})
    s3 = score(RAMESH)
    assert s3["confidence"] == "Low"
    assert s3["eligibility"]["indicative_limit"] == 4_513_881  # ₹45.1L — lower-edge rule at Low

    for s in ("bureau", "epfo_ecr", "upi_months"):
        client.post("/admin/killswitch", json={"source_id": s, "killed": False})
    r = score(RAMESH)
    assert r["score"] == 781 and r["eligibility"]["indicative_limit"] == 7_523_135  # deterministic replay
