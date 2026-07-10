/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        craft: {
          950: "#0a0a12",
          900: "#12121f",
          800: "#1e1e30",
          700: "#2c2c44",
          accent: "#6366f1",
          glow: "#a5b4fc",
          warm: "#f59e0b",
        },
      },
    },
  },
  plugins: [],
};
