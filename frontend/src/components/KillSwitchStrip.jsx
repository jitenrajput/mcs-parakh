/* S9 — demo control strip: kill a source live, watch the band widen (UC5). */

import { useEffect, useState } from 'react'
import { api } from '../api'

export default function KillSwitchStrip() {
  const [state, setState] = useState(null)
  const [open, setOpen] = useState(false)

  useEffect(() => { api.killState().then(setState).catch(() => {}) }, [])

  const toggle = async s => setState(await api.kill(s.source_id, !s.killed))

  return (
    <div className="fixed bottom-4 left-4 z-50">
      {open && state && (
        <div className="mb-2 hairline bg-navy-950/95 backdrop-blur p-3 w-64 seal-in">
          <div className="caps-label text-amber-500 mb-2">Demo panel · kill a source</div>
          {state.sources.map(s => (
            <label key={s.source_id} className="flex items-center justify-between py-1 text-[13px] text-paper/85 cursor-pointer">
              <span className={s.killed ? 'line-through text-band-red' : ''}>{s.label}</span>
              <input type="checkbox" checked={!s.killed} onChange={() => toggle(s)} className="accent-teal-500" />
            </label>
          ))}
          <p className="text-[10.5px] text-paper/40 mt-2 leading-snug">
            Re-run any assessment after killing a source: the score survives, the confidence band widens. That's the point.
          </p>
        </div>
      )}
      <button onClick={() => setOpen(o => !o)}
        className="hairline bg-navy-950/90 text-amber-500 px-3 py-1.5 caps-label hover:bg-navy-800">
        ⏻ demo panel
      </button>
    </div>
  )
}
