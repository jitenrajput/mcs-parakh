"""Synthetic MSME data generator v2 — MCS Parakh (IDBI Innovate 2026 PoC).

ALL DATA IS SYNTHETIC. Schemas are field-faithful to public conventions so the
adapter layer can swap in IDBI sandbox APIs during the prototype phase:
  - AA bank data  -> ReBIT deposit.xsd shape (Profile/Summary/Transactions)
  - GST returns   -> GSTR-1 / GSTR-3B records with due & filing dates
  - EPFO ECR      -> employer-consented path (NOT via AA - see docs/12)
  - Bureau        -> CMR-style commercial report (null for new-to-credit)

Canonical persona numbers come from docs/12-score-policy.md - do not drift.

Usage:  python generate.py --count 60 --months 24 --out ../../data --seed 42
"""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

GEN_VERSION = "parakh-datagen 2.0 (MCS-Labs)"
ANCHOR_YEAR, ANCHOR_MONTH = 2026, 6  # last complete data month

STATE_CODES = ["24", "27", "07", "29", "33", "09", "06", "08"]
CITIES = {
    "24": ["Ahmedabad", "Surat", "Rajkot", "Vadodara"],
    "27": ["Mumbai", "Pune", "Nagpur"], "07": ["New Delhi"],
    "29": ["Bengaluru", "Mysuru"], "33": ["Chennai", "Coimbatore"],
    "09": ["Noida", "Lucknow"], "06": ["Gurugram", "Faridabad"],
    "08": ["Jaipur", "Udaipur"],
}
NAME_A = ["Shree", "Om", "Jay", "New", "Royal", "Krishna", "Ganesh", "Balaji", "Shakti",
          "Sunrise", "Apex", "Prime", "Silver", "Golden", "National", "Modern", "Classic"]
NAME_B = ["Auto Components", "Textiles", "Traders", "Electronics", "Packaging",
          "Engineering Works", "Food Products", "Plastics", "Enterprises", "Industries",
          "Exports", "Agro Foods", "Pharma Distributors", "Steel Works", "Garments", "Ceramics"]
SECTORS = {"Auto Components": "manufacturing", "Textiles": "manufacturing", "Traders": "trading",
           "Electronics": "trading", "Packaging": "manufacturing", "Engineering Works": "manufacturing",
           "Food Products": "manufacturing", "Plastics": "manufacturing", "Enterprises": "trading",
           "Industries": "manufacturing", "Exports": "trading", "Agro Foods": "trading",
           "Pharma Distributors": "trading", "Steel Works": "manufacturing", "Garments": "manufacturing",
           "Ceramics": "manufacturing"}

# Behavioural archetypes --------------------------------------------------------
ARCHETYPES = {
    "healthy_manufacturer": dict(
        weight=0.25, turnover_lakh=(8, 40), growth=(0.012, 0.02), season_amp=0.05,
        gst_delay_days=(0, 3), gst_miss_prob=0.0, underreport=0.02,
        emi_ratio=(0.04, 0.08), bounce_prob=0.01, employees=(6, 25), epfo_ontime=0.97,
        upi_share=(0.25, 0.45), cash_share=(0.05, 0.12), ntc_prob=0.05, vintage=(5, 18),
        collection_ratio=(0.95, 1.02), min_bal_months=(1.2, 2.5), dpd_pool=[0, 0, 0, 0, 15],
    ),
    "growth_ecom": dict(
        weight=0.20, turnover_lakh=(3, 15), growth=(0.05, 0.03), season_amp=0.10,
        gst_delay_days=(4, 8), gst_miss_prob=0.02, underreport=0.03,
        emi_ratio=(0.0, 0.03), bounce_prob=0.015, employees=(0, 6), epfo_ontime=0.90,
        upi_share=(0.65, 0.9), cash_share=(0.0, 0.04), ntc_prob=0.75, vintage=(1, 4),
        collection_ratio=(0.98, 1.05), min_bal_months=(0.6, 1.5), dpd_pool=[0, 0, 15],
    ),
    "stable_services": dict(
        weight=0.20, turnover_lakh=(2, 12), growth=(0.004, 0.015), season_amp=0.03,
        gst_delay_days=(1, 5), gst_miss_prob=0.01, underreport=0.03,
        emi_ratio=(0.03, 0.09), bounce_prob=0.02, employees=(2, 10), epfo_ontime=0.92,
        upi_share=(0.4, 0.6), cash_share=(0.03, 0.1), ntc_prob=0.25, vintage=(3, 12),
        collection_ratio=(0.93, 1.0), min_bal_months=(0.8, 1.8), dpd_pool=[0, 0, 0, 15, 30],
    ),
    "seasonal_retailer": dict(
        weight=0.15, turnover_lakh=(3, 18), growth=(0.006, 0.02), season_amp=0.35,
        gst_delay_days=(3, 8), gst_miss_prob=0.03, underreport=0.05,
        emi_ratio=(0.05, 0.11), bounce_prob=0.03, employees=(1, 8), epfo_ontime=0.85,
        upi_share=(0.5, 0.75), cash_share=(0.08, 0.2), ntc_prob=0.35, vintage=(2, 10),
        collection_ratio=(0.9, 1.0), min_bal_months=(0.4, 1.2), dpd_pool=[0, 0, 15, 30],
    ),
    "stressed_trader": dict(
        weight=0.20, turnover_lakh=(2, 20), growth=(-0.03, 0.02), season_amp=0.08,
        gst_delay_days=(12, 22), gst_miss_prob=0.10, underreport=0.10,
        emi_ratio=(0.14, 0.24), bounce_prob=0.16, employees=(0, 8), epfo_ontime=0.55,
        upi_share=(0.3, 0.55), cash_share=(0.12, 0.3), ntc_prob=0.2, vintage=(2, 12),
        collection_ratio=(0.8, 0.95), min_bal_months=(0.05, 0.4), dpd_pool=[30, 60, 90],
    ),
}

# Canonical demo personas (docs/12-score-policy.md) — numbers must not drift ----
DEMO_PERSONAS = [
    dict(gstin="24AAACS1234F1Z5", name="Shree Ganesh Auto Components", owner="Rameshbhai Patel",
         city="Rajkot", state="24", archetype="healthy_manufacturer", ntc=False, seed=101,
         over=dict(turnover_lakh=24, growth=(0.015, 0.008), gst_delay_days=(0, 2),
                   emi_ratio=0.06, employees=18, vintage=12.0, epfo_ontime=0.98,
                   upi_share=0.30, min_bal_months=2.0, bounce_prob=0.0, dpd=0)),
    dict(gstin="24AABCT9876K1Z3", name="TrendKart Online", owner="Meena Shah",
         city="Surat", state="24", archetype="growth_ecom", ntc=True, seed=202,
         over=dict(turnover_lakh=8, growth=(0.055, 0.02), gst_delay_days=(12, 16),
                   emi_ratio=0.0, employees=0, vintage=3.0, epfo_ontime=None,
                   upi_share=0.80, min_bal_months=0.78, bounce_prob=0.0, dpd=None)),
    dict(gstin="24AADCM4321P1Z8", name="Maruti Trading Co", owner="Dineshbhai Soni",
         city="Ahmedabad", state="24", archetype="stressed_trader", ntc=False, seed=303,
         over=dict(turnover_lakh=13, growth=(-0.045, 0.01), gst_delay_days=(16, 24),
                   emi_ratio=0.28, employees=4, vintage=9.0, epfo_ontime=0.5,
                   upi_share=0.40, min_bal_months=0.15, bounce_prob=0.35, dpd=60)),
]

# Watchlist fixtures — clear 6-month deterioration for the portfolio alert demo -
WATCHLIST = [
    dict(gstin="24AAWPS7001A1Z6", name="Sunrise Packaging", owner="Alpesh Shah",
         city="Vadodara", state="24", archetype="stable_services", ntc=False, seed=404,
         decline_from=-7, over=dict(turnover_lakh=9, employees=6, vintage=7.0)),
    dict(gstin="24AAOTX5502B1Z1", name="Om Textiles", owner="Bharat Mistry",
         city="Surat", state="24", archetype="seasonal_retailer", ntc=False, seed=505,
         decline_from=-6, over=dict(turnover_lakh=12, employees=5, vintage=6.0)),
]

GSTR1_DUE_DAY, GSTR3B_DUE_DAY, ECR_DUE_DAY = 11, 20, 15


def month_seq(months: int) -> list[str]:
    y, m = ANCHOR_YEAR, ANCHOR_MONTH
    seq = []
    for _ in range(months):
        seq.append(f"{y:04d}-{m:02d}")
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    return list(reversed(seq))


def next_month(period: str) -> tuple[int, int]:
    y, m = int(period[:4]), int(period[5:7])
    return (y + 1, 1) if m == 12 else (y, m + 1)


def add_days(y: int, m: int, day: int, delta: int) -> str:
    """Date arithmetic without datetime.now() — deterministic."""
    import datetime as _dt
    d = _dt.date(y, m, min(day, 28)) + _dt.timedelta(days=delta)
    return d.isoformat()


def make_gstin(rng: random.Random, state: str) -> str:
    pan = "".join(rng.choice("ABCDEFGHJKLMNPQRSTUVWXYZ") for _ in range(5))
    return f"{state}{pan}{''.join(rng.choice('0123456789') for _ in range(4))}{rng.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')}1Z{rng.choice('0123456789')}"


def pick(rng, spec, default=None):
    if spec is None:
        return default
    if isinstance(spec, tuple):
        return rng.uniform(*spec)
    return spec


def gen_msme(rng: random.Random, archetype: str, months: int,
             fixed: dict | None = None, decline_from: int | None = None) -> dict:
    p = ARCHETYPES[archetype]
    over = (fixed or {}).get("over", {})
    state = (fixed or {}).get("state") or rng.choice(STATE_CODES)
    city = (fixed or {}).get("city") or rng.choice(CITIES[state])
    if fixed:
        name, gstin, ntc = fixed["name"], fixed["gstin"], fixed["ntc"]
        owner = fixed.get("owner", "Proprietor")
    else:
        b = rng.choice(NAME_B)
        name, gstin = f"{rng.choice(NAME_A)} {b}", make_gstin(rng, state)
        ntc = rng.random() < p["ntc_prob"]
        owner = "Proprietor"
    sector_word = name.split()[-1] if name.split()[-1] in SECTORS else rng.choice(list(SECTORS))
    sector = "ecommerce" if archetype == "growth_ecom" else SECTORS.get(sector_word, "trading")

    vintage = over.get("vintage") or round(rng.uniform(*p["vintage"]), 1)
    base_turnover = (over.get("turnover_lakh") or rng.uniform(*p["turnover_lakh"])) * 100_000
    growth_mu, growth_sd = over.get("growth", p["growth"])
    upi_share = pick(rng, over.get("upi_share"), rng.uniform(*p["upi_share"]))
    cash_share = rng.uniform(*p["cash_share"])
    emi_ratio = pick(rng, over.get("emi_ratio"), rng.uniform(*p["emi_ratio"]))
    employees = over.get("employees", rng.randint(*p["employees"]))
    collection = rng.uniform(*p["collection_ratio"])
    min_bal_factor = pick(rng, over.get("min_bal_months"), rng.uniform(*p["min_bal_months"]))
    bounce_prob = over.get("bounce_prob", p["bounce_prob"])
    epfo_ontime = over.get("epfo_ontime", p["epfo_ontime"])
    delay_range = over.get("gst_delay_days", p["gst_delay_days"])

    periods = month_seq(months)
    gst, bank_months, upi_months, ecr = [], [], [], []
    txns = []
    turnover = base_turnover
    pan = gstin[2:12]

    for i, period in enumerate(periods):
        declining = decline_from is not None and i >= months + decline_from
        g = rng.gauss(growth_mu, growth_sd)
        if declining:
            g = rng.gauss(-0.07, 0.015)
        season = 1 + p["season_amp"] * math.sin(2 * math.pi * ((i % 12) / 12))
        turnover = max(30_000, turnover * (1 + g))
        t_m = turnover * season
        y_due, m_due = next_month(period)

        # --- GST: GSTR-1 + GSTR-3B with due/filing dates -----------------------
        missed = rng.random() < (p["gst_miss_prob"] + (0.15 if declining else 0))
        delay = 0 if missed else max(0, int(rng.gauss((delay_range[0] + delay_range[1]) / 2,
                                                      max(1, (delay_range[1] - delay_range[0]) / 3))))
        if declining:
            delay += rng.randint(6, 14)
        declared = t_m * (1 - p["underreport"] * rng.uniform(0.5, 1.5))
        gap = round(abs(rng.gauss(0, 1.6)) + (5 if archetype == "stressed_trader" or declining else 0), 1)
        ret_prd = f"{period[5:7]}{period[:4]}"
        gst.append(dict(
            ret_prd=ret_prd,
            gstr1=dict(due_dt=add_days(y_due, m_due, GSTR1_DUE_DAY, 0),
                       dof=None if missed else add_days(y_due, m_due, GSTR1_DUE_DAY, delay),
                       status="NF" if missed else "FIL", ttl_val=round(declared)),
            gstr3b=dict(due_dt=add_days(y_due, m_due, GSTR3B_DUE_DAY, 0),
                        dof=None if missed else add_days(y_due, m_due, GSTR3B_DUE_DAY, delay),
                        status="NF" if missed else "FIL",
                        tax_paid=0 if missed else round(declared * 0.18 * 0.35)),
            gstr1_vs_3b_gap_pct=gap,
        ))

        # --- Bank month (aggregates feed the engine) ---------------------------
        credits = t_m * collection
        upi_amt, cash_dep = credits * upi_share, credits * cash_share
        salary = employees * rng.uniform(14_000, 22_000)
        emi = base_turnover * emi_ratio
        supplier = t_m * rng.uniform(0.55, 0.7)
        debits = supplier + salary + emi + t_m * rng.uniform(0.06, 0.15)
        bounces = (1 if rng.random() < bounce_prob else 0) + (1 if declining and rng.random() < 0.5 else 0)
        min_bal = max(0, t_m * min_bal_factor * rng.uniform(0.8, 1.1) - bounces * t_m * 0.25)
        bank_months.append(dict(
            period=period, total_credits=round(credits), total_debits=round(debits),
            upi_credits=round(upi_amt), cash_deposits=round(cash_dep),
            neft_rtgs_credits=round(credits - upi_amt - cash_dep),
            salary_debits=round(salary), emi_debits=round(emi), supplier_debits=round(supplier),
            inward_bounce_count=bounces, min_balance=round(min_bal),
            avg_balance=round(min_bal + credits * 0.25),
        ))

        # --- ReBIT-shaped sample transactions (last 3 months, demo realism) ----
        if i >= months - 3:
            bal = min_bal + credits * 0.3
            for k in range(12):
                is_cr = rng.random() < 0.55
                amt = round(rng.uniform(0.01, 0.08) * (credits if is_cr else debits))
                bal += amt if is_cr else -amt
                mode = rng.choice(["UPI", "UPI", "FT", "CASH", "OTHERS"] if is_cr
                                  else ["FT", "FT", "OTHERS", "CASH", "CHEQUE"])
                narr = (rng.choice(["UPI/CR/cust payment", "NEFT-DEALER SETTLEMENT", "IMPS/order"])
                        if is_cr else
                        rng.choice(["TO SUPPLIER NEFT", "ACH DR EMI", "SALARY", "RENT", "GST PMT", "ELEC BILL"]))
                txns.append(dict(
                    txnId=f"S{period.replace('-', '')}{k:03d}", type="CREDIT" if is_cr else "DEBIT",
                    mode=mode, amount=amt, currentBalance=round(max(0, bal)),
                    transactionTimestamp=f"{period}-{min(2 + k * 2, 28):02d}T{9 + (k % 9):02d}:15:00+05:30",
                    valueDate=f"{period}-{min(2 + k * 2, 28):02d}", narration=narr,
                    reference=f"REF{rng.randint(10 ** 9, 10 ** 10 - 1)}"))

        # --- UPI summary --------------------------------------------------------
        avg_ticket = rng.uniform(350, 2_500) if sector == "ecommerce" else rng.uniform(800, 6_000)
        n_upi = max(1, int(upi_amt / avg_ticket))
        upi_months.append(dict(period=period, inflow_amount=round(upi_amt), inflow_count=n_upi,
                               unique_payers=max(1, int(n_upi * rng.uniform(0.5, 0.85))),
                               qr_share_pct=round(rng.uniform(30, 85), 1)))

        # --- EPFO ECR (employer-consented path; absent if no employees) --------
        if employees > 0 and epfo_ontime is not None:
            on_time = rng.random() < (epfo_ontime - (0.3 if declining else 0))
            ecr.append(dict(wage_month=ret_prd, total_members=employees,
                            gross_wages=round(salary),
                            epf_contribution=round(min(salary, employees * 15000) * 0.24),
                            due_dt=add_days(y_due, m_due, ECR_DUE_DAY, 0),
                            payment_date=add_days(y_due, m_due, ECR_DUE_DAY,
                                                  0 if on_time else rng.randint(5, 25)),
                            paid_on_time=on_time))

    # --- Bureau (CMR-style; None for new-to-credit) -----------------------------
    if ntc:
        bureau = None
    else:
        dpd = over.get("dpd", rng.choice(p["dpd_pool"]))
        n_loans = rng.randint(1, 3)
        bureau = dict(report_type="COMMERCIAL_CCR_LITE",
                      cmr_rank=(2 if dpd == 0 else 4 if dpd <= 15 else 6 if dpd <= 30 else 8),
                      credit_facilities=n_loans, total_outstanding=round(base_turnover * emi_ratio * 30),
                      emi_monthly=round(base_turnover * emi_ratio),
                      max_dpd_12m=dpd, enquiries_3m=rng.randint(0, 2), enquiries_24m=rng.randint(1, 6),
                      wilful_default=False, suit_filed=False)

    # --- forward label (kept for the stretch GBM; never used by the scorecard) --
    recent = bank_months[-6:]
    growth_6m = (recent[-1]["total_credits"] - recent[0]["total_credits"]) / max(1, recent[0]["total_credits"])
    emi_load = sum(m["emi_debits"] for m in recent) / max(1, sum(m["total_credits"] for m in recent))
    bounce_total = sum(m["inward_bounce_count"] for m in bank_months)
    z = -2.2 - 3.0 * growth_6m + 9.0 * emi_load + 0.55 * bounce_total
    p_def = 1 / (1 + math.exp(-z))

    aa_deposit = dict(  # ReBIT deposit.xsd shape
        type="deposit", maskedAccNumber=f"XXXXXXXX{rng.randint(1000, 9999)}", version="1.1",
        linkedAccRef=f"REF-{gstin[:8]}",
        profile=dict(holders=dict(type="SINGLE", holder=dict(
            name=owner, pan=pan, ckycCompliance=True, nominee="REGISTERED",
            address=f"{city}, {state} IN"))),
        summary=dict(currentBalance=str(bank_months[-1]["avg_balance"]), currency="INR",
                     type="CURRENT", branch=f"{city} Main", facility="OD" if emi_ratio > 0.1 else "",
                     ifscCode="IBKL0000001", status="ACTIVE",
                     openingDate=f"{ANCHOR_YEAR - int(vintage)}-04-01",
                     drawingLimit=str(round(base_turnover * 0.5)), currentODLimit=str(round(base_turnover * 0.5)),
                     exchgeRate="", micrCode="", pending=dict(amount=0.0)),
        transactions=dict(startDate=periods[0] + "-01", endDate=periods[-1] + "-30", transaction=txns),
        monthly_aggregates=bank_months,  # engine consumption; derived view, documented in docs/02
    )

    return dict(
        _synthetic=True, dataset_version=None,  # stamped by main()
        generator=GEN_VERSION,
        profile=dict(gstin=gstin, name=name, owner=owner, city=city, state_code=state,
                     sector=sector, archetype=archetype, vintage_years=vintage,
                     employees=employees, new_to_credit=ntc,
                     udyam_registered=bool(fixed) or rng.random() < 0.8),
        sources=dict(aa_deposit=aa_deposit, gst_returns=gst, upi_months=upi_months,
                     epfo_ecr=ecr, bureau=bureau),
        label=dict(p_default_true=round(p_def, 4)),
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=60)
    ap.add_argument("--months", type=int, default=24)
    ap.add_argument("--out", type=Path, default=Path("../../data"))
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    ds_version = f"DS-{args.seed}-2026.07"
    out_dir = args.out / "msmes"
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.json"):
        old.unlink()
    rng = random.Random(args.seed)
    names, weights = zip(*[(k, v["weight"]) for k, v in ARCHETYPES.items()])
    index = []

    def emit(m, flags):
        m["dataset_version"] = ds_version
        (out_dir / f"{m['profile']['gstin']}.json").write_text(json.dumps(m, indent=1))
        index.append({**{k: m["profile"][k] for k in ("gstin", "name", "city", "archetype", "new_to_credit")},
                      **flags})

    for pers in DEMO_PERSONAS:
        emit(gen_msme(random.Random(pers["seed"]), pers["archetype"], args.months, fixed=pers),
             dict(demo_persona=True, watchlist=False))
    for w in WATCHLIST:
        emit(gen_msme(random.Random(w["seed"]), w["archetype"], args.months, fixed=w,
                      decline_from=w["decline_from"]),
             dict(demo_persona=False, watchlist=True))
    for _ in range(args.count):
        emit(gen_msme(rng, rng.choices(names, weights=weights)[0], args.months),
             dict(demo_persona=False, watchlist=False))

    (args.out / "index.json").write_text(json.dumps(
        dict(_synthetic=True, dataset_version=ds_version, generator=GEN_VERSION,
             count=len(index), msmes=index), indent=1))
    print(f"Generated {len(index)} MSMEs -> {args.out.resolve()}  [{ds_version}]")
    print("  personas:", [r["gstin"] for r in index if r.get("demo_persona")])
    print("  watchlist:", [r["gstin"] for r in index if r.get("watchlist")])


if __name__ == "__main__":
    main()
