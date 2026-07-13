"use client";

import type { Theme } from "@/components/shared/ThemeProvider";

const BLUR_MS = 110;
const HOLD_MS = 10;

/**
 * Soft blur wipe into the next theme — blurs out, swaps theme, blurs back in.
 */
export function runThemeBlurTransition(
  next: Theme,
  applyTheme: () => void,
  _origin?: { x: number; y: number }
): Promise<void> {
  if (typeof window === "undefined") {
    applyTheme();
    return Promise.resolve();
  }

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    applyTheme();
    return Promise.resolve();
  }

  document.querySelectorAll("[data-theme-blur-overlay]").forEach((el) => el.remove());

  const root = document.documentElement;
  const overlay = document.createElement("div");
  overlay.dataset.themeBlurOverlay = "1";
  overlay.setAttribute("aria-hidden", "true");
  Object.assign(overlay.style, {
    position: "fixed",
    inset: "0",
    zIndex: "99999",
    pointerEvents: "none",
    backdropFilter: "blur(0px)",
    background:
      next === "dark" ? "rgba(10, 16, 28, 0)" : "rgba(248, 250, 252, 0)",
    transition: `backdrop-filter ${BLUR_MS}ms ease-out, background ${BLUR_MS}ms ease-out`,
  });
  // Safari
  overlay.style.setProperty("-webkit-backdrop-filter", "blur(0px)");
  document.body.appendChild(overlay);

  void overlay.offsetWidth;

  overlay.style.backdropFilter = "blur(7px)";
  overlay.style.setProperty("-webkit-backdrop-filter", "blur(7px)");
  overlay.style.background =
    next === "dark" ? "rgba(10, 16, 28, 0.12)" : "rgba(248, 250, 252, 0.16)";

  root.style.transition = `filter ${BLUR_MS}ms ease-out`;
  root.style.filter = "blur(4px)";

  return new Promise((resolve) => {
    window.setTimeout(() => {
      applyTheme();

      window.setTimeout(() => {
        overlay.style.backdropFilter = "blur(0px)";
        overlay.style.setProperty("-webkit-backdrop-filter", "blur(0px)");
        overlay.style.background =
          next === "dark" ? "rgba(10, 16, 28, 0)" : "rgba(248, 250, 252, 0)";
        root.style.filter = "blur(0px)";

        window.setTimeout(() => {
          overlay.remove();
          root.style.transition = "";
          root.style.filter = "";
          resolve();
        }, BLUR_MS);
      }, HOLD_MS);
    }, BLUR_MS);
  });
}
