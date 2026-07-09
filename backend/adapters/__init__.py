"""Source adapters — the through-line of the architecture (docs/02 §3).

One `SourceAdapter` contract, N implementations:
  PoC       -> MockAdapter reads slices of the synthetic dataset
  Prototype -> IDBI sandbox adapters (same contract, different fetch)
  Production-> live AA/GSTN/EPFO/bureau/ULI adapters

Scoring code never changes across the three stages. Every fetch is bound to a
consent reference. PARTIAL is never silently treated as complete.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal, Protocol

Status = Literal["OK", "PARTIAL", "PENDING", "FAILED", "CONSENT_REVOKED"]

SOURCE_IDS = ["aa_deposit", "gst_returns", "upi_months", "epfo_ecr", "bureau"]
SOURCE_LABELS = {
    "aa_deposit": "Bank statements (Account Aggregator)",
    "gst_returns": "GST returns (GSTR-1/3B)",
    "upi_months": "UPI flows",
    "epfo_ecr": "EPFO payroll (employer-consented)",
    "bureau": "Credit bureau (commercial)",
}


@dataclass
class FetchResult:
    source_id: str
    status: Status
    payload: object | None
    coverage: float
    consent_id: str
    fetched_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    error: str | None = None


class SourceAdapter(Protocol):
    source_id: str

    async def fetch(self, gstin: str, consent_id: str) -> FetchResult: ...


class MockAdapter:
    """PoC adapter: serves one source slice from the synthetic dataset.

    A small artificial latency makes the S5 'card assembling' moment visible.
    """

    def __init__(self, source_id: str, data_dir: Path, latency_s: float = 0.15):
        self.source_id = source_id
        self.data_dir = data_dir
        self.latency_s = latency_s

    async def fetch(self, gstin: str, consent_id: str) -> FetchResult:
        await asyncio.sleep(self.latency_s)
        path = self.data_dir / "msmes" / f"{gstin}.json"
        if not path.exists():
            return FetchResult(self.source_id, "FAILED", None, 0.0, consent_id,
                               error="subject not found at provider")
        payload = json.loads(path.read_text())["sources"].get(self.source_id)
        if payload in (None, [], {}):
            # Absent-at-source (e.g. NTC has no bureau file) — not a failure.
            return FetchResult(self.source_id, "OK", None, 0.0, consent_id,
                               error="no data held for subject")
        return FetchResult(self.source_id, "OK", payload, 1.0, consent_id)


class AdapterRegistry:
    """Holds adapters + the demo kill-switch (FR-2.4 / UC5)."""

    def __init__(self, data_dir: Path):
        self.adapters: dict[str, MockAdapter] = {
            s: MockAdapter(s, data_dir) for s in SOURCE_IDS}
        self.killed: set[str] = set()

    def set_killed(self, source_id: str, killed: bool) -> None:
        if source_id not in self.adapters:
            raise KeyError(source_id)
        (self.killed.add if killed else self.killed.discard)(source_id)

    async def fetch_all(self, gstin: str, consent_id: str) -> dict[str, FetchResult]:
        async def one(sid: str) -> FetchResult:
            if sid in self.killed:
                return FetchResult(sid, "FAILED", None, 0.0, consent_id,
                                   error="provider unreachable (demo kill-switch)")
            try:
                return await asyncio.wait_for(
                    self.adapters[sid].fetch(gstin, consent_id), timeout=5.0)
            except asyncio.TimeoutError:
                return FetchResult(sid, "FAILED", None, 0.0, consent_id, error="timeout")

        results = await asyncio.gather(*(one(s) for s in SOURCE_IDS))
        return {r.source_id: r for r in results}

    @staticmethod
    def to_sources(results: dict[str, FetchResult]) -> dict:
        """FetchResults -> the engine's `sources` dict. FAILED -> absent."""
        return {sid: (r.payload if r.status == "OK" else None)
                for sid, r in results.items()}

    def visible(self, record: dict) -> dict:
        """The record as the engine may see it right now: killed sources blanked.

        Bulk views (the lender book) need the same coverage the card gets, but
        without fanning 5 adapters x 65 MSMEs through their demo latency. Same
        end state as `to_sources` over a live fetch, which is what /score does.
        """
        if not self.killed:
            return record
        return dict(record, sources={sid: (None if sid in self.killed else payload)
                                     for sid, payload in record["sources"].items()})
