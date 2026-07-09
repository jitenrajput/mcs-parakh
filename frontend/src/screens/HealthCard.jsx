/* S2 — the Parakh Card, lender view: gauge + seals + reasons + propensity + CGTMSE. */

import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api, inr, BAND_COLOR } from '../api'
import { ScoreGauge, SourceSeals, DimensionRow, SyntheticStamp, Footer, RED_ON_DARK } from '../components/bits'
import { TopBar, SkeletonRows, ApiDown } from './LenderDashboard'
import KillSwitchStrip from '../components/KillSwitchStrip'

export default function HealthCard() {
  const { gstin } = useParams()
  const [r, setR] = useState(null)
  const [err, setErr] = useState(null)
  const [trend, setTrend] = useState(null)

  useEffect(() => {
    setR(null); setErr(null)
    api.score(gstin).then(setR).catch(setErr)
    api.portfolio().then(p => setTrend(p.msmes.find(m => m.gstin === gstin))).catch(() => {})
  }, [gstin])

  if (err?.status === 404) return <UnknownGstin gstin={gstin} />
  if (err) return <ApiDown retry={() => { setErr(null); api.score(gstin).then(setR).catch(setErr) }} />

  return (
    <div className="ledger-bg min-h-screen text-paper">
      <TopBar />
      <div className="max-w-6xl mx-auto px-4 pb-4">
        <div className="pt-4 flex items-center justify-between flex-wrap gap-2">
          <Link to="/lender" className="text-paper/50 text-sm hover:text-paper">← Portfolio</Link>
          {r && <Link to={`/msme/${gstin}`}
            className="bg-teal-700 hover:bg-teal-500 px-4 py-1.5 font-display font-bold text-sm">
            FLIP → what {r.name.split(' ')[0]} sees
          </Link>}
        </div>

        {!r ? <SkeletonRows /> : (
          <div className="mt-4 grid lg:grid-cols-3 gap-4">
            {/* — the card — */}
            <div className="lg:col-span-2 hairline bg-navy-900/70 p-5 rise">
              <div className="flex flex-wrap justify-between gap-4">
                <div>
                  <h2 className="font-display font-extrabold text-2xl leading-tight">{r.name}</h2>
                  <div className="font-mono text-xs text-paper/45 mt-1">{r.gstin}</div>
                  <div className="mt-4"><SourceSeals coverage={r.coverage} fetches={r.fetches} dark /></div>
                  <div className="caps-label text-paper/35 mt-1.5">data seals · {r.confidence} confidence ±{r.confidence_width}</div>
                  {trend?.alerts?.length > 0 && (
                    <div className="mt-3 border border-band-red-lit/45 bg-band-red/15 px-3 py-2 text-band-red-lit text-[13px]">
                      ⚠ {trend.alerts.map(a => a.text).join(' · ')}
                    </div>
                  )}
                </div>
                <ScoreGauge score={r.score} band={r.band} width={r.confidence_width} dark />
              </div>
              <div className="mt-4 pt-4 hairline-b border-t border-[color:var(--hair)]">
                <div className="caps-label text-paper/35 mb-2">Five dimensions · weights set by credit policy</div>
                <div className="grid sm:grid-cols-2 gap-x-8">
                  <div>{Object.entries(r.dimensions).slice(0, 3).map(([d, v]) => <DimensionRow key={d} dim={d} data={v} dark />)}</div>
                  <div>{Object.entries(r.dimensions).slice(3).map(([d, v]) => <DimensionRow key={d} dim={d} data={v} dark />)}</div>
                </div>
              </div>
              <div className="grid sm:grid-cols-2 gap-6 mt-4">
                <ReasonCol title="Working against" items={r.reasons_negative} tone={RED_ON_DARK}
                  emptyCaveat={r.missing_sources?.length ? `Limited data — ${r.missing_sources.length} of 5 sources unavailable; score is provisional` : null} />
                <ReasonCol title="Working for" items={r.reasons_positive} tone="#57B79F" />
              </div>
            </div>

            {/* — the memo rail — */}
            <div className="space-y-4">
              <div className="hairline bg-navy-900/70 p-4 rise rise-1">
                <div className="caps-label text-amber-500">Indicative eligibility</div>
                <div className="tnum font-display font-extrabold text-3xl mt-1">{inr(r.eligibility.indicative_limit)}</div>
                <div className="text-paper/50 text-xs mt-1 leading-snug">{r.eligibility.basis}</div>
                <div className="tnum font-mono text-xs text-paper/60 mt-2">
                  Annual turnover {inr(r.eligibility.annual_turnover)} · ceiling {inr(r.eligibility.nayak_ceiling)}
                </div>
              </div>
              <Propensity r={r} />
              <Cgtmse r={r} />
              <div className="hairline bg-navy-900/70 p-4 text-[11px] text-paper/40 rise rise-4">
                <div className="caps-label text-paper/35 mb-1">Decision record</div>
                engine {r.versions.engine} · scorecard {r.versions.scorecard} · dataset {r.versions.dataset}<br />
                consent {r.consent_id} · every score reconstructable (draft MRM 2026)
              </div>
            </div>
          </div>
        )}
        <Footer />
      </div>
      <KillSwitchStrip />
      <SyntheticStamp />
    </div>
  )
}

function ReasonCol({ title, items, tone, emptyCaveat }) {
  return (
    <div>
      <div className="caps-label mb-2" style={{ color: tone }}>{title}</div>
      {items.length === 0 && <div className="text-[13px] text-paper/45 py-1 italic">{emptyCaveat ?? '— none flagged'}</div>}
      {items.map((x, i) => (
        <div key={i} className="text-[13px] text-paper/80 py-1 flex gap-2">
          <span style={{ color: tone }}>▪</span> {x.text}
          <span className="ml-auto tnum font-mono text-[11px] text-paper/35">{x.points_delta > 0 ? '+' : ''}{x.points_delta}</span>
        </div>
      ))}
    </div>
  )
}

function Propensity({ r }) {
  const d = r.dimensions
  const suggestions = []
  // Band gate mirrors docs/12 RM action gates: Weak = coaching, Critical = rehab — no cross-sell.
  const rehabOnly = r.band === 'Weak' || r.band === 'Critical'
  if (!rehabOnly && d.cash_flow.score < 60 && d.growth.score >= 50) suggestions.push(['Overdraft / CC line', 'volatile inflows need a cushion, not a term EMI'])
  if (!rehabOnly && d.cash_flow.score >= 60 && d.growth.score >= 65) suggestions.push(['Term loan (expansion)', 'steady inflows + growth momentum carry an EMI'])
  if (!rehabOnly && d.growth.score >= 80) suggestions.push(['Higher WC limit review', 'turnover is outgrowing the current limit'])
  if (!rehabOnly && r.coverage.epfo_ecr) suggestions.push(['Salary account cross-sell', 'active payroll runs through EPFO'])
  if (!suggestions.length) suggestions.push(['Rehabilitation path', 'stabilize before new exposure — see MSME-side actions'])
  return (
    <div className="hairline bg-navy-900/70 p-4 rise rise-2">
      <div className="caps-label text-teal-300">Product propensity</div>
      {suggestions.slice(0, 3).map(([p, why]) => (
        <div key={p} className="mt-2">
          <div className="font-semibold text-[13.5px]">{p}</div>
          <div className="text-paper/50 text-xs">{why}</div>
        </div>
      ))}
    </div>
  )
}

function Cgtmse({ r }) {
  const ok = r.band !== 'Critical' && r.band !== 'Weak' && r.eligibility.indicative_limit <= 10e7
  return (
    <div className={`hairline p-4 rise rise-3 ${ok ? 'bg-teal-700/15' : 'bg-navy-900/70'}`}>
      <div className="caps-label" style={{ color: ok ? '#57B79F' : '#8892a6' }}>CGTMSE guarantee</div>
      <div className="font-semibold text-[13.5px] mt-1">{ok ? 'Eligible — collateral-free cover' : 'Not eligible at current band'}</div>
      <div className="text-paper/50 text-xs mt-1 leading-snug">
        Micro/Small · ≤ ₹10 Cr · no collateral/third-party guarantee · via MLI. Cover 75–90% (Circulars 250 & 241).
      </div>
    </div>
  )
}

export function UnknownGstin({ gstin }) {
  return (
    <div className="ledger-bg min-h-screen text-paper grid place-items-center px-4">
      <div className="hairline bg-navy-900/70 p-8 max-w-lg">
        <div className="font-display font-bold text-xl">That GSTIN isn't in the synthetic dataset</div>
        <div className="font-mono text-xs text-paper/40 mt-1">{gstin}</div>
        <p className="text-paper/60 text-sm mt-3">This PoC scores 65 synthetic businesses. Try one of the demo personas:</p>
        <div className="mt-3 space-y-2">
          {[['24AAACS1234F1Z5', 'Shree Ganesh Auto Components · 781 Prime'],
            ['24AABCT9876K1Z3', 'TrendKart Online · 692 Watch'],
            ['24AADCM4321P1Z8', 'Maruti Trading Co · 410 Critical']].map(([g, label]) => (
            <Link key={g} to={`/lender/${g}`} className="block hairline px-3 py-2 text-sm hover:bg-navy-800">
              <span className="font-mono text-xs text-amber-500">{g}</span> — {label}
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}
