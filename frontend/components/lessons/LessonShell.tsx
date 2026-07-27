"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Bot, Timer } from "lucide-react";
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
  if (!lesson)
    return (
      // Never a dead end (audit F2).
      <div className="mx-auto mt-16 max-w-md text-center">
        <p className="text-lg font-semibold text-craft-ink">That lesson doesn&apos;t exist.</p>
        <p className="mt-2 text-sm text-craft-muted">
          It may have moved when the course was updated. Everything current is on the dashboard.
        </p>
        <Link href="/dashboard" className="btn-primary mt-6">
          Back to my courses
        </Link>
      </div>
    );

  return (
    /*
      Centred inside the content column, not the viewport. The old
      clamp(50vw - 36rem - sidebar) shifted the card left to centre it against
      the whole window, which with a 272px sidebar left visibly uneven gutters
      (416px left / 352px right at 1920). Plain mx-auto is symmetric and
      predictable, and the rem-based cap grows with the fluid root size.

      max-w-4xl rather than 6xl: a 1224px card around a 714px column left 255px
      of dead gutter inside the card on each side. The frame should track the
      content it frames.
    */
    <div className="mx-auto flex min-h-0 w-full max-w-4xl flex-1 flex-col">
      <Reveal className="shrink-0">
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
              {/* No step chip: the player shows "beat 3 / 8" and the
                  assessment shows "2 / 5". One position signal per screen
                  (audit B1/B2). */}
            </p>

            <h1 className="lesson-shell-title mt-3 text-3xl font-bold tracking-tight text-craft-ink">
              {lesson.title}
            </h1>
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

      {/* justify-center so that when a step caps its own height, the leftover
          space splits above and below it rather than all pooling underneath. */}
      <div className="lesson-shell-body mt-4 flex min-h-0 flex-1 flex-col justify-center sm:mt-6">
        {children}
      </div>
    </div>
  );
}
