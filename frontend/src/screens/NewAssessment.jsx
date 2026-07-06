/* S3+S4+S5 — GSTIN → AA-style consent (the compliance showpiece) → card assembles. */

import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { api, SOURCE_META } from '../api'
import { SyntheticStamp } from '../components/bits'
import { TopBar } from './LenderDashboard'
import { UnknownGstin } from './HealthCard'

export default function NewAssessment() {
  const { gstin } = useParams()
  const nav = useNavigate()
  const [step, setStep] = useState('consent')       // consent | fetching | declined
  const [fetches, setFetches] = useState([])
  const [notFound, setNotFound] = useState(false)

  const approve = async () => {
    setStep('fetching')
    try {
      const consent = await api.consent(gstin)
      const r = await api.score(gstin, consent.consent_id)
      // reveal seals one by one — the theatre moment (S5)
      for (let i = 0; i < r.fetches.length; i++) {
        await new Promise(res => setTimeout(res, 420))
        setFetches(f => [...f, r.fetches[i]])
      }
      await new Promise(res => setTimeout(res, 650))
      nav(`/lender/${gstin}`)
    } catch (e) {
      if (e.status === 404) setNotFound(true); else setStep('consent')
    }
  }

  if (notFound) return <UnknownGstin gstin={gstin} />

  return (
    <div className="ledger-bg min-h-screen text-paper">
      <TopBar />
      <div className="max-w-xl mx-auto px-4 py-10">
        {step === 'consent' && (
          <div className="hairline bg-paper text-ink p-6 rise">
            <div className="caps-label text-teal-700">Account Aggregator consent · mock journey</div>
            <h2 className="font-display font-extrabold text-xl mt-1">Share your business data with IDBI Bank?</h2>
            <div className="mt-4 space-y-2 text-[13.5px]">
              <KV k="Who is asking" v="IDBI-Parakh-PoC (FIU)" />
              <KV k="Purpose (code 103)" v="Aggregated statement — credit underwriting" />
              <KV k="Data requested" v="DEPOSIT · GSTR1_3B · last 24 months" />
              <KV k="Also, with your separate consent" v="EPFO payroll (employer route) · bureau report" />
              <KV k="Valid for" v="90 days · one-time fetch" />
              <KV k="Withdraw" v="Anytime — as easily as you give it (DPDP Rules 2025)" />
            </div>
            <div className="mt-4 bg-paper-dark p-3 text-xs text-ink-soft leading-relaxed">
              Only the fields needed for your score are used — nothing else is stored (data minimization).
              The Account Aggregator never sees your data: it flows encrypted from your bank to the lender.
              No phone contacts, no photos, no biometrics — ever.
            </div>
            <div className="mt-5 flex gap-3">
              <button onClick={approve} className="flex-1 bg-teal-700 text-paper py-2.5 font-display font-bold hover:bg-teal-500">
                APPROVE with OTP (mock)
              </button>
              <button onClick={() => setStep('declined')} className="px-5 hairline-teal text-teal-700 font-semibold text-sm hover:bg-teal-700/10">
                Decline
              </button>
            </div>
            <div className="font-mono text-[10px] text-ink-soft/60 mt-3">GSTIN {gstin} · ReBIT consent-artefact fields · AA Master Direction para 6.3</div>
          </div>
        )}

        {step === 'declined' && (
          <div className="hairline bg-paper text-ink p-6 text-center rise">
            <div className="font-display font-bold text-xl">No problem — nothing was accessed.</div>
            <p className="text-ink-soft text-sm mt-2">No data was pulled, nothing was stored. You can start again anytime.</p>
            <button onClick={() => setStep('consent')} className="mt-4 bg-teal-700 text-paper px-6 py-2 font-display font-bold text-sm">Start again</button>
          </div>
        )}

        {step === 'fetching' && (
          <div className="text-center pt-8">
            <div className="caps-label text-amber-500">Assaying {gstin}</div>
            <div className="font-display font-bold text-2xl mt-1">Collecting the seals…</div>
            <div className="flex justify-center gap-4 mt-8 flex-wrap">
              {fetches.map(f => (
                <div key={f.source} className="seal-in">
                  <div className={`w-16 h-16 stamp-chip font-mono text-sm ${f.status === 'OK' ? '' : 'opacity-50'}`}
                    style={{ color: f.status === 'OK' ? '#57B79F' : '#C0392B', border: `2px ${f.status === 'OK' ? 'solid' : 'dashed'} currentColor` }}>
                    {SOURCE_META[f.source]?.short}
                  </div>
                  <div className={`text-[10px] mt-1.5 ${f.status === 'OK' ? 'text-teal-300' : 'text-band-red'}`}>
                    {f.status === 'OK' ? (f.error ? 'no file held' : 'sealed ✓') : 'unreachable'}
                  </div>
                </div>
              ))}
            </div>
            {fetches.some(f => f.status === 'FAILED') && (
              <p className="text-paper/60 text-sm mt-6 max-w-sm mx-auto">
                A source didn't respond — that's normal in the real world. Parakh scores on what it has
                and widens the confidence band instead of failing.
              </p>
            )}
          </div>
        )}
      </div>
      <SyntheticStamp />
    </div>
  )
}

function KV({ k, v }) {
  return (
    <div className="flex justify-between gap-4 border-b border-ink/10 pb-1.5">
      <span className="text-ink-soft">{k}</span><span className="font-semibold text-right">{v}</span>
    </div>
  )
}
