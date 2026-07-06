"""Feature extraction — deterministic, per-source, auditable.

Input: the `sources` dict of an MSME record (same shape the mock adapters emit,
and the same shape IDBI sandbox adapters must map to in the prototype phase).
Output: flat feature dict (None = source absent -> neutral prior downstream)
plus a coverage map of which sources were available.
"""

from __future__ import annotations

import statistics as st

from . import config


def _mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else 0.0


def extract(sources: dict, profile: dict) -> tuple[dict, dict]:
    f: dict[str, float | None] = {}
    coverage = {s: bool(sources.get(s)) for s in config.MAJOR_SOURCES + config.MINOR_SOURCES}

    # ---- AA bank (monthly aggregates over last 12m) ---------------------------
    bank = (sources.get("aa_deposit") or {}).get("monthly_aggregates") or []
    last12 = bank[-12:]
    if last12:
        credits = [m["total_credits"] for m in last12]
        debits = [m["total_debits"] for m in last12]
        mu = _mean(credits)
        f["inflow_cov"] = (st.pstdev(credits) / mu) if mu > 0 else None
        avg_debit = _mean(debits)
        f["balance_floor_ratio"] = (_mean([m["min_balance"] for m in last12]) / avg_debit) if avg_debit > 0 else None
        tot_c = sum(credits)
        f["net_margin"] = (tot_c - sum(debits)) / tot_c if tot_c > 0 else None
        f["emi_to_inflow"] = sum(m["emi_debits"] for m in last12) / tot_c if tot_c > 0 else None
        f["bounces_12m"] = float(sum(m["inward_bounce_count"] for m in last12))
    else:
        f.update({k: None for k in ("inflow_cov", "balance_floor_ratio", "net_margin",
                                    "emi_to_inflow", "bounces_12m")})

    # ---- GST (turnover over 12 periods; filing DISCIPLINE over the recent 6 —
    # recency window: momentum is creditable, and improvement actions must move
    # the score the way a bank's rolling review would) ---------------------------
    gst = (sources.get("gst_returns") or [])[-12:]
    if gst:
        missed, gaps, turnovers = 0, [], []
        delays6, late6 = [], 0
        recent6 = gst[-6:]
        for r in gst:
            g3 = r["gstr3b"]
            if g3["status"] == "NF" or g3["dof"] is None:
                missed += 1
                continue
            gaps.append(r.get("gstr1_vs_3b_gap_pct", 0.0))
            turnovers.append(r["gstr1"]["ttl_val"])
        for r in recent6:
            g3 = r["gstr3b"]
            if g3["status"] == "NF" or g3["dof"] is None:
                continue
            d = _days_between(g3["due_dt"], g3["dof"])
            delays6.append(max(0, d))
            if d > 5:
                late6 += 1
        f["gst_avg_delay_days"] = _mean(delays6) if delays6 else 30.0
        f["gst_late_count_6m"] = float(late6)
        f["gst_missed_12m"] = float(missed)
        f["gstr1_3b_gap_pct"] = _mean(gaps) if gaps else 8.0
        # growth from declared turnover (robust MoM slope, trimmed)
        if len(turnovers) >= 6:
            mom = [(b - a) / a for a, b in zip(turnovers, turnovers[1:]) if a > 0]
            mom_sorted = sorted(mom)
            trim = mom_sorted[1:-1] if len(mom_sorted) > 4 else mom_sorted
            f["turnover_slope_pct"] = _mean(trim)
            f["growth_volatility"] = st.pstdev(mom) if len(mom) > 1 else 0.0
            half = len(turnovers) // 2
            recent3, prior3 = turnovers[-3:], turnovers[-6:-3] or turnovers[:half]
            f["growth_q_pct"] = (_mean(recent3) - _mean(prior3)) / _mean(prior3) if _mean(prior3) > 0 else None
        else:
            f["turnover_slope_pct"] = f["growth_volatility"] = f["growth_q_pct"] = None
        f["annual_turnover"] = float(sum(r["gstr1"]["ttl_val"] for r in gst))
    else:
        f.update({k: None for k in ("gst_avg_delay_days", "gst_late_count_12m", "gst_missed_12m",
                                    "gstr1_3b_gap_pct", "turnover_slope_pct", "growth_volatility",
                                    "growth_q_pct")})
        # fallback annual turnover from bank credits (conservative haircut)
        f["annual_turnover"] = sum(m["total_credits"] for m in last12) * 0.95 if last12 else None

    # ---- Bureau ----------------------------------------------------------------
    bureau = sources.get("bureau")
    f["bureau_max_dpd"] = float(bureau["max_dpd_12m"]) if bureau else None

    # ---- EPFO (employer-consented path) ----------------------------------------
    ecr = sources.get("epfo_ecr") or []
    last12e = ecr[-12:]
    f["payroll_on_time"] = (_mean([1.0 if e["paid_on_time"] else 0.0 for e in last12e])
                            if last12e else None)
    f["employees"] = float(last12e[-1]["total_members"]) if last12e else (
        float(profile.get("employees", 0)) or None)

    # ---- Profile-derived ---------------------------------------------------------
    f["vintage_years"] = float(profile.get("vintage_years") or 0.5)
    f["udyam_registered"] = 1.0 if profile.get("udyam_registered") else 0.0

    return f, coverage


def _days_between(d1: str, d2: str) -> int:
    import datetime as _dt
    a = _dt.date.fromisoformat(d1)
    b = _dt.date.fromisoformat(d2)
    return (b - a).days
