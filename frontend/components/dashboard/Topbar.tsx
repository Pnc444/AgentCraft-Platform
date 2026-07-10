"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Bot, CircleUserRound, Menu } from "lucide-react";
import clsx from "clsx";
import { useAuthStore } from "@/stores/authStore";

interface TopbarProps {
  onOpenSidebar: () => void;
  onToggleAiPanel: () => void;
}

export function Topbar({ onOpenSidebar, onToggleAiPanel }: TopbarProps) {
  const user = useAuthStore((s) => s.user);
  const pathname = usePathname();

  return (
    <header className="flex h-16 shrink-0 items-center gap-4 border-b border-white/5 bg-craft-900/50 px-6">
      <button type="button" onClick={onOpenSidebar} className="text-slate-400 hover:text-white lg:hidden" aria-label="Open menu">
        <Menu className="h-5 w-5" />
      </button>

      <div className="min-w-0 flex-1" />

      <button
        type="button"
        onClick={onToggleAiPanel}
        className="text-slate-400 hover:text-white xl:hidden"
        aria-label="Toggle AI assistant"
      >
        <Bot className="h-5 w-5" />
      </button>

      <Link
        href="/dashboard/profile"
        className={clsx(
          "flex items-center gap-2 rounded-full border px-3 py-1.5 text-sm transition-colors",
          pathname === "/dashboard/profile"
            ? "border-craft-accent/50 bg-craft-accent/10 text-white"
            : "border-white/10 text-slate-300 hover:border-white/25 hover:text-white"
        )}
        title="View your profile"
      >
        <CircleUserRound className="h-4 w-4" />
        {user?.username ?? "Profile"}
      </Link>
    </header>
  );
}
