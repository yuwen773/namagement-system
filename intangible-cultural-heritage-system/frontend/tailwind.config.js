/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fef5ee',
          100: '#fde8d7',
          200: '#fbcdae',
          300: '#f8ab7a',
          400: '#f47d44',
          500: '#f15a24',
          600: '#e23f15',
          700: '#bb2d13',
          800: '#952617',
          900: '#792216',
        },
        heritage: {
          gold: '#d4af37',
          bronze: '#cd7f32',
          jade: '#00a86b',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Playfair Display', 'serif'],
      }
    },
  },
  plugins: [],
}
