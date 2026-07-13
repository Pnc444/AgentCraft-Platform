/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        craft: {
          canvas: "var(--craft-canvas)",
          surface: "var(--craft-surface)",
          card: "var(--craft-card)",
          soft: "var(--craft-soft)",
          border: "var(--craft-border)",
          ink: "var(--craft-ink)",
          muted: "var(--craft-muted)",
          faint: "var(--craft-faint)",
          accent: "var(--craft-accent)",
          secondary: "var(--craft-secondary)",
          "accent-soft": "var(--craft-accent-soft)",
          cyan: "var(--craft-cyan)",
          glow: "var(--craft-glow)",
          navy: "var(--craft-navy)",
          "navy-soft": "var(--craft-navy-soft)",
          success: "var(--craft-success)",
          warning: "var(--craft-warning)",
          hero: "var(--craft-hero)",
          inverse: "var(--craft-inverse)",
          "inverse-muted": "var(--craft-inverse-muted)",
        },
      },
      fontFamily: {
        sans: ["var(--font-sans)", "system-ui", "sans-serif"],
        serif: ["var(--font-serif)", "Georgia", "serif"],
      },
      boxShadow: {
        soft: "var(--shadow-soft)",
        card: "var(--shadow-card)",
        elevated: "var(--shadow-elevated)",
        float: "var(--shadow-float)",
        btn: "var(--shadow-btn)",
        "btn-hover": "var(--shadow-btn-hover)",
        navy: "var(--shadow-navy)",
        header: "var(--shadow-header)",
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
