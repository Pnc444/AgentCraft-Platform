"use client";

import { useMemo } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { CheckCircle2, ChevronLeft, ChevronRight, ClipboardCheck, Sparkles } from "lucide-react";
import clsx from "clsx";
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";
import { ProgressBar } from "@/components/shared/ProgressBar";
import { Reveal } from "@/components/shared/Reveal";
import { completedCheckpointIds, completedInteractionKeys } from "@/lib/lesson-interactions";
import {
  assessmentLabelForLessonType,
  isExamLessonType,
  lessonStepHref,
} from "@/lib/lesson-steps";

export default function LessonProgressPage() {
  const router = useRouter();
  const {
    slug,
    lessonSlug,
    lesson,
    videoUrl,
    needsVideo,
    videoDone,
    setNotice,
    progressPending,
    prev,
    next,
    guidedBlocks,
  } = useLessonWorkspace();

  if (!lesson) return null;

  const isExamLesson = isExamLessonType(lesson.lesson_type);
  const assessmentLabel = assessmentLabelForLessonType(lesson.lesson_type);

  const checkpointBlocks = useMemo(
    () =>
      guidedBlocks
        .map((block, index) => ({
          id: `${lesson.id}:${index}:${block.title}`,
          title: block.title,
          checkpoint_after: !!block.checkpoint_after,
        }))
        .filter((block) => block.checkpoint_after),
    [guidedBlocks, lesson.id]
  );
  const completedIds = useMemo(
    () => completedCheckpointIds(lesson.interaction_log),
    [lesson.interaction_log]
  );
  const tryTasks = useMemo(
    () =>
      guidedBlocks.flatMap((block, blockIndex) =>
        (block.try_this || []).map((task, taskIndex) => ({
          id: `task:${lesson.id}:${blockIndex}:${taskIndex}`,
          label: task,
          blockTitle: block.title,
        }))
      ),
    [guidedBlocks, lesson.id]
  );
  const completedTaskIds = useMemo(
    () => completedInteractionKeys(lesson.interaction_log, "guided_task"),
    [lesson.interaction_log]
  );

  const checkpointPct = checkpointBlocks.length
    ? Math.round((completedIds.size / checkpointBlocks.length) * 100)
    : 0;

  function goToQuiz() {
    if (needsVideo && !videoDone) {
      setNotice("Watch the lesson video all the way through before taking the Recap Quiz.");
      router.push(lessonStepHref(slug, lessonSlug, "video"));
      return;
    }
    setNotice(null);
    router.push(lessonStepHref(slug, lessonSlug, "quiz"));
  }

  return (
    <div className="space-y-4">
      <Reveal variant="up">
        <div className="card card-interactive p-6">
          <h2 className="text-base font-semibold text-craft-ink">Your progress</h2>
          <p className="mt-1 text-sm text-craft-muted">
            {lesson.status === "completed"
              ? `Completed${lesson.score != null ? ` · ${assessmentLabel} ${lesson.score}%` : ""}`
              : needsVideo && !videoDone
                ? `Watch the video, then pass the ${assessmentLabel} (80%+) to finish.`
                : `Pass the ${assessmentLabel} with 80% or higher to complete this lesson.`}
          </p>

          <dl
            className={clsx(
              "mt-5 grid gap-3",
              videoUrl ? "sm:grid-cols-3" : "sm:grid-cols-2"
            )}
          >
            {videoUrl && (
              <div className="rounded-xl bg-craft-soft px-3 py-3 ring-1 ring-craft-border">
                <dt className="text-[11px] font-medium uppercase tracking-wide text-craft-faint">
                  Video
                </dt>
                <dd className="mt-1 text-sm font-semibold text-craft-ink">
                  {!needsVideo
                    ? lesson.video_watched
                      ? "Optional · watched"
                      : "Optional · can skip"
                    : videoDone
                      ? "Watched"
                      : "Not finished"}
                </dd>
              </div>
            )}
            <div className="rounded-xl bg-craft-soft px-3 py-3 ring-1 ring-craft-border">
              <dt className="text-[11px] font-medium uppercase tracking-wide text-craft-faint">
                {assessmentLabel}
              </dt>
              <dd className="mt-1 text-sm font-semibold text-craft-ink">
                {lesson.score != null ? `${lesson.score}%` : "Not taken"}
              </dd>
            </div>
            <div className="rounded-xl bg-craft-soft px-3 py-3 ring-1 ring-craft-border">
              <dt className="text-[11px] font-medium uppercase tracking-wide text-craft-faint">
                Status
              </dt>
              <dd className="mt-1 text-sm font-semibold capitalize text-craft-ink">
                {lesson.status.replace("_", " ")}
              </dd>
            </div>
          </dl>

          {checkpointBlocks.length ? (
            <div className="mt-5 rounded-xl bg-craft-soft px-4 py-4 ring-1 ring-craft-border">
              <div className="flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />
                <p className="text-sm font-semibold text-craft-ink">Learning Momentum</p>
              </div>
              <p className="mt-2 text-sm text-craft-muted">
                Mini checkpoints from the content page are saved on this device so students can feel progress before the final recap quiz.
              </p>
              <div className="mt-3 flex items-center gap-3">
                <ProgressBar value={checkpointPct} className="flex-1" />
                <span className="text-sm font-medium text-craft-ink">
                  {completedIds.size} / {checkpointBlocks.length}
                </span>
              </div>
              <ul className="mt-3 space-y-2 text-sm text-craft-muted">
                {checkpointBlocks.map((block) => {
                  const done = completedIds.has(block.id);
                  return (
                    <li key={block.id} className="flex items-center gap-2">
                      <span
                        className={clsx(
                          "inline-flex h-2.5 w-2.5 rounded-full",
                          done ? "bg-emerald-500" : "bg-craft-faint"
                        )}
                      />
                      <span className={done ? "text-craft-ink" : undefined}>{block.title}</span>
                    </li>
                  );
                })}
              </ul>
            </div>
          ) : null}

          {tryTasks.length ? (
            <div className="mt-5 rounded-xl bg-craft-soft px-4 py-4 ring-1 ring-craft-border">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />
                <p className="text-sm font-semibold text-craft-ink">Hands-on Tasks</p>
              </div>
              <p className="mt-2 text-sm text-craft-muted">
                These are the action steps you completed from the content page. They now travel with lesson progress instead of living only in browser storage.
              </p>
              <div className="mt-3 flex items-center gap-3">
                <ProgressBar
                  value={tryTasks.length ? Math.round((completedTaskIds.size / tryTasks.length) * 100) : 0}
                  className="flex-1"
                />
                <span className="text-sm font-medium text-craft-ink">
                  {completedTaskIds.size} / {tryTasks.length}
                </span>
              </div>
              <ul className="mt-3 space-y-2 text-sm text-craft-muted">
                {tryTasks.map((task) => {
                  const done = completedTaskIds.has(task.id);
                  return (
                    <li key={task.id} className="flex items-start gap-2">
                      <span
                        className={clsx(
                          "mt-1 inline-flex h-2.5 w-2.5 rounded-full",
                          done ? "bg-emerald-500" : "bg-craft-faint"
                        )}
                      />
                      <span>
                        <span className={done ? "text-craft-ink" : undefined}>{task.label}</span>
                        <span className="block text-xs text-craft-faint">{task.blockTitle}</span>
                      </span>
                    </li>
                  );
                })}
              </ul>
            </div>
          ) : null}

          <div className="mt-5 flex flex-wrap gap-3">
            {lesson.status !== "completed" && (
              <button
                type="button"
                disabled={progressPending}
                onClick={goToQuiz}
                className="btn-primary"
              >
                <ClipboardCheck className="h-4 w-4" />
                {`Take ${assessmentLabel}`}
              </button>
            )}
            {lesson.status === "completed" && (
              <>
                <span className="inline-flex items-center gap-2 rounded-full bg-teal-600 px-3 py-2 text-sm font-medium text-white shadow-soft dark:bg-teal-500 dark:text-teal-950">
                  <CheckCircle2 className="h-4 w-4" />
                  Lesson complete
                </span>
                <Link href={lessonStepHref(slug, lessonSlug, "quiz")} className="btn-secondary">
                  {`Review ${assessmentLabel}`}
                </Link>
              </>
            )}
            {!isExamLesson && (
              <Link href={lessonStepHref(slug, lessonSlug, "content")} className="btn-secondary">
                Review content
              </Link>
            )}
            {videoUrl && (
              <Link href={lessonStepHref(slug, lessonSlug, "video")} className="btn-secondary">
                {lesson.video_watched
                  ? "Review video"
                  : needsVideo
                    ? "Watch video"
                    : "Watch video (optional)"}
              </Link>
            )}
          </div>
        </div>
      </Reveal>

      <Reveal delay={100}>
        <nav className="flex items-center justify-between gap-4 pt-2">
          {prev ? (
            <Link href={lessonStepHref(slug, prev.slug, "content")} className="btn-secondary">
              <ChevronLeft className="h-4 w-4" />
              {prev.title}
            </Link>
          ) : (
            <span />
          )}
          {next ? (
            <Link href={lessonStepHref(slug, next.slug, "content")} className="btn-secondary">
              {next.title}
              <ChevronRight className="h-4 w-4" />
            </Link>
          ) : (
            <span />
          )}
        </nav>
      </Reveal>
    </div>
  );
}
