"use client";

import Link from "next/link";
import { useAuthStore } from "@/stores/authStore";

export function FinalCta() {
  const accessToken = useAuthStore((s) => s.accessToken);
  const hasHydrated = useAuthStore((s) => s.hasHydrated);
  const isAuthed = hasHydrated && !!accessToken;

  return (
    <section className="border-t border-slate-200 bg-[#F8FAFC] py-24">
      <div className="mx-auto max-w-3xl px-6 text-center">
        <div className="rounded-3xl border border-slate-200/80 bg-white p-10 shadow-float ring-1 ring-black/[0.03] sm:p-12">
          <p className="text-xs font-bold uppercase tracking-[0.2em] text-cyan-600">
            Ready to begin?
          </p>
          <h2 className="mt-3 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
            Start your path from zero to building real AI agents
          </h2>
          <p className="mt-5 text-lg text-slate-500">
            Join AgentCraft and take your first lesson in minutes — short steps, hands-on practice,
            and a clear roadmap all the way through.
          </p>
          <div className="mt-9 flex flex-wrap items-center justify-center gap-3">
            {isAuthed ? (
              <Link href="/dashboard" className="btn-landing-primary px-8 py-3.5">
                Go to Dashboard
              </Link>
            ) : (
              <>
                <Link href="/register" className="btn-landing-primary px-8 py-3.5">
                  Get started
                </Link>
                <Link href="/login" className="btn-landing-secondary px-8 py-3.5">
                  Log in
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
