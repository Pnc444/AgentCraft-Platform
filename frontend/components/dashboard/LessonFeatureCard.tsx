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
      <div className="flex flex-col sm:flex-row">
        <div
          className="flex min-h-[9rem] items-center justify-center bg-gradient-to-br from-[#1e1233] via-[#2e1f4a] to-violet-700 sm:min-h-0 sm:w-44 sm:shrink-0 lg:w-52"
          aria-hidden
        >
          <Sparkles className="h-14 w-14 text-violet-200/85" />
        </div>

        <div className="flex min-w-0 flex-1 flex-col justify-between gap-4 p-5 sm:p-6">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between sm:gap-6">
            <div className="min-w-0 flex-1">
              <p className="text-[11px] font-semibold uppercase tracking-[0.14em] text-craft-faint">
                Lesson
              </p>
              <div className="mt-1 flex flex-wrap items-center gap-2">
                <h2 className="text-xl font-bold text-craft-ink sm:text-2xl">
                  {TRACK_LESSON_TITLE}
                </h2>
              </div>
              <p className="mt-2 flex flex-wrap items-center gap-2 text-sm font-medium text-craft-ink">
                <span>Module · {moduleDisplayTitle(active)}</span>
                <DifficultyBadge difficulty={active.difficulty} />
              </p>
              <p className="mt-1.5 line-clamp-3 text-sm leading-relaxed text-craft-muted">
                {blurb}
              </p>
            </div>

            {showProgress ? (
              <div className="flex shrink-0 items-center gap-3 self-start sm:gap-4">
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

          <div className="flex flex-wrap items-center justify-between gap-3">
            {!showProgress ? (
              <p className="text-sm text-craft-muted">
                {formatModuleProgress(completed, total)}
                {inProgressMod
                  ? ` · Current: ${moduleDisplayTitle(inProgressMod)}`
                  : null}
              </p>
            ) : (
              <span className="hidden sm:block" />
            )}
            <div className="ml-auto flex flex-wrap items-center gap-2">
              {overviewHref ? (
                <Link href={overviewHref} className="btn-secondary min-h-[44px] px-4">
                  Module overview
                </Link>
              ) : null}
              {ctaHref ? (
                <Link
                  href={ctaHref}
                  className="btn-primary min-h-[44px] px-5"
                  onMouseEnter={() => onWarm?.()}
                  onFocus={() => onWarm?.()}
                  onTouchStart={() => onWarm?.()}
                >
                  {showStart ? "Start Lesson" : "Continue"}
                  <ArrowRight className="h-4 w-4" />
                </Link>
              ) : (
                <p className="text-sm font-medium text-emerald-600 dark:text-emerald-400">
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
