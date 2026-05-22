import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1B3A2D',
          light: '#2D5A42',
        },
        gold: '#C9A84C',
        cream: '#F7F4EF',
        dark: '#0F1F17',
        muted: '#7A7A72',
      },
      fontFamily: {
        cormorant: ['Cormorant Garamond', 'Georgia', 'serif'],
        dm: ['DM Sans', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'display': ['clamp(3.5rem, 8vw, 7rem)', { lineHeight: '0.95', letterSpacing: '-0.02em' }],
        'display-sm': ['clamp(2.5rem, 5vw, 4.5rem)', { lineHeight: '1.05', letterSpacing: '-0.01em' }],
        'label': ['10px', { lineHeight: '1.4', letterSpacing: '0.25em' }],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-slow': 'bounce 2s infinite',
      },
      backgroundImage: {
        'gradient-dark': 'linear-gradient(to bottom, rgba(15,31,23,0.7) 0%, rgba(15,31,23,0.4) 50%, rgba(15,31,23,0.85) 100%)',
      },
      boxShadow: {
        'card': '0 4px 24px rgba(15,31,23,0.08)',
        'card-hover': '0 8px 40px rgba(15,31,23,0.14)',
        'nav': '0 1px 20px rgba(15,31,23,0.08)',
      },
      transitionDuration: {
        '400': '400ms',
      },
    },
  },
  plugins: [],
}
export default config
