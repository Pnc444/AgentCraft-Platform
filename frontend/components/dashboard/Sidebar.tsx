"use client";

import Link from "next/link";
import { useParams, usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  BookOpen,
  Check,
  ChevronDown,
  ChevronRight,
  Home,
  LayoutDashboard,
  LogOut,
  PanelLeftClose,
  PanelLeftOpen,
} from "lucide-react";
import clsx from "clsx";
import { getCourse, getCourses, getDashboardStats } from "@/lib/api/courses";
import { useAuthStore } from "@/stores/authStore";
import { Logo, LogoIcon } from "@/components/shared/Logo";

const COLLAPSED_KEY = "agentcraft-sidebar-collapsed";

interface SidebarProps {
  mobileOpen: boolean;
  onMobileClose: () => void;
}

export function Sidebar({ mobileOpen, onMobileClose }: SidebarProps) {
  const pathname = usePathname();
  const router = useRouter();
  const logout = useAuthStore((s) => s.logout);

  const [collapsed, setCollapsed] = useState(false);
  const [lessonsOpen, setLessonsOpen] = useState(pathname.includes("/courses/"));

  // Restore collapsed state after mount (avoids SSR/client mismatch).
  useEffect(() => {
    setCollapsed(localStorage.getItem(COLLAPSED_KEY) === "1");
  }, []);

  function toggleCollapsed() {
    setCollapsed((prev) => {
      localStorage.setItem(COLLAPSED_KEY, prev ? "0" : "1");
      return !prev;
    });
  }

  const { data: courses } = useQuery({ queryKey: ["courses"], queryFn: getCourses });
  const { data: stats } = useQuery({ queryKey: ["dashboard-stats"], queryFn: getDashboardStats });

  function handleLogout() {
    logout();
    router.push("/login");
  }

  const navItemCls = (active: boolean) =>
    clsx(
      "flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-colors",
      collapsed && "justify-center px-0",
      active ? "bg-craft-accent/15 text-white" : "text-slate-400 hover:bg-white/5 hover:text-white"
    );

  return (
    <aside
      className={clsx(
        "fixed inset-y-0 left-0 z-40 flex flex-col border-r border-white/5 bg-craft-900 transition-all lg:static lg:translate-x-0",
        collapsed ? "w-16" : "w-72",
        mobileOpen ? "translate-x-0" : "-translate-x-full"
      )}
      aria-label="Main navigation"
    >
      <div className={clsx("flex h-16 items-center", collapsed ? "justify-center" : "justify-between px-5")}>
        {collapsed ? (
          <Link href="/dashboard" aria-label="Go to dashboard" title="Dashboard">
            <LogoIcon className="transition-transform hover:scale-110" />
          </Link>
        ) : (
          <Logo href="/dashboard" />
        )}
        {!collapsed && (
          <button
            type="button"
            onClick={toggleCollapsed}
            className="hidden text-slate-500 transition-colors hover:text-white lg:block"
            aria-label="Collapse sidebar"
            title="Collapse sidebar"
          >
            <PanelLeftClose className="h-5 w-5" />
          </button>
        )}
      </div>

      {collapsed && (
        <button
          type="button"
          onClick={toggleCollapsed}
          className="mx-auto mb-1 hidden text-slate-500 transition-colors hover:text-white lg:block"
          aria-label="Expand sidebar"
          title="Expand sidebar"
        >
          <PanelLeftOpen className="h-5 w-5" />
        </button>
      )}

      <nav className={clsx("flex-1 space-y-1 overflow-y-auto py-2", collapsed ? "px-2" : "px-3")}>
        <Link href="/" onClick={onMobileClose} className={navItemCls(false)} title="Home">
          <Home className="h-4 w-4 shrink-0" />
          {!collapsed && "Home"}
        </Link>

        <Link
          href="/dashboard"
          onClick={onMobileClose}
          className={navItemCls(pathname === "/dashboard")}
          title="Dashboard"
        >
          <LayoutDashboard className="h-4 w-4 shrink-0" />
          {!collapsed && "Dashboard"}
        </Link>

        <button
          type="button"
          onClick={() => {
            if (collapsed) {
              toggleCollapsed();
              setLessonsOpen(true);
            } else {
              setLessonsOpen((v) => !v);
            }
          }}
          className={navItemCls(pathname.includes("/courses/"))}
          aria-expanded={lessonsOpen}
          title="Lessons"
        >
          <BookOpen className="h-4 w-4 shrink-0" />
          {!collapsed && (
            <>
              Lessons
              <ChevronDown
                className={clsx("ml-auto h-4 w-4 transition-transform", lessonsOpen && "rotate-180")}
              />
            </>
          )}
        </button>

        {!collapsed && lessonsOpen && (
          <div className="ml-4 space-y-0.5 border-l border-white/10 pl-2">
            {courses?.map((course) => (
              <CourseTreeItem key={course.slug} course={course} onNavigate={onMobileClose} />
            ))}
            {courses?.length === 0 && (
              <p className="px-2 py-2 text-sm text-slate-600">No lessons yet.</p>
            )}
          </div>
        )}
      </nav>

      {!collapsed && (
        <div className="border-t border-white/5 px-5 py-4">
          <p className="text-xs uppercase tracking-wide text-slate-600">Learning path</p>
          <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-craft-800">
            <div
              className="h-full rounded-full bg-gradient-to-r from-craft-accent to-craft-glow transition-all"
              style={{ width: `${stats?.overall_progress_pct ?? 0}%` }}
            />
          </div>
          <p className="mt-2 text-xs text-slate-500">
            {stats ? `${stats.lessons_completed} of ${stats.total_lessons} lessons complete` : "Keep going — one lesson at a time."}
          </p>
        </div>
      )}

      <div className={clsx("border-t border-white/5 p-3", collapsed && "px-2")}>
        <button type="button" onClick={handleLogout} className={navItemCls(false)} title="Log out">
          <LogOut className="h-4 w-4 shrink-0" />
          {!collapsed && "Log out"}
        </button>
      </div>
    </aside>
  );
}

interface CourseTreeItemProps {
  course: { slug: string; title: string; total_lessons: number; completed_lessons: number };
  onNavigate: () => void;
}

function CourseTreeItem({ course, onNavigate }: CourseTreeItemProps) {
  const params = useParams();
  const pathname = usePathname();
  const isActiveCourse = params.slug === course.slug;
  const [open, setOpen] = useState(isActiveCourse);

  // Lessons are fetched lazily, only when the course is expanded.
  const { data: detail } = useQuery({
    queryKey: ["course", course.slug],
    queryFn: () => getCourse(course.slug),
    enabled: open,
  });

  return (
    <div>
      <div
        className={clsx(
          "flex items-center rounded-lg transition-colors",
          isActiveCourse ? "text-white" : "text-slate-400 hover:text-white"
        )}
      >
        <button
          type="button"
          onClick={() => setOpen((v) => !v)}
          className="p-1.5 text-slate-500 hover:text-white"
          aria-expanded={open}
          aria-label={`${open ? "Collapse" : "Expand"} ${course.title}`}
        >
          <ChevronRight className={clsx("h-3.5 w-3.5 transition-transform", open && "rotate-90")} />
        </button>
        <Link
          href={`/dashboard/courses/${course.slug}`}
          onClick={onNavigate}
          className="min-w-0 flex-1 truncate py-1.5 pr-2 text-sm hover:underline"
        >
          {course.title}
        </Link>
        <span className="pr-2 text-xs text-slate-600">
          {course.completed_lessons}/{course.total_lessons}
        </span>
      </div>

      {open && (
        <div className="ml-4 space-y-0.5 border-l border-white/10 pl-2">
          {detail?.lessons.map((lesson) => {
            const href = `/dashboard/courses/${course.slug}/lessons/${lesson.slug}`;
            const active = pathname === href;
            const completed = lesson.status === "completed";
            return (
              <Link
                key={lesson.id}
                href={href}
                onClick={onNavigate}
                className={clsx(
                  "flex items-center gap-2 rounded-md px-2 py-1.5 text-sm transition-colors",
                  active
                    ? "bg-craft-accent/15 text-white"
                    : "text-slate-500 hover:bg-white/5 hover:text-white"
                )}
              >
                {completed ? (
                  <Check className="h-3.5 w-3.5 shrink-0 text-emerald-400" />
                ) : (
                  <span className="h-1.5 w-1.5 shrink-0 rounded-full bg-slate-600" />
                )}
                <span className="truncate">{lesson.title}</span>
              </Link>
            );
          })}
          {!detail && <p className="px-2 py-1.5 text-xs text-slate-600">Loading…</p>}
        </div>
      )}
    </div>
  );
}
