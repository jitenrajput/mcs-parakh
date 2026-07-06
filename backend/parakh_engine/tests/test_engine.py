"""P1 gate tests — canonical personas, determinism, degradation, monotonicity.

Run from backend/:  python -m pytest parakh_engine/tests -q
"""

import copy
import json
from pathlib import Path

import pytest

from parakh_engine import score, score_with_overrides

DATA = Path(__file__).resolve().parents[3] / "data"

RAMESH = "24AAACS1234F1Z5"
MEENA = "24AABCT9876K1Z3"
DINESH = "24AADCM4321P1Z8"


def load(gstin: str) -> dict:
    return json.loads((DATA / "msmes" / f"{gstin}.json").read_text())


# ---- P1 gate: canonical persona numbers (docs/12-score-policy.md) -------------

def test_ramesh_prime():
    r = score(load(RAMESH))
    assert 770 <= r.score <= 795
    assert r.band == "Prime"
    assert r.confidence == "High" and r.confidence_width == 15
    assert not r.missing_sources


def test_meena_watch_medium_confidence():
    r = score(load(MEENA))
    assert 680 <= r.score <= 700
    assert r.band == "Watch"
    assert r.confidence == "Medium" and r.confidence_width == 35
    assert set(r.missing_sources) == {"bureau", "epfo_ecr"}  # NTC, no payroll


def test_dinesh_critical():
    r = score(load(DINESH))
    assert 395 <= r.score <= 425
    assert r.band == "Critical"
    assert r.eligibility["indicative_limit"] == 0  # Critical multiplier = 0


# ---- Determinism (NFR-6) -------------------------------------------------------

def test_deterministic():
    rec = load(MEENA)
    assert score(rec).to_dict() == score(copy.deepcopy(rec)).to_dict()


# ---- Graceful degradation (FR-1.4 / kill-switch) --------------------------------

def test_killing_source_widens_band_never_crashes():
    full = score(load(RAMESH))
    degraded = score_with_overrides(load(RAMESH), drop_sources=["bureau"])
    assert degraded.confidence_width > full.confidence_width
    assert degraded.score > 300  # still scores, no crash

    barely = score_with_overrides(load(RAMESH), drop_sources=["bureau", "gst_returns"])
    assert barely.confidence == "Low" and barely.confidence_width == 60


def test_missing_source_is_unknown_not_bad():
    """Neutral prior: killing EPFO must not crater the score."""
    full = score(load(RAMESH))
    no_epfo = score_with_overrides(load(RAMESH), drop_sources=["epfo_ecr"])
    assert abs(full.score - no_epfo.score) < 60


# ---- Monotonicity spot-checks (regulator-defensible directions) -----------------

def test_higher_emi_lowers_obligation_and_score():
    rec = load(RAMESH)
    worse = copy.deepcopy(rec)
    for m in worse["sources"]["aa_deposit"]["monthly_aggregates"]:
        m["emi_debits"] *= 5
    r0, r1 = score(rec), score(worse)
    assert r1.dimensions["obligation"]["score"] < r0.dimensions["obligation"]["score"]
    assert r1.score < r0.score


def test_late_gst_lowers_compliance_and_score():
    rec = load(RAMESH)
    worse = copy.deepcopy(rec)
    for ret in worse["sources"]["gst_returns"]:
        for form in ("gstr1", "gstr3b"):
            if ret[form]["dof"]:
                due = ret[form]["due_dt"]
                y, m, d = due.split("-")
                ret[form]["dof"] = f"{y}-{m}-{min(int(d) + 20, 28):02d}"
    r0, r1 = score(rec), score(worse)
    assert r1.dimensions["compliance"]["score"] < r0.dimensions["compliance"]["score"]
    assert r1.score < r0.score


# ---- Eligibility: lower-edge rule ------------------------------------------------

def test_eligibility_lower_edge_rule():
    r = score(load(MEENA))  # 691 +/- 35 -> lower edge 656 -> Watch (60%)
    assert r.band_lower_edge == "Watch"
    assert r.eligibility["band_multiplier"] == 0.60
    assert r.eligibility["indicative_limit"] == round(r.eligibility["nayak_ceiling"] * 0.60)


# ---- Version stamps (governance) --------------------------------------------------

def test_version_stamps_present():
    r = score(load(RAMESH))
    assert r.versions["engine"] and r.versions["scorecard"].startswith("SC-")
    assert r.versions["dataset"].startswith("DS-")
