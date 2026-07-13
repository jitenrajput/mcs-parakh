# 08 — Git Workflow

Optimized for a 4-day, 4-person push where the repo itself is a judged deliverable (G1c). Simple enough to never slow us; disciplined enough that the public repo looks professional to the jury.

## Branching — trunk-based, short-lived branches

- **`master` = always demoable.** Anything merged must keep the persona walkthrough green. The jury may clone at any moment after we submit the link.
- **Feature branches** for anything > ~30 min of work: `feat/T-107-scorecard`, `fix/T-207-gauge-mobile`. Branch names carry the tracker ID.
- Docs, tracker updates, README, data regeneration: **commit straight to `master`** (no branch ceremony for non-code).
- Merge = fast-forward or squash into master, same day the branch opens. **No branch lives overnight** — half-done work merges behind an unwired flag rather than diverging.
- No `develop`, no GitFlow, no release branches — wrong tool for a 4-day project.

## Commit conventions

```
<type>(<tracker-id>): <imperative summary ≤ 72 chars>
```
Types: `feat` `fix` `data` `docs` `test` `chore` `deploy`.
Examples:
- `feat(T-107): scorecard bins→points with 300-900 affine scaling`
- `data(T-105): regenerate 63 MSMEs with ReBIT-faithful fields`
- `docs(T-306): deck skeleton v1 with sourced stats`

Rules: tracker status updates ride **in the same commit** as the work · no `WIP`/`asdf` commits on master (squash first) · commit messages are jury-visible — write them like the repo is being graded, because it is.

**Attribution rule:** all commits and co-author trailers attribute to **MCS-Labs** only (`Co-Authored-By: MCS-Labs <dev@mconnectsolutions.com>`). No AI-vendor names (Claude/Anthropic/etc.) anywhere in git history, commit messages, or release notes.

## Tags — milestone markers

| Tag | When |
|---|---|
| `v0.1-engine` | P1 gate passes (Jul 7) |
| `v0.2-e2e` | P2 gate passes (Jul 8 noon) |
| `v0.3-deployed` | P3 gate passes (Jul 8 eve) |
| `v1.0-poc-submission` | The exact commit submitted Jul 9 — **never force-push over this** |

## Repo hygiene (jury-facing, NFR-3)

- **Evaluation-only source-available `LICENSE`** file before submission (proprietary; not open-source — preserves IDBI ROFR/exclusivity).
- **No secrets ever**: AWS keys/tokens via env only; `.env` in `.gitignore`; `git grep -iE "(api[_-]?key|secret|token|password)"` before every push (NP runs it daily).
- **Synthetic data is committed deliberately** (jury should run without a datagen step) and watermarked SYNTHETIC in every file.
- History stays clean: no force-push to master after Jul 7; if history surgery is ever needed, JR decides.
- `README.md` is the front door: quickstart (2 commands), architecture diagram, demo GIF, live links, honest-mock note.

## Remote & access

- Push to a **public GitHub repo** under JR's account by Jul 7 evening (submission needs the URL; going public early lets NP test the fresh-clone path for real).
- All four members added as collaborators; Claude works through JR's local checkout.
- After submission: repo frozen except README polish until Jul 21 shortlist — the judged artifact shouldn't churn under review.

## Daily rhythm

1. Pull master before starting.
2. Branch if code, commit direct if docs/data.
3. Merge before the 21:00 sync; tracker updated in the merging commit.
4. NP runs the hygiene grep + persona walkthrough on merged master.
