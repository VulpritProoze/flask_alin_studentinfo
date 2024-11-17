/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*"],
  theme: {
    extend: {
      screens: {
        'x-sm': '100px',
        'sm': '300px'
      }
    },
  },
  plugins: [],
}

