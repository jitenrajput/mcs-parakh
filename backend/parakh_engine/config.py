"""Scorecard configuration — SC-2026.07.1 (docs/12-score-policy.md).

Every number here is credit POLICY, not code. Any change mints a new
scorecard_version; old versions are retained (RBI draft-MRM principle).
"""

ENGINE_VERSION = "0.1.0"
SCORECARD_VERSION = "SC-2026.07.1"

# Dimension weights (LOCKED Jul 06) — must sum to 1.0
WEIGHTS = {
    "cash_flow": 0.30,
    "compliance": 0.20,
    "obligation": 0.20,
    "growth": 0.15,
    "stability": 0.15,
}

# Component recipe per dimension: (feature, weight, good_value, bad_value).
# grade() maps feature linearly bad->0, good->100 (direction implied by ordering).
# A missing feature (None) contributes the NEUTRAL prior and is flagged.
NEUTRAL = 60.0
COMPONENTS = {
    "cash_flow": [
        ("inflow_cov",          0.35, 0.08, 0.60),   # lower variation = steadier sales
        ("balance_floor_ratio", 0.30, 1.50, 0.02),   # months of outflow held as floor
        ("net_margin",          0.35, 0.18, -0.05),  # (credits-debits)/credits
    ],
    "compliance": [
        ("gst_avg_delay_days",  0.40, 1.0, 25.0),   # recent-6m window (momentum)
        ("gst_late_count_6m",   0.20, 0.0, 5.0),
        ("gst_missed_12m",      0.20, 0.0, 3.0),
        ("gstr1_3b_gap_pct",    0.20, 1.0, 8.0),
    ],
    "growth": [
        ("turnover_slope_pct",  0.50, 0.05, -0.06),  # avg MoM growth, robust
        ("growth_q_pct",        0.30, 0.12, -0.15),  # last 3m vs prior 3m
        ("growth_volatility",   0.20, 0.03, 0.30),
    ],
    "obligation": [
        ("emi_to_inflow",       0.45, 0.05, 0.35),
        ("bounces_12m",         0.30, 0.0, 6.0),
        ("bureau_max_dpd",      0.25, 0.0, 90.0),
    ],
    "stability": [
        ("vintage_years",       0.35, 10.0, 0.5),
        ("employees",           0.20, 15.0, 0.0),
        ("payroll_on_time",     0.25, 0.97, 0.40),
        ("udyam_registered",    0.20, 1.0, 0.0),
    ],
}

# 300-900 scaling: score = SCALE_A + SCALE_B * composite(0-100), clamped.
# Calibrated on DS-42-2026.07 so the canonical personas land at 780/690/410.
SCALE_A = 199.0
SCALE_B = 6.28
SCORE_MIN, SCORE_MAX = 300, 900

# Bands + multipliers (LOCKED): applied at the LOWER EDGE of the confidence band.
BANDS = [
    ("Prime",    780, 1.00),
    ("Good",     720, 0.80),
    ("Watch",    600, 0.60),
    ("Weak",     480, 0.30),
    ("Critical", 300, 0.00),
]

# Confidence: majors/minors coverage -> band width (docs/12).
MAJOR_SOURCES = ["aa_deposit", "gst_returns", "bureau"]
MINOR_SOURCES = ["upi_months", "epfo_ecr"]
CONFIDENCE_TIERS = [  # (min_coverage, label, +/- width)
    (0.95, "High", 15),
    (0.60, "Medium", 35),
    (0.00, "Low", 60),
]

NAYAK_WC_FACTOR = 0.20  # working-capital ceiling = 20% of annual turnover

# Human templates for reason codes (EN; UI translates via strings.json later)
REASON_LABELS = {
    "inflow_cov":          ("Steady monthly inflows", "Volatile monthly inflows"),
    "balance_floor_ratio": ("Healthy balance cushion", "Thin balance cushion"),
    "net_margin":          ("Strong cash-flow margin", "Weak cash-flow margin"),
    "gst_avg_delay_days":  ("GST filed on time", "GST filed late (avg {v:.0f} days)"),
    "gst_late_count_6m":   ("Recent GST filings on time", "{v:.0f} late GST filings in last 6m"),
    "gst_missed_12m":      ("No missed GST returns", "{v:.0f} missed GST returns"),
    "gstr1_3b_gap_pct":    ("GSTR-1 and 3B consistent", "GSTR-1 vs 3B gap {v:.1f}%"),
    "turnover_slope_pct":  ("Growing turnover", "Declining turnover"),
    "growth_q_pct":        ("Recent quarter improving", "Recent quarter weakening"),
    "growth_volatility":   ("Consistent growth", "Erratic growth"),
    "emi_to_inflow":       ("Light EMI burden", "EMI burden {v:.0%} of inflows"),
    "bounces_12m":         ("No payment bounces", "{v:.0f} payment bounces in 12m"),
    "bureau_max_dpd":      ("Clean repayment record", "Max {v:.0f} days past due"),
    "vintage_years":       ("Established business ({v:.0f} yrs)", "Young business ({v:.1f} yrs)"),
    "employees":           ("Stable team on payroll", "No formal payroll"),
    "payroll_on_time":     ("PF deposits on time", "Irregular PF deposits"),
    "udyam_registered":    ("Udyam registered", "Not Udyam registered"),
}
