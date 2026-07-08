/* S6+S7+S8 — Meena's phone: warm paper, her language, rupee-priced actions.
   Kal-Parakh re-runs the REAL engine — and we say so on screen. */

import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api, inr, DIM_LABEL } from '../api'
import { ScoreGauge, SourceSeals, DimensionRow, SyntheticStamp } from '../components/bits'
import { useT, LangToggle, STRINGS, locReason } from '../i18n'

const ACTION_ORDER = ['gst_on_time_3m', 'gst_on_time_6m', 'clear_bounces_6m', 'reduce_emi_25pct']

export default function MsmeView() {
  const { gstin } = useParams()
  const { t, lang } = useT()
  const [r, setR] = useState(null)
  const [actions, setActions] = useState([])
  const [picked, setPicked] = useState([])
  const [sim, setSim] = useState(null)
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    setR(null); setSim(null); setPicked([])
    api.score(gstin).then(setR).catch(() => {})
    api.simActions(gstin).then(d => setActions(ACTION_ORDER.map(id => d.actions.find(a => a.id === id)).filter(Boolean)))
  }, [gstin])

  const runSim = async next => {
    setPicked(next)
    if (!next.length) return setSim(null)
    setBusy(true)
    try { setSim(await api.simulate(gstin, next)) } finally { setBusy(false) }
  }

  if (!r) return <div className="paper-bg min-h-screen grid place-items-center text-ink-soft font-display">Loading your card…</div>

  const first = r.name.split(' ')[0]
  const shown = sim?.after ?? { score: r.score, band: r.band, indicative_limit: r.eligibility.indicative_limit }
  // When a projection is active, the whole card reflects the simulated future.
  const dims = sim?.after?.dimensions ?? r.dimensions
  const posReasons = sim?.after?.reasons_positive ?? r.reasons_positive
  const negReasons = sim?.after?.reasons_negative ?? r.reasons_negative
  const missingN = r.missing_sources?.length || 0
  const riskCaveat = missingN > 0 ? (STRINGS[lang]?.limited_data ?? STRINGS.en.limited_data).replace('{n}', missingN) : null

  return (
    <div className="paper-bg min-h-screen text-ink pb-10" lang={lang}>
      <div className="max-w-md mx-auto px-4">
        <div className="flex items-center justify-between pt-5">
          <Link to="/" className="text-ink-soft text-sm">← Parakh</Link>
          <LangToggle />
        </div>

        {/* — her card — */}
        <div className="mt-4 bg-paper border-2 border-ink/80 p-5 relative rise"
          style={{ boxShadow: '6px 6px 0 rgba(28,36,52,0.12)' }}>
          <div className="absolute -top-px -right-px w-6 h-6 bg-amber-500" style={{ clipPath: 'polygon(0 0,100% 0,100% 100%)' }} />
          <div className="caps-label text-teal-700">{t('your_score')}</div>
          <div className="font-display font-extrabold text-xl leading-tight mt-0.5">{r.name}</div>
          <div className="flex justify-center -mt-1"><ScoreGauge score={shown.score} band={shown.band} width={sim ? 0 : r.confidence_width} size={230} /></div>
          {sim && (
            <div className="text-center -mt-2 mb-1 text-teal-700 font-display font-bold seal-in">
              {r.score} → {shown.score} <span className="text-band-green">(+{sim.delta_score})</span>
            </div>
          )}
          <p className="text-center text-xs text-ink-soft">{t('band_note')}</p>
          <div className="flex items-center justify-between mt-4 pt-3 border-t border-ink/15">
            <div>
              <div className="caps-label text-ink-soft/70">{t('data_used')}</div>
              <div className="mt-1"><SourceSeals coverage={r.coverage} fetches={r.fetches} size="sm" /></div>
            </div>
            <div className="text-right">
              <div className="caps-label text-ink-soft/70">{t('confidence')}</div>
              <div className="font-display font-bold">{t('conf_' + r.confidence.toLowerCase())} ±{r.confidence_width}</div>
            </div>
          </div>
        </div>

        {/* — readiness meter — */}
        <div className="mt-4 bg-navy-800 text-paper p-4 rise rise-1" style={{ boxShadow: '6px 6px 0 rgba(28,36,52,0.18)' }}>
          <div className="caps-label text-amber-500">{t('readiness')}</div>
          <div className="flex items-end justify-between mt-1">
            <div>
              <div className="text-paper/60 text-xs">{t('eligible_today')}</div>
              <div className="tnum font-display font-extrabold text-2xl">{inr(r.eligibility.indicative_limit)}</div>
            </div>
            {sim && (
              <div className="text-right seal-in">
                <div className="text-teal-300 text-xs">{t('eligible_after')}</div>
                <div className="tnum font-display font-extrabold text-2xl text-band-green">{inr(sim.after.indicative_limit)}</div>
                {sim.delta_limit > 0 && <div className="text-band-green text-sm font-bold">+{inr(sim.delta_limit)}</div>}
              </div>
            )}
          </div>
          <div className="text-paper/45 text-[11px] mt-2">{t('apply_hint')}</div>
        </div>

        {/* — Kal-Parakh — */}
        <div className="mt-4 rise rise-2">
          <div className="font-display font-extrabold text-lg">{t('improve')} <span className="caps-label text-teal-700 ml-1">Kal-Parakh · कल-परख</span></div>
          <p className="text-ink-soft text-[12.5px] mt-0.5">{t('improve_sub')}</p>
          <div className="mt-3 space-y-2">
            {actions.map(a => {
              const on = picked.includes(a.id)
              const na = a.applicable === false  // doesn't move THIS business's score
              const loc = STRINGS[lang]?.actions?.[a.id] ?? a  // localized label/hint, API text as fallback
              return (
                <button key={a.id} disabled={busy || na}
                  onClick={() => runSim(on ? picked.filter(x => x !== a.id) : [...picked, a.id])}
                  className={`w-full text-left p-3 border-2 transition-all ${na ? 'border-ink/10 bg-ink/[0.03] opacity-55 cursor-not-allowed' : on ? 'border-teal-700 bg-teal-700/10' : 'border-ink/20 bg-paper hover:border-ink/40'}`}>
                  <div className="flex items-center gap-2.5">
                    <span className={`w-5 h-5 stamp-chip text-[11px] ${on ? 'bg-teal-700 text-paper' : 'border border-ink/30 text-transparent'}`}>✓</span>
                    <span className="font-semibold text-[13.5px] flex-1">{loc.label}</span>
                  </div>
                  <div className={`text-[11px] mt-1 ml-7 ${na ? 'text-teal-700 italic' : 'text-ink-soft'}`}>{na ? t('not_applicable') : loc.hint}</div>
                </button>
              )
            })}
          </div>
          {picked.length > 0 && (
            <button onClick={() => runSim([])} className="mt-2 text-teal-700 text-sm underline">{t('reset')}</button>
          )}
          {sim && (
            <div className="mt-3 bg-paper-dark border border-ink/15 p-3 text-[11.5px] text-ink-soft seal-in">
              ⚙ {lang === 'en' ? sim.note : t('sim_note')}
            </div>
          )}
        </div>

        {/* — strengths & risks in plain words — */}
        <div className="mt-5 grid grid-cols-1 gap-4 rise rise-3">
          <PlainList title={t('strengths')} items={posReasons} tone="#1E8E5A" lang={lang} />
          <PlainList title={t('risks')} items={negReasons} tone="#C0392B" lang={lang} emptyCaveat={riskCaveat} />
        </div>

        <div className="mt-5 rise rise-4">
          <div className="caps-label text-ink-soft/70 mb-1">{t('score_makeup')}</div>
          {Object.entries(dims).map(([d, v]) => <DimensionRow key={d} dim={d} data={v} label={STRINGS[lang]?.dims?.[d] ?? DIM_LABEL[d]} />)}
        </div>

        <div className="text-center text-[10.5px] text-ink-soft/60 mt-8">
          MCS Parakh · {t('built_for')} · {t('synthetic')} · {t('card_yours').replace('{name}', first)}
        </div>
      </div>
      <SyntheticStamp t={t} />
    </div>
  )
}

function PlainList({ title, items, tone, lang, emptyCaveat }) {
  return (
    <div className="bg-paper border border-ink/20 p-4">
      <div className="caps-label mb-2" style={{ color: tone }}>{title}</div>
      {items.length === 0 && <div className="text-[13.5px] py-1 italic text-ink-soft/50">{emptyCaveat ?? '— ' + (STRINGS[lang]?.none_flagged ?? STRINGS.en.none_flagged)}</div>}
      {items.map((x, i) => (
        <div key={i} className="text-[13.5px] py-1 flex gap-2"><span style={{ color: tone }}>▪</span>{locReason(x, lang)}</div>
      ))}
    </div>
  )
}
