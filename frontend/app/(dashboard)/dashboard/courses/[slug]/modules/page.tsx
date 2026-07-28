"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { ArrowRight, Check, ChevronDown, Circle } from "lucide-react";
import clsx from "clsx";
import { getCourses } from "@/lib/api/courses";
import type { CourseDetail, LessonSummary } from "@/types";
import { entryStepForLessonType, lessonStepHref } from "@/lib/lesson-steps";
import { nextModule } from "@/components/dashboard/LessonFeatureCard";
import { Reveal } from "@/components/shared/Reveal";
import { usePageChrome } from "@/stores/pageChrome";
import {
  TRACK_LESSON_TITLE,
  currentModule,
  isModuleComplete,
  moduleDisplayTitle,
  moduleHasStarted,
  trackModulesFrom,
} from "@/lib/learning-track";

function resumeHref(course: CourseDetail) {
  const step: LessonSummary | null = nextModule(course);
  if (!step) return `/dashboard/courses/${course.slug}`;
  return lessonStepHref(course.slug, step.slug, entryStepForLessonType(step.lesson_type));
}

/** Module overview for Creating an AI Agent — status per module. */
export default function ModuleOverviewPage() {
  const { slug } = useParams<{ slug: string }>();
  const setChrome = usePageChrome((s) => s.setChrome);
  const clearChrome = usePageChrome((s) => s.clearChrome);
  const queryClient = useQueryClient();
  // Which module cards are expanded to show their steps. Collapsed by default:
  // the overview's job is the ten-module shape, the dropdown is the detail.
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});

  const { data: allCourses, isLoading } = useQuery({
    queryKey: ["courses"],
    queryFn: async () => {
      const list = await getCourses();
      for (const c of list) {
        queryClient.setQueryData(["course", c.slug], c);
      }
      return list;
    },
  });

  const trackModules = useMemo(
    () => trackModulesFrom(allCourses ?? []),
    [allCourses]
  );

  const active =
    trackModules.find((m) => m.slug === slug) ?? currentModule(trackModules);
  const lessonsHref = active
    ? `/dashboard/courses/${active.slug}`
    : "/dashboard";

  useEffect(() => {
    setChrome({
      title: "Module overview",
      subtitle: TRACK_LESSON_TITLE,
      showAskTutor: false,
      onAskTutor: null,
      headerTabs: null,
      activeTab: null,
      onTabChange: null,
    });
    return () => clearChrome();
  }, [clearChrome, setChrome]);

  if (isLoading && !trackModules.length) {
    return <p className="animate-pulse text-craft-faint">Loading…</p>;
  }

  if (!trackModules.length) {
    return (
      <div className="mx-auto mt-16 max-w-md text-center">
        <p className="text-lg font-semibold text-craft-ink">No modules available yet.</p>
        <Link href="/dashboard" className="btn-primary mt-6">
          Back to dashboard
        </Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-2xl">
      <Reveal>
        <Link
          href={lessonsHref}
          className="text-sm font-semibold text-violet-600 hover:underline dark:text-violet-400"
        >
          ← Back to lesson
        </Link>
      </Reveal>

      <ul className="mt-4 space-y-2">
        {trackModules.map((mod, i) => {
          const done = isModuleComplete(mod);
          const started = moduleHasStarted(mod);
          const activeMod = mod.slug === active?.slug;
          const href = resumeHref(mod);
          const cta = done ? "Review" : started ? "Continue" : "Start";

          const steps = mod.lessons ?? [];
          const isOpen = !!expanded[mod.slug];

          return (
            <Reveal key={mod.slug} delay={Math.min(40 + i * 25, 220)}>
              <li
                className={clsx(
                  "card overflow-hidden p-0",
                  activeMod && "ring-2 ring-violet-500/40",
                  done &&
                    "border-emerald-300/40 bg-emerald-50/30 dark:border-emerald-500/20 dark:bg-emerald-500/5"
                )}
              >
                <div className="flex items-center gap-3 p-4">
                  <span
                    className={clsx(
                      "flex h-9 w-9 shrink-0 items-center justify-center rounded-full",
                      done
                        ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-300"
                        : "bg-craft-soft text-craft-muted"
                    )}
                    aria-label={done ? "Completed" : "Not completed"}
                  >
                    {done ? (
                      <Check className="h-4 w-4" strokeWidth={2.5} />
                    ) : (
                      <Circle className="h-4 w-4" strokeWidth={2} />
                    )}
                  </span>
                  <div className="min-w-0 flex-1">
                    <p className="text-[11px] font-semibold leading-snug text-craft-ink sm:truncate sm:text-sm md:text-base">
                      {moduleDisplayTitle(mod)}
                    </p>
                    <p className="mt-0.5 text-[10px] text-craft-faint sm:text-xs">
                      {mod.completed_lessons}/{mod.total_lessons} steps · {mod.completion_pct}%
                    </p>
                  </div>
                  {href ? (
                    <Link
                      href={href}
                      className="btn-secondary shrink-0 px-2.5 py-1.5 text-xs sm:px-4 sm:py-2 sm:text-sm"
                    >
                      {cta}
                      <ArrowRight className="h-3.5 w-3.5" />
                    </Link>
                  ) : null}
                  {steps.length > 0 && (
                    <button
                      type="button"
                      onClick={() =>
                        setExpanded((prev) => ({ ...prev, [mod.slug]: !prev[mod.slug] }))
                      }
                      aria-expanded={isOpen}
                      aria-label={
                        isOpen
                          ? `Hide ${moduleDisplayTitle(mod)} steps`
                          : `Show ${moduleDisplayTitle(mod)} steps`
                      }
                      className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-craft-muted transition hover:bg-craft-soft hover:text-craft-ink"
                    >
                      <ChevronDown
                        className={clsx("h-4 w-4 transition-transform", isOpen && "rotate-180")}
                      />
                    </button>
                  )}
                </div>

                {/* Every step is open — free pacing, no locks. */}
                {isOpen && steps.length > 0 && (
                  <ul className="border-t border-craft-border bg-craft-soft/40 px-3 py-2">
                    {steps.map((step) => {
                      const stepDone = step.status === "completed";
                      const stepHref = lessonStepHref(
                        mod.slug,
                        step.slug,
                        entryStepForLessonType(step.lesson_type)
                      );
                      return (
                        <li key={step.slug}>
                          <Link
                            href={stepHref}
                            className="flex items-center gap-2.5 rounded-lg px-2 py-2 transition hover:bg-craft-soft"
                          >
                            <span
                              className={clsx(
                                "flex h-6 w-6 shrink-0 items-center justify-center rounded-full",
                                stepDone
                                  ? "text-emerald-600 dark:text-emerald-400"
                                  : "text-craft-muted"
                              )}
                            >
                              {stepDone ? (
                                <Check className="h-3.5 w-3.5" strokeWidth={2.5} />
                              ) : (
                                <Circle className="h-3.5 w-3.5" strokeWidth={2} />
                              )}
                            </span>
                            <span className="min-w-0 flex-1 text-[11px] leading-snug text-craft-ink sm:truncate sm:text-sm">
                              {step.title}
                            </span>
                            <span className="shrink-0 text-[10px] text-craft-faint sm:text-xs">
                              {step.type_label} · {step.estimated_minutes} min
                            </span>
                          </Link>
                        </li>
                      );
                    })}
                  </ul>
                )}
              </li>
            </Reveal>
          );
        })}
      </ul>
    </div>
  );
}
