# 00 — End Goal

Every task, doc, commit, and decision in this project must trace to one of these levels. If it doesn't, we don't do it this week.

## Goal hierarchy

```
G0  WIN IDBI Innovate 2026 (Demo Day, Aug 21)
 └─ G1  Get SHORTLISTED (announced Jul 21) ← THIS WEEK'S ONLY GOAL
     ├─ G1a  Mandatory: deck (IDBI template, PDF ≤ 5 MB) that survives a bank jury
     ├─ G1b  Booster: deployed demo link that works on a phone
     └─ G1c  Booster: public GitHub repo that runs in 2 commands
 └─ G2  Prototype phase (Jul 22–31, only if shortlisted): swap mock adapters
        for IDBI sandbox APIs on AWS — our architecture is pre-designed for this
```

## What "winning PoC" means (G1 definition of done)

1. **Clickable deployed demo** running 3 scripted personas end-to-end:
   GSTIN → AA-style consent → Health Card assembles → lender/MSME flip → portfolio early-warning.
2. **10-slide deck** with zero unverifiable stats (only numbers from `research-findings.md` §3) and the corrected differentiation story (product model vs FIT Rank — never the data recipe).
3. **Public repo**: evaluation-only source-available license (not open-source), no secrets, README with architecture diagram + demo GIF, `2 commands to run`.
4. **Three bank-grade credibility signals** visible in the demo:
   - AA-style 7-step consent screen (RBI AA Master Direction literacy)
   - Explainable reason codes on every score (FREE-AI / draft MRM 2026 alignment)
   - Graceful degradation: kill a data source live → score recomputes with wider confidence band.

## The one-line pitch (memorize)

> Scores exist. Rails exist. Yet the addressable MSME credit gap is ₹30 lakh crore and AA penetration
> of MSME lending is ~1%. **MCS Parakh is the bank-native product layer that lets IDBI actually act
> on GST/AA/UPI data** — a two-sided, explainable, continuously-monitored Financial Health Card,
> where the MSME can see and improve its own score and the bank watches the portfolio in real time.

## Anti-goals (things that LOOK like progress but aren't)

- Building real integrations this week (mocks are honest and sufficient; adapters make them swappable).
- Training "real ML" on labels we invented (circular — scorecard leads, GBM is the scale story).
- Feature creep beyond the 3 personas + 6 use cases (see 01-requirements.md).
- Polishing anything not visible in the demo or deck.
- Submitting at 11:59 PM.

## Success metrics for this week

| Metric | Target |
|---|---|
| Demo flow completes without errors | 100% across 3 personas, on mobile + incognito |
| Deck stats verifiable to primary source | 10/10 slides |
| Repo fresh-clone-to-running | ≤ 2 commands, ≤ 5 min |
| Submission time | Jul 09, before 12:00 noon IST |
| Team formation on Hack2Skill | confirmed complete (also closes Jul 09) |
