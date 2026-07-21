"use client";

import Link from "next/link";
import { useParams, usePathname, useRouter } from "next/navigation";
import { useEffect, useMemo, useState, type CSSProperties } from "react";
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
import type { CourseDetail, Skill } from "@/types";

const COLLAPSED_KEY = "agentcraft-sidebar-collapsed";
const SIDEBAR_WIDTH_KEY = "agentcraft-sidebar-width";
const COLLAPSED_WIDTH_PX = 64;
const DEFAULT_SIDEBAR_WIDTH_PX = 272;
const MIN_SIDEBAR_WIDTH_PX = 224;
const MAX_SIDEBAR_WIDTH_PX = 360;

function clampSidebarWidth(width: number) {
  if (typeof window === "undefined") {
    return Math.min(MAX_SIDEBAR_WIDTH_PX, Math.max(MIN_SIDEBAR_WIDTH_PX, width));
  }

  const maxWidth = Math.min(MAX_SIDEBAR_WIDTH_PX, Math.max(MIN_SIDEBAR_WIDTH_PX, window.innerWidth - 160));
  return Math.min(maxWidth, Math.max(MIN_SIDEBAR_WIDTH_PX, width));
}

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

/** Next module to open for a skill path: in-progress, else first unfinished, else first. */
function continueCourseForPath(path: LearningPath): CourseDetail | null {
  if (!path.courses.length) return null;
  const inProgress = path.courses.find((c) => c.completion_pct > 0 && c.completion_pct < 100);
  if (inProgress) return inProgress;
  const notStarted = path.courses.find((c) => c.completion_pct === 0);
  if (notStarted) return notStarted;
  return path.courses[0];
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
  const [sidebarWidth, setSidebarWidth] = useState(DEFAULT_SIDEBAR_WIDTH_PX);
  const [isResizing, setIsResizing] = useState(false);
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
    const storedWidth = Number(localStorage.getItem(SIDEBAR_WIDTH_KEY));
    if (Number.isFinite(storedWidth) && storedWidth > 0) {
      setSidebarWidth(clampSidebarWidth(storedWidth));
    }
  }, []);

  useEffect(() => {
    document.documentElement.style.setProperty(
      "--sidebar-w",
      collapsed ? `${COLLAPSED_WIDTH_PX}px` : `${sidebarWidth}px`
    );
  }, [collapsed, sidebarWidth]);

  useEffect(() => {
    if (collapsed) return;
    localStorage.setItem(SIDEBAR_WIDTH_KEY, String(sidebarWidth));
  }, [collapsed, sidebarWidth]);

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

  function startResizing(event: React.MouseEvent<HTMLDivElement>) {
    if (collapsed) return;

    function handleMouseMove(moveEvent: MouseEvent) {
      setSidebarWidth(clampSidebarWidth(moveEvent.clientX));
    }

    function stopResizing() {
      setIsResizing(false);
      document.body.style.removeProperty("cursor");
      document.body.style.removeProperty("user-select");
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", stopResizing);
    }

    setIsResizing(true);
    document.body.style.cursor = "col-resize";
    document.body.style.userSelect = "none";
    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", stopResizing);
  }

  function nudgeSidebarWidth(delta: number) {
    setSidebarWidth((current) => clampSidebarWidth(current + delta));
  }

  function handleResizeKeyDown(event: React.KeyboardEvent<HTMLDivElement>) {
    if (collapsed) return;

    if (event.key === "ArrowLeft") {
      event.preventDefault();
      nudgeSidebarWidth(-16);
      return;
    }
    if (event.key === "ArrowRight") {
      event.preventDefault();
      nudgeSidebarWidth(16);
      return;
    }
    if (event.key === "Home") {
      event.preventDefault();
      setSidebarWidth(MIN_SIDEBAR_WIDTH_PX);
      return;
    }
    if (event.key === "End") {
      event.preventDefault();
      setSidebarWidth(clampSidebarWidth(MAX_SIDEBAR_WIDTH_PX));
    }
  }

  function togglePath(slug: string) {
    setOpenPaths((prev) => ({ ...prev, [slug]: !prev[slug] }));
  }

  function openPathCourse(path: LearningPath) {
    const target = continueCourseForPath(path);
    setLessonsOpen(true);
    setOpenPaths((prev) => ({ ...prev, [path.skill.slug]: true }));
    if (!target) return;
    onMobileClose();
    router.push(`/dashboard/courses/${target.slug}`);
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
        ? "bg-craft-accent-soft text-cyan-800 shadow-soft ring-1 ring-cyan-500/20 dark:text-cyan-200"
        : "text-craft-muted hover:bg-craft-soft hover:text-craft-ink"
    );

  const sidebarStyle = {
    "--sidebar-live-w": `${sidebarWidth}px`,
  } as CSSProperties;

  return (
    <aside
      className={clsx(
        "fixed inset-y-0 left-0 z-40 flex min-h-0 flex-col overflow-hidden border-r border-craft-border bg-craft-surface shadow-soft transition-[width,transform] lg:relative lg:static lg:h-screen lg:translate-x-0 lg:shadow-[4px_0_24px_rgba(15,23,42,0.04)] dark:lg:shadow-[4px_0_24px_rgba(0,0,0,0.35)]",
        collapsed ? "w-16 lg:w-16" : "w-72 lg:w-[var(--sidebar-live-w)]",
        mobileOpen ? "translate-x-0" : "-translate-x-full"
      )}
      style={sidebarStyle}
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
            className="hidden text-craft-faint transition hover:text-craft-ink lg:block"
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
          className="mx-auto mb-1 hidden text-craft-faint transition hover:text-craft-ink lg:block"
          aria-label="Expand sidebar"
        >
          <PanelLeftOpen className="h-5 w-5" />
        </button>
      )}

      <nav className={clsx("min-h-0 flex-1 space-y-1 overflow-y-auto overscroll-contain py-2", collapsed ? "px-2" : "px-3")}>
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
          className={navItemCls(lessonsOpen || pathname.includes("/courses/"))}
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
          <div className="ml-2 space-y-2 border-l border-craft-border pl-2">
            {learningPaths.map((path) => {
              const isOpen = !!openPaths[path.skill.slug];
              return (
                <div key={path.skill.slug} className="space-y-1.5">
                  <div
                    className={clsx(
                      "flex items-center rounded-lg px-1 transition",
                      isOpen
                        ? "text-craft-ink"
                        : "text-craft-muted hover:bg-craft-soft hover:text-craft-ink"
                    )}
                  >
                    <button
                      type="button"
                      onClick={() => togglePath(path.skill.slug)}
                      className={clsx(
                        "rounded-md p-1.5 transition",
                        isOpen
                          ? "text-craft-ink"
                          : "text-craft-faint hover:text-craft-ink"
                      )}
                      aria-expanded={isOpen}
                      aria-label={`${isOpen ? "Collapse" : "Expand"} ${path.skill.name}`}
                    >
                      <ChevronRight
                        className={clsx(
                          "h-3.5 w-3.5 shrink-0 transition-transform",
                          isOpen && "rotate-90"
                        )}
                      />
                    </button>
                    <button
                      type="button"
                      onClick={() => openPathCourse(path)}
                      className="min-w-0 flex-1 truncate rounded-md py-1.5 pr-2 text-left text-sm font-medium"
                      title={path.skill.name}
                    >
                      {path.skill.name}
                    </button>
                    <span className="pr-2 text-xs tabular-nums text-craft-faint">
                      {path.completed}/{path.total}
                    </span>
                  </div>

                  {isOpen && (
                    <div className="ml-3 space-y-1 border-l border-craft-border pl-2">
                      {path.courses.map((course) => (
                        <CourseTreeItem
                          key={course.slug}
                          course={course}
                          onNavigate={onMobileClose}
                        />
                      ))}
                      {path.courses.length === 0 && (
                        <p className="px-2 py-2 text-sm text-craft-faint">No modules yet.</p>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
            {learningPaths.length === 0 && (
              <p className="px-2 py-2 text-sm text-craft-faint">No learning paths yet.</p>
            )}
          </div>
        )}
      </nav>

      <div className={clsx("border-t border-craft-border p-3", collapsed && "px-2")}>
        <button type="button" onClick={handleLogout} className={navItemCls(false)} title="Log out">
          <LogOut className="h-4 w-4 shrink-0" />
          {!collapsed && "Log out"}
        </button>
      </div>

      {!collapsed && (
        <div
          role="separator"
          tabIndex={0}
          aria-orientation="vertical"
          aria-label="Resize sidebar"
          onMouseDown={(event) => {
            event.preventDefault();
            startResizing(event);
          }}
          onKeyDown={handleResizeKeyDown}
          className={clsx(
            "absolute inset-y-0 right-0 hidden w-3 cursor-col-resize lg:flex",
            isResizing ? "bg-cyan-500/20" : "hover:bg-cyan-500/10"
          )}
        />
      )}
    </aside>
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
  const courseHref = `/dashboard/courses/${course.slug}`;
  const isActiveCourse = pathname === courseHref;
  const hasActiveLesson = pathname.startsWith(`${courseHref}/lessons/`);
  const [open, setOpen] = useState(isActiveCourse);

  useEffect(() => {
    if (isActiveCourse || hasActiveLesson) setOpen(true);
  }, [hasActiveLesson, isActiveCourse]);

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
          isActiveCourse
            ? "bg-craft-accent-soft text-cyan-800 shadow-soft ring-1 ring-cyan-500/20 dark:text-cyan-200"
            : open || hasActiveLesson
              ? "text-craft-ink"
              : "text-craft-muted hover:bg-craft-soft hover:text-craft-ink"
        )}
      >
        <button
          type="button"
          onClick={() => setOpen((v) => !v)}
          className={clsx(
            "rounded-md p-1.5 transition",
            isActiveCourse
              ? "text-cyan-700 dark:text-cyan-300"
              : open || hasActiveLesson
                ? "text-craft-ink"
                : "text-craft-faint hover:text-craft-ink"
          )}
          aria-expanded={open}
          aria-label={`${open ? "Collapse" : "Expand"} ${course.title}`}
        >
          <ChevronRight className={clsx("h-3.5 w-3.5 transition-transform", open && "rotate-90")} />
        </button>
        <Link
          href={courseHref}
          onClick={onNavigate}
          onMouseEnter={() => {
            void queryClient.prefetchQuery({
              queryKey: ["course", course.slug],
              queryFn: () => getCourse(course.slug),
              staleTime: 5 * 60_000,
            });
          }}
          className="min-w-0 flex-1 truncate rounded-md py-1.5 pr-2 text-sm font-medium"
          title={course.title}
        >
          {course.title}
        </Link>
        <span className="pr-2 text-xs tabular-nums text-craft-faint">
          {completedCount}/{totalCount}
        </span>
      </div>

      {open && (
        <div className="ml-4 space-y-0.5 border-l border-craft-border pl-2">
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
                    ? "bg-craft-accent-soft font-medium text-cyan-800 dark:text-cyan-200"
                    : "text-craft-muted hover:bg-craft-soft hover:text-craft-ink"
                )}
                title={lesson.title}
              >
                {completed ? (
                  <Check className="h-3.5 w-3.5 shrink-0 text-emerald-600" />
                ) : inProgress ? (
                  <CircleDashed className="h-3.5 w-3.5 shrink-0 text-cyan-600" />
                ) : (
                  <span className="h-1.5 w-1.5 shrink-0 rounded-full bg-craft-faint" />
                )}
                <span className="truncate">{lesson.title}</span>
              </Link>
            );
          })}
          {needsFetch && !detail && (
            <p className="px-2 py-1.5 text-xs text-craft-faint">Loading…</p>
          )}
        </div>
      )}
    </div>
  );
}
