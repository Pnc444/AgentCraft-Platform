"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu } from "lucide-react";
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
