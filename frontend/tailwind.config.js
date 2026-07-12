/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        craft: {
          canvas: "#F8FAFC",
          surface: "#FFFFFF",
          card: "#FFFFFF",
          border: "#E2E8F0",
          ink: "#0F172A",
          muted: "#64748B",
          accent: "#06B6D4",
          secondary: "#0891B2",
          "accent-soft": "#ECFEFF",
          cyan: "#22D3EE",
          glow: "#22D3EE",
          navy: "#0F172A",
          "navy-soft": "#1E293B",
          success: "#10B981",
          warning: "#F59E0B",
          hero: "#0F172A",
        },
      },
      fontFamily: {
        sans: ["var(--font-sans)", "system-ui", "sans-serif"],
        serif: ["var(--font-serif)", "Georgia", "serif"],
      },
      boxShadow: {
        soft: "0 1px 2px rgba(15, 23, 42, 0.04), 0 8px 24px rgba(15, 23, 42, 0.06)",
        card: "0 1px 3px rgba(15, 23, 42, 0.04), 0 4px 16px rgba(15, 23, 42, 0.04)",
      },
      keyframes: {
        "fade-up": {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "grid-drift": {
          "0%": { transform: "translate3d(0, 0, 0)" },
          "100%": { transform: "translate3d(-48px, -48px, 0)" },
        },
        "glow-drift": {
          "0%, 100%": { transform: "translate3d(0, 0, 0) scale(1)", opacity: "0.4" },
          "50%": { transform: "translate3d(-24px, 16px, 0) scale(1.08)", opacity: "0.55" },
        },
      },
      animation: {
        "fade-up": "fade-up 0.45s ease-out both",
        "grid-drift": "grid-drift 28s linear infinite",
        "glow-drift": "glow-drift 12s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
