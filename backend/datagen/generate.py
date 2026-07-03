"""Synthetic MSME data generator for M-Connect Parakh (IDBI Innovate 2026 PoC).

Generates realistic-shaped GST returns, bank statement aggregates + sample
transactions, UPI flow summaries, EPFO records and a bureau stub for N
synthetic MSMEs across behavioural archetypes, plus a 12-month-forward
stress label for model training.

All data is synthetic. Schemas follow public GST/AA conventions loosely so
the adapter layer can later swap in IDBI sandbox APIs (prototype phase).

Usage:
    python generate.py --count 60 --months 18 --out ../data --seed 42
"""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

ANCHOR_YEAR, ANCHOR_MONTH = 2026, 6  # last complete data month (Jun 2026)

STATE_CODES = ["24", "27", "07", "29", "33", "09", "06", "08"]  # GJ, MH, DL, KA, TN, UP, HR, RJ
CITIES = {
    "24": ["Ahmedabad", "Surat", "Rajkot", "Vadodara"],
    "27": ["Mumbai", "Pune", "Nagpur"],
    "07": ["New Delhi"],
    "29": ["Bengaluru", "Mysuru"],
    "33": ["Chennai", "Coimbatore"],
    "09": ["Noida", "Lucknow"],
    "06": ["Gurugram", "Faridabad"],
    "08": ["Jaipur", "Udaipur"],
}
NAME_A = ["Shree", "Om", "Jay", "New", "Royal", "Krishna", "Ganesh", "Balaji", "Shakti", "Sunrise",
          "Apex", "Prime", "Silver", "Golden", "National", "Perfect", "Modern", "Classic"]
NAME_B = ["Auto Components", "Textiles", "Traders", "Electronics", "Packaging", "Engineering Works",
          "Food Products", "Plastics", "Enterprises", "Industries", "Exports", "Agro Foods",
          "Pharma Distributors", "Steel Works", "Garments", "Ceramics"]
SECTORS = {
    "Auto Components": "manufacturing", "Textiles": "manufacturing", "Traders": "trading",
    "Electronics": "trading", "Packaging": "manufacturing", "Engineering Works": "manufacturing",
    "Food Products": "manufacturing", "Plastics": "manufacturing", "Enterprises": "trading",
    "Industries": "manufacturing", "Exports": "trading", "Agro Foods": "trading",
    "Pharma Distributors": "trading", "Steel Works": "manufacturing", "Garments": "manufacturing",
    "Ceramics": "manufacturing", "Online": "ecommerce", "E-Retail": "ecommerce",
}

# Behavioural archetypes -----------------------------------------------------
ARCHETYPES = {
    "healthy_manufacturer": dict(
        weight=0.25, turnover_lakh=(8, 40), growth=(0.012, 0.02), season_amp=0.05,
        gst_delay_days=(1, 3), gst_miss_prob=0.0, underreport=0.02,
        emi_ratio=(0.04, 0.08), bounce_prob=0.01, employees=(6, 25), epfo_ontime=0.97,
        upi_share=(0.25, 0.45), cash_share=(0.05, 0.12), ntc_prob=0.05, vintage=(5, 18),
        collection_ratio=(0.95, 1.02), min_bal_months=(1.2, 2.5),
    ),
    "growth_ecom": dict(
        weight=0.20, turnover_lakh=(3, 15), growth=(0.09, 0.04), season_amp=0.10,
        gst_delay_days=(3, 6), gst_miss_prob=0.02, underreport=0.03,
        emi_ratio=(0.0, 0.03), bounce_prob=0.015, employees=(0, 6), epfo_ontime=0.90,
        upi_share=(0.65, 0.9), cash_share=(0.0, 0.04), ntc_prob=0.75, vintage=(1, 4),
        collection_ratio=(0.98, 1.05), min_bal_months=(0.6, 1.5),
    ),
    "stable_services": dict(
        weight=0.20, turnover_lakh=(2, 12), growth=(0.004, 0.015), season_amp=0.03,
        gst_delay_days=(2, 5), gst_miss_prob=0.01, underreport=0.03,
        emi_ratio=(0.03, 0.09), bounce_prob=0.02, employees=(2, 10), epfo_ontime=0.92,
        upi_share=(0.4, 0.6), cash_share=(0.03, 0.1), ntc_prob=0.25, vintage=(3, 12),
        collection_ratio=(0.93, 1.0), min_bal_months=(0.8, 1.8),
    ),
    "seasonal_retailer": dict(
        weight=0.15, turnover_lakh=(3, 18), growth=(0.006, 0.02), season_amp=0.35,
        gst_delay_days=(4, 8), gst_miss_prob=0.03, underreport=0.05,
        emi_ratio=(0.05, 0.11), bounce_prob=0.03, employees=(1, 8), epfo_ontime=0.85,
        upi_share=(0.5, 0.75), cash_share=(0.08, 0.2), ntc_prob=0.35, vintage=(2, 10),
        collection_ratio=(0.9, 1.0), min_bal_months=(0.4, 1.2),
    ),
    "stressed_trader": dict(
        weight=0.20, turnover_lakh=(2, 20), growth=(-0.03, 0.025), season_amp=0.08,
        gst_delay_days=(12, 15), gst_miss_prob=0.12, underreport=0.10,
        emi_ratio=(0.12, 0.22), bounce_prob=0.16, employees=(0, 8), epfo_ontime=0.6,
        upi_share=(0.3, 0.55), cash_share=(0.12, 0.3), ntc_prob=0.2, vintage=(2, 12),
        collection_ratio=(0.8, 0.95), min_bal_months=(0.05, 0.5),
    ),
}

# Fixed demo personas (stable GSTINs for the scripted demo) ------------------
DEMO_PERSONAS = [
    dict(gstin="24AAACS1234F1Z5", name="Shree Ganesh Auto Components", city="Rajkot",
         state="24", archetype="healthy_manufacturer", ntc=False, seed=101),
    dict(gstin="24AABCT9876K1Z3", name="TrendKart Online", city="Surat",
         state="24", archetype="growth_ecom", ntc=True, seed=202),
    dict(gstin="24AADCM4321P1Z8", name="Maruti Trading Co", city="Ahmedabad",
         state="24", archetype="stressed_trader", ntc=False, seed=303),
]


def month_seq(months: int) -> list[str]:
    """Last `months` periods ending at the anchor month, oldest first."""
    y, m = ANCHOR_YEAR, ANCHOR_MONTH
    seq = []
    for _ in range(months):
        seq.append(f"{y:04d}-{m:02d}")
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    return list(reversed(seq))


def make_gstin(rng: random.Random, state: str) -> str:
    pan = "".join(rng.choice("ABCDEFGHJKLMNPQRSTUVWXYZ") for _ in range(5))
    digits = "".join(rng.choice("0123456789") for _ in range(4))
    return f"{state}{pan}{digits}{rng.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')}1Z{rng.choice('0123456789')}"


def gen_msme(rng: random.Random, archetype: str, months: int, fixed: dict | None = None) -> dict:
    p = ARCHETYPES[archetype]
    state = (fixed or {}).get("state") or rng.choice(STATE_CODES)
    city = (fixed or {}).get("city") or rng.choice(CITIES[state])
    if fixed:
        name, gstin, ntc = fixed["name"], fixed["gstin"], fixed["ntc"]
    else:
        b = rng.choice(NAME_B)
        name = f"{rng.choice(NAME_A)} {b}"
        gstin = make_gstin(rng, state)
        ntc = rng.random() < p["ntc_prob"]
    sector_word = name.split()[-1] if name.split()[-1] in SECTORS else rng.choice(list(SECTORS))
    sector = SECTORS.get(sector_word, "trading")
    if archetype == "growth_ecom":
        sector = "ecommerce"

    vintage = round(rng.uniform(*p["vintage"]), 1)
    base_turnover = rng.uniform(*p["turnover_lakh"]) * 100_000  # ₹/month
    upi_share = rng.uniform(*p["upi_share"])
    cash_share = rng.uniform(*p["cash_share"])
    emi_ratio = rng.uniform(*p["emi_ratio"])
    employees = rng.randint(*p["employees"])
    collection = rng.uniform(*p["collection_ratio"])
    min_bal_factor = rng.uniform(*p["min_bal_months"])

    periods = month_seq(months)
    gst, bank_months, upi_months, epfo, txn_sample = [], [], [], [], []
    turnover = base_turnover
    bounce_total, late_filings, missed_filings = 0, 0, 0

    for i, period in enumerate(periods):
        g = rng.gauss(*p["growth"])
        season = 1 + p["season_amp"] * math.sin(2 * math.pi * ((i % 12) / 12))
        turnover = max(30_000, turnover * (1 + g))
        t_m = turnover * season

        # --- GST return ---
        missed = rng.random() < p["gst_miss_prob"]
        delay = 0 if missed else max(0, int(rng.gauss(*p["gst_delay_days"])))
        if missed:
            missed_filings += 1
        elif delay > 5:
            late_filings += 1
        declared = t_m * (1 - p["underreport"] * rng.uniform(0.5, 1.5))
        gst.append(dict(
            period=period, filed=not missed,
            filing_delay_days=None if missed else delay,
            turnover_declared=round(declared),
            tax_paid=round(declared * 0.18 * 0.35),  # rough net GST cash component
            gstr1_vs_3b_gap_pct=round(abs(rng.gauss(0, 2)) + (4 if archetype == "stressed_trader" else 0), 1),
        ))

        # --- Bank month ---
        credits = t_m * collection
        upi_amt = credits * upi_share
        cash_dep = credits * cash_share
        other_credits = credits - upi_amt - cash_dep
        salary = employees * rng.uniform(14_000, 22_000)
        emi = base_turnover * emi_ratio
        supplier = t_m * rng.uniform(0.55, 0.7)
        rent_util = t_m * rng.uniform(0.03, 0.07)
        drawings = t_m * rng.uniform(0.03, 0.08)
        debits = supplier + salary + emi + rent_util + drawings
        bounces = 1 if rng.random() < p["bounce_prob"] else 0
        bounces += 1 if (archetype == "stressed_trader" and rng.random() < 0.5 and i > months * 0.6) else 0
        bounce_total += bounces
        min_bal = max(0, t_m * min_bal_factor * rng.uniform(0.7, 1.2) - (bounces * t_m * 0.3))
        bank_months.append(dict(
            period=period,
            total_credits=round(credits), total_debits=round(debits),
            upi_credits=round(upi_amt), cash_deposits=round(cash_dep),
            neft_rtgs_credits=round(other_credits),
            salary_debits=round(salary), emi_debits=round(emi),
            supplier_debits=round(supplier),
            inward_bounce_count=bounces,
            min_balance=round(min_bal), avg_balance=round(min_bal + credits * 0.25),
        ))

        # --- UPI summary ---
        avg_ticket = rng.uniform(350, 2_500) if sector == "ecommerce" else rng.uniform(800, 6_000)
        upi_count = max(1, int(upi_amt / avg_ticket))
        upi_months.append(dict(
            period=period, inflow_amount=round(upi_amt), inflow_count=upi_count,
            unique_payers=max(1, int(upi_count * rng.uniform(0.5, 0.85))),
            qr_share_pct=round(rng.uniform(30, 85), 1),
        ))

        # --- EPFO ---
        if employees > 0:
            epfo.append(dict(
                period=period, employees=employees,
                wage_bill=round(salary),
                contribution_paid_on_time=rng.random() < p["epfo_ontime"],
            ))

        # --- sample transactions (for demo realism) ---
        for _ in range(6):
            is_credit = rng.random() < 0.55
            amt = rng.uniform(0.005, 0.06) * (credits if is_credit else debits)
            txn_sample.append(dict(
                period=period, type="CR" if is_credit else "DR",
                channel=rng.choice(["UPI", "NEFT", "IMPS", "CASH", "CHEQUE"]),
                amount=round(amt),
                narration=rng.choice(
                    ["UPI/cust payment", "NEFT/dealer", "IMPS/order settle", "CASH DEP", "TO SUPPLIER",
                     "EMI DEBIT", "SALARY", "RENT", "GST PAYMENT", "ELECTRICITY BILL"]),
            ))

    # --- forward 12m stress label (ground truth for training) ---
    recent = bank_months[-6:]
    growth_6m = (recent[-1]["total_credits"] - recent[0]["total_credits"]) / max(1, recent[0]["total_credits"])
    emi_load = sum(m["emi_debits"] for m in recent) / max(1, sum(m["total_credits"] for m in recent))
    bal_cushion = sum(m["min_balance"] for m in recent) / max(1, sum(m["total_credits"] for m in recent))
    z = (-2.2 - 3.0 * growth_6m + 9.0 * emi_load + 0.55 * bounce_total
         + 0.35 * late_filings + 0.8 * missed_filings - 2.0 * bal_cushion)
    p_default = 1 / (1 + math.exp(-z))
    default_12m = rng.random() < p_default

    bureau = None if ntc else dict(
        existing_loans=rng.randint(1, 3),
        emi_monthly=round(base_turnover * emi_ratio),
        max_dpd_last_12m=(rng.choice([0, 0, 0, 15, 30]) if archetype != "stressed_trader"
                          else rng.choice([30, 60, 90])),
    )

    return dict(
        profile=dict(gstin=gstin, name=name, city=city, state_code=state, sector=sector,
                     archetype=archetype, vintage_years=vintage, employees=employees,
                     new_to_credit=ntc, udyam_registered=rng.random() < 0.8),
        gst_returns=gst, bank_months=bank_months, upi_months=upi_months,
        epfo=epfo, bureau=bureau, sample_transactions=txn_sample,
        label=dict(default_12m=default_12m, p_default_true=round(p_default, 4)),
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate synthetic MSME dataset")
    ap.add_argument("--count", type=int, default=60, help="number of random MSMEs (plus 3 demo personas)")
    ap.add_argument("--months", type=int, default=18)
    ap.add_argument("--out", type=Path, default=Path("../data"))
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    out_dir = args.out / "msmes"
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)

    names, weights = zip(*[(k, v["weight"]) for k, v in ARCHETYPES.items()])
    index = []

    for persona in DEMO_PERSONAS:
        m = gen_msme(random.Random(persona["seed"]), persona["archetype"], args.months, fixed=persona)
        (out_dir / f"{m['profile']['gstin']}.json").write_text(json.dumps(m, indent=1))
        index.append({**{k: m["profile"][k] for k in ("gstin", "name", "city", "archetype", "new_to_credit")},
                      "default_12m": m["label"]["default_12m"], "demo_persona": True})

    for _ in range(args.count):
        arch = rng.choices(names, weights=weights)[0]
        m = gen_msme(rng, arch, args.months)
        (out_dir / f"{m['profile']['gstin']}.json").write_text(json.dumps(m, indent=1))
        index.append({**{k: m["profile"][k] for k in ("gstin", "name", "city", "archetype", "new_to_credit")},
                      "default_12m": m["label"]["default_12m"], "demo_persona": False})

    (args.out / "index.json").write_text(json.dumps(index, indent=1))
    n_def = sum(1 for r in index if r["default_12m"])
    print(f"Generated {len(index)} MSMEs -> {args.out.resolve()}")
    print(f"  default_12m rate: {n_def}/{len(index)} ({100 * n_def / len(index):.0f}%)")
    print(f"  demo personas: {[r['gstin'] for r in index if r['demo_persona']]}")


if __name__ == "__main__":
    main()
