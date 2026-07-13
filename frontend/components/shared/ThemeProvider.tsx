"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";
import { runThemeBlurTransition } from "@/lib/theme-blur-transition";

export type Theme = "light" | "dark";

const STORAGE_KEY = "agentcraft-theme";

type ThemeContextValue = {
  theme: Theme;
  setTheme: (theme: Theme, origin?: { x: number; y: number }) => void;
  toggleTheme: (origin?: { x: number; y: number }) => void;
  ready: boolean;
  transitioning: boolean;
};

const ThemeContext = createContext<ThemeContextValue | null>(null);

function applyThemeClass(theme: Theme) {
  const root = document.documentElement;
  root.classList.toggle("dark", theme === "dark");
  root.style.colorScheme = theme;
}

function readStoredTheme(): Theme | null {
  try {
    const value = localStorage.getItem(STORAGE_KEY);
    if (value === "light" || value === "dark") return value;
  } catch {
    /* ignore */
  }
  return null;
}

function systemTheme(): Theme {
  if (typeof window === "undefined") return "light";
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setThemeState] = useState<Theme>("light");
  const [ready, setReady] = useState(false);
  const [transitioning, setTransitioning] = useState(false);
  const themeRef = useRef(theme);
  themeRef.current = theme;
  const busyRef = useRef(false);

  useEffect(() => {
    const initial = readStoredTheme() ?? systemTheme();
    setThemeState(initial);
    applyThemeClass(initial);
    setReady(true);
  }, []);

  const persist = useCallback((next: Theme) => {
    try {
      localStorage.setItem(STORAGE_KEY, next);
    } catch {
      /* ignore */
    }
  }, []);

  const setTheme = useCallback(
    (next: Theme, origin?: { x: number; y: number }) => {
      if (next === themeRef.current) return;
      if (busyRef.current) return;

      busyRef.current = true;
      setTransitioning(true);

      void runThemeBlurTransition(
        next,
        () => {
          setThemeState(next);
          applyThemeClass(next);
          persist(next);
        },
        origin
      ).finally(() => {
        busyRef.current = false;
        setTransitioning(false);
      });
    },
    [persist]
  );

  const toggleTheme = useCallback(
    (origin?: { x: number; y: number }) => {
      setTheme(themeRef.current === "dark" ? "light" : "dark", origin);
    },
    [setTheme]
  );

  const value = useMemo(
    () => ({ theme, setTheme, toggleTheme, ready, transitioning }),
    [theme, setTheme, toggleTheme, ready, transitioning]
  );

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme must be used within ThemeProvider");
  return ctx;
}
