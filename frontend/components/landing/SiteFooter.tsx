"use client";

import { LogoIcon } from "@/components/shared/Logo";
import { Reveal } from "@/components/shared/Reveal";

export function SiteFooter() {
  return (
    <footer className="border-t border-craft-border bg-craft-surface py-10 shadow-[0_-8px_24px_rgba(15,23,42,0.03)] dark:shadow-[0_-8px_24px_rgba(0,0,0,0.35)]">
      <Reveal variant="fade" className="mx-auto max-w-6xl px-6">
        <div className="flex flex-wrap items-center justify-between gap-4 text-sm text-craft-muted">
          <p className="flex items-center gap-2">
            <LogoIcon className="h-5 w-5" />
            <span>
              Knight&apos;s{" "}
              <span className="text-violet-600 dark:text-violet-400">Academy</span> — learn AI agents
              from zero.
            </span>
          </p>
          <p>© {new Date().getFullYear()} Knight's Academy</p>
        </div>
      </Reveal>
    </footer>
  );
}
