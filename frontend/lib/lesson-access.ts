import type { LessonSummary } from "@/types";

/**
 * Which steps inside a module a learner may open.
 *
 * Free pacing: every step is reachable. Module and step locks were removed so
 * learners can skip ahead, review, or jump via the studio module bar.
 */

/** Index of the first not-completed step; -1 when the module is fully done. */
export function frontierIndex(lessons: LessonSummary[]): number {
  return lessons.findIndex((lesson) => lesson.status !== "completed");
}

export function isLessonReachable(
  _lessons: LessonSummary[],
  _index: number,
  _moduleUnlocked: boolean,
  _bypass = false
): boolean {
  return true;
}
