"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { useQueries, useQuery } from "@tanstack/react-query";
import { PanelLeftClose, PanelLeftOpen } from "lucide-react";
import clsx from "clsx";
import { getCourse, getCourses } from "@/lib/api/courses";
import {
  TRACK_LESSON_TITLE,
  moduleDisplayTitle,
  trackModulesFrom,
} from "@/lib/learning-track";
import { entryStepForLessonType, lessonStepHref } from "@/lib/lesson-steps";
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";
import { usePageChrome } from "@/stores/pageChrome";
import type { CourseDetail } from "@/types";

const COLLAPSED_KEY = "agentcraft-lesson-modules-collapsed";

/** Compact sidebar labels. */
const MODULE_NAV_SHORT: Record<string, string> = {
  "module-1-introduction-to-ai": "Intro to AI",
  "module-1-5-how-llms-work": "How LLMs Work",
  "module-2-exploring-llm-models": "LLM Models",
  "module-3-prompting": "Prompting",
  "module-4-ai-agents": "AI Agents",
  "module-4-5-docker-and-environments": "Docker",
  "module-5-hermes": "Hermes",
  "module-6-openclaw": "OpenClaw",
  "module-7-claude": "Claude",
  "module-8-capstone-safety-evaluation": "Capstone",
};

function moduleNavLabel(mod: { slug: string; title: string }) {
  return MODULE_NAV_SHORT[mod.slug] ?? moduleDisplayTitle(mod);
}

/** First openable step in a module — free pacing, no lock order. */
function moduleEntryHref(mod: CourseDetail) {
  const lessons = mod.lessons ?? [];
  const target =
    lessons.find((l) => l.status === "in_progress") ??
    lessons.find((l) => l.status !== "completed") ??
    lessons[0];
  if (!target) return `/dashboard/courses/${mod.slug}`;
  return lessonStepHref(
    mod.slug,
    target.slug,
    entryStepForLessonType(target.lesson_type)
  );
}

/** Lesson chrome: W3Schools-style left module rail + main content. */
export function LessonStudioLayout({ children }: { children: React.ReactNode }) {
  const { lesson, course, slug, lessonSlug, openTutor, isLoading } =
    useLessonWorkspace();
  const setChrome = usePageChrome((s) => s.setChrome);
  const clearChrome = usePageChrome((s) => s.clearChrome);
  const navRef = useRef<HTMLElement>(null);
  const [collapsed, setCollapsed] = useState(false);

  const lessons = course?.lessons ?? [];
  const lessonIndex = lessons.findIndex((l) => l.slug === lesson?.slug);
  const stepOrdinal = lessonIndex >= 0 ? lessonIndex + 1 : 1;
  const moduleTitle = course ? moduleDisplayTitle(course) : "";

  const { data: allCourses } = useQuery({
    queryKey: ["courses"],
    queryFn: getCourses,
    staleTime: 5 * 60_000,
  });

  const trackSummaries = useMemo(
    () => trackModulesFrom(allCourses ?? []),
    [allCourses]
  );

  const detailQueries = useQueries({
    queries: trackSummaries.map((m) => ({
      queryKey: ["course", m.slug] as const,
      queryFn: () => getCourse(m.slug),
      staleTime: 5 * 60_000,
      enabled: trackSummaries.length > 0,
    })),
  });

  const trackModules = useMemo(() => {
    return trackSummaries.map((summary, i) => {
      const detail = detailQueries[i]?.data;
      return detail ?? ({ ...summary, lessons: [] } as CourseDetail);
    });
  }, [trackSummaries, detailQueries]);

  useEffect(() => {
    setCollapsed(localStorage.getItem(COLLAPSED_KEY) === "1");
  }, []);

  function toggleCollapsed() {
    setCollapsed((v) => {
      const next = !v;
      localStorage.setItem(COLLAPSED_KEY, next ? "1" : "0");
      return next;
    });
  }

  useEffect(() => {
    if (!lesson) {
      clearChrome();
      return;
    }
    setChrome({
      title: lesson.title,
      subtitle: moduleTitle
        ? `${moduleTitle} · Step ${stepOrdinal}/${lessons.length || "—"}`
        : `${lesson.estimated_minutes} min · Step ${stepOrdinal}/${lessons.length || "—"}`,
      showAskTutor: true,
      onAskTutor: openTutor,
      headerTabs: null,
      activeTab: null,
      onTabChange: null,
    });
    return () => clearChrome();
  }, [
    lesson,
    moduleTitle,
    stepOrdinal,
    lessons.length,
    openTutor,
    setChrome,
    clearChrome,
  ]);

  // Keep the active module (and step) visible in the rail.
  useEffect(() => {
    if (collapsed) return;
    const root = navRef.current;
    if (!root || !slug) return;
    const active =
      root.querySelector<HTMLElement>(`[data-step-slug="${lessonSlug}"]`) ??
      root.querySelector<HTMLElement>(`[data-module-slug="${slug}"]`);
    active?.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }, [slug, lessonSlug, collapsed]);

  if (isLoading || !lesson) {
    return <>{children}</>;
  }

  const hubHref = course ? `/dashboard/courses/${course.slug}` : "/dashboard";
  const overviewHref = `/dashboard/courses/${slug}/modules`;

  return (
    <div className="mx-auto flex min-h-full w-full max-w-[1400px] items-start gap-2 sm:h-full sm:min-h-0 sm:items-stretch sm:gap-3">
      {!collapsed ? (
        <aside className="sticky top-0 flex max-h-[calc(100dvh-5rem)] w-[7.75rem] shrink-0 flex-col overflow-hidden rounded-lg border border-craft-border bg-craft-soft/60 sm:static sm:max-h-none sm:w-48 lg:w-56">
          <div className="flex shrink-0 items-start justify-between gap-1 border-b border-craft-border px-2 py-2 sm:px-3 sm:py-2.5">
            <div className="min-w-0">
              <Link
                href={hubHref}
                className="text-[10px] font-medium text-craft-muted transition hover:text-violet-600 dark:hover:text-violet-400 sm:text-xs"
              >
                ← Lessons
              </Link>
              <p className="mt-1 text-[9px] font-bold uppercase leading-snug tracking-[0.12em] text-craft-faint sm:text-[10px]">
                {TRACK_LESSON_TITLE}
              </p>
            </div>
            <button
              type="button"
              onClick={toggleCollapsed}
              className="shrink-0 rounded-md p-1 text-craft-faint transition hover:bg-craft-surface hover:text-craft-ink"
              aria-label="Hide modules"
              title="Hide modules"
            >
              <PanelLeftClose className="h-4 w-4" />
            </button>
          </div>

          <nav
            ref={navRef}
            className="min-h-0 flex-1 overflow-y-auto scrollbar-hide py-1"
            aria-label="Modules"
          >
            {trackModules.map((mod) => {
              const activeMod = mod.slug === slug;
              const label = moduleNavLabel(mod);
              const fullLabel = moduleDisplayTitle(mod);
              const steps = mod.lessons ?? [];

              return (
                <div key={mod.slug} className="mb-0.5">
                  <Link
                    href={moduleEntryHref(mod)}
                    data-module-slug={mod.slug}
                    aria-current={activeMod ? "page" : undefined}
                    title={fullLabel}
                    className={clsx(
                      "relative block border-l-[3px] px-2 py-1.5 text-[11px] font-medium leading-snug transition sm:px-3 sm:py-2 sm:text-sm",
                      activeMod
                        ? "border-violet-500 bg-craft-surface text-craft-ink"
                        : "border-transparent text-craft-ink/80 hover:bg-craft-surface/70 hover:text-craft-ink"
                    )}
                  >
                    {label}
                  </Link>

                  {activeMod && steps.length > 0 ? (
                    <ul className="pb-1">
                      {steps.map((step) => {
                        const activeStep = step.slug === lessonSlug;
                        return (
                          <li key={step.slug}>
                            <Link
                              href={lessonStepHref(
                                mod.slug,
                                step.slug,
                                entryStepForLessonType(step.lesson_type)
                              )}
                              data-step-slug={step.slug}
                              aria-current={activeStep ? "page" : undefined}
                              title={step.title}
                              className={clsx(
                                "relative block truncate border-l-[3px] py-1 pl-3.5 pr-2 text-[10px] leading-snug transition sm:pl-5 sm:pr-3 sm:text-xs",
                                activeStep
                                  ? "border-violet-500 bg-violet-500/10 font-semibold text-craft-ink"
                                  : "border-transparent text-craft-muted hover:bg-craft-surface/60 hover:text-craft-ink"
                              )}
                            >
                              {step.title}
                            </Link>
                          </li>
                        );
                      })}
                    </ul>
                  ) : null}
                </div>
              );
            })}
          </nav>

          <Link
            href={overviewHref}
            className="shrink-0 border-t border-craft-border px-2.5 py-2 text-[10px] font-semibold text-craft-muted transition hover:bg-craft-surface hover:text-craft-ink sm:px-3 sm:text-xs"
          >
            Module overview
          </Link>
        </aside>
      ) : null}

      {/* When rail is closed, reopen sits above the card — no empty column */}
      <div className="flex min-h-0 min-w-0 flex-1 flex-col gap-1.5">
        {collapsed ? (
          <button
            type="button"
            onClick={toggleCollapsed}
            className="inline-flex h-8 w-fit shrink-0 items-center gap-1.5 rounded-lg border border-craft-border bg-craft-surface px-2.5 text-[11px] font-semibold text-craft-muted transition hover:border-violet-400 hover:text-craft-ink"
            aria-label="Show modules"
            title="Show modules"
          >
            <PanelLeftOpen className="h-3.5 w-3.5" />
            Modules
          </button>
        ) : null}
        <div className="min-h-0 min-w-0 flex-1">{children}</div>
      </div>
    </div>
  );
}
