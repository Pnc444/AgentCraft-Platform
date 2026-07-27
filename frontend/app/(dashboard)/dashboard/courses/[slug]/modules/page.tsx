"use client";

import Link from "next/link";
import { useEffect, useMemo } from "react";
import { useParams } from "next/navigation";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { ArrowRight, Check, Circle, Lock } from "lucide-react";
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

/** Module is unlocked if it's the first, or the previous module is complete. */
function isModuleUnlocked(modules: CourseDetail[], index: number) {
  if (index <= 0) return true;
  return isModuleComplete(modules[index - 1]);
}

/** Module overview for Creating an AI Agent — status per module. */
export default function ModuleOverviewPage() {
  const { slug } = useParams<{ slug: string }>();
  const setChrome = usePageChrome((s) => s.setChrome);
  const clearChrome = usePageChrome((s) => s.clearChrome);
  const queryClient = useQueryClient();

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
          const unlocked = isModuleUnlocked(trackModules, i);
          const started = moduleHasStarted(mod);
          const activeMod = mod.slug === active?.slug;
          const href = unlocked ? resumeHref(mod) : undefined;
          const cta = done ? "Review" : started ? "Continue" : "Start";

          return (
            <Reveal key={mod.slug} delay={Math.min(40 + i * 25, 220)}>
              <li
                className={clsx(
                  "card flex items-center gap-3 p-4",
                  activeMod && unlocked && "ring-2 ring-violet-500/40",
                  done &&
                    "border-emerald-300/40 bg-emerald-50/30 dark:border-emerald-500/20 dark:bg-emerald-500/5",
                  !unlocked && "opacity-70"
                )}
              >
                <span
                  className={clsx(
                    "flex h-9 w-9 shrink-0 items-center justify-center rounded-full",
                    done
                      ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-300"
                      : unlocked
                        ? "bg-craft-soft text-craft-muted"
                        : "bg-craft-soft text-craft-faint"
                  )}
                  aria-label={
                    done ? "Completed" : unlocked ? "Not completed" : "Locked"
                  }
                >
                  {done ? (
                    <Check className="h-4 w-4" strokeWidth={2.5} />
                  ) : unlocked ? (
                    <Circle className="h-4 w-4" strokeWidth={2} />
                  ) : (
                    <Lock className="h-4 w-4" />
                  )}
                </span>
                <div className="min-w-0 flex-1">
                  <p className="truncate font-semibold text-craft-ink">
                    {moduleDisplayTitle(mod)}
                  </p>
                  <p className="mt-0.5 text-xs text-craft-faint">
                    {mod.completed_lessons}/{mod.total_lessons} steps
                    {unlocked ? ` · ${mod.completion_pct}%` : " · Locked"}
                  </p>
                </div>
                {href ? (
                  <Link href={href} className="btn-secondary shrink-0 px-4 py-2">
                    {cta}
                    <ArrowRight className="h-3.5 w-3.5" />
                  </Link>
                ) : null}
              </li>
            </Reveal>
          );
        })}
      </ul>
    </div>
  );
}
