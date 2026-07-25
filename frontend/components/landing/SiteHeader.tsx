"use client";

import Link from "next/link";
import { LayoutDashboard } from "lucide-react";
import { useAuthStore } from "@/stores/authStore";
import { Logo } from "@/components/shared/Logo";
import { ThemeToggle } from "@/components/shared/ThemeToggle";

export function SiteHeader() {
  const accessToken = useAuthStore((s) => s.accessToken);
  const hasHydrated = useAuthStore((s) => s.hasHydrated);
  const isAuthed = hasHydrated && !!accessToken;

  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-white/10 bg-[#0F172A] shadow-header backdrop-blur-md dark:bg-craft-hero">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between gap-6 px-6">
        <Logo inverted />

        <div className="flex items-center gap-3">
          <ThemeToggle compact inverted />
          {isAuthed ? (
            <Link href="/dashboard" className="btn-glow" title="Dashboard">
              <LayoutDashboard className="h-4 w-4" />
              Dashboard
            </Link>
          ) : (
            <>
              <Link
                href="/login"
                className="px-3 py-2 text-sm text-slate-300 transition hover:text-white"
              >
                Log in
              </Link>
              <Link
                href="/register"
                className="rounded-full bg-cyan-500 px-4 py-2 text-sm font-semibold text-white shadow-btn transition duration-300 hover:-translate-y-0.5 hover:bg-cyan-400 hover:shadow-btn-hover"
              >
                Join now
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
