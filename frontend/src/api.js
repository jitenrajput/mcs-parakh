const BASE = import.meta.env.VITE_API_URL || '/api'

async function req(path, opts) {
  const r = await fetch(BASE + path, {
    headers: { 'Content-Type': 'application/json' }, ...opts,
  })
  if (!r.ok) {
    const detail = await r.json().catch(() => ({}))
    throw Object.assign(new Error(detail.detail || `API ${r.status}`), { status: r.status })
  }
  return r.json()
}

export const api = {
  msmes: () => req('/msmes'),
  portfolio: () => req('/portfolio'),
  score: (gstin, consent_id) => req('/score', { method: 'POST', body: JSON.stringify({ gstin, consent_id }) }),
  getScore: gstin => req(`/score/${gstin}`),
  explain: gstin => req(`/explain/${gstin}`),
  consent: gstin => req('/consent', { method: 'POST', body: JSON.stringify({ gstin }) }),
  simulate: (gstin, actions) => req('/simulate', { method: 'POST', body: JSON.stringify({ gstin, actions }) }),
  simActions: () => req('/simulate/actions'),
  killState: () => req('/admin/killswitch'),
  kill: (source_id, killed) => req('/admin/killswitch', { method: 'POST', body: JSON.stringify({ source_id, killed }) }),
  version: () => req('/model/version'),
}

/* Indian formatting — domain texture, never $-style (docs/11 rule 4) */
export function inr(n) {
  if (n == null) return '—'
  if (Math.abs(n) >= 1e7) return `₹${(n / 1e7).toFixed(2)} Cr`
  if (Math.abs(n) >= 1e5) return `₹${(n / 1e5).toFixed(1)} L`
  return '₹' + new Intl.NumberFormat('en-IN').format(Math.round(n))
}

export const BAND_COLOR = {
  Prime: '#1E8E5A', Good: '#57B79F', Watch: '#E8A33D', Weak: '#D96F32', Critical: '#C0392B',
}
export const DIM_LABEL = {
  cash_flow: 'Cash-Flow Strength', compliance: 'Compliance Discipline',
  obligation: 'Obligation Load', growth: 'Growth Trajectory', stability: 'Business Stability',
}
export const SOURCE_META = {
  aa_deposit: { short: 'AA', label: 'Bank (AA)' },
  gst_returns: { short: 'GST', label: 'GST returns' },
  upi_months: { short: 'UPI', label: 'UPI flows' },
  epfo_ecr: { short: 'PF', label: 'EPFO payroll' },
  bureau: { short: 'CIC', label: 'Credit bureau' },
}
