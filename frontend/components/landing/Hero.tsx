"use client";

import Link from "next/link";
import { useAuthStore } from "@/stores/authStore";

export function Hero() {
  const accessToken = useAuthStore((s) => s.accessToken);
  const hasHydrated = useAuthStore((s) => s.hasHydrated);
  const isAuthed = hasHydrated && !!accessToken;

  return (
    <section id="home" className="relative flex min-h-screen items-center overflow-hidden pb-16 pt-24">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_rgba(99,102,241,0.08),_transparent_55%)]" />
      <div className="absolute bottom-0 right-0 h-1/2 w-1/2 bg-[radial-gradient(ellipse_at_bottom_right,_rgba(245,158,11,0.06),_transparent_60%)]" />

      <div className="relative mx-auto grid max-w-6xl gap-12 px-6 lg:grid-cols-2 lg:items-center">
        <div>
          <p className="mb-4 text-sm font-medium uppercase tracking-widest text-craft-warm">
            AI learning platform
          </p>
          <h1 className="text-4xl font-bold leading-tight text-white sm:text-5xl lg:text-6xl">
            Learn AI agents from zero, one step at a time.
          </h1>
          <p className="mt-6 max-w-xl text-lg text-slate-400">
            AgentCraft helps students progress from beginner concepts to real AI agent projects
            through guided lessons, hands-on practice, and a structured learning roadmap.
          </p>
          <div className="mt-8 flex flex-wrap gap-4">
            <Link
              href={isAuthed ? "/dashboard" : "/register"}
              className="rounded-lg bg-craft-accent px-6 py-3 font-medium text-white transition-colors hover:bg-indigo-500"
            >
              {isAuthed ? "Go to Dashboard" : "Join Now"}
            </Link>
            <a
              href="#roadmap"
              className="rounded-lg border border-white/20 px-6 py-3 font-medium text-slate-200 transition-colors hover:border-white/40"
            >
              View Roadmap
            </a>
          </div>
        </div>

        <div className="relative">
          <div className="rounded-2xl border border-white/10 bg-craft-900/80 p-6 shadow-2xl shadow-indigo-500/10">
            <div className="mb-4 flex items-center gap-2">
              <span className="h-3 w-3 rounded-full bg-red-400" />
              <span className="h-3 w-3 rounded-full bg-yellow-400" />
              <span className="h-3 w-3 rounded-full bg-green-400" />
            </div>
            <div className="space-y-3 font-mono text-sm text-slate-300">
              <p><span className="text-craft-glow">lesson_01</span> → What is an AI agent?</p>
              <p><span className="text-craft-glow">project</span> → Build a scoped assistant</p>
              <p><span className="text-craft-glow">progress</span> ████████░░ 80%</p>
            </div>
            <div className="mt-6 h-2 overflow-hidden rounded-full bg-craft-800">
              <div className="h-full w-4/5 rounded-full bg-gradient-to-r from-craft-accent to-craft-glow" />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
