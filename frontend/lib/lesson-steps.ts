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

export function statusUiFor(status: LessonStatus | string) {
  return LESSON_STATUS_UI[status as LessonStatusKey] ?? LESSON_STATUS_UI.not_started;
}

/** Next step after Content — Video when present, otherwise Recap Quiz. */
export function stepAfterContent(hasVideo: boolean): LessonStep {
  return hasVideo ? "video" : "quiz";
}
