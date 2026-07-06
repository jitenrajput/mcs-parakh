# 07 — Project Management Methodology

## Why Kanban-with-gates (not Scrum)

A 4-day runway with a fixed deadline and a 4-person part-time team leaves no room for sprint ceremonies. We run **Kanban with phase gates**: continuous flow, WIP limits, binary exit gates (04-phases-timeline.md), and one daily sync. Scrum artifacts we deliberately skip: sprint planning, retros, story points. The deadline is the sprint.

## Operating rules

1. **The tracker is the truth** (05-tracker.md). If it's not in the tracker, it's not happening. Status updates ride in the same commit as the work.
2. **WIP limit = 1 per person** (plus at most 1 blocked item). Finish, then pull.
3. **Pull order:** MUST before SHOULD before COULD, within the current phase. Never pull from a future phase while the current gate is unmet.
4. **Daily sync — 15 min, 21:00 IST** (WhatsApp/call): yesterday/today/blockers, tracker updated live during the call. JR chairs; NP keeps time.
5. **Blockers get names and hours, not days.** A blocker unresolved for 4 working hours escalates to JR for a cut/flip decision.
6. **Definition of Done (any task):** code committed + tracker updated + the relevant flow still passes (NP or self-run persona walkthrough). For engine tasks: unit test included (NFR-5).
7. **Gates are binary.** "Almost clickable" = not done. If a gate is at risk, cut scope from the pre-agreed cut list (06-gaps.md §2) — never move the gate, never cut the never-cut list.
8. **Decisions are deliberate:** working defaults keep us moving, but D-numbers in 06-gaps.md stay flagged until JR explicitly confirms. Flipping a default = one commit touching 06-gaps.md + affected tracker rows.
9. **Honesty rule (product & process):** every mock labeled; every stat sourced; status reported as it is — a red tracker Tuesday beats a surprise Thursday.

## Roles

| Person | Role | Owns |
|---|---|---|
| Jitendra (JR) | Product lead / decider | Scope, decisions D-1…D-7, deploy, deck, submission |
| Jayesh (JT) | Project lead | Deck content + speaker notes, demo video, template access (B-4) |
| Zaid (ZS) | ML/Python | Datagen, scoring engine, alerts, GBM stretch |
| Nirmal (NP) | QA | Gates verification, persona walkthroughs, fresh-clone test, deck-vs-demo consistency |
| Frontend (TBD) | UI | React build (Claude generates, owner integrates + polishes) |
| Claude (CL) | Force multiplier | Code generation across all streams, docs, research, unblocking |

## Communication

- **Async first:** tracker + commit messages carry status; the daily sync handles only exceptions.
- **Escalation path:** blocked > 4 hrs → JR; JR unavailable > 2 hrs on a blocking decision → working default from 06-gaps.md applies and is flagged.
- **No status meetings besides the daily.** Questions go to the group chat with the T-number in the message.

## Quality control (NP's checklist, run daily from Jul 7)

1. Three persona walkthroughs pass on the current build.
2. Kill-switch → confidence band widens correctly.
3. Mobile viewport renders (Chrome DevTools + a real phone from Jul 8).
4. Deck numbers match research-findings.md §3 exactly (no drift).
5. Fresh clone → 2 commands → running (from Jul 8).
6. No secrets in repo (`git grep` for keys/tokens before every push).
