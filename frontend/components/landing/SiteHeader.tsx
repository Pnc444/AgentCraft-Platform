"use client";

import Link from "next/link";
import { useAuthStore } from "@/stores/authStore";

export function SiteHeader() {
  const accessToken = useAuthStore((s) => s.accessToken);
  const hasHydrated = useAuthStore((s) => s.hasHydrated);
  const isAuthed = hasHydrated && !!accessToken;

  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-white/5 bg-craft-950/80 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
        <Link href="/" className="flex items-center gap-2 text-lg font-bold text-white">
          <span aria-hidden>⚡</span>
          Agent<span className="text-craft-accent">Craft</span>
        </Link>
        <nav className="hidden items-center gap-8 text-sm text-slate-400 sm:flex">
          <a href="#about" className="transition-colors hover:text-white">About</a>
          <a href="#features" className="transition-colors hover:text-white">Features</a>
          <a href="#roadmap" className="transition-colors hover:text-white">Roadmap</a>
        </nav>
        <div className="flex items-center gap-3">
          {isAuthed ? (
            <Link
              href="/dashboard"
              className="rounded-lg bg-craft-accent px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-500"
            >
              Dashboard
            </Link>
          ) : (
            <>
              <Link href="/login" className="px-3 py-2 text-sm text-slate-300 transition-colors hover:text-white">
                Log in
              </Link>
              <Link
                href="/register"
                className="rounded-lg bg-craft-accent px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-500"
              >
                Join Now
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
