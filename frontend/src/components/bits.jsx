/* Signature components — the hallmark metaphor made real (docs/11 rule 3). */

import { BAND_COLOR, SOURCE_META, DIM_LABEL } from '../api'

/* Assay-stamp grade chip: notched corner, stamped letter */
export function GradeChip({ grade, dark }) {
  const tone = { A: '#1E8E5A', B: '#57B79F', C: '#E8A33D', D: '#D96F32', E: '#C0392B' }[grade] || '#888'
  return (
    <span className="stamp-chip w-7 h-7 text-sm"
      style={{ color: tone, border: `1.5px solid ${tone}`, background: dark ? 'rgba(0,0,0,0.25)' : 'rgba(255,255,255,0.5)' }}>
      {grade}
    </span>
  )
}

/* Dimension bar: grade chip + thin bar underneath (locked design) */
export function DimensionRow({ dim, data, dark, label }) {
  return (
    <div className="flex items-center gap-3 py-1.5">
      <GradeChip grade={data.grade} dark={dark} />
      <div className="flex-1 min-w-0">
        <div className="flex items-baseline gap-1.5">
          <div className={`text-[13px] font-semibold truncate ${dark ? 'text-paper/90' : 'text-ink'}`}>{label ?? DIM_LABEL[dim]}</div>
          {data.weight != null && (
            <span className={`tnum font-mono text-[10px] shrink-0 ${dark ? 'text-paper/40' : 'text-ink-soft'}`}
              title="weight set by credit policy">{Math.round(data.weight * 100)}%</span>
          )}
        </div>
        <div className={`h-[3px] mt-1 ${dark ? 'bg-paper/10' : 'bg-ink/10'}`}>
          <div className="h-full" style={{ width: `${data.score}%`, background: BAND_COLOR[data.score >= 80 ? 'Prime' : data.score >= 65 ? 'Good' : data.score >= 50 ? 'Watch' : data.score >= 35 ? 'Weak' : 'Critical'] }} />
        </div>
      </div>
      <div className={`tnum font-mono text-xs ${dark ? 'text-paper/50' : 'text-ink-soft'}`}>{data.score}</div>
    </div>
  )
}

/* Seal-dot coverage ring: five source seals, lit or dim — the confidence WHY */
export function SourceSeals({ coverage, fetches, dark, size = 'md' }) {
  const dims = size === 'md' ? 'w-9 h-9 text-[10px]' : 'w-7 h-7 text-[9px]'
  return (
    <div className="flex gap-2">
      {Object.entries(SOURCE_META).map(([sid, meta]) => {
        const ok = coverage?.[sid]
        const failed = fetches?.find(f => f.source === sid)?.status === 'FAILED'
        /* An off seal states a fact ("not counted"), not an error — so it stays legible
           grey whether the provider is down or simply holds nothing. Why it is off
           lives in the tooltip, the fetch banner and the coverage caveat. */
        return (
          <div key={sid} title={meta.label + (ok ? ' — included' : failed ? ' — provider unreachable' : ' — no data held')}
            className={`${dims} stamp-chip font-mono font-semibold`}
            style={{
              color: ok ? '#57B79F' : (dark ? '#C6CEDA' : '#4C5768'),
              border: `1.5px ${ok ? 'solid' : 'dashed'} currentColor`,
              background: ok ? 'transparent' : (dark ? 'rgba(198,206,218,0.08)' : 'rgba(76,87,104,0.06)'),
            }}>
            {meta.short}
          </div>
        )
      })}
    </div>
  )
}

/* The gauge: 300-900 arc, band-coloured segments, confidence halo */
/* Option B "Navy Assay" hallmark mark — JR's pick, T-312 (assets/brand/logo-b-navy-assay.svg).
   Keyline thickened slightly so it survives 28px header rendering. */
export function BrandMark({ size = 28 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 120 120" className="shrink-0" aria-label="Parakh">
      <rect x="8" y="8" width="104" height="104" rx="22" fill="#14243D" />
      <rect x="15" y="15" width="90" height="90" rx="16" fill="none" stroke="#0E6E5C" strokeWidth="5" />
      <path d="M8 86 L8 90 A22 22 0 0 0 30 112 L34 112 Z" fill="#E8A33D" />
      <text x="60" y="86" textAnchor="middle" fontFamily="Mukta,'Noto Sans Devanagari','Nirmala UI',sans-serif"
        fontWeight="700" fontSize="62" fill="#F7F5F0">प</text>
    </svg>
  )
}

export function ScoreGauge({ score, band, width, dark, size = 240 }) {
  const cx = size / 2, cy = size / 2 + 10, r = size / 2 - 18
  const a0 = Math.PI
  const frac = v => Math.max(0, Math.min(1, (v - 300) / 600))
  const arc = (v1, v2, rr = r) => {
    const [x1, y1] = [cx + rr * Math.cos(a0 - frac(v1) * Math.PI), cy - rr * Math.sin(a0 - frac(v1) * Math.PI)]
    const [x2, y2] = [cx + rr * Math.cos(a0 - frac(v2) * Math.PI), cy - rr * Math.sin(a0 - frac(v2) * Math.PI)]
    return `M ${x1} ${y1} A ${rr} ${rr} 0 ${frac(v2) - frac(v1) > 0.5 ? 1 : 0} 1 ${x2} ${y2}`
  }
  const bands = [[300, 480, '#C0392B'], [480, 600, '#D96F32'], [600, 720, '#E8A33D'], [720, 780, '#57B79F'], [780, 900, '#1E8E5A']]
  const na = a0 - frac(score) * Math.PI
  return (
    <svg width={size} height={size * 0.62} viewBox={`0 0 ${size} ${size * 0.62}`} className="overflow-visible">
      {bands.map(([v1, v2, c]) => <path key={v1} d={arc(v1 + 4, v2 - 4)} stroke={c} strokeWidth="6" fill="none" strokeLinecap="butt" opacity={dark ? 0.9 : 0.92} />)}
      {/* confidence range = thin bracket arc OUTSIDE the colour scale — shows ±width without smearing the bands */}
      {width ? <path d={arc(Math.max(300, score - width), Math.min(900, score + width), r + 10)} stroke={BAND_COLOR[band]} strokeOpacity="0.85" strokeWidth="3" strokeLinecap="round" fill="none" /> : null}
      {/* pointer = tick across the arc + band-color jewel just inside it — clears the score digits at any angle.
         Outer end stops short of the bracket arc (r+10) so the tick never crosses it. */}
      <line x1={cx + (r - 16) * Math.cos(na)} y1={cy - (r - 16) * Math.sin(na)}
        x2={cx + (r + 5) * Math.cos(na)} y2={cy - (r + 5) * Math.sin(na)}
        stroke={dark ? '#F7F5F0' : '#1C2434'} strokeWidth="3" />
      <circle cx={cx + r * 0.76 * Math.cos(na)} cy={cy - r * 0.76 * Math.sin(na)} r="4.5"
        fill={BAND_COLOR[band]} stroke={dark ? '#F7F5F0' : '#1C2434'} strokeWidth="1.5" />
      <text x={cx} y={cy - r * 0.36} textAnchor="middle" className="tnum"
        fontFamily="Mukta" fontWeight="800" fontSize={size * 0.19} fill={dark ? '#F7F5F0' : '#1C2434'}>{score}</text>
      <text x={cx} y={cy - r * 0.16} textAnchor="middle" fontFamily="Mukta" fontWeight="700"
        fontSize={size * 0.062} letterSpacing="2" fill={BAND_COLOR[band]}>{band?.toUpperCase()}{width ? `  ±${width}` : ''}</text>
      <text x={cx - r} y={cy + 14} textAnchor="middle" fontSize="10" fill={dark ? '#8892a6' : '#485062'} className="tnum">300</text>
      <text x={cx + r} y={cy + 14} textAnchor="middle" fontSize="10" fill={dark ? '#8892a6' : '#485062'} className="tnum">900</text>
    </svg>
  )
}

/* Sparkline for portfolio trends */
export function Sparkline({ series, w = 96, h = 26 }) {
  if (!series?.length) return null
  const scores = series.map(p => p.score)
  const min = Math.min(...scores) - 8, max = Math.max(...scores) + 8
  const pts = scores.map((s, i) => `${(i / (scores.length - 1)) * w},${h - ((s - min) / (max - min)) * h}`).join(' ')
  const falling = scores[scores.length - 1] < scores[0]
  return (
    <svg width={w} height={h} className="overflow-visible">
      <polyline points={pts} fill="none" stroke={falling ? '#C0392B' : '#57B79F'} strokeWidth="1.75" />
      <circle cx={w} cy={h - ((scores[scores.length - 1] - min) / (max - min)) * h} r="2.4" fill={falling ? '#C0392B' : '#57B79F'} />
    </svg>
  )
}

export function SyntheticStamp({ t }) {
  return (
    <div className="fixed bottom-4 right-4 z-50 synthetic-stamp bg-paper/85"
      style={{ color: '#C0392B' }}>
      {t?.('synthetic') || 'SYNTHETIC DATA'} · DS-42-2026.07
    </div>
  )
}

export function Footer() {
  return (
    <div className="text-center text-[11px] py-6 opacity-50">
      MCS Parakh · Team M-Connect Labs · built for IDBI Innovate 2026 · all data synthetic ·{' '}
      <a className="underline" href={(import.meta.env.VITE_API_URL || '/api') + '/docs'} target="_blank" rel="noreferrer">API docs</a>
    </div>
  )
}
