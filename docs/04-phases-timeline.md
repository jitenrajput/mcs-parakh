# 04 — Phases & Timeline

Five phases; each has an **exit gate** — a binary check, not a feeling. A phase isn't done until its gate passes. If a gate is at risk, we cut COULD/SHOULD scope (see 06-gaps.md cut-list), never the gate.

## Phase map

| Phase | Window | Theme | Exit gate |
|---|---|---|---|
| **P0 Research & blueprint** | Jul 3–6 | PS locked, research verified 2×, this blueprint | ✅ DONE (this doc set committed) |
| **P1 Foundation** | Mon Jul 6 (eve) → Tue Jul 7 (noon) | Data fidelity + scoring engine | `pytest` green; all 3 personas score in expected bands (~780 / ~690 / ~410) with correct reason codes from CLI |
| **P2 End-to-end product** | Tue Jul 7 → Wed Jul 8 (noon) | API + full UI | Full demo flow clickable locally: GSTIN → consent → card → flip → portfolio; kill-switch works |
| **P3 Ship & tell** | Wed Jul 8 | Deploy + deck + QA hardening | Public URLs pass phone + incognito test; deck PDF ≤ 5 MB with 10/10 stats sourced; README 2-command run verified on fresh clone |
| **P4 Submit** | Thu Jul 9 AM | Submission + confirmation | Submitted before noon IST; screenshot saved; Hack2Skill team formation confirmed |
| **P5 Prototype prep** | Jul 10–21 (light) | Await shortlist; pre-read IDBI sandbox docs; rest | Shortlist Jul 21 → G2 kickoff |

## Day-by-day timeline

### Mon Jul 6 (evening) — P1 start
- Upgrade `datagen` to ReBIT `deposit.xsd` + `GSTR1_3B` field fidelity (FR-2.3, NFR-8); regenerate dataset; verify personas + 2 deteriorating accounts. — *Zaid + Claude*
- Scaffold `parakh_engine` pure module + test skeleton. — *Claude*
- **Team actions:** confirm frontend owner · confirm/adjust the 3 working defaults (06-gaps.md §3).

### Tue Jul 7 — P1 close, P2 core
- AM: scorecard (bins/points/weights/scaling) + reason codes + confidence bands + unit tests → **P1 gate**. — *Zaid + Claude*
- PM: `SourceAdapter` + 5 mocks + kill-switch; FastAPI routes + Pydantic schemas + audit stub; score time-series + alert rules. — *Claude + Zaid*
- PM (parallel): React scaffold; Health Card + consent screen against local API. — *Frontend + Claude*

### Wed Jul 8 — P2 close, P3
- AM: lender portfolio + MSME view + flip; propensity + CGTMSE panels → **P2 gate** by noon. — *Frontend + Claude*
- PM: Docker → App Runner; frontend → Amplify; DynamoDB/SQLite decision executed; phone + incognito test → **P3 gate**. — *Jitendra + Claude*
- PM (parallel): deck in IDBI template — stats ONLY from `research-findings.md` §3; screenshots from deployed app; 2-min demo video (optional). — *Jitendra + Jayesh*
- Stretch (only if P2 gate passed by noon): LightGBM + SHAP lens (FR-1.7). — *Zaid*
- QA all day: persona walkthroughs, deck-vs-demo consistency, fresh-clone test. — *Nirmal*

### Thu Jul 9 — P4
- 09:00 final team review (15 min, blocking issues only).
- 10:00 export PDF ≤ 5 MB, fill slide-1 template fields, **submit deck + demo link + repo link**.
- Verify team formation complete on Hack2Skill (separate deadline, same day).
- Save confirmation screenshot. Done.

## Slack & buffers

- GBM lens, propensity panel, demo video = pre-agreed cut list (in cut order).
- Deploy fallback: Render/Railway if App Runner burns > 3 hours.
- Jul 8 evening is the hard buffer: nothing new starts after 20:00 Jul 8 — polish and QA only.
