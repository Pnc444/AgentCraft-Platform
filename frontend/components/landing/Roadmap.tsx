"use client";

import { useState } from "react";
import { Check, Lock } from "lucide-react";
import clsx from "clsx";
import { ROADMAP_STAGES } from "@/lib/roadmap-data";

export function Roadmap() {
  const [active, setActive] = useState(0);
  const stage = ROADMAP_STAGES[active];

  return (
    <section id="roadmap" className="border-t border-white/5 py-24">
      <div className="mx-auto max-w-6xl px-6">
        <div className="text-center">
          <p className="text-sm font-medium uppercase tracking-widest text-craft-warm">The journey</p>
          <h2 className="mt-4 text-3xl font-bold text-white sm:text-4xl">Your learning roadmap</h2>
          <p className="mx-auto mt-4 max-w-2xl text-slate-400">
            Nine stages from your first concept to a deployed, portfolio-ready AI agent project.
            Click a stage to see what it covers.
          </p>
        </div>

        <div className="mt-12 flex gap-2 overflow-x-auto pb-4">
          {ROADMAP_STAGES.map((s, i) => (
            <button
              key={s.level}
              type="button"
              onClick={() => setActive(i)}
              className={clsx(
                "flex min-w-[7rem] flex-col items-center gap-2 rounded-xl border p-4 transition-colors",
                i === active
                  ? "border-craft-accent bg-craft-accent/10"
                  : "border-white/10 bg-craft-900/40 hover:border-white/25"
              )}
            >
              <span
                className={clsx(
                  "flex h-8 w-8 items-center justify-center rounded-full text-sm font-bold",
                  s.locked ? "bg-craft-800 text-slate-500" : "bg-craft-accent text-white"
                )}
              >
                {s.locked ? <Lock className="h-4 w-4" /> : s.level}
              </span>
              <span className="whitespace-nowrap text-xs text-slate-300">{s.title}</span>
            </button>
          ))}
        </div>

        <div className="mt-8 rounded-2xl border border-white/10 bg-craft-900/60 p-8">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <p className="text-sm text-craft-warm">Level {stage.level} of {ROADMAP_STAGES.length}</p>
              <h3 className="mt-1 text-2xl font-bold text-white">{stage.title}</h3>
            </div>
            {stage.locked && (
              <span className="flex items-center gap-2 rounded-full border border-white/10 px-4 py-1.5 text-sm text-slate-400">
                <Lock className="h-4 w-4" /> Unlocks as you progress
              </span>
            )}
          </div>
          <p className="mt-4 max-w-2xl text-slate-400">{stage.description}</p>

          <div className="mt-6 flex flex-wrap gap-2">
            {stage.skills.map((skill) => (
              <span key={skill} className="rounded-full bg-craft-800 px-3 py-1 text-sm text-slate-300">
                {skill}
              </span>
            ))}
          </div>

          <div className="mt-6 flex items-center gap-3 rounded-xl border border-emerald-500/20 bg-emerald-950/20 p-4 text-sm text-emerald-300">
            <Check className="h-4 w-4 shrink-0" />
            <span><strong>Checkpoint:</strong> {stage.checkpoint}</span>
          </div>
        </div>
      </div>
    </section>
  );
}
