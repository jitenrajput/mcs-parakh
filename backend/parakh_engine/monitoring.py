"""Parakh Watch — score time-series + deterioration alerts (FR-1.5/1.6).

Score is a pure function of a time-windowed snapshot, so continuous monitoring
is just re-scoring on rolling monthly windows. Alert rules are transparent,
same as everything else in the engine.
"""

from __future__ import annotations

import copy

from .engine import score

TREND_MONTHS = 8          # points on the sparkline
ALERT_DROP_1M = 40        # points lost in one month
ALERT_SLOPE_MONTHS = 3    # consecutive declining months


def _slice_record(record: dict, drop_last_n: int) -> dict:
    """Snapshot of the record as it looked `drop_last_n` months ago."""
    if drop_last_n == 0:
        return record
    rec = copy.deepcopy(record)
    src = rec["sources"]
    if src.get("aa_deposit"):
        src["aa_deposit"]["monthly_aggregates"] = \
            src["aa_deposit"]["monthly_aggregates"][:-drop_last_n]
    for key in ("gst_returns", "upi_months", "epfo_ecr"):
        if src.get(key):
            src[key] = src[key][:-drop_last_n]
    return rec


def score_series(record: dict, months: int = TREND_MONTHS) -> list[dict]:
    """Oldest-first list of {period, score} over the trailing window."""
    bank = (record["sources"].get("aa_deposit") or {}).get("monthly_aggregates") or []
    out = []
    for back in range(months - 1, -1, -1):
        snap = _slice_record(record, back)
        agg = (snap["sources"].get("aa_deposit") or {}).get("monthly_aggregates") or []
        if len(agg) < 12:  # need a full feature window
            continue
        out.append(dict(period=bank[-(back + 1)]["period"] if back < len(bank) else None,
                        score=score(snap).score))
    return out


def alerts_for(record: dict, series: list[dict]) -> list[dict]:
    """Transparent trip-wires; each alert carries its reason."""
    out = []
    scores = [p["score"] for p in series]
    if len(scores) >= 2 and scores[-2] - scores[-1] >= ALERT_DROP_1M:
        out.append(dict(rule="sharp_drop",
                        text=f"Score fell {scores[-2] - scores[-1]} points in one month"))
    if len(scores) >= ALERT_SLOPE_MONTHS + 1:
        tail = scores[-(ALERT_SLOPE_MONTHS + 1):]
        if all(b < a for a, b in zip(tail, tail[1:])):
            out.append(dict(rule="declining_trend",
                            text=f"Score declining {ALERT_SLOPE_MONTHS} months in a row "
                                 f"({tail[0]} → {tail[-1]})"))
    bank = (record["sources"].get("aa_deposit") or {}).get("monthly_aggregates") or []
    recent = bank[-3:]
    bounces = sum(m["inward_bounce_count"] for m in recent)
    if bounces >= 2:
        out.append(dict(rule="bounces", text=f"{bounces} payment bounces in last 3 months"))
    gst = (record["sources"].get("gst_returns") or [])[-3:]
    missed = sum(1 for r in gst if r["gstr3b"]["status"] == "NF")
    if missed:
        out.append(dict(rule="gst_lapse", text=f"{missed} GST return(s) not filed recently"))
    if recent:
        credits = sum(m["total_credits"] for m in recent)
        emi = sum(m["emi_debits"] for m in recent)
        if credits > 0 and emi / credits > 0.25:
            out.append(dict(rule="emi_pressure",
                            text=f"EMI burden {emi / credits:.0%} of inflows"))
    return out


# ---- Kal-Parakh: honest simulation = modify inputs, re-run the real engine ----

ACTIONS = {
    "gst_on_time_3m": dict(
        label="File GSTR-1 & 3B on time for the next 3 months",
        hint="Sets the 3 most recent filings to their due date"),
    "gst_on_time_6m": dict(
        label="File GSTR-1 & 3B on time for 6 months",
        hint="Sets the 6 most recent filings to their due date"),
    "clear_bounces_6m": dict(
        label="No payment bounces for 6 months",
        hint="Clears inward bounces in the last 6 months"),
    "reduce_emi_25pct": dict(
        label="Refinance / part-prepay EMIs (−25%)",
        hint="Reduces EMI debits 25% across the last 12 months"),
}


def apply_action(record: dict, action_id: str) -> dict:
    rec = copy.deepcopy(record)
    src = rec["sources"]
    if action_id in ("gst_on_time_3m", "gst_on_time_6m"):
        n = 3 if action_id.endswith("3m") else 6
        for ret in (src.get("gst_returns") or [])[-n:]:
            for form in ("gstr1", "gstr3b"):
                ret[form]["dof"] = ret[form]["due_dt"]
                ret[form]["status"] = "FIL"
    elif action_id == "clear_bounces_6m":
        for m in ((src.get("aa_deposit") or {}).get("monthly_aggregates") or [])[-6:]:
            m["inward_bounce_count"] = 0
    elif action_id == "reduce_emi_25pct":
        for m in ((src.get("aa_deposit") or {}).get("monthly_aggregates") or [])[-12:]:
            m["emi_debits"] = round(m["emi_debits"] * 0.75)
    else:
        raise KeyError(action_id)
    return rec


def simulate(record: dict, action_ids: list[str]) -> dict:
    before = score(record)
    rec = record
    for a in action_ids:
        rec = apply_action(rec, a)
    after = score(rec)
    return dict(
        actions=[dict(id=a, **ACTIONS[a]) for a in action_ids],
        before=dict(score=before.score, band=before.band,
                    indicative_limit=before.eligibility["indicative_limit"]),
        after=dict(score=after.score, band=after.band,
                   indicative_limit=after.eligibility["indicative_limit"]),
        delta_score=after.score - before.score,
        delta_limit=after.eligibility["indicative_limit"] - before.eligibility["indicative_limit"],
        note="Projection re-runs the actual scoring engine with modified inputs — not an animation.",
    )
