"use client";

import Link from "next/link";
import { useParams, usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  BookOpen,
  Check,
  ChevronRight,
  CircleDashed,
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
import { ProgressBar } from "@/components/shared/ProgressBar";

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
  const [pathOpen, setPathOpen] = useState(pathname.includes("/courses/"));

  useEffect(() => {
    setCollapsed(localStorage.getItem(COLLAPSED_KEY) === "1");
  }, []);

  useEffect(() => {
    if (pathname.includes("/courses/")) {
      setLessonsOpen(true);
      setPathOpen(true);
    }
  }, [pathname]);

  function toggleCollapsed() {
    setCollapsed((prev) => {
      localStorage.setItem(COLLAPSED_KEY, prev ? "0" : "1");
      return !prev;
    });
  }

  const { data: courses } = useQuery({ queryKey: ["courses"], queryFn: getCourses });
  const { data: stats } = useQuery({ queryKey: ["dashboard-stats"], queryFn: getDashboardStats });

  const pathTitle = "Create an AI Agent";
  const pathCompleted = courses?.reduce((sum, c) => sum + c.completed_lessons, 0) ?? 0;
  const pathTotal = courses?.reduce((sum, c) => sum + c.total_lessons, 0) ?? 0;

  function handleLogout() {
    logout();
    router.push("/login");
  }

  const navItemCls = (active: boolean) =>
    clsx(
      "flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition",
      collapsed && "justify-center px-0",
      active
        ? "bg-cyan-50 text-cyan-800"
        : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
    );

  return (
    <aside
      className={clsx(
        "fixed inset-y-0 left-0 z-40 flex flex-col border-r border-slate-200 bg-white transition-all lg:static lg:translate-x-0",
        collapsed ? "w-16" : "w-72",
        mobileOpen ? "translate-x-0" : "-translate-x-full"
      )}
      aria-label="Main navigation"
    >
      <div
        className={clsx(
          "flex h-16 items-center",
          collapsed ? "justify-center" : "justify-between px-5"
        )}
      >
        {collapsed ? (
          <Link href="/?landing=1" aria-label="Go to home" title="Home">
            <LogoIcon className="transition-transform hover:scale-105" />
          </Link>
        ) : (
          <Logo href="/?landing=1" />
        )}
        {!collapsed && (
          <button
            type="button"
            onClick={toggleCollapsed}
            className="hidden text-slate-400 transition hover:text-slate-700 lg:block"
            aria-label="Collapse sidebar"
          >
            <PanelLeftClose className="h-5 w-5" />
          </button>
        )}
      </div>

      {collapsed && (
        <button
          type="button"
          onClick={toggleCollapsed}
          className="mx-auto mb-1 hidden text-slate-400 transition hover:text-slate-700 lg:block"
          aria-label="Expand sidebar"
        >
          <PanelLeftOpen className="h-5 w-5" />
        </button>
      )}

      <nav className={clsx("flex-1 space-y-1 overflow-y-auto py-2", collapsed ? "px-2" : "px-3")}>
        <Link href="/?landing=1" onClick={onMobileClose} className={navItemCls(false)} title="Home">
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
              setPathOpen(true);
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
              <ChevronRight
                className={clsx(
                  "ml-auto h-4 w-4 transition-transform",
                  lessonsOpen && "rotate-90"
                )}
              />
            </>
          )}
        </button>

        {!collapsed && lessonsOpen && (
          <div className="ml-2 space-y-1 border-l border-slate-200 pl-2">
            <div>
              <button
                type="button"
                onClick={() => setPathOpen((v) => !v)}
                className={clsx(
                  "flex w-full items-center gap-2 rounded-lg px-2 py-2 text-sm font-medium transition",
                  pathOpen || pathname.includes("/courses/")
                    ? "text-slate-900"
                    : "text-slate-500 hover:text-slate-900"
                )}
                aria-expanded={pathOpen}
              >
                <ChevronRight
                  className={clsx(
                    "h-3.5 w-3.5 shrink-0 transition-transform",
                    pathOpen && "rotate-90"
                  )}
                />
                <span className="min-w-0 flex-1 truncate text-left">{pathTitle}</span>
                <span className="text-xs tabular-nums text-slate-400">
                  {pathCompleted}/{pathTotal}
                </span>
              </button>

              {pathOpen && (
                <div className="ml-3 space-y-1 border-l border-slate-200 pl-2">
                  {courses?.map((course) => (
                    <CourseTreeItem
                      key={course.slug}
                      course={course}
                      onNavigate={onMobileClose}
                    />
                  ))}
                  {courses?.length === 0 && (
                    <p className="px-2 py-2 text-sm text-slate-400">No modules yet.</p>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </nav>

      {!collapsed && (
        <div className="mx-3 mb-3 rounded-2xl bg-[#0F172A] px-4 py-4 text-white">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
            Overall progress
          </p>
          <ProgressBar
            className="mt-3 border-slate-500 bg-slate-800 shadow-none"
            value={stats?.overall_progress_pct ?? 0}
          />
          <p className="mt-2 text-xs text-slate-400">
            {stats
              ? `${stats.lessons_completed} of ${stats.total_lessons} lessons complete`
              : "Keep going — one lesson at a time."}
          </p>
        </div>
      )}

      <div className={clsx("border-t border-slate-200 p-3", collapsed && "px-2")}>
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

  useEffect(() => {
    if (isActiveCourse) setOpen(true);
  }, [isActiveCourse]);

  const { data: detail } = useQuery({
    queryKey: ["course", course.slug],
    queryFn: () => getCourse(course.slug),
    enabled: open,
  });

  const completedCount = detail
    ? detail.lessons.filter((l) => l.status === "completed").length
    : course.completed_lessons;
  const totalCount = detail?.lessons.length ?? course.total_lessons;

  return (
    <div>
      <div
        className={clsx(
          "flex items-center rounded-lg transition",
          isActiveCourse ? "text-slate-900" : "text-slate-500 hover:text-slate-900"
        )}
      >
        <button
          type="button"
          onClick={() => setOpen((v) => !v)}
          className="p-1.5 text-slate-400 hover:text-slate-700"
          aria-expanded={open}
          aria-label={`${open ? "Collapse" : "Expand"} ${course.title}`}
        >
          <ChevronRight className={clsx("h-3.5 w-3.5 transition-transform", open && "rotate-90")} />
        </button>
        <Link
          href={`/dashboard/courses/${course.slug}`}
          onClick={onNavigate}
          className="min-w-0 flex-1 truncate py-1.5 pr-2 text-sm font-medium hover:underline"
        >
          {course.title}
        </Link>
        <span className="pr-2 text-xs tabular-nums text-slate-400">
          {completedCount}/{totalCount}
        </span>
      </div>

      {open && (
        <div className="ml-4 space-y-0.5 border-l border-slate-200 pl-2">
          {detail?.lessons.map((lesson) => {
            const href = `/dashboard/courses/${course.slug}/lessons/${lesson.slug}`;
            const active = pathname === href;
            const completed = lesson.status === "completed";
            const inProgress = lesson.status === "in_progress";
            return (
              <Link
                key={lesson.id}
                href={href}
                onClick={onNavigate}
                className={clsx(
                  "flex items-center gap-2 rounded-lg px-2 py-1.5 text-sm transition",
                  active
                    ? "bg-cyan-50 font-medium text-cyan-800"
                    : "text-slate-500 hover:bg-slate-50 hover:text-slate-900"
                )}
              >
                {completed ? (
                  <Check className="h-3.5 w-3.5 shrink-0 text-emerald-600" />
                ) : inProgress ? (
                  <CircleDashed className="h-3.5 w-3.5 shrink-0 text-cyan-600" />
                ) : (
                  <span className="h-1.5 w-1.5 shrink-0 rounded-full bg-slate-300" />
                )}
                <span className="truncate">{lesson.title}</span>
              </Link>
            );
          })}
          {!detail && <p className="px-2 py-1.5 text-xs text-slate-400">Loading…</p>}
        </div>
      )}
    </div>
  );
}
