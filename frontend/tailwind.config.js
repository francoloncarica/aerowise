/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        aero: {
          50: '#f5f3ff',
          100: '#ede9fe',
          200: '#ddd6fe',
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
          950: '#1a0a2e',
        },
        gold: {
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#8b5cf6',
          600: '#7c3aed',
        },
        surface: {
          50: '#f8f8f8',
          100: '#e0e0e0',
          200: '#2a2a30',
          300: '#222228',
          400: '#1a1a22',
          500: '#151518',
          600: '#111114',
          700: '#0d0d0f',
          800: '#0a0a0c',
          900: '#060608',
        },
      },
    },
  },
  plugins: [],
};
