"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Bot, Timer } from "lucide-react";
import { isExamLessonType, lessonStepPosition } from "@/lib/lesson-steps";
import { Reveal } from "@/components/shared/Reveal";
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";

/**
 * Lesson page frame.
 *
 * There is deliberately no step-tab strip here. Tabs let a learner jump between
 * Content / Video / Quiz / Progress in any direction, which combined with the
 * per-page prev/next buttons formed a navigation loop — four primary
 * destinations for what is often a single video. Movement is now linear and
 * driven by the call-to-action at the end of each step; this header carries
 * orientation ("Step 2 of 3") but is not navigation.
 */
export function LessonShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { lesson, isLoading, notice, openTutor } = useLessonWorkspace();

  if (isLoading) return <p className="animate-pulse text-craft-faint">Loading lesson…</p>;
  if (!lesson) return <p className="text-craft-muted">Lesson not found.</p>;

  const step = lessonStepPosition(pathname, {
    isExam: isExamLessonType(lesson.lesson_type),
  });

  return (
    <div className="mx-auto w-full max-w-6xl lg:ml-[clamp(0px,calc(50vw-36rem-var(--sidebar-w,18rem)),calc(100%-72rem))] lg:mr-0">
      <Reveal>
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="min-w-0 flex-1">
            <p className="flex flex-wrap items-center gap-x-2 gap-y-1 text-sm text-craft-muted">
              <Link
                href={`/dashboard/courses/${lesson.course_slug}`}
                className="font-medium text-cyan-600 hover:underline dark:text-cyan-400"
              >
                {lesson.course_title}
              </Link>
              <span aria-hidden className="text-craft-faint">
                ·
              </span>
              <span className="inline-flex items-center gap-1">
                <Timer className="h-3.5 w-3.5" />
                {lesson.estimated_minutes} min
              </span>
              <span aria-hidden className="text-craft-faint">
                ·
              </span>
              <span>
                {step.label} · step {step.current} of {step.total}
              </span>
            </p>

            <h1 className="mt-3 text-3xl font-bold tracking-tight text-craft-ink">{lesson.title}</h1>
          </div>

          <button
            type="button"
            onClick={openTutor}
            className="inline-flex items-center gap-2 rounded-full border border-craft-border bg-craft-surface/70 px-3 py-1.5 text-xs font-medium text-craft-muted transition hover:border-craft-faint hover:bg-craft-soft hover:text-craft-ink"
          >
            <Bot className="h-3.5 w-3.5" />
            Ask tutor
          </button>
        </div>
      </Reveal>

      {notice && (
        <div className="mt-4 rounded-xl border border-amber-500/30 bg-amber-50 px-4 py-3 text-sm text-amber-800 dark:bg-amber-500/10 dark:text-amber-200">
          {notice}
        </div>
      )}

      <div className="mt-6">{children}</div>
    </div>
  );
}
