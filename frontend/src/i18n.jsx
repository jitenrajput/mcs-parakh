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
