"use client";

import Link from "next/link";
import { useAuthStore } from "@/stores/authStore";

export function FinalCta() {
  const accessToken = useAuthStore((s) => s.accessToken);
  const hasHydrated = useAuthStore((s) => s.hasHydrated);
  const isAuthed = hasHydrated && !!accessToken;

  return (
    <section id="get-started" className="relative overflow-hidden border-t border-stone-800/40 bg-craft-950 py-32 sm:py-40">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_rgba(99,102,241,0.1),_transparent_65%)]" />
      <div className="absolute bottom-0 left-1/2 h-1/2 w-2/3 -translate-x-1/2 bg-[radial-gradient(ellipse_at_bottom,_rgba(245,158,11,0.06),_transparent_60%)]" />

      <div className="relative mx-auto max-w-3xl px-6 py-8 text-center">
        <p className="text-sm font-medium uppercase tracking-widest text-craft-warm">Ready to begin?</p>
        <h2 className="mt-4 text-3xl font-bold leading-tight text-white sm:text-4xl lg:text-5xl">
          Start your path from zero to building real AI agents
        </h2>
        <p className="mt-6 text-lg text-slate-400">
          Join AgentCraft and take your first lesson in minutes — short steps, hands-on practice,
          and a clear roadmap all the way through.
        </p>
        <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
          {isAuthed ? (
            <Link href="/dashboard" className="rounded-lg bg-craft-accent px-8 py-3.5 font-medium text-white transition-colors hover:bg-indigo-500">
              Go to Dashboard
            </Link>
          ) : (
            <>
              <Link href="/register" className="rounded-lg bg-craft-accent px-8 py-3.5 font-medium text-white transition-colors hover:bg-indigo-500">
                Get Started — Free
              </Link>
              <Link href="/login" className="rounded-lg border border-white/20 px-8 py-3.5 font-medium text-slate-200 transition-colors hover:border-white/40">
                Log In
              </Link>
            </>
          )}
        </div>
      </div>
    </section>
  );
}
