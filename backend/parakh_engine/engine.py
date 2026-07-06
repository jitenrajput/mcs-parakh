"""Parakh scoring engine — pure, stateless, deterministic (NFR-5/6).

score(msme_record) -> ScoreResult with:
  composite 300-900, five dimension scores + A-E grades, reason codes,
  confidence band (coverage-driven), band + eligibility (lower-edge rule),
  version stamps (engine / scorecard / dataset).

No framework, no I/O, no randomness. Same input -> same output, always.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict

from . import config
from .features import extract


@dataclass
class Reason:
    feature: str
    text: str
    dimension: str
    points_delta: float  # +/- vs neutral, weighted into the dimension


@dataclass
class ScoreResult:
    gstin: str
    name: str
    score: int
    band: str                 # band at the point score
    band_lower_edge: str      # band used for eligibility (lower-edge rule)
    confidence: str
    confidence_width: int
    dimensions: dict          # name -> {score, grade}
    reasons_positive: list
    reasons_negative: list
    coverage: dict
    missing_sources: list
    eligibility: dict         # ceiling, multiplier, indicative_limit (INR)
    versions: dict
    composite_0_100: float = field(repr=False, default=0.0)

    def to_dict(self) -> dict:
        return asdict(self)


def grade_component(x: float | None, good: float, bad: float) -> tuple[float, bool]:
    """Linear map bad->0, good->100 (works in either direction). None -> neutral."""
    if x is None:
        return config.NEUTRAL, True
    t = (x - bad) / (good - bad)
    return max(0.0, min(100.0, t * 100.0)), False


def letter(score_0_100: float) -> str:
    return ("A" if score_0_100 >= 80 else "B" if score_0_100 >= 65 else
            "C" if score_0_100 >= 50 else "D" if score_0_100 >= 35 else "E")


def band_for(score: float) -> tuple[str, float]:
    for name, floor, mult in config.BANDS:
        if score >= floor:
            return name, mult
    return "Critical", 0.0


def score(record: dict) -> ScoreResult:
    profile, sources = record["profile"], record["sources"]
    feats, coverage = extract(sources, profile)

    dims: dict[str, float] = {}
    reasons: list[Reason] = []
    for dim, comps in config.COMPONENTS.items():
        total = 0.0
        for feat, w, good, bad in comps:
            comp_score, was_neutral = grade_component(feats.get(feat), good, bad)
            total += w * comp_score
            if not was_neutral:
                delta = w * (comp_score - config.NEUTRAL)
                pos_t, neg_t = config.REASON_LABELS[feat]
                text = (pos_t if delta >= 0 else neg_t)
                v = feats[feat]
                text = text.format(v=v) if "{v" in text else text
                reasons.append(Reason(feat, text, dim, round(delta, 1)))
        dims[dim] = round(total, 1)

    composite = sum(config.WEIGHTS[d] * s for d, s in dims.items())
    raw = config.SCALE_A + config.SCALE_B * composite
    pt = int(round(max(config.SCORE_MIN, min(config.SCORE_MAX, raw))))

    # --- confidence from coverage (majors 0.25 each missing, minors 0.10) -------
    mm = sum(1 for s in config.MAJOR_SOURCES if not coverage.get(s))
    mn = sum(1 for s in config.MINOR_SOURCES if not coverage.get(s))
    cov = 1.0 - 0.25 * mm - 0.10 * mn
    conf_label, width = "Low", 60
    for min_cov, label, w in config.CONFIDENCE_TIERS:
        if cov >= min_cov:
            conf_label, width = label, w
            break

    band_pt, mult_pt = band_for(pt)
    # Confidence-conservative rule (docs/12, amended Jul 06 night): at Low
    # confidence, eligibility is banded at the lower edge (score - 60); at
    # High/Medium the point band applies and the +/- range is displayed.
    if conf_label == "Low":
        lower = max(config.SCORE_MIN, pt - width)
        band_elig, mult = band_for(lower)
        basis_note = f"{band_elig} multiplier at Low-confidence lower edge ({pt}-{width}={lower})"
    else:
        band_elig, mult = band_pt, mult_pt
        basis_note = f"{band_elig} multiplier at point score {pt} ({conf_label} confidence)"

    # --- indicative eligibility (Nayak turnover method) --------------------------
    annual = feats.get("annual_turnover") or 0.0
    ceiling = config.NAYAK_WC_FACTOR * annual
    eligibility = dict(
        annual_turnover=round(annual),
        nayak_ceiling=round(ceiling),
        band_multiplier=mult,
        indicative_limit=round(ceiling * mult),
        basis=f"20% of annual turnover x {basis_note}; "
              f"indicative only - bank credit policy owns sanction",
    )

    reasons.sort(key=lambda r: r.points_delta)
    return ScoreResult(
        gstin=profile["gstin"], name=profile["name"], score=pt,
        band=band_pt, band_lower_edge=band_elig,
        confidence=conf_label, confidence_width=width,
        dimensions={d: dict(score=s, grade=letter(s)) for d, s in dims.items()},
        reasons_positive=[asdict(r) for r in reversed(reasons[-3:])],
        reasons_negative=[asdict(r) for r in reasons[:3]],
        coverage=coverage,
        missing_sources=[s for s, ok in coverage.items() if not ok],
        eligibility=eligibility,
        versions=dict(engine=config.ENGINE_VERSION, scorecard=config.SCORECARD_VERSION,
                      dataset=record.get("dataset_version", "unknown")),
        composite_0_100=round(composite, 2),
    )


def score_with_overrides(record: dict, drop_sources: list[str] | None = None) -> ScoreResult:
    """Kill-switch support: re-score with sources removed (graceful degradation)."""
    import copy
    rec = copy.deepcopy(record)
    for s in drop_sources or []:
        rec["sources"][s] = None if s == "bureau" else []
        if s == "aa_deposit":
            rec["sources"][s] = {}
    return score(rec)
