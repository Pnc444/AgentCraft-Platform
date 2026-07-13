"use client";

import Link from "next/link";
import { useParams, usePathname, useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
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
import { getCourse, getCourses, getLesson } from "@/lib/api/courses";
import { useAuthStore } from "@/stores/authStore";
import { Logo, LogoIcon } from "@/components/shared/Logo";
import { ProgressBar } from "@/components/shared/ProgressBar";
import type { CourseDetail, Skill } from "@/types";

const COLLAPSED_KEY = "agentcraft-sidebar-collapsed";

interface LearningPath {
  skill: Skill;
  courses: CourseDetail[];
  completed: number;
  total: number;
  progressPct: number;
}

/** Group published courses into skill-based learning paths for the sidebar tree. */
function groupCoursesBySkill(courses: CourseDetail[]): LearningPath[] {
  const bySkill = new Map<string, LearningPath>();
  for (const course of courses) {
    const key = course.skill.slug;
    let path = bySkill.get(key);
    if (!path) {
      path = {
        skill: course.skill,
        courses: [],
        completed: 0,
        total: 0,
        progressPct: 0,
      };
      bySkill.set(key, path);
    }
    path.courses.push(course);
    path.completed += course.completed_lessons;
    path.total += course.total_lessons;
  }
  return Array.from(bySkill.values())
    .map((path) => ({
      ...path,
      courses: [...path.courses].sort((a, b) => a.order - b.order || a.title.localeCompare(b.title)),
      progressPct: path.total ? Math.round((path.completed / path.total) * 100) : 0,
    }))
    .sort((a, b) => a.skill.order - b.skill.order || a.skill.name.localeCompare(b.skill.name));
}

interface SidebarProps {
  mobileOpen: boolean;
  onMobileClose: () => void;
}

export function Sidebar({ mobileOpen, onMobileClose }: SidebarProps) {
  const pathname = usePathname();
  const router = useRouter();
  const logout = useAuthStore((s) => s.logout);

  const queryClient = useQueryClient();
  const [collapsed, setCollapsed] = useState(false);
  const [lessonsOpen, setLessonsOpen] = useState(pathname.includes("/courses/"));
  const [openPaths, setOpenPaths] = useState<Record<string, boolean>>({});

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
  const learningPaths = useMemo(
    () => (courses?.length ? groupCoursesBySkill(courses) : []),
    [courses]
  );

  useEffect(() => {
    setCollapsed(localStorage.getItem(COLLAPSED_KEY) === "1");
  }, []);

  useEffect(() => {
    if (!pathname.includes("/courses/") || !learningPaths.length) return;
    setLessonsOpen(true);
    const activeSlug = pathname.split("/")[3];
    const activePath = learningPaths.find((p) => p.courses.some((c) => c.slug === activeSlug));
    if (activePath) {
      setOpenPaths((prev) => ({ ...prev, [activePath.skill.slug]: true }));
    }
  }, [pathname, learningPaths]);

  function toggleCollapsed() {
    setCollapsed((prev) => {
      localStorage.setItem(COLLAPSED_KEY, prev ? "0" : "1");
      return !prev;
    });
  }

  function togglePath(slug: string) {
    setOpenPaths((prev) => ({ ...prev, [slug]: !prev[slug] }));
  }

  function handleLogout() {
    logout();
    router.push("/login");
  }

  const navItemCls = (active: boolean) =>
    clsx(
      "flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition",
      collapsed && "justify-center px-0",
      active
        ? "bg-cyan-50 text-cyan-800 shadow-soft ring-1 ring-cyan-100/80"
        : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
    );

  return (
    <aside
      className={clsx(
        "fixed inset-y-0 left-0 z-40 flex flex-col border-r border-slate-200/80 bg-white shadow-soft transition-all lg:static lg:translate-x-0 lg:shadow-[4px_0_24px_rgba(15,23,42,0.04)]",
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
              if (learningPaths[0]) {
                setOpenPaths((prev) => ({ ...prev, [learningPaths[0].skill.slug]: true }));
              }
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
          <div className="ml-2 space-y-2 border-l border-slate-200 pl-2">
            {learningPaths.map((path) => {
              const isOpen = !!openPaths[path.skill.slug];
              const pathActive = path.courses.some((c) => pathname.includes(`/courses/${c.slug}`));
              return (
                <div key={path.skill.slug} className="space-y-1.5">
                  <button
                    type="button"
                    onClick={() => togglePath(path.skill.slug)}
                    className={clsx(
                      "flex w-full items-center gap-2 rounded-lg px-2 py-2 text-sm font-medium transition",
                      isOpen || pathActive
                        ? "text-slate-900"
                        : "text-slate-500 hover:text-slate-900"
                    )}
                    aria-expanded={isOpen}
                  >
                    <ChevronRight
                      className={clsx(
                        "h-3.5 w-3.5 shrink-0 transition-transform",
                        isOpen && "rotate-90"
                      )}
                    />
                    <span className="min-w-0 flex-1 truncate text-left">{path.skill.name}</span>
                  </button>

                  <PathProgressCard
                    completed={path.completed}
                    total={path.total}
                    progressPct={path.progressPct}
                  />

                  {isOpen && (
                    <div className="ml-3 space-y-1 border-l border-slate-200 pl-2">
                      {path.courses.map((course) => (
                        <CourseTreeItem
                          key={course.slug}
                          course={course}
                          onNavigate={onMobileClose}
                        />
                      ))}
                      {path.courses.length === 0 && (
                        <p className="px-2 py-2 text-sm text-slate-400">No modules yet.</p>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
            {learningPaths.length === 0 && (
              <p className="px-2 py-2 text-sm text-slate-400">No learning paths yet.</p>
            )}
          </div>
        )}
      </nav>

      <div className={clsx("border-t border-slate-200 p-3", collapsed && "px-2")}>
        <button type="button" onClick={handleLogout} className={navItemCls(false)} title="Log out">
          <LogOut className="h-4 w-4 shrink-0" />
          {!collapsed && "Log out"}
        </button>
      </div>
    </aside>
  );
}

function PathProgressCard({
  completed,
  total,
  progressPct,
}: {
  completed: number;
  total: number;
  progressPct: number;
}) {
  return (
    <div className="mx-1 mb-0.5 rounded-lg bg-slate-50 px-2.5 py-2 ring-1 ring-slate-200/70">
      <div className="flex items-center justify-between gap-2">
        <p className="text-[11px] font-medium text-slate-500">Progress</p>
        <p className="text-[11px] tabular-nums text-slate-400">
          {completed}/{total}
          <span className="ml-1 text-slate-300">·</span>
          <span className="ml-1 text-cyan-700">{progressPct}%</span>
        </p>
      </div>
      <ProgressBar className="mt-1.5 h-1 border-slate-200" value={progressPct} />
    </div>
  );
}

interface CourseTreeItemProps {
  course: CourseDetail;
  onNavigate: () => void;
}

function CourseTreeItem({ course, onNavigate }: CourseTreeItemProps) {
  const params = useParams();
  const pathname = usePathname();
  const queryClient = useQueryClient();
  const isActiveCourse = params.slug === course.slug;
  const [open, setOpen] = useState(isActiveCourse);

  useEffect(() => {
    if (isActiveCourse) setOpen(true);
  }, [isActiveCourse]);

  // Prefer lessons already embedded in the curriculum list; only fetch if missing.
  const needsFetch = open && !(course.lessons && course.lessons.length);
  const { data: detail } = useQuery({
    queryKey: ["course", course.slug],
    queryFn: () => getCourse(course.slug),
    enabled: needsFetch,
    initialData: course.lessons?.length ? course : undefined,
    staleTime: 5 * 60_000,
  });

  const lessons = detail?.lessons ?? course.lessons ?? [];
  const completedCount = lessons.filter((l) => l.status === "completed").length;
  const totalCount = lessons.length || course.total_lessons;

  function prefetchLesson(lessonSlug: string) {
    void queryClient.prefetchQuery({
      queryKey: ["lesson", course.slug, lessonSlug],
      queryFn: () => getLesson(course.slug, lessonSlug),
      staleTime: 5 * 60_000,
    });
  }

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
          onMouseEnter={() => {
            void queryClient.prefetchQuery({
              queryKey: ["course", course.slug],
              queryFn: () => getCourse(course.slug),
              staleTime: 5 * 60_000,
            });
          }}
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
          {lessons.map((lesson) => {
            const href = `/dashboard/courses/${course.slug}/lessons/${lesson.slug}/content`;
            const active =
              pathname === href ||
              pathname.startsWith(`/dashboard/courses/${course.slug}/lessons/${lesson.slug}/`);
            const completed = lesson.status === "completed";
            const inProgress = lesson.status === "in_progress";
            return (
              <Link
                key={lesson.id}
                href={href}
                onClick={onNavigate}
                onMouseEnter={() => prefetchLesson(lesson.slug)}
                onFocus={() => prefetchLesson(lesson.slug)}
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
          {needsFetch && !detail && (
            <p className="px-2 py-1.5 text-xs text-slate-400">Loading…</p>
          )}
        </div>
      )}
    </div>
  );
}
