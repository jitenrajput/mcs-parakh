/* Tiny i18n: one object per language (FR-4.10). Adding a language = one block.
   Voice: "a helpful CA who respects you" — never government-form language. */

import { createContext, useContext, useState } from 'react'

export const STRINGS = {
  en: {
    your_score: 'Your Parakh Score',
    great_start: 'A strong start!',
    strengths: 'What is working for you',
    risks: 'What is holding you back',
    improve: 'Grow your eligibility',
    improve_sub: 'Every action shows its value in rupees — projected by the real scoring engine, not an estimate.',
    readiness: 'Loan readiness',
    eligible_today: 'Indicative limit today',
    eligible_after: 'After these actions',
    apply_hint: 'Talk to your IDBI branch with this card — it speaks their language.',
    confidence: 'Confidence',
    data_used: 'Data used for this score',
    simulate: 'Show my tomorrow',
    reset: 'Reset',
    synthetic: 'SYNTHETIC DATA',
    band_note: 'Score band 300–900, like your personal credit score — but built from how your business actually runs.',
    conf_high: 'High', conf_medium: 'Medium', conf_low: 'Low',
    sim_note: 'Projection re-runs the actual scoring engine with modified inputs — not an animation.',
    score_makeup: 'Score make-up',
    none_flagged: 'Nothing notable',
    limited_data: 'Limited data — {n} of 5 sources unavailable, so this score is provisional',
    not_applicable: "Won't change your score right now",
    built_for: 'built for IDBI Innovate 2026',
    card_yours: 'Hi {name}, this card is yours — no one changes it but you.',
    dims: { cash_flow: 'Cash-Flow Strength', compliance: 'Compliance Discipline', obligation: 'Obligation Load', growth: 'Growth Trajectory', stability: 'Business Stability' },
    actions: {
      gst_on_time_3m: { label: 'File GSTR-1 & 3B on time for the next 3 months', hint: 'Sets the 3 most recent filings to their due date' },
      gst_on_time_6m: { label: 'File GSTR-1 & 3B on time for 6 months', hint: 'Sets the 6 most recent filings to their due date' },
      clear_bounces_6m: { label: 'No payment bounces for 6 months', hint: 'Clears inward bounces in the last 6 months' },
      reduce_emi_25pct: { label: 'Refinance / part-prepay EMIs (−25%)', hint: 'Reduces EMI debits 25% across the last 12 months' },
    },
  },
  hi: {
    your_score: 'आपका परख स्कोर',
    great_start: 'मज़बूत शुरुआत!',
    strengths: 'आपके पक्ष में क्या है',
    risks: 'क्या पीछे खींच रहा है',
    improve: 'अपनी पात्रता बढ़ाइए',
    improve_sub: 'हर कदम का असर रुपयों में — असली स्कोरिंग इंजन से निकला अनुमान, कोई अंदाज़ा नहीं।',
    readiness: 'लोन की तैयारी',
    eligible_today: 'आज की अनुमानित सीमा',
    eligible_after: 'इन कदमों के बाद',
    apply_hint: 'यह कार्ड लेकर IDBI शाखा जाइए — यह बैंक की भाषा बोलता है।',
    confidence: 'भरोसे का स्तर',
    data_used: 'इस स्कोर में शामिल डेटा',
    simulate: 'मेरा कल दिखाइए',
    reset: 'रीसेट',
    synthetic: 'नमूना डेटा',
    band_note: 'स्कोर 300–900 — आपके निजी क्रेडिट स्कोर जैसा, पर आपके व्यापार की असल चाल से बना।',
    conf_high: 'उच्च', conf_medium: 'मध्यम', conf_low: 'कम',
    sim_note: 'यह अनुमान असली स्कोरिंग इंजन को बदले हुए इनपुट के साथ दोबारा चलाकर निकला है — कोई एनीमेशन नहीं।',
    score_makeup: 'स्कोर का ब्यौरा',
    none_flagged: 'कुछ खास नहीं',
    limited_data: 'सीमित डेटा — 5 में से {n} स्रोत उपलब्ध नहीं, इसलिए यह स्कोर अनंतिम है',
    not_applicable: 'अभी आपके स्कोर पर कोई असर नहीं',
    built_for: 'IDBI Innovate 2026 के लिए बना',
    card_yours: 'नमस्ते {name}, यह कार्ड आपका है — इसे आपके सिवा कोई नहीं बदलता।',
    dims: { cash_flow: 'कैश-फ्लो ताकत', compliance: 'अनुपालन अनुशासन', obligation: 'देनदारी बोझ', growth: 'वृद्धि दिशा', stability: 'व्यवसाय स्थिरता' },
    reasons: {
      inflow_cov: { pos: 'नियमित मासिक आमदनी', neg: 'अस्थिर मासिक आमदनी' },
      balance_floor_ratio: { pos: 'अच्छा बैलेंस कुशन', neg: 'कमज़ोर बैलेंस कुशन' },
      net_margin: { pos: 'मज़बूत कैश-फ्लो मार्जिन', neg: 'कमज़ोर कैश-फ्लो मार्जिन' },
      gst_avg_delay_days: { pos: 'GST समय पर भरा', neg: 'GST देर से भरा (औसत {v} दिन)' },
      gst_late_count_6m: { pos: 'हाल की GST फाइलिंग समय पर', neg: 'पिछले 6 महीनों में {v} देर से GST फाइलिंग' },
      gst_missed_12m: { pos: 'कोई GST रिटर्न नहीं छूटा', neg: '{v} GST रिटर्न छूटे' },
      gstr1_3b_gap_pct: { pos: 'GSTR-1 और 3B मेल खाते हैं', neg: 'GSTR-1 बनाम 3B अंतर {v}%' },
      turnover_slope_pct: { pos: 'बढ़ता कारोबार', neg: 'घटता कारोबार' },
      growth_q_pct: { pos: 'हाल की तिमाही सुधर रही है', neg: 'हाल की तिमाही कमज़ोर हो रही है' },
      growth_volatility: { pos: 'स्थिर वृद्धि', neg: 'अनियमित वृद्धि' },
      emi_to_inflow: { pos: 'हल्का EMI बोझ', neg: 'EMI बोझ आमदनी का {v}' },
      bounces_12m: { pos: 'कोई पेमेंट बाउंस नहीं', neg: '12 महीनों में {v} पेमेंट बाउंस' },
      bureau_max_dpd: { pos: 'साफ़ चुकौती रिकॉर्ड', neg: 'अधिकतम {v} दिन की देरी' },
      vintage_years: { pos: 'स्थापित व्यवसाय ({v} वर्ष)', neg: 'नया व्यवसाय ({v} वर्ष)' },
      employees: { pos: 'पेरोल पर स्थिर टीम', neg: 'कोई औपचारिक पेरोल नहीं' },
      payroll_on_time: { pos: 'PF जमा समय पर', neg: 'अनियमित PF जमा' },
      udyam_registered: { pos: 'उद्यम पंजीकृत', neg: 'उद्यम पंजीकृत नहीं' },
    },
    actions: {
      gst_on_time_3m: { label: 'अगले 3 महीने GSTR-1 और 3B समय पर भरें', hint: 'सबसे हाल की 3 फाइलिंग नियत तारीख़ पर मानी जाती हैं' },
      gst_on_time_6m: { label: '6 महीने तक GSTR-1 और 3B समय पर भरें', hint: 'सबसे हाल की 6 फाइलिंग नियत तारीख़ पर मानी जाती हैं' },
      clear_bounces_6m: { label: '6 महीने तक कोई पेमेंट बाउंस नहीं', hint: 'पिछले 6 महीनों के इनवर्ड बाउंस हटाकर देखा जाता है' },
      reduce_emi_25pct: { label: 'EMI रीफाइनेंस / आंशिक चुकौती (−25%)', hint: 'पिछले 12 महीनों की EMI 25% कम मानी जाती है' },
    },
  },
  gu: {
    your_score: 'તમારો પરખ સ્કોર',
    great_start: 'સરસ શરૂઆત!',
    strengths: 'તમારા પક્ષમાં શું છે',
    risks: 'શું પાછળ ખેંચે છે',
    improve: 'તમારી પાત્રતા વધારો',
    improve_sub: 'દરેક પગલાની કિંમત રૂપિયામાં — સાચા સ્કોરિંગ એન્જિનનું અનુમાન, અંદાજ નહીં.',
    readiness: 'લોન માટે તૈયારી',
    eligible_today: 'આજની અંદાજિત મર્યાદા',
    eligible_after: 'આ પગલાં પછી',
    apply_hint: 'આ કાર્ડ લઈને IDBI શાખાએ જાઓ — તે બેંકની ભાષા બોલે છે.',
    confidence: 'વિશ્વાસનું સ્તર',
    data_used: 'આ સ્કોરમાં વપરાયેલ ડેટા',
    simulate: 'મારું આવતીકાલ બતાવો',
    reset: 'રીસેટ',
    synthetic: 'નમૂનાનો ડેટા',
    band_note: 'સ્કોર 300–900 — તમારા અંગત ક્રેડિટ સ્કોર જેવો, પણ તમારા ધંધાની સાચી ચાલ પરથી બનેલો.',
    conf_high: 'ઉચ્ચ', conf_medium: 'મધ્યમ', conf_low: 'ઓછો',
    sim_note: 'આ અંદાજ સાચા સ્કોરિંગ એન્જિનને બદલેલા ઇનપુટ સાથે ફરી ચલાવીને મળ્યો છે — કોઈ એનિમેશન નથી.',
    score_makeup: 'સ્કોરની વિગત',
    none_flagged: 'ખાસ કંઈ નહીં',
    limited_data: 'મર્યાદિત ડેટા — 5 માંથી {n} સ્રોત ઉપલબ્ધ નથી, તેથી આ સ્કોર કામચલાઉ છે',
    not_applicable: 'અત્યારે તમારા સ્કોર પર કોઈ અસર નહીં',
    built_for: 'IDBI Innovate 2026 માટે બનાવેલ',
    card_yours: 'નમસ્તે {name}, આ કાર્ડ તમારું છે — તમારા સિવાય કોઈ બદલતું નથી.',
    dims: { cash_flow: 'કેશ-ફ્લો તાકાત', compliance: 'અનુપાલન શિસ્ત', obligation: 'જવાબદારી બોજ', growth: 'વૃદ્ધિ દિશા', stability: 'વ્યવસાય સ્થિરતા' },
    reasons: {
      inflow_cov: { pos: 'નિયમિત માસિક આવક', neg: 'અસ્થિર માસિક આવક' },
      balance_floor_ratio: { pos: 'સારું બેલેન્સ કુશન', neg: 'નબળું બેલેન્સ કુશન' },
      net_margin: { pos: 'મજબૂત કેશ-ફ્લો માર્જિન', neg: 'નબળું કેશ-ફ્લો માર્જિન' },
      gst_avg_delay_days: { pos: 'GST સમયસર ભર્યું', neg: 'GST મોડું ભર્યું (સરેરાશ {v} દિવસ)' },
      gst_late_count_6m: { pos: 'તાજેતરની GST ફાઇલિંગ સમયસર', neg: 'છેલ્લા 6 મહિનામાં {v} મોડી GST ફાઇલિંગ' },
      gst_missed_12m: { pos: 'કોઈ GST રિટર્ન ચૂક્યું નથી', neg: '{v} GST રિટર્ન ચૂક્યાં' },
      gstr1_3b_gap_pct: { pos: 'GSTR-1 અને 3B સુસંગત', neg: 'GSTR-1 vs 3B તફાવત {v}%' },
      turnover_slope_pct: { pos: 'વધતો વેપાર', neg: 'ઘટતો વેપાર' },
      growth_q_pct: { pos: 'તાજેતરનું ત્રિમાસિક સુધરી રહ્યું છે', neg: 'તાજેતરનું ત્રિમાસિક નબળું પડી રહ્યું છે' },
      growth_volatility: { pos: 'સ્થિર વૃદ્ધિ', neg: 'અનિયમિત વૃદ્ધિ' },
      emi_to_inflow: { pos: 'હળવો EMI બોજ', neg: 'EMI બોજ આવકનો {v}' },
      bounces_12m: { pos: 'કોઈ પેમેન્ટ બાઉન્સ નહીં', neg: '12 મહિનામાં {v} પેમેન્ટ બાઉન્સ' },
      bureau_max_dpd: { pos: 'સ્વચ્છ ચુકવણી રેકોર્ડ', neg: 'મહત્તમ {v} દિવસ મોડું' },
      vintage_years: { pos: 'સ્થાપિત વ્યવસાય ({v} વર્ષ)', neg: 'નવો વ્યવસાય ({v} વર્ષ)' },
      employees: { pos: 'પેરોલ પર સ્થિર ટીમ', neg: 'કોઈ ઔપચારિક પેરોલ નહીં' },
      payroll_on_time: { pos: 'PF જમા સમયસર', neg: 'અનિયમિત PF જમા' },
      udyam_registered: { pos: 'ઉદ્યમ નોંધાયેલ', neg: 'ઉદ્યમ નોંધાયેલ નથી' },
    },
    actions: {
      gst_on_time_3m: { label: 'આગામી 3 મહિના GSTR-1 અને 3B સમયસર ભરો', hint: 'સૌથી તાજેતરની 3 ફાઇલિંગ નિયત તારીખે ગણાય છે' },
      gst_on_time_6m: { label: '6 મહિના સુધી GSTR-1 અને 3B સમયસર ભરો', hint: 'સૌથી તાજેતરની 6 ફાઇલિંગ નિયત તારીખે ગણાય છે' },
      clear_bounces_6m: { label: '6 મહિના સુધી કોઈ પેમેન્ટ બાઉન્સ નહીં', hint: 'છેલ્લા 6 મહિનાના ઇનવર્ડ બાઉન્સ દૂર ગણીને જોવાય છે' },
      reduce_emi_25pct: { label: 'EMI રિફાઇનાન્સ / આંશિક ચુકવણી (−25%)', hint: 'છેલ્લા 12 મહિનાની EMI 25% ઓછી ગણાય છે' },
    },
  },
}

const I18nCtx = createContext({ lang: 'en', t: k => k, setLang: () => {} })

export function I18nProvider({ children }) {
  const [lang, setLang] = useState('en')
  const t = k => STRINGS[lang][k] ?? STRINGS.en[k] ?? k
  return <I18nCtx.Provider value={{ lang, t, setLang }}>{children}</I18nCtx.Provider>
}

export const useT = () => useContext(I18nCtx)

/* Localize an engine reason: EN uses the engine text as-is; HI/GU use a template
   keyed by feature + sign, with the pre-formatted value ({v}) substituted in.
   Falls back to the English engine text if a template is missing. */
export function locReason(r, lang) {
  if (lang === 'en') return r.text
  const tmpl = STRINGS[lang]?.reasons?.[r.feature]?.[r.points_delta >= 0 ? 'pos' : 'neg']
  if (!tmpl) return r.text
  return r.vstr != null ? tmpl.replace('{v}', r.vstr) : tmpl
}

export function LangToggle() {
  const { lang, setLang } = useT()
  return (
    <div className="inline-flex hairline-teal">
      {['en', 'hi', 'gu'].map(l => (
        <button key={l} onClick={() => setLang(l)}
          className={`px-2.5 py-1 text-xs font-semibold ${lang === l ? 'bg-teal-700 text-paper' : 'text-teal-700 hover:bg-teal-700/10'}`}>
          {l === 'en' ? 'EN' : l === 'hi' ? 'हिं' : 'ગુ'}
        </button>
      ))}
    </div>
  )
}
