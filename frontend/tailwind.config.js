/**
 * The --craft-* variables hold plain hex, and raw CSS in globals.css reads them
 * directly (e.g. `color: var(--craft-ink)`), so they must stay hex. A bare
 * `var(--x)` color, though, makes Tailwind silently DROP every opacity modifier:
 * `bg-craft-surface/95` emitted no CSS rule at all, so translucent surfaces
 * rendered fully transparent. Wrapping in color-mix keeps the hex vars working
 * for raw CSS while giving Tailwind a slot for <alpha-value>.
 */
const alphaVar = (name) =>
  `color-mix(in srgb, var(${name}) calc(<alpha-value> * 100%), transparent)`;

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        craft: {
          canvas: alphaVar("--craft-canvas"),
          surface: alphaVar("--craft-surface"),
          card: alphaVar("--craft-card"),
          soft: alphaVar("--craft-soft"),
          border: alphaVar("--craft-border"),
          ink: alphaVar("--craft-ink"),
          muted: alphaVar("--craft-muted"),
          faint: alphaVar("--craft-faint"),
          accent: alphaVar("--craft-accent"),
          secondary: alphaVar("--craft-secondary"),
          "accent-soft": alphaVar("--craft-accent-soft"),
          cyan: alphaVar("--craft-cyan"),
          glow: alphaVar("--craft-glow"),
          navy: alphaVar("--craft-navy"),
          "navy-soft": alphaVar("--craft-navy-soft"),
          success: alphaVar("--craft-success"),
          warning: alphaVar("--craft-warning"),
          hero: alphaVar("--craft-hero"),
          inverse: alphaVar("--craft-inverse"),
          "inverse-muted": alphaVar("--craft-inverse-muted"),
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
