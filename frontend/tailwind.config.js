/** Tokens from docs/11-branding.md — the single visual source of truth. */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        navy: { 950: '#0B1526', 900: '#101D33', 800: '#14243D', 700: '#1B3050', 600: '#24405F' },
        teal: { 700: '#0E6E5C', 500: '#15866F', 300: '#57B79F' },
        amber: { 500: '#E8A33D', 400: '#F0B65C' },
        paper: { DEFAULT: '#F7F5F0', dark: '#EFEBE2' },
        ink: { DEFAULT: '#1C2434', soft: '#485062' },
        /* `red` is the band colour — correct as a thick arc stroke, but only ~2.3:1
           on navy, so `red-lit` carries the same alarm as text on dark surfaces. */
        band: { red: '#C0392B', 'red-lit': '#F2897C', amber: '#E8A33D', green: '#1E8E5A' },
      },
      fontFamily: {
        display: ['Mukta', 'Noto Sans', 'sans-serif'],
        body: ['"Noto Sans"', 'sans-serif'],
        mono: ['"Noto Sans Mono"', 'ui-monospace', 'monospace'],
      },
      letterSpacing: { caps: '0.14em' },
    },
  },
  plugins: [],
}
