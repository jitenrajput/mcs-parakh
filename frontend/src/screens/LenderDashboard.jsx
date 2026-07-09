/* S1 — the RM's Monday morning: dense navy ledger, alerts first (docs/11 rule 5). */

import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api, inr, BAND_COLOR } from '../api'
import { BrandMark, Sparkline, SyntheticStamp, Footer } from '../components/bits'
import KillSwitchStrip from '../components/KillSwitchStrip'

export default function LenderDashboard() {
  const [book, setBook] = useState(null)
  const [err, setErr] = useState(null)
  const [gstin, setGstin] = useState('')
  const nav = useNavigate()

  useEffect(() => { api.portfolio().then(setBook).catch(setErr) }, [])

  if (err) return <ApiDown retry={() => { setErr(null); api.portfolio().then(setBook).catch(setErr) }} />

  const alerts = book?.msmes.filter(m => m.alerts.length) || []
  const rest = book?.msmes.filter(m => !m.alerts.length) || []

  return (
    <div className="ledger-bg min-h-screen text-paper">
      <TopBar />
      <div className="max-w-6xl mx-auto px-4 pb-4">
        <div className="flex flex-wrap items-end justify-between gap-3 pt-5">
          <div>
            <h2 className="font-display font-bold text-xl">Portfolio · MSME Book</h2>
            <div className="text-paper/50 text-xs mt-0.5 tnum">
              {book ? `${book.count} accounts · ${book.with_alerts} on Parakh Watch` : 'Loading the book…'}
            </div>
          </div>
          <form onSubmit={e => { e.preventDefault(); if (gstin.trim()) nav(`/assess/${gstin.trim().toUpperCase()}`) }}
            className="flex">
            <input value={gstin} onChange={e => setGstin(e.target.value)} placeholder="New assessment — enter GSTIN"
              className="bg-navy-900 hairline px-3 py-2 text-sm font-mono w-72 placeholder:text-paper/30 outline-none focus:border-amber-500/60" />
            <button className="bg-amber-500 text-navy-950 px-4 font-display font-bold text-sm hover:bg-amber-400">ASSAY →</button>
          </form>
        </div>

        {!book ? <SkeletonRows /> : (
          <>
            {alerts.length > 0 && (
              <section className="mt-5">
                <div className="caps-label text-band-red-lit mb-2">⚠ Parakh Watch — needs your eyes</div>
                <div className="hairline bg-navy-900/60">
                  {alerts.map(m => <Row key={m.gstin} m={m} alert />)}
                </div>
              </section>
            )}
            <section className="mt-6">
              <div className="caps-label text-paper/40 mb-2">Book · ranked by momentum</div>
              <div className="hairline bg-navy-900/40">
                <div className="grid grid-cols-12 gap-2 px-3 py-2 caps-label text-paper/35 hairline-b">
                  <div className="col-span-4">Account</div><div className="col-span-2">Trend 8m</div>
                  <div className="col-span-1 text-right">Δ1m</div><div className="col-span-2 text-right">Score</div>
                  <div className="col-span-3 text-right">Indicative limit</div>
                </div>
                {rest.map(m => <Row key={m.gstin} m={m} />)}
              </div>
            </section>
          </>
        )}
        <Footer />
      </div>
      <KillSwitchStrip />
      <SyntheticStamp />
    </div>
  )
}

function Row({ m, alert }) {
  return (
    <Link to={`/lender/${m.gstin}`} className="ledger-row grid grid-cols-12 gap-2 px-3 py-2.5 items-center">
      <div className="col-span-4 min-w-0">
        <div className="font-semibold text-[13.5px] truncate">{m.name}
          {m.demo_persona && <span className="ml-2 text-[9px] px-1 border border-teal-300/40 text-teal-300">DEMO</span>}
        </div>
        <div className="font-mono text-[10.5px] text-paper/40">{m.gstin} · {m.city}</div>
        {alert && <div className="text-band-red-lit text-[11.5px] mt-0.5">{m.alerts[0].text}</div>}
      </div>
      <div className="col-span-2"><Sparkline series={m.trend} /></div>
      <div className={`col-span-1 text-right tnum font-mono text-xs ${m.delta_1m < 0 ? 'text-band-red' : 'text-teal-300'}`}>
        {m.delta_1m > 0 ? '+' : ''}{m.delta_1m}
      </div>
      <div className="col-span-2 text-right">
        <span className="tnum font-display font-bold text-lg" style={{ color: BAND_COLOR[m.band] }}>{m.score}</span>
        <span className="text-[10px] text-paper/40 ml-1.5">{m.band}</span>
      </div>
      <div className="col-span-3 text-right tnum font-mono text-[13px] text-paper/80">{inr(m.indicative_limit)}</div>
    </Link>
  )
}

export function TopBar() {
  return (
    <div className="hairline-b bg-navy-950/80 backdrop-blur sticky top-0 z-40">
      <div className="max-w-6xl mx-auto px-4 py-2.5 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2">
          <BrandMark size={28} />
          <span className="font-display font-bold">Parakh</span>
          <span className="caps-label text-paper/30 hidden sm:inline">Lender console</span>
        </Link>
        <div className="caps-label text-paper/30">IDBI Innovate 2026 · PoC</div>
      </div>
    </div>
  )
}

export function SkeletonRows() {
  return (
    <div className="mt-6 hairline bg-navy-900/40 animate-pulse">
      {Array.from({ length: 8 }).map((_, i) => (
        <div key={i} className="ledger-row px-3 py-3.5 flex gap-4">
          <div className="h-3 bg-paper/10 w-1/3" /><div className="h-3 bg-paper/10 w-16" /><div className="h-3 bg-paper/10 w-10 ml-auto" />
        </div>
      ))}
    </div>
  )
}

export function ApiDown({ retry }) {
  return (
    <div className="ledger-bg min-h-screen text-paper grid place-items-center px-4">
      <div className="hairline bg-navy-900/70 p-8 max-w-md text-center">
        <div className="font-display font-bold text-2xl">Warming up the engine…</div>
        <p className="text-paper/60 text-sm mt-2">The scoring service is starting (free-tier demo hosting naps when idle). Give it ~10 seconds.</p>
        <button onClick={retry} className="mt-4 bg-amber-500 text-navy-950 px-5 py-2 font-display font-bold text-sm hover:bg-amber-400">RETRY</button>
      </div>
    </div>
  )
}
