import type { CheckpointQuestion } from "@/components/lessons/CheckpointQuiz";
import type { LessonStatus } from "@/types";

export const LESSON_STATUS_UI = {
  completed: { text: "Completed", pct: 100 },
  in_progress: { text: "In progress", pct: 50 },
  not_started: { text: "Not started", pct: 0 },
  stuck: { text: "Needs help", pct: 50 },
} as const;

export type LessonStatusKey = keyof typeof LESSON_STATUS_UI;

export type LessonStep = "content" | "video" | "quiz" | "progress";

export function getCheckpointQuestions(config: Record<string, unknown>): CheckpointQuestion[] {
  const raw = config?.questions;
  if (!Array.isArray(raw)) return [];
  return raw.filter(
    (q): q is CheckpointQuestion =>
      !!q &&
      typeof q === "object" &&
      typeof (q as CheckpointQuestion).prompt === "string" &&
      Array.isArray((q as CheckpointQuestion).options)
  );
}

export function lessonStepHref(
  courseSlug: string,
  lessonSlug: string,
  step: LessonStep = "content"
) {
  return `/dashboard/courses/${courseSlug}/lessons/${lessonSlug}/${step}`;
}

/** Coarse status label — prefer `lessonStepProgress` in the lesson shell. */
export function statusUiFor(status: LessonStatus | string) {
  return LESSON_STATUS_UI[status as LessonStatusKey] ?? LESSON_STATUS_UI.not_started;
}

/** Next step after Content — Video when present, otherwise Recap Quiz. */
export function stepAfterContent(hasVideo: boolean): LessonStep {
  return hasVideo ? "video" : "quiz";
}

type StepProgressInput = {
  status: LessonStatus | string;
  score: number | null;
  video_watched: boolean;
};

/**
 * Progress from required lesson steps:
 * Content (opened) → Video (if require_full_watch) → Recap Quiz (≥80%).
 */
export function lessonStepProgress(
  lesson: StepProgressInput,
  opts: { needsVideo: boolean }
): { text: string; pct: number; done: number; total: number } {
  const quizPassed =
    lesson.status === "completed" ||
    (lesson.score != null && lesson.score >= 80);

  const total = opts.needsVideo ? 3 : 2;

  if (lesson.status === "not_started") {
    return { text: "Not started", pct: 0, done: 0, total };
  }

  if (lesson.status === "completed" || quizPassed) {
    return { text: "Completed", pct: 100, done: total, total };
  }

  const contentDone = true; // opened → in_progress / stuck
  const videoDone = !opts.needsVideo || lesson.video_watched;
  const doneCount =
    (contentDone ? 1 : 0) +
    (opts.needsVideo && lesson.video_watched ? 1 : 0) +
    (quizPassed ? 1 : 0);
  const pct = Math.round((doneCount / total) * 100);

  if (lesson.status === "stuck") {
    return { text: "Needs help", pct, done: doneCount, total };
  }

  let text = `${doneCount} of ${total} steps`;
  if (opts.needsVideo && !videoDone) text = "Watch video";
  else if (!quizPassed) text = "Take quiz";

  return { text, pct, done: doneCount, total };
}
