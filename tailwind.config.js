const defaultTheme = require('tailwindcss/defaultTheme')

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './src/frontend/index.html"',
    "./src/frontend/**/*.{js,ts,jsx,tsx}"
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
      colors: {
        'my-purple': {
          DEFAULT: '#4c1a57',
          '50': '#fbf5fe',
          '100': '#f7eafd',
          '200': '#eed3fb',
          '300': '#e3b1f6',
          '400': '#d383ef',
          '500': '#be53e2',
          '600': '#a433c6',
          '700': '#8927a4',
          '800': '#712286',
          '900': '#4c1a57',
          '950': '#3d0a48',
        },
        'my-rose': {
          DEFAULT: '#f7aef8',
          '50': '#fef5fe',
          '100': '#fce9fe',
          '200': '#fad2fc',
          '300': '#f7aef8',
          '400': '#f37ff3',
          '500': '#e74ee6',
          '600': '#cb2ec8',
          '700': '#a823a2',
          '800': '#891f83',
          '900': '#711e6b',
          '950': '#4a0844',
        },
        'my-green': {
          DEFAULT: '#89CE94',
          '50': '#f3faf4',
          '100': '#e3f5e5',
          '200': '#c9e9ce',
          '300': '#89ce94',
          '400': '#6cbc79',
          '500': '#489f56',
          '600': '#368343',
          '700': '#2e6737',
          '800': '#28532f',
          '900': '#234429',
          '950': '#0e2513',
        },
        'my-blue': {
          DEFAULT: '#31AFD4',
          '50': '#eefbfd',
          '100': '#d5f2f8',
          '200': '#afe5f2',
          '300': '#78d0e8',
          '400': '#31afd4',
          '500': '#1e96bc',
          '600': '#1c799e',
          '700': '#1d6281',
          '800': '#20516a',
          '900': '#1f445a',
          '950': '#0f2c3d',
        },
        'my-pink': {
          DEFAULT: '#DC136C',
          '50': '#fef1f8',
          '100': '#fee5f3',
          '200': '#ffcbe9',
          '300': '#ffa1d5',
          '400': '#ff66b7',
          '500': '#fb3999',
          '600': '#dc136c',
          '700': '#cd095b',
          '800': '#a90b4b',
          '900': '#8c0f41',
          '950': '#560123',
        },
      }
    },
    fontFamily: {
      sans: ['Montserrat', ...defaultTheme.fontFamily.sans],
      serif: ['Cardo', ...defaultTheme.fontFamily.serif],
    },
  },
  plugins: [require("tailwindcss-animate")],
}