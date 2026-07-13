"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu } from "lucide-react";
import clsx from "clsx";
import { useAuthStore } from "@/stores/authStore";
import { UserAvatar } from "@/components/shared/UserAvatar";

interface TopbarProps {
  onOpenSidebar: () => void;
}

export function Topbar({ onOpenSidebar }: TopbarProps) {
  const user = useAuthStore((s) => s.user);
  const pathname = usePathname();

  return (
    <header className="relative z-20 flex h-16 shrink-0 items-center gap-4 border-b border-slate-200/80 bg-white/95 shadow-soft backdrop-blur-sm px-6">
      <button
        type="button"
        onClick={onOpenSidebar}
        className="text-slate-500 transition hover:text-slate-900 lg:hidden"
        aria-label="Open menu"
      >
        <Menu className="h-5 w-5" />
      </button>

      <div className="min-w-0 flex-1" />

      <Link
        href="/dashboard/profile"
        className={clsx(
          "flex items-center gap-2 rounded-full border px-2 py-1.5 pr-3 text-sm font-medium shadow-soft transition duration-300 hover:shadow-card",
          pathname === "/dashboard/profile"
            ? "border-cyan-300 bg-cyan-50 text-cyan-800"
            : "border-slate-200/90 text-slate-600 hover:border-slate-300 hover:text-slate-900"
        )}
        title="View your profile"
      >
        <UserAvatar size="sm" />
        {user?.username ?? "Profile"}
      </Link>
    </header>
  );
}
