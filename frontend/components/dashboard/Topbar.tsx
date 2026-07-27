"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, Sparkles } from "lucide-react";
import clsx from "clsx";
import { useAuthStore } from "@/stores/authStore";
import { usePageChrome } from "@/stores/pageChrome";
import { UserAvatar } from "@/components/shared/UserAvatar";
import { ThemeToggle } from "@/components/shared/ThemeToggle";

interface TopbarProps {
  onOpenSidebar: () => void;
}

export function Topbar({ onOpenSidebar }: TopbarProps) {
  const user = useAuthStore((s) => s.user);
  const pathname = usePathname();
  const title = usePageChrome((s) => s.title);
  const subtitle = usePageChrome((s) => s.subtitle);
  const showAskTutor = usePageChrome((s) => s.showAskTutor);
  const onAskTutor = usePageChrome((s) => s.onAskTutor);
  const headerTabs = usePageChrome((s) => s.headerTabs);
  const activeTab = usePageChrome((s) => s.activeTab);
  const onTabChange = usePageChrome((s) => s.onTabChange);

  return (
    <header className="relative z-20 flex min-h-14 shrink-0 items-center gap-2 border-b border-craft-border/80 bg-craft-surface/90 px-3 backdrop-blur-sm sm:gap-3 sm:px-4 lg:px-6">
      <button
        type="button"
        onClick={onOpenSidebar}
        className="shrink-0 text-craft-muted transition hover:text-craft-ink lg:hidden"
        aria-label="Open menu"
      >
        <Menu className="h-5 w-5" />
      </button>

      <div className="min-w-0 flex-1 py-2">
        {title ? (
          <div className="min-w-0">
            <h1 className="truncate text-base font-bold tracking-tight text-craft-ink sm:text-lg lg:text-xl">
              {title}
            </h1>
            {subtitle ? (
              <p className="mt-0.5 truncate text-xs text-craft-muted sm:text-sm">{subtitle}</p>
            ) : null}
          </div>
        ) : null}
      </div>

      {headerTabs && headerTabs.length > 0 && onTabChange ? (
        <div className="hidden shrink-0 rounded-full border border-craft-border bg-craft-surface p-0.5 text-xs font-medium sm:flex sm:text-sm">
          {headerTabs.map((tab) => (
            <button
              key={tab.id}
              type="button"
              onClick={() => onTabChange(tab.id)}
              className={clsx(
                "rounded-full px-3 py-1.5 capitalize transition",
                activeTab === tab.id
                  ? "bg-craft-soft text-craft-ink"
                  : "text-craft-muted hover:text-craft-ink"
              )}
            >
              {tab.label}
            </button>
          ))}
        </div>
      ) : null}

      {showAskTutor && onAskTutor ? (
        <button
          type="button"
          onClick={onAskTutor}
          className="inline-flex shrink-0 items-center gap-1.5 rounded-xl border border-craft-border bg-craft-surface px-2.5 py-2 text-xs font-medium text-craft-ink shadow-soft transition hover:border-violet-400 hover:bg-craft-accent-soft sm:gap-2 sm:px-3 sm:text-sm"
        >
          <Sparkles className="h-4 w-4 shrink-0 text-violet-600" />
          Ask Tutor
        </button>
      ) : null}

      <ThemeToggle compact />

      <Link
        href="/dashboard/profile"
        className={clsx(
          "flex shrink-0 items-center gap-2 rounded-full px-1.5 py-1 text-sm font-medium transition",
          pathname === "/dashboard/profile" || pathname.startsWith("/dashboard/settings")
            ? "bg-craft-soft text-craft-ink"
            : "text-craft-muted hover:bg-craft-soft hover:text-craft-ink"
        )}
        title="View your profile"
      >
        <UserAvatar size="sm" />
        <span className="hidden max-w-[8rem] truncate lg:inline">{user?.username ?? "Profile"}</span>
      </Link>
    </header>
  );
}
