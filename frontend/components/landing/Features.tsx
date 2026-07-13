"use client";

import type { ReactNode } from "react";
import { Reveal } from "@/components/shared/Reveal";

export function Features() {
  return (
    <section id="features" className="border-t border-craft-border bg-craft-surface py-24">
      <div className="mx-auto max-w-6xl space-y-20 px-6">
        <FeatureRow
          title="Learn in small steps"
          body="Students are not expected to understand everything at once. Lessons are broken into manageable chunks so each concept builds on the last."
          visual={
            <div className="space-y-2">
              <div className="rounded-xl bg-craft-accent-soft px-4 py-3 text-sm font-medium text-cyan-800 shadow-soft ring-1 ring-cyan-500/20 dark:text-cyan-200">
                Lesson 1 — What is an agent?
              </div>
              <div className="rounded-xl bg-craft-soft px-4 py-3 text-sm text-craft-muted shadow-soft ring-1 ring-craft-border">
                Lesson 2 — Tools &amp; memory
              </div>
              <div className="rounded-xl bg-craft-soft/70 px-4 py-3 text-sm text-craft-faint ring-1 ring-craft-border/80">
                Lesson 3 — Workflows
              </div>
            </div>
          }
        />

        <FeatureRow
          reverse
          title="Build real projects"
          body="Learn by building, not just reading. AgentCraft guides you toward small working projects that build confidence step by step."
          visual={
            <div>
              <p className="font-mono text-sm font-medium text-cyan-600 dark:text-cyan-400">
                mini_project.py
              </p>
              <pre className="mt-3 overflow-x-auto rounded-xl bg-craft-navy p-4 text-sm text-slate-200 shadow-navy ring-1 ring-white/10">
                <code>{`assistant = Agent(
  purpose="summarize notes",
  tools=[read_file, search]
)`}</code>
              </pre>
            </div>
          }
        />

        <FeatureRow
          title="Scoped practice"
          body="Safe, limited-scope AI learning. Students are not thrown into full-access agents immediately — the platform teaches structure, constraints, and safe tool use."
          visual={
            <div className="rounded-xl border border-emerald-500/30 bg-emerald-50 p-6 shadow-soft dark:bg-emerald-500/10">
              <p className="text-sm font-semibold text-emerald-800 dark:text-emerald-300">
                Sandbox workspace
              </p>
              <ul className="mt-3 space-y-2 text-sm text-emerald-900/80 dark:text-emerald-200/80">
                <li>Allowed: read files, search docs</li>
                <li>Blocked: unrestricted web, shell</li>
              </ul>
            </div>
          }
        />

        <FeatureRow
          reverse
          title="Track progress"
          body="See where you are in the learning path and what comes next. Checkpoints keep the journey clear and motivating."
          visual={
            <div>
              <div className="flex items-center justify-between text-sm text-craft-muted">
                <span>Level 4 of 9</span>
                <span className="font-medium text-cyan-600 dark:text-cyan-400">Backend Basics</span>
              </div>
              <div className="mt-4 h-2 overflow-hidden rounded-full bg-craft-soft shadow-[inset_0_1px_2px_rgba(15,23,42,0.08)] dark:shadow-[inset_0_1px_2px_rgba(0,0,0,0.35)]">
                <div
                  className="h-full rounded-full bg-cyan-500 shadow-[0_0_12px_rgba(6,182,212,0.45)]"
                  style={{ width: "44%" }}
                />
              </div>
            </div>
          }
        />
      </div>
    </section>
  );
}

function FeatureRow({
  title,
  body,
  visual,
  reverse = false,
}: {
  title: string;
  body: string;
  visual: ReactNode;
  reverse?: boolean;
}) {
  return (
    <div className="grid items-center gap-10 lg:grid-cols-2">
      <Reveal
        variant={reverse ? "right" : "left"}
        className={reverse ? "lg:order-2" : undefined}
      >
        <h3 className="text-2xl font-bold tracking-tight text-craft-ink">{title}</h3>
        <p className="mt-4 leading-relaxed text-craft-muted">{body}</p>
      </Reveal>
      <Reveal
        variant={reverse ? "left" : "right"}
        delay={120}
        className={reverse ? "lg:order-1" : undefined}
      >
        <div className="landing-card card-interactive p-6">{visual}</div>
      </Reveal>
    </div>
  );
}
