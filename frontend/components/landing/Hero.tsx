"use client";

import Link from "next/link";
import {
  ArrowRight,
  Boxes,
  CheckCircle2,
  FlaskConical,
  Lightbulb,
  Rocket,
  Wrench,
} from "lucide-react";
import { useAuthStore } from "@/stores/authStore";
import { AcademyBackdrop } from "@/components/shared/AcademyBackdrop";
import { Reveal } from "@/components/shared/Reveal";

const WORKFLOW = [
  { label: "Understand", icon: Lightbulb, blurb: "Learn the concepts" },
  { label: "Design", icon: Boxes, blurb: "Plan the agent" },
  { label: "Build", icon: Wrench, blurb: "Assemble tools" },
  { label: "Test", icon: FlaskConical, blurb: "Validate safely" },
  { label: "Deploy", icon: Rocket, blurb: "Ship with care" },
];

export function Hero() {
  const accessToken = useAuthStore((s) => s.accessToken);
  const hasHydrated = useAuthStore((s) => s.hasHydrated);
  const isAuthed = hasHydrated && !!accessToken;

  return (
    <section id="home" className="relative overflow-hidden bg-craft-canvas pb-20 pt-28">
      <AcademyBackdrop />

      <div className="relative mx-auto grid max-w-6xl items-center gap-12 px-6 lg:grid-cols-2">
        <Reveal variant="left">
          <p className="mb-4 text-xs font-bold uppercase tracking-[0.22em] text-cyan-600 dark:text-cyan-400">
            AI Agent Building Academy
          </p>
          <h1 className="text-4xl font-bold leading-[1.12] tracking-tight text-craft-ink sm:text-5xl lg:text-[3.15rem]">
            Learn AI agents from zero,{" "}
            <span className="text-cyan-600 dark:text-cyan-400">one step at a time.</span>
          </h1>
          <p className="mt-6 max-w-lg text-lg leading-relaxed text-craft-muted">
            AgentCraft helps students progress from beginner concepts to real AI agent projects
            through guided lessons, hands-on practice, and a structured learning roadmap.
          </p>
          <div className="mt-9 flex flex-wrap gap-3">
            <Link href={isAuthed ? "/dashboard" : "/register"} className="btn-landing-primary">
              {isAuthed ? "Go to Dashboard" : "Start learning"}
              <ArrowRight className="h-4 w-4" />
            </Link>
            <Link href={isAuthed ? "/dashboard" : "/register"} className="btn-landing-secondary">
              {isAuthed ? "Explore Modules" : "Join now"}
            </Link>
          </div>
        </Reveal>

        <Reveal variant="right" delay={120}>
          <div className="overflow-hidden rounded-2xl border border-craft-border bg-craft-card shadow-float">
            <div className="border-b border-craft-border bg-gradient-to-b from-craft-surface to-craft-soft/80 px-5 py-4">
              <p className="font-serif text-sm italic text-craft-muted">
                Build. Test. Improve. Ship real agents.
              </p>
            </div>
            <div className="grid grid-cols-5 gap-2 px-4 py-5 sm:gap-3 sm:px-5">
              {WORKFLOW.map(({ label, icon: Icon, blurb }, i) => (
                <div key={label} className="text-center">
                  <span
                    className="mx-auto flex h-10 w-10 items-center justify-center rounded-xl bg-craft-accent-soft text-cyan-700 shadow-soft ring-1 ring-cyan-500/20 float-soft dark:text-cyan-300"
                    style={{ animationDelay: `${i * 0.4}s` }}
                  >
                    <Icon className="h-4 w-4" />
                  </span>
                  <p className="mt-2 text-[11px] font-semibold text-craft-ink sm:text-xs">{label}</p>
                  <p className="mt-0.5 hidden text-[10px] text-craft-faint sm:block">{blurb}</p>
                </div>
              ))}
            </div>

            <div className="bg-craft-navy px-5 py-5 text-craft-inverse shadow-[inset_0_1px_0_rgba(255,255,255,0.06)]">
              <p className="text-xs font-semibold uppercase tracking-wide text-craft-inverse-muted">
                Your Progress
              </p>
              <div className="mt-4 flex flex-wrap items-center gap-6">
                <div className="hero-progress-item relative flex h-20 w-20 shrink-0 items-center justify-center drop-shadow-[0_8px_16px_rgba(34,211,238,0.18)]">
                  <svg className="h-20 w-20 -rotate-90" viewBox="0 0 36 36" aria-hidden>
                    <circle
                      cx="18"
                      cy="18"
                      r="15.5"
                      fill="none"
                      stroke="#1E293B"
                      strokeWidth="3"
                    />
                    <circle
                      className="hero-ring-progress"
                      cx="18"
                      cy="18"
                      r="15.5"
                      fill="none"
                      stroke="#22D3EE"
                      strokeWidth="3"
                      strokeLinecap="round"
                    />
                  </svg>
                  <span className="absolute text-center text-sm font-bold leading-tight text-white">
                    42%
                    <span className="block text-[9px] font-medium text-craft-faint">Overall</span>
                  </span>
                </div>

                <div className="hero-progress-item min-w-0 flex-1">
                  <p className="text-xs text-craft-faint">Current Module</p>
                  <p className="mt-0.5 text-sm font-semibold text-white">Module 3: Prompting</p>
                  <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-700">
                    <div className="hero-bar-fill h-full w-1/3 rounded-full bg-cyan-400" />
                  </div>
                  <p className="mt-1 text-[11px] text-craft-faint">Lesson 2 of 6</p>
                </div>

                <div className="hero-progress-item shrink-0">
                  <p className="text-xs text-craft-faint">Next Up</p>
                  <p className="mt-0.5 flex items-center gap-1 text-sm font-semibold text-white">
                    <CheckCircle2 className="h-3.5 w-3.5 text-cyan-400" />
                    AI Agents
                  </p>
                  <Link
                    href={isAuthed ? "/dashboard" : "/register"}
                    className="mt-2 inline-flex items-center gap-1 text-xs font-semibold text-cyan-400 hover:text-cyan-300"
                  >
                    Continue <ArrowRight className="hero-continue-arrow h-3 w-3" />
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
