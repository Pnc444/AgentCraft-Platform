import type { LessonSummary } from "@/types";

/**
 * Which steps inside a module a learner may open.
 *
 * The rule mirrors what the resume button already does (LessonFeatureCard's
 * nextStep): a learner's frontier is the first step that isn't completed.
 * Everything at or before the frontier is theirs to open — completed steps
 * for review, the frontier itself to continue. Steps past it are visible but
 * locked, the same honesty the module list uses: you can see where you're
 * going, you just can't skip to it.
 */

/** Index of the first not-completed step; -1 when the module is fully done. */
export function frontierIndex(lessons: LessonSummary[]): number {
  return lessons.findIndex((lesson) => lesson.status !== "completed");
}

export function isLessonReachable(
  lessons: LessonSummary[],
  index: number,
  moduleUnlocked: boolean,
  bypass = false
): boolean {
  if (bypass) return true;
  if (!moduleUnlocked) return false;
  const frontier = frontierIndex(lessons);
  return frontier === -1 || index <= frontier;
}
