/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./templates/**/*.{html,js}",
    "./static/js/**/*.{html,js}",
  ],
  theme: {
    extend: {
      colors: {
        'wine-900': '#78350f',
        'wine-800': '#92400e',
        'wine-700': '#b45309',
        'wine-600': '#d97706',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'avenir', 'helvetica', 'arial', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
