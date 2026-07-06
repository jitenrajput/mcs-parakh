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
export function DimensionRow({ dim, data, dark }) {
  return (
    <div className="flex items-center gap-3 py-1.5">
      <GradeChip grade={data.grade} dark={dark} />
      <div className="flex-1 min-w-0">
        <div className={`text-[13px] font-semibold truncate ${dark ? 'text-paper/90' : 'text-ink'}`}>{DIM_LABEL[dim]}</div>
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
        return (
          <div key={sid} title={meta.label + (ok ? ' — included' : failed ? ' — provider unreachable' : ' — no data held')}
            className={`${dims} stamp-chip font-mono font-semibold ${ok ? '' : 'opacity-35'}`}
            style={{
              color: ok ? '#57B79F' : failed ? '#C0392B' : (dark ? '#8892a6' : '#485062'),
              border: `1.5px ${ok ? 'solid' : 'dashed'} currentColor`,
            }}>
            {meta.short}
          </div>
        )
      })}
    </div>
  )
}

/* The gauge: 300-900 arc, band-coloured segments, confidence halo */
export function ScoreGauge({ score, band, width, dark, size = 240 }) {
  const cx = size / 2, cy = size / 2 + 10, r = size / 2 - 18
  const a0 = Math.PI, toXY = a => [cx + r * Math.cos(a), cy - r * Math.sin(a)]
  const frac = v => Math.max(0, Math.min(1, (v - 300) / 600))
  const arc = (v1, v2, rr = r) => {
    const [x1, y1] = [cx + rr * Math.cos(a0 - frac(v1) * Math.PI), cy - rr * Math.sin(a0 - frac(v1) * Math.PI)]
    const [x2, y2] = [cx + rr * Math.cos(a0 - frac(v2) * Math.PI), cy - rr * Math.sin(a0 - frac(v2) * Math.PI)]
    return `M ${x1} ${y1} A ${rr} ${rr} 0 ${frac(v2) - frac(v1) > 0.5 ? 1 : 0} 1 ${x2} ${y2}`
  }
  const bands = [[300, 480, '#C0392B'], [480, 600, '#D96F32'], [600, 720, '#E8A33D'], [720, 780, '#57B79F'], [780, 900, '#1E8E5A']]
  const na = a0 - frac(score) * Math.PI
  const [nx, ny] = toXY(na)
  return (
    <svg width={size} height={size * 0.62} viewBox={`0 0 ${size} ${size * 0.62}`} className="overflow-visible">
      {width ? <path d={arc(Math.max(300, score - width), Math.min(900, score + width), r)} stroke={BAND_COLOR[band]} strokeOpacity="0.18" strokeWidth="22" fill="none" /> : null}
      {bands.map(([v1, v2, c]) => <path key={v1} d={arc(v1 + 4, v2 - 4)} stroke={c} strokeWidth="5" fill="none" strokeLinecap="butt" opacity={dark ? 0.85 : 0.9} />)}
      <line x1={cx} y1={cy} x2={nx} y2={ny} stroke={dark ? '#F7F5F0' : '#1C2434'} strokeWidth="2.5" />
      <circle cx={cx} cy={cy} r="5" fill={BAND_COLOR[band]} stroke={dark ? '#F7F5F0' : '#1C2434'} strokeWidth="1.5" />
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
    <div className="fixed bottom-4 right-4 z-50 text-band-red/70 synthetic-stamp bg-paper/40 backdrop-blur-[1px]">
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
