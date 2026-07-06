# 10 — UX: Users, Journeys, Screens (LOCKED Jul 06)

## Users — six exist, two + the jury get built

| # | User | PoC treatment |
|---|---|---|
| U1 | RM / Credit Officer | **BUILD** — merged "Lender" role |
| U2 | MSME Owner | **BUILD** — mobile-first, EN/HI/GU |
| U3 | Credit-policy team | Deck + static weights-config screen if cheap |
| U4 | Auditor/Regulator | Deck only (audit stub backs it) |
| U5 | IDBI executive | Deck only (business slide) |
| U6 | **The Jury** | **BUILD** — Demo Launcher; jurors open the link alone, no narrator |

## Journeys
- **J1 Lender** — "RM's Monday morning": portfolio → alert triage (Maruti −55) → reasons → new lead → consent → card assembles (one source fails → band widens) → 690 NTC → propensity + CGTMSE.
- **J2 MSME** — "Meena finds her next ₹10 lakh": invite → AA consent (HI/GU toggle) → own card → improve actions in ₹ → simulator (+₹3.8L) → readiness meter.
- **J3 Jury** — unguided 3 minutes: Launcher → RM seat → alert → drill → flip → simulator. **Every screen must survive being the first screen.**

## Screens (11)

| # | Screen | Notes |
|---|---|---|
| S0 | Demo Launcher (MUST) | Seat-picker (RM/MSME), 3 persona cards, 30-sec explainer, reset, synthetic banner |
| S1 | Portfolio dashboard | Ranked book, sparklines, alert badges |
| S2 | Health Card detail | Gauge + coverage ring + A–E chips + reasons + trend + propensity + CGTMSE |
| S3 | New assessment (GSTIN) | Kicks off consent |
| S4 | Consent (AA 7-step + DPDP) | Compliance showpiece |
| S5 | Card assembling | Sources light up; kill-switch theatre |
| S6 | MSME: My Health Card | Language toggle |
| S7 | MSME: Improve + Simulator | THE wow screen |
| S8 | MSME: Readiness meter | Today vs after |
| S9 | Demo control strip | Kill-switches, persona switcher, clearly a demo panel |
| S10 | API docs (/docs) | FastAPI freebie, linked in footer |

## UX hard rules
1. 5-second rule on lender screens. 2. Rupees, not points (MSME). 3. No dead ends — every element taps open its "why". 4. Confidence always visible (ring travels with score). 5. Two dialects, one system: lender = dense/desktop/analyst; MSME = warm/mobile/vernacular.

## Error & empty states (7 — a juror can never reach an un-designed screen)
Consent declined (friendly restart) · one source failed (ring dims + toast, doubles as kill-switch visual) · all failed (reset prompt) · unknown GSTIN (persona chips = error becomes navigation) · empty portfolio (skeleton cards) · API cold ("warming up the engine" + retry) · 404 (silent redirect to S0). NP tests all seven deliberately.

## Locked resolutions (Jul 06)
1. **Demo script** — 2-min narration drafted (internal `ux-design.md`); JT fits to screens; **JR voices** (founder first-person).
2. **Logo** — hallmark-stamp "प" concept (A); CL generates SVGs Jul 7, JR picks.
3. **Error states** — the 7 above, designed treatment, MUST.
4. **URL** — `parakh.mconnectsolutions.com` (owned domain, ₹0, CNAME on Jul 8).
5. **Hygiene** — synthetic-data disclaimer page, event footer, slowapi rate limit (60 req/min/IP), UptimeRobot 5-min ping (doubles as keep-warm).
6. **Deck ↔ app consistency** — `tokens.json` read by Tailwind AND copied to Slides master; screenshots only from the deployed app.
7. **Microcopy** — "helpful CA" voice; ~10 critical strings in EN/HI/GU (`strings.json`), JR native-reviews Jul 7 eve.
8. **Pitch roles** — JR: open/business/close + architecture (cheat card) · JT: drives demo · ZS: model/parameter Q&A (translation table) · NP: timekeeper + backup laptop/hotspot. Every role has an understudy (JR).
