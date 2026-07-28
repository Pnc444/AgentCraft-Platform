"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Award,
  BookOpen,
  Flame,
  LayoutDashboard,
  LogOut,
  PanelLeftClose,
  PanelLeftOpen,
  Settings,
  Trophy,
} from "lucide-react";
import clsx from "clsx";
import { getCourses } from "@/lib/api/courses";
import { recordAndGetVisitStreak } from "@/lib/visit-streak";
import { useAuthStore } from "@/stores/authStore";
import { Logo } from "@/components/shared/Logo";
import { currentModule, trackModulesFrom } from "@/lib/learning-track";

const COLLAPSED_KEY = "agentcraft-sidebar-collapsed";

interface SidebarProps {
  mobileOpen: boolean;
  onMobileClose: () => void;
}

function navItemCls(active: boolean, collapsed: boolean) {
  return clsx(
    "flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition",
    collapsed && "justify-center px-2",
    active
      ? "bg-violet-600 text-white shadow-btn"
      : "text-craft-muted hover:bg-craft-soft hover:text-craft-ink"
  );
}

export function Sidebar({ mobileOpen, onMobileClose }: SidebarProps) {
  const pathname = usePathname();
  const router = useRouter();
  const logout = useAuthStore((s) => s.logout);
  const queryClient = useQueryClient();
  const [collapsed, setCollapsed] = useState(false);
  const [streak, setStreak] = useState(0);

  const { data: courses } = useQuery({
    queryKey: ["courses"],
    queryFn: async () => {
      const list = await getCourses();
      for (const course of list) {
        queryClient.setQueryData(["course", course.slug], course);
      }
      return list;
    },
  });

  const lessonsHref = useMemo(() => {
    const track = trackModulesFrom(courses ?? []);
    const target = currentModule(track) ?? track[0];
    if (target) return `/dashboard/courses/${target.slug}`;
    if (!courses?.length) return "/dashboard";
    return `/dashboard/courses/${courses[0].slug}`;
  }, [courses]);

  useEffect(() => {
    setCollapsed(localStorage.getItem(COLLAPSED_KEY) === "1");
    setStreak(recordAndGetVisitStreak());
  }, []);

  function toggleCollapsed() {
    setCollapsed((v) => {
      const next = !v;
      localStorage.setItem(COLLAPSED_KEY, next ? "1" : "0");
      return next;
    });
  }

  function handleLogout() {
    logout();
    router.replace("/login");
  }

  const onLesson =
    pathname.includes("/courses/") || pathname.startsWith("/dashboard/courses");

  return (
    <aside
      className={clsx(
        "fixed inset-y-0 left-0 z-40 flex min-h-0 flex-col overflow-hidden border-r border-craft-border bg-craft-surface transition-[width,transform] lg:relative lg:static lg:h-screen lg:translate-x-0",
        collapsed ? "w-16" : "w-64",
        mobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
      )}
      aria-label="Main navigation"
    >
      <div
        className={clsx(
          "flex h-16 shrink-0 items-center",
          collapsed ? "justify-center" : "justify-between px-4"
        )}
      >
        {!collapsed && <Logo href="/dashboard" />}
        <button
          type="button"
          onClick={toggleCollapsed}
          className="hidden text-craft-faint transition hover:text-craft-ink lg:block"
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? <PanelLeftOpen className="h-5 w-5" /> : <PanelLeftClose className="h-5 w-5" />}
        </button>
      </div>

      <nav
        className={clsx(
          "min-h-0 flex-1 space-y-1 overflow-y-auto py-2 max-lg:scrollbar-hide",
          collapsed ? "px-2" : "px-3"
        )}
      >
        <Link
          href="/dashboard"
          onClick={onMobileClose}
          className={navItemCls(pathname === "/dashboard", collapsed)}
          title="Dashboard"
        >
          <LayoutDashboard className="h-4 w-4 shrink-0" />
          {!collapsed && "Dashboard"}
        </Link>

        <Link
          href={lessonsHref}
          onClick={onMobileClose}
          className={navItemCls(onLesson, collapsed)}
          title="Lessons"
        >
          <BookOpen className="h-4 w-4 shrink-0" />
          {!collapsed && "Lessons"}
        </Link>

        <Link
          href="/dashboard/certificates"
          onClick={onMobileClose}
          className={navItemCls(pathname.startsWith("/dashboard/certificates"), collapsed)}
          title="Certificates"
        >
          <Award className="h-4 w-4 shrink-0" />
          {!collapsed && "Certificates"}
        </Link>

        <Link
          href="/dashboard/profile"
          onClick={onMobileClose}
          className={navItemCls(
            pathname.startsWith("/dashboard/profile") || pathname.startsWith("/dashboard/settings"),
            collapsed
          )}
          title="Settings"
        >
          <Settings className="h-4 w-4 shrink-0" />
          {!collapsed && "Settings"}
        </Link>
      </nav>

      {!collapsed && (
        <div className="mx-3 mb-3 rounded-2xl border border-craft-border bg-craft-soft/80 p-3">
          <p className="text-xs font-semibold text-craft-ink">Keep going!</p>
          <div className="mt-2 flex items-center justify-between gap-2">
            <span className="inline-flex items-center gap-1.5 text-sm font-medium text-craft-muted">
              <Flame className="h-4 w-4 text-orange-500" />
              {streak} day streak
            </span>
            <Trophy className="h-4 w-4 text-violet-500" />
          </div>
        </div>
      )}

      <div className={clsx("border-t border-craft-border p-3", collapsed && "px-2")}>
        <button type="button" onClick={handleLogout} className={navItemCls(false, collapsed)} title="Log out">
          <LogOut className="h-4 w-4 shrink-0" />
          {!collapsed && "Log out"}
        </button>
      </div>
    </aside>
  );
}
