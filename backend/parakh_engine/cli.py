"""CLI — score MSMEs from the synthetic dataset (P1 gate check).

  python -m parakh_engine.cli --data ../data            # all, summary table
  python -m parakh_engine.cli --data ../data --gstin 24AABCT9876K1Z3   # detail
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import score


def load(data_dir: Path, gstin: str) -> dict:
    return json.loads((data_dir / "msmes" / f"{gstin}.json").read_text())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, default=Path("../data"))
    ap.add_argument("--gstin", default=None)
    args = ap.parse_args()

    index = json.loads((args.data / "index.json").read_text())
    rows = index["msmes"] if args.gstin is None else [
        m for m in index["msmes"] if m["gstin"] == args.gstin]

    results = []
    for m in rows:
        r = score(load(args.data, m["gstin"]))
        results.append((m, r))

    if args.gstin:
        r = results[0][1]
        print(json.dumps(r.to_dict(), indent=2))
        return

    results.sort(key=lambda x: x[1].score)
    print(f"{'GSTIN':<17} {'Name':<30} {'Score':>5} {'Band':<9} {'Conf':<7} Flags")
    for m, r in results:
        flags = ("PERSONA " if m.get("demo_persona") else "") + ("WATCH" if m.get("watchlist") else "")
        print(f"{r.gstin:<17} {r.name[:29]:<30} {r.score:>5} {r.band:<9} "
              f"{r.confidence}±{r.confidence_width:<3} {flags}")
    scores = sorted(r.score for _, r in results)
    p = lambda q: scores[int(q * (len(scores) - 1))]
    print(f"\nn={len(scores)}  p10={p(.1)}  p50={p(.5)}  p90={p(.9)}")


if __name__ == "__main__":
    main()
