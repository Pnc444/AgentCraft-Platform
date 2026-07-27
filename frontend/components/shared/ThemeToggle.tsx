"use client";

import { Moon, Sun } from "lucide-react";
import clsx from "clsx";
import { useTheme } from "@/components/shared/ThemeProvider";

interface ThemeToggleProps {
  className?: string;
  /** Compact icon-only control for dense chrome */
  compact?: boolean;
  /** For navy / inverted headers */
  inverted?: boolean;
}

export function ThemeToggle({ className, compact = false, inverted = false }: ThemeToggleProps) {
  const { theme, toggleTheme, ready, transitioning } = useTheme();
  const isDark = theme === "dark";

  return (
    <button
      type="button"
      onClick={(e) => {
        toggleTheme({ x: e.clientX, y: e.clientY });
      }}
      disabled={!ready || transitioning}
      className={clsx(
        "inline-flex items-center justify-center gap-2 rounded-full border transition duration-300",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-violet-500",
        "disabled:opacity-60",
        inverted
          ? "border-violet-300/50 bg-violet-400/15 text-violet-100 shadow-[0_0_0_1px_rgba(103,232,249,0.25)] hover:border-violet-200 hover:bg-violet-400/25"
          : "border-craft-border bg-craft-surface text-craft-ink shadow-soft hover:border-violet-400/50 hover:shadow-card",
        compact ? "h-9 w-9" : "px-3 py-2 text-sm font-medium",
        className
      )}
      aria-label={isDark ? "Switch to light mode" : "Switch to dark mode"}
      title={isDark ? "Light mode" : "Dark mode"}
    >
      {isDark ? (
        <Sun className="h-4 w-4 text-violet-200" />
      ) : (
        <Moon className={clsx("h-4 w-4", inverted ? "text-violet-100" : "text-violet-700")} />
      )}
      {!compact && <span>{isDark ? "Light" : "Dark"}</span>}
    </button>
  );
}
