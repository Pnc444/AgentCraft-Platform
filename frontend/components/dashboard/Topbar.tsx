"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, Menu } from "lucide-react";
import clsx from "clsx";
import { useAuthStore } from "@/stores/authStore";
import { UserAvatar } from "@/components/shared/UserAvatar";
import { ThemeToggle } from "@/components/shared/ThemeToggle";

interface TopbarProps {
  onOpenSidebar: () => void;
}

export function Topbar({ onOpenSidebar }: TopbarProps) {
  const user = useAuthStore((s) => s.user);
  const pathname = usePathname();

  return (
    <header className="relative z-20 flex h-16 shrink-0 items-center gap-4 border-b border-craft-border bg-craft-surface/95 px-6 shadow-soft backdrop-blur-sm">
      <button
        type="button"
        onClick={onOpenSidebar}
        className="text-craft-muted transition hover:text-craft-ink lg:hidden"
        aria-label="Open menu"
      >
        <Menu className="h-5 w-5" />
      </button>

      <Link
        href="/dashboard"
        className={clsx(
          "flex items-center gap-2 rounded-xl px-3 py-2 text-sm font-medium transition",
          pathname === "/dashboard"
            ? "bg-craft-accent-soft text-cyan-800 ring-1 ring-cyan-500/20 dark:text-cyan-200"
            : "text-craft-muted hover:bg-craft-soft hover:text-craft-ink"
        )}
        title="Dashboard"
      >
        <LayoutDashboard className="h-4 w-4 shrink-0" />
        <span className="hidden sm:inline">Dashboard</span>
      </Link>

      <div className="min-w-0 flex-1" />

      <ThemeToggle compact />

      <Link
        href="/dashboard/profile"
        className={clsx(
          "flex items-center gap-2 rounded-full border px-2 py-1.5 pr-3 text-sm font-medium shadow-soft transition duration-300 hover:shadow-card",
          pathname === "/dashboard/profile"
            ? "border-cyan-300 bg-cyan-50 text-cyan-800 dark:border-cyan-500/40 dark:bg-cyan-500/10 dark:text-cyan-200"
            : "border-craft-border text-craft-muted hover:border-craft-faint hover:text-craft-ink"
        )}
        title="View your profile"
      >
        <UserAvatar size="sm" />
        {user?.username ?? "Profile"}
      </Link>
    </header>
  );
}
