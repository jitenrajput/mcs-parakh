/* S0 — Demo Launcher: built for the jury (U6). Nobody lands on a login screen. */

import { Link } from 'react-router-dom'
import { Footer, SyntheticStamp } from '../components/bits'

const PERSONAS = [
  { gstin: '24AAACS1234F1Z5', name: 'Shree Ganesh Auto Components', who: 'Rameshbhai Patel · Rajkot',
    story: '12 years, 18 employees, supplies two OEMs. Wants a CNC machine.', score: '781 · Prime', tone: '#1E8E5A' },
  { gstin: '24AABCT9876K1Z3', name: 'TrendKart Online', who: 'Meena Shah · Surat',
    story: 'Ethnic wear online. No CIBIL file at all — invisible to every bureau.', score: '692 · Watch', tone: '#E8A33D' },
  { gstin: '24AADCM4321P1Z8', name: 'Maruti Trading Co', who: 'Dineshbhai Soni · Ahmedabad',
    story: 'Textiles trader, 9 years. Inflows sliding, EMIs biting.', score: '410 · Critical', tone: '#C0392B' },
]

export default function Launcher() {
  return (
    <div className="ledger-bg min-h-screen text-paper">
      <div className="max-w-5xl mx-auto px-5 pt-14 pb-6">
        <header className="rise">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-navy-800 hairline grid place-items-center relative">
              <span className="font-display font-extrabold text-2xl text-paper">प</span>
              <span className="absolute -top-px -right-px w-3.5 h-3.5 bg-amber-500" style={{ clipPath: 'polygon(0 0,100% 0,100% 100%)' }} />
            </div>
            <div>
              <h1 className="font-display font-extrabold text-3xl leading-none">Parakh <span className="text-paper/40 font-semibold text-lg">परख</span></h1>
              <p className="caps-label text-amber-500 mt-1">Every genuine business, recognized.</p>
            </div>
          </div>
          <p className="mt-6 max-w-2xl text-paper/75 text-[15px] leading-relaxed">
            For centuries, a goldsmith could tell <em>khara sona</em> — genuine gold — with a touchstone.
            India's 7.9 crore MSMEs are gold that's never been assayed. <strong className="text-paper">Parakh is the touchstone</strong>:
            one score from GST, bank flows, UPI and payroll — that the bank monitors live, and the business can see and improve.
          </p>
        </header>

        <div className="mt-9 grid md:grid-cols-2 gap-4 rise rise-1">
          <Link to="/lender" className="hairline bg-navy-800/70 p-6 hover:bg-navy-700/70 transition-colors group">
            <div className="caps-label text-teal-300">Take a seat as</div>
            <div className="font-display font-bold text-2xl mt-1">🏦 The Bank RM</div>
            <p className="text-paper/60 text-sm mt-2">Your Monday-morning book: 65 MSMEs ranked by health, two flashing alerts, one ₹75L lead.</p>
            <div className="mt-3 text-amber-500 text-sm font-semibold group-hover:translate-x-1 transition-transform">Open the portfolio →</div>
          </Link>
          <Link to={`/msme/${PERSONAS[1].gstin}`} className="hairline bg-navy-800/70 p-6 hover:bg-navy-700/70 transition-colors group">
            <div className="caps-label text-teal-300">Take a seat as</div>
            <div className="font-display font-bold text-2xl mt-1">🏪 The MSME Owner</div>
            <p className="text-paper/60 text-sm mt-2">Meena's phone: her own score, in her own language, with actions priced in rupees.</p>
            <div className="mt-3 text-amber-500 text-sm font-semibold group-hover:translate-x-1 transition-transform">Open her card →</div>
          </Link>
        </div>

        <div className="mt-8 rise rise-2">
          <div className="caps-label text-paper/40 mb-3">Or meet the three businesses</div>
          <div className="grid md:grid-cols-3 gap-3">
            {PERSONAS.map(p => (
              <Link key={p.gstin} to={`/lender/${p.gstin}`} className="hairline bg-navy-900/70 p-4 hover:bg-navy-800 transition-colors">
                <div className="flex justify-between items-start">
                  <div className="font-display font-bold text-[15px] leading-tight">{p.name}</div>
                  <span className="tnum font-mono text-xs px-1.5 py-0.5" style={{ color: p.tone, border: `1px solid ${p.tone}` }}>{p.score}</span>
                </div>
                <div className="text-paper/50 text-xs mt-1">{p.who}</div>
                <p className="text-paper/70 text-[13px] mt-2 leading-snug">{p.story}</p>
                <div className="font-mono text-[10px] text-paper/35 mt-2">{p.gstin}</div>
              </Link>
            ))}
          </div>
        </div>

        <div className="mt-8 hairline-teal bg-teal-700/10 p-4 text-[13px] text-paper/70 rise rise-3">
          <span className="caps-label text-teal-300 mr-2">What am I looking at?</span>
          A two-sided MSME Financial Health Card built for IDBI Innovate 2026 (PS-3). The score is a transparent
          5-dimension scorecard (300–900) with reason codes, a confidence ring that widens when data sources fail,
          and <strong>Kal-Parakh</strong> — a simulator that re-runs the real engine to price improvement actions in rupees.
          Everything here runs on schema-faithful <strong>synthetic data</strong>; every mock is labeled.
        </div>
        <Footer />
      </div>
      <SyntheticStamp />
    </div>
  )
}
