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
    <header className="relative z-20 flex h-14 shrink-0 items-center gap-3 border-b border-craft-border/80 bg-craft-surface/88 px-4 backdrop-blur-sm lg:px-6">
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
          "flex items-center gap-2 rounded-full px-1.5 py-1 text-sm font-medium transition",
          pathname === "/dashboard/profile"
            ? "bg-craft-soft text-craft-ink"
            : "text-craft-muted hover:bg-craft-soft hover:text-craft-ink"
        )}
        title="View your profile"
      >
        <UserAvatar size="sm" />
        <span className="hidden sm:inline">{user?.username ?? "Profile"}</span>
      </Link>
    </header>
  );
}
