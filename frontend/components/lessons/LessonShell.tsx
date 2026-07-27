"use client";

import Link from "next/link";
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";
import { LessonStudioLayout } from "@/components/lessons/LessonStudioLayout";

/**
 * Lesson page frame — studio chrome around the player.
 * Fills the shell viewport; the player owns in-card scrolling.
 */
export function LessonShell({ children }: { children: React.ReactNode }) {
  const { lesson, isLoading, notice } = useLessonWorkspace();

  if (isLoading) {
    return <p className="animate-pulse text-craft-faint">Loading lesson…</p>;
  }
  if (!lesson) {
    return (
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
  }

  return (
    <LessonStudioLayout>
      {notice ? (
        <div className="mb-2 shrink-0 rounded-xl border border-amber-500/30 bg-amber-50 px-3 py-2 text-sm text-amber-800 dark:bg-amber-500/10 dark:text-amber-200">
          {notice}
        </div>
      ) : null}
      <div className="min-h-0 flex-1">{children}</div>
    </LessonStudioLayout>
  );
}
