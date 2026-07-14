"use client";

import Link from "next/link";
import { Timer } from "lucide-react";
import { Reveal } from "@/components/shared/Reveal";
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";

/**
 * Lesson page frame. Width is centered against the VIEWPORT, not the main
 * column, by shifting left to compensate for the sidebar (--sidebar-w is set
 * by the Sidebar component). Falls back to normal centering on small screens.
 */
export function LessonShell({ children }: { children: React.ReactNode }) {
  const { lesson, isLoading, notice } = useLessonWorkspace();

  if (isLoading) return <p className="animate-pulse text-craft-faint">Loading lesson…</p>;
  if (!lesson) return <p className="text-craft-muted">Lesson not found.</p>;

  return (
    <div className="mx-auto w-full max-w-6xl lg:ml-[clamp(0px,calc(50vw-36rem-var(--sidebar-w,18rem)),calc(100%-72rem))] lg:mr-0">
      <Reveal>
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
          <span className="capitalize">{lesson.lesson_type.replace("_", " ")}</span>
        </p>

        <h1 className="mt-3 text-3xl font-bold tracking-tight text-craft-ink">{lesson.title}</h1>
      </Reveal>

      {notice && (
        <div className="mt-4 rounded-xl border border-amber-500/30 bg-amber-50 px-4 py-3 text-sm text-amber-800 dark:bg-amber-500/10 dark:text-amber-200">
          {notice}
        </div>
      )}

      <div className="mt-8 rounded-2xl border border-craft-border bg-craft-surface/70 p-6 shadow-soft sm:p-8 lg:p-10">
        {children}
      </div>
    </div>
  );
}
