"use client";

import Link from "next/link";
import { ArrowRight, Sparkles } from "lucide-react";
import type { CourseDetail, LessonSummary } from "@/types";
import { entryStepForLessonType, lessonStepHref } from "@/lib/lesson-steps";
import {
  TRACK_LESSON_BLURB,
  TRACK_LESSON_TITLE,
  currentModule,
  formatModuleProgress,
  isModuleComplete,
  lessonProgressPct,
  moduleDisplayTitle,
  moduleHasStarted,
  modulesCompletedCount,
} from "@/lib/learning-track";
import { DifficultyBadge } from "@/components/dashboard/DifficultyBadge";
import { ProgressRing } from "@/components/shared/ProgressRing";

function nextStep(course: CourseDetail): LessonSummary | null {
  return (
    course.lessons.find((l) => l.status === "in_progress") ??
    course.lessons.find((l) => l.status === "not_started") ??
    null
  );
}

interface LessonFeatureCardProps {
  /** Active / resume module (API course). */
  course: CourseDetail;
  /** All modules in Creating an AI Agent. Defaults to [course]. */
  trackModules?: CourseDetail[];
  description?: string;
  onWarm?: () => void;
  className?: string;
  /** When false, hide the progress panel in the top-right. */
  showProgress?: boolean;
  /** Optional link to module overview (shown left of Start/Continue). */
  overviewHref?: string;
}

/**
 * Lesson card for “Creating an AI Agent” with the active module.
 * Start/Continue opens the next incomplete step inside that module.
 */
export function LessonFeatureCard({
  course,
  trackModules,
  description,
  onWarm,
  className,
  showProgress = true,
  overviewHref,
}: LessonFeatureCardProps) {
  const modules = trackModules?.length ? trackModules : [course];
  const active = currentModule(modules) ?? course;
  const resumeTarget = nextStep(active);
  const hasStarted = modules.some(moduleHasStarted);
  const showStart = !hasStarted;
  const completed = modulesCompletedCount(modules);
  const total = modules.length;
  const pct = lessonProgressPct(modules);
  const inProgressMod =
    modules.find((m) => moduleHasStarted(m) && !isModuleComplete(m)) ?? null;

  const ctaHref = resumeTarget
    ? lessonStepHref(
        active.slug,
        resumeTarget.slug,
        entryStepForLessonType(resumeTarget.lesson_type)
      )
    : null;

  const blurb = description ?? TRACK_LESSON_BLURB;

  return (
    <article className={className ?? "card overflow-hidden p-0"}>
      {/* Mobile: short frosted header. sm+: side accent strip. */}
      <div className="flex flex-col sm:flex-row">
        <div
          className="relative flex h-10 shrink-0 items-center justify-center overflow-hidden bg-gradient-to-br from-[#1e1233] via-[#2e1f4a] to-violet-700 sm:h-auto sm:w-40 sm:bg-gradient-to-b lg:w-48"
          aria-hidden
        >
          <div className="pointer-events-none absolute -right-4 -top-6 h-16 w-16 rounded-full bg-violet-400/25 blur-2xl sm:hidden" />
          <div className="pointer-events-none absolute -bottom-6 left-4 h-12 w-12 rounded-full bg-fuchsia-400/20 blur-2xl sm:hidden" />
          <div className="relative flex h-7 w-7 items-center justify-center rounded-xl border border-white/20 bg-white/10 shadow-soft backdrop-blur-sm sm:h-auto sm:w-auto sm:rounded-none sm:border-0 sm:bg-transparent sm:shadow-none sm:backdrop-blur-none">
            <Sparkles className="h-3.5 w-3.5 text-violet-100 sm:h-12 sm:w-12 sm:text-violet-200/85" />
          </div>
        </div>

        <div className="flex min-w-0 flex-1 flex-col justify-between gap-2 bg-gradient-to-b from-violet-50/50 to-transparent p-3 dark:from-violet-950/20 sm:gap-4 sm:bg-none sm:p-6 sm:dark:from-transparent">
          <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between sm:gap-6">
            <div className="min-w-0 flex-1">
              <div className="flex items-start justify-between gap-2">
                <div className="min-w-0">
                  <p className="text-[9px] font-semibold uppercase tracking-[0.16em] text-violet-500/80 dark:text-violet-300/70 sm:text-[11px] sm:tracking-[0.14em] sm:text-craft-faint sm:dark:text-craft-faint">
                    Lesson
                  </p>
                  <h2 className="mt-0.5 text-sm font-bold leading-snug tracking-tight text-craft-ink sm:mt-1 sm:text-2xl">
                    {TRACK_LESSON_TITLE}
                  </h2>
                </div>
                {showProgress ? (
                  <ProgressRing
                    value={pct}
                    size={40}
                    stroke={4}
                    className="shrink-0 sm:hidden"
                    sublabel="done"
                  />
                ) : null}
              </div>

              <div className="mt-1.5 flex flex-wrap items-center gap-1 sm:mt-2 sm:gap-2">
                <span className="inline-flex max-w-full items-center rounded-full border border-craft-border/80 bg-craft-surface/80 px-2 py-0.5 text-[10px] font-medium text-craft-ink shadow-soft sm:rounded-none sm:border-0 sm:bg-transparent sm:px-0 sm:py-0 sm:text-sm sm:shadow-none">
                  <span className="truncate">
                    <span className="text-craft-faint sm:text-craft-ink">Module · </span>
                    {moduleDisplayTitle(active)}
                  </span>
                </span>
                <DifficultyBadge difficulty={active.difficulty} />
              </div>

              <p className="mt-1.5 hidden text-sm leading-relaxed text-craft-muted sm:mt-1.5 sm:line-clamp-3 sm:block">
                {blurb}
              </p>
            </div>

            {showProgress ? (
              <div className="hidden shrink-0 items-center gap-4 self-start sm:flex">
                <ProgressRing
                  value={pct}
                  size={72}
                  stroke={7}
                  className="shrink-0"
                  sublabel="Lesson"
                />
                <ul className="min-w-0 space-y-1.5 text-sm text-craft-muted">
                  <li className="flex items-start gap-2">
                    <span className="mt-1.5 h-2 w-2 shrink-0 rounded-full bg-emerald-500" />
                    <span>
                      Completed{" "}
                      <span className="font-medium text-craft-ink">
                        {formatModuleProgress(completed, total)}
                      </span>
                    </span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="mt-1.5 h-2 w-2 shrink-0 rounded-full bg-violet-500" />
                    <span>
                      In Progress{" "}
                      <span className="font-medium text-craft-ink">
                        {inProgressMod ? moduleDisplayTitle(inProgressMod) : "—"}
                      </span>
                    </span>
                  </li>
                </ul>
              </div>
            ) : null}
          </div>

          {showProgress ? (
            <div className="flex flex-wrap gap-1 sm:hidden">
              <span className="inline-flex items-center gap-1 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-2 py-0.5 text-[10px] font-medium text-emerald-700 dark:text-emerald-300">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                Done {formatModuleProgress(completed, total)}
              </span>
              <span className="inline-flex max-w-full items-center gap-1 rounded-full border border-violet-500/20 bg-violet-500/10 px-2 py-0.5 text-[10px] font-medium text-violet-700 dark:text-violet-300">
                <span className="h-1.5 w-1.5 shrink-0 rounded-full bg-violet-500" />
                <span className="truncate">
                  Now {inProgressMod ? moduleDisplayTitle(inProgressMod) : "—"}
                </span>
              </span>
            </div>
          ) : null}

          <div className="flex flex-wrap items-center justify-between gap-2 border-t border-craft-border/60 pt-2 sm:gap-3 sm:border-0 sm:pt-0">
            {!showProgress ? (
              <p className="text-[10px] text-craft-muted sm:text-sm">
                {formatModuleProgress(completed, total)}
                {inProgressMod
                  ? ` · Current: ${moduleDisplayTitle(inProgressMod)}`
                  : null}
              </p>
            ) : (
              <span className="hidden sm:block" />
            )}
            <div className="ml-auto flex w-full items-center gap-2 sm:w-auto sm:flex-wrap">
              {overviewHref ? (
                <Link
                  href={overviewHref}
                  className="btn-secondary min-h-[36px] flex-1 rounded-2xl px-3 text-xs sm:min-h-[44px] sm:flex-none sm:rounded-xl sm:px-4 sm:text-sm"
                >
                  <span className="sm:hidden">Overview</span>
                  <span className="hidden sm:inline">Module overview</span>
                </Link>
              ) : null}
              {ctaHref ? (
                <Link
                  href={ctaHref}
                  className="btn-primary min-h-[36px] flex-1 rounded-2xl px-3 text-xs sm:min-h-[44px] sm:flex-none sm:rounded-xl sm:px-5 sm:text-sm"
                  onMouseEnter={() => onWarm?.()}
                  onFocus={() => onWarm?.()}
                  onTouchStart={() => onWarm?.()}
                >
                  {showStart ? (
                    <>
                      <span className="sm:hidden">Start</span>
                      <span className="hidden sm:inline">Start Lesson</span>
                    </>
                  ) : (
                    "Continue"
                  )}
                  <ArrowRight className="h-3.5 w-3.5 sm:h-4 sm:w-4" />
                </Link>
              ) : (
                <p className="text-xs font-medium text-emerald-600 dark:text-emerald-400 sm:text-sm">
                  Lesson complete
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </article>
  );
}

export { moduleHasStarted as courseHasStarted, nextStep as nextModule };
