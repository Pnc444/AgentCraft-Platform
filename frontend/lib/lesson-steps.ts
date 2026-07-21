import type { CheckpointQuestion } from "@/components/lessons/CheckpointQuiz";
import type {
  CapstoneAssignment,
  GuidedLessonBlock,
  LessonArtifact,
  LessonType,
  LessonStatus,
} from "@/types";

export const LESSON_STATUS_UI = {
  completed: { text: "Completed", pct: 100 },
  in_progress: { text: "In progress", pct: 50 },
  not_started: { text: "Not started", pct: 0 },
  stuck: { text: "Needs help", pct: 50 },
} as const;

export type LessonStatusKey = keyof typeof LESSON_STATUS_UI;

export type LessonStep = "content" | "video" | "quiz" | "progress";

function isQuestion(value: unknown): value is CheckpointQuestion {
  return (
    !!value &&
    typeof value === "object" &&
    typeof (value as CheckpointQuestion).prompt === "string" &&
    Array.isArray((value as CheckpointQuestion).options)
  );
}

export function getRecapQuestions(config: Record<string, unknown>): CheckpointQuestion[] {
  const raw = config?.questions;
  if (!Array.isArray(raw)) return [];
  return raw.filter(isQuestion);
}

export function getCheckpointQuestions(config: Record<string, unknown>): CheckpointQuestion[] {
  const raw = config?.checkpoint_questions;
  if (!Array.isArray(raw)) return [];
  return raw.filter(isQuestion);
}

export function getGuidedLessonBlocks(config: Record<string, unknown>): GuidedLessonBlock[] {
  const raw = config?.guided_blocks;
  if (!Array.isArray(raw)) return [];
  return raw.filter(
    (block): block is GuidedLessonBlock =>
      !!block &&
      typeof block === "object" &&
      typeof (block as GuidedLessonBlock).title === "string" &&
      typeof (block as GuidedLessonBlock).body === "string"
  );
}

export function getLessonArtifacts(config: Record<string, unknown>): LessonArtifact[] {
  const raw = config?.artifact_bundle;
  if (!Array.isArray(raw)) return [];
  return raw.filter(
    (artifact): artifact is LessonArtifact =>
      !!artifact &&
      typeof artifact === "object" &&
      typeof (artifact as LessonArtifact).path === "string" &&
      typeof (artifact as LessonArtifact).summary === "string"
  );
}

export function getCapstoneAssignment(config: Record<string, unknown>): CapstoneAssignment | null {
  const raw = config?.capstone_assignment;
  if (!raw || typeof raw !== "object") return null;
  const assignment = raw as CapstoneAssignment;
  if (!assignment.title || !assignment.summary || !Array.isArray(assignment.sections)) return null;
  if (!Array.isArray(assignment.review_questions)) return null;
  return assignment;
}

export function lessonStepHref(
  courseSlug: string,
  lessonSlug: string,
  step: LessonStep = "content"
) {
  return `/dashboard/courses/${courseSlug}/lessons/${lessonSlug}/${step}`;
}

/** First step a lesson should open on when launched from course/dashboard navigation. */
export function entryStepForLessonType(lessonType: LessonType | string): LessonStep {
  return lessonType === "quiz" ? "quiz" : "content";
}

export function isExamLessonType(lessonType: LessonType | string): boolean {
  return lessonType === "quiz";
}

export function assessmentLabelForLessonType(lessonType: LessonType | string): string {
  return isExamLessonType(lessonType) ? "Exam" : "Recap Quiz";
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
