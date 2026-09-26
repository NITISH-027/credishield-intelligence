/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        theme: {
          bg: '#07090D',
          surface: '#0D1118',
          elevated: '#121824',
          border: '#202734',
          borderLight: '#2C3547',
          text: '#F4F3EF',
          secondary: '#8F98A8',
          muted: '#5F6877',
        },
        accent: {
          gradientStart: '#6757D9',
          gradientEnd: '#D58BAA',
          positive: '#55C89A',
          attention: '#E7B85C',
          negative: '#E56B75',
          unknown: '#8D82E8',
        }
      },
      fontFamily: {
        serif: ['"Instrument Serif"', 'Georgia', 'serif'],
        sans: ['"Manrope"', 'system-ui', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'Menlo', 'monospace'],
      }
    },
  },
  plugins: [],
}
