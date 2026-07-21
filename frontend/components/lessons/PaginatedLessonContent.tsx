"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import clsx from "clsx";
import {
  AlertTriangle,
  BookOpen,
  ChevronLeft,
  ChevronRight,
  ClipboardCheck,
  CheckCircle2,
  FileText,
  GraduationCap,
  Lightbulb,
  Sparkles,
  Wrench,
} from "lucide-react";
import { CheckpointQuiz } from "@/components/lessons/CheckpointQuiz";
import type { CheckpointQuestion } from "@/components/lessons/CheckpointQuiz";
import { LessonArtifactPack } from "@/components/lessons/LessonArtifactPack";
import { LessonCapstoneStudio } from "@/components/lessons/LessonCapstoneStudio";
import { LessonContent } from "@/components/lessons/LessonContent";
import { OpenClawFileExplorer } from "@/components/lessons/OpenClawFileExplorer";
import { lessonStepHref, stepAfterContent } from "@/lib/lesson-steps";
import type { CapstoneAssignment, LessonArtifact, LessonDetail } from "@/types";

type BlockLayout = {
  title: string;
  body: string;
  analogy?: string;
  try_this?: string[];
  remember?: string;
  checkpoint_after?: boolean;
  checkpoint_questions?: CheckpointQuestion[];
  kind?: string | null;
  predict_first?: { question: string; hint?: string };
  inlineArtifacts: LessonArtifact[];
  inlineCapstoneStudio: boolean;
  inlineFileExplorer: boolean;
};

type CheckpointBlock = {
  id: string;
  title: string;
  checkpoint_after: boolean;
  questions: CheckpointQuestion[];
};

interface Props {
  lesson: LessonDetail;
  slug: string;
  lessonSlug: string;
  videoUrl: string;
  blockLayouts: BlockLayout[];
  checkpointBlocks: CheckpointBlock[];
  checkpointPct: number;
  optimisticCheckpointIds: string[];
  capstoneAssignment: CapstoneAssignment | null;
  hasInlineCapstoneStudio: boolean;
  remainingArtifacts: LessonArtifact[];
  checkpointQuestions: CheckpointQuestion[];
  completedCheckpointSet: Set<string>;
  completedTaskSet: Set<string>;
  revealedPredictFirstSet: Set<string>;
  revealPredictFirst: (id: string) => void;
  markCheckpointComplete: (id: string) => void;
  reopenCheckpoint: (id: string) => void;
  toggleGuidedTask: (id: string, blockTitle: string, task: string, done: boolean) => void;
  recordArtifactInteraction: (event: { type: string; key: string; status?: string; details?: Record<string, unknown> }) => void;
}

function inferBlockKind(title: string) {
  const normalized = title.trim().toLowerCase();
  if (normalized === "common mistake") return "common_mistake";
  if (normalized === "teach it back") return "teach_it_back";
  return null;
}

function getAdaptiveCheckpointQuestions(
  questions: CheckpointQuestion[],
  index: number,
  title: string
) {
  if (!questions.length) return [];
  if (questions.length <= 3) return questions;
  const titleSeed = Array.from(title).reduce((sum, char) => sum + char.charCodeAt(0), 0);
  const start = (index + titleSeed) % questions.length;
  return Array.from({ length: 3 }, (_, offset) => questions[(start + offset) % questions.length]).filter(Boolean);
}

// Wraps the lesson block content + optional checkpoint for one slide
function BlockSlide({
  block,
  blockIndex,
  lesson,
  completedCheckpointSet,
  completedTaskSet,
  revealedPredictFirstSet,
  checkpointQuestions,
  capstoneAssignment,
  revealPredictFirst,
  markCheckpointComplete,
  reopenCheckpoint,
  toggleGuidedTask,
  recordArtifactInteraction,
}: {
  block: BlockLayout;
  blockIndex: number;
  lesson: LessonDetail;
  completedCheckpointSet: Set<string>;
  completedTaskSet: Set<string>;
  revealedPredictFirstSet: Set<string>;
  checkpointQuestions: CheckpointQuestion[];
  capstoneAssignment: CapstoneAssignment | null;
  revealPredictFirst: (id: string) => void;
  markCheckpointComplete: (id: string) => void;
  reopenCheckpoint: (id: string) => void;
  toggleGuidedTask: (id: string, blockTitle: string, task: string, done: boolean) => void;
  recordArtifactInteraction: Props["recordArtifactInteraction"];
}) {
  const checkpointId = `${lesson.id}:${blockIndex}:${block.title}`;
  const checkpointPassed = completedCheckpointSet.has(checkpointId);
  const revealId = `predict-first:${lesson.id}:${blockIndex}:${block.title}`;
  const predictFirstRevealed = !block.predict_first || revealedPredictFirstSet.has(revealId);
  const blockCheckpointQuestions =
    block.checkpoint_questions?.length
      ? block.checkpoint_questions
      : getAdaptiveCheckpointQuestions(checkpointQuestions, blockIndex, block.title);
  const blockKind = block.kind ?? inferBlockKind(block.title);

  return (
    <div className="space-y-4 px-1 pb-2">
      {block.predict_first ? (
        <div className="rounded-xl border-2 border-cyan-500/30 bg-cyan-50/60 px-4 py-4 dark:bg-cyan-500/10">
          <p className="flex items-center gap-2 text-sm font-semibold text-cyan-800 dark:text-cyan-200">
            <Lightbulb className="h-4 w-4" />
            Think first
          </p>
          <p className="mt-2 text-sm text-craft-ink">{block.predict_first.question}</p>
          {block.predict_first.hint ? (
            <p className="mt-1 text-xs italic text-craft-muted">{block.predict_first.hint}</p>
          ) : null}
          {!predictFirstRevealed ? (
            <button
              type="button"
              onClick={() => revealPredictFirst(revealId)}
              className="btn-secondary mt-3 px-3 py-2 text-xs"
            >
              I&apos;ve thought about it. Show the explanation
            </button>
          ) : (
            <p className="mt-2 text-xs font-medium text-emerald-700 dark:text-emerald-300">
              ✓ Good. You engaged before reading. Now see how your thinking compares.
            </p>
          )}
        </div>
      ) : null}

      {predictFirstRevealed ? <LessonContent content={block.body} /> : null}

      {predictFirstRevealed && block.analogy ? (
        <div className="rounded-xl border border-cyan-500/20 bg-craft-accent-soft/40 px-4 py-3">
          <p className="flex items-center gap-2 text-sm font-semibold text-craft-ink">
            <Lightbulb className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />
            Analogy
          </p>
          <div className="mt-2">
            <LessonContent content={block.analogy} />
          </div>
        </div>
      ) : null}

      {predictFirstRevealed && block.try_this?.length ? (
        <div className="rounded-xl border border-craft-border bg-craft-soft/70 px-4 py-3">
          <p className="flex items-center gap-2 text-sm font-semibold text-craft-ink">
            <Sparkles className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />
            Try this now
          </p>
          <ul className="mt-3 space-y-2 text-sm text-craft-muted">
            {block.try_this.map((step, taskIndex) => {
              const taskId = `task:${lesson.id}:${blockIndex}:${taskIndex}`;
              const done = completedTaskSet.has(taskId);
              return (
                <li key={taskId}>
                  <button
                    type="button"
                    onClick={() => toggleGuidedTask(taskId, block.title, step, !done)}
                    className="flex w-full items-start gap-3 rounded-xl border border-craft-border bg-craft-surface px-3 py-3 text-left transition hover:border-craft-faint"
                  >
                    <span
                      className={clsx(
                        "mt-0.5 inline-flex h-5 w-5 shrink-0 items-center justify-center rounded-full border text-xs font-semibold",
                        done
                          ? "border-emerald-500 bg-emerald-500 text-white"
                          : "border-craft-faint text-craft-faint"
                      )}
                    >
                      {done ? <CheckCircle2 className="h-3.5 w-3.5" /> : taskIndex + 1}
                    </span>
                    <span className={done ? "text-craft-ink" : undefined}>{step}</span>
                  </button>
                </li>
              );
            })}
          </ul>
        </div>
      ) : null}

      {predictFirstRevealed && block.remember ? (
        <div className="rounded-xl border border-amber-500/20 bg-amber-50/80 px-4 py-3 dark:bg-amber-500/10">
          <p className="text-sm font-semibold text-craft-ink">Remember this</p>
          <p className="mt-2 text-sm text-craft-muted">{block.remember}</p>
        </div>
      ) : null}

      {predictFirstRevealed && block.inlineArtifacts.length ? (
        <div className="rounded-xl border border-craft-border bg-craft-soft/70 px-4 py-4">
          <p className="flex items-center gap-2 text-sm font-semibold text-craft-ink">
            <Wrench className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />
            Practice file for this step
          </p>
          <p className="mt-2 text-sm text-craft-muted">
            Use the real file below while this idea is still fresh.
          </p>
          <div className="mt-3">
            <LessonArtifactPack
              artifacts={block.inlineArtifacts}
              interactionLog={lesson.interaction_log}
              variant="inline"
              onRecordInteraction={recordArtifactInteraction}
            />
          </div>
        </div>
      ) : null}

      {predictFirstRevealed && block.inlineFileExplorer ? <OpenClawFileExplorer /> : null}

      {predictFirstRevealed && block.inlineCapstoneStudio && capstoneAssignment ? (
        <div className="rounded-xl border border-craft-border bg-craft-soft/70 px-4 py-4">
          <p className="flex items-center gap-2 text-sm font-semibold text-craft-ink">
            <ClipboardCheck className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />
            Build the capstone here
          </p>
          <div className="mt-3">
            <LessonCapstoneStudio
              assignment={capstoneAssignment}
              evaluationRubric={Array.isArray(lesson.sandbox_config.evaluation_rubric) ? (lesson.sandbox_config.evaluation_rubric as Array<{ criterion: string; weight: number; description: string }>) : []}
              evaluationCases={Array.isArray(lesson.sandbox_config.evaluation_cases) ? (lesson.sandbox_config.evaluation_cases as Array<{ name: string; goal: string; expected: string }>) : []}
              interactionLog={lesson.interaction_log}
              onRecordInteraction={recordArtifactInteraction}
            />
          </div>
        </div>
      ) : null}

      {predictFirstRevealed && block.checkpoint_after && blockCheckpointQuestions.length ? (
        <div className="rounded-xl border border-craft-border bg-craft-soft/40 px-4 py-4">
          <p className="flex items-center gap-2 text-sm font-bold text-craft-ink">
            <Sparkles className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />
            Mini Checkpoint
          </p>
          <div className="mt-3">
            {checkpointPassed ? (
              <div className="space-y-3">
                <div className="rounded-xl border border-emerald-400/30 bg-emerald-50/80 px-4 py-3 dark:bg-emerald-500/10">
                  <p className="flex items-center gap-2 text-sm font-semibold text-emerald-800 dark:text-emerald-300">
                    <CheckCircle2 className="h-4 w-4" />
                    Checkpoint complete
                  </p>
                  <p className="mt-2 text-sm text-craft-muted">
                    You locked in &ldquo;{block.title}&rdquo;. Practice again for another rep.
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => reopenCheckpoint(checkpointId)}
                  className="btn-secondary"
                >
                  Practice checkpoint again
                </button>
              </div>
            ) : (
              <CheckpointQuiz
                questions={blockCheckpointQuestions}
                onPassed={() => markCheckpointComplete(checkpointId)}
              />
            )}
          </div>
        </div>
      ) : null}
    </div>
  );
}

export function PaginatedLessonContent({
  lesson,
  slug,
  lessonSlug,
  videoUrl,
  blockLayouts,
  checkpointBlocks,
  checkpointPct,
  optimisticCheckpointIds,
  capstoneAssignment,
  hasInlineCapstoneStudio,
  remainingArtifacts,
  checkpointQuestions,
  completedCheckpointSet,
  completedTaskSet,
  revealedPredictFirstSet,
  revealPredictFirst,
  markCheckpointComplete,
  reopenCheckpoint,
  toggleGuidedTask,
  recordArtifactInteraction,
}: Props) {
  const evaluationRubric = Array.isArray(lesson.sandbox_config.evaluation_rubric)
    ? (lesson.sandbox_config.evaluation_rubric as Array<{ criterion: string; weight: number; description: string }>)
    : [];
  const evaluationCases = Array.isArray(lesson.sandbox_config.evaluation_cases)
    ? (lesson.sandbox_config.evaluation_cases as Array<{ name: string; goal: string; expected: string }>)
    : [];
  // Slides = each guided block + one final wrap-up slide
  const totalSlides = blockLayouts.length + 1;
  const wrapUpIndex = blockLayouts.length;

  const [currentIndex, setCurrentIndex] = useState(0);
  const [animClass, setAnimClass] = useState<"slide-active" | "slide-enter" | "slide-enter-back">("slide-active");
  const slideRef = useRef<HTMLDivElement>(null);

  const nextStep = stepAfterContent(!!videoUrl);
  const nextLabel = nextStep === "video" ? "Continue to Video" : "Continue to Recap Quiz";

  // Determine if the current block has an unpassed checkpoint (soft gate)
  const currentBlock = currentIndex < blockLayouts.length ? blockLayouts[currentIndex] : null;
  const currentCheckpointId = currentBlock
    ? `${lesson.id}:${currentIndex}:${currentBlock.title}`
    : null;
  const currentCheckpointGated =
    currentBlock?.checkpoint_after &&
    currentCheckpointId !== null &&
    !completedCheckpointSet.has(currentCheckpointId);

  function navigate(direction: "forward" | "back") {
    const entering = direction === "forward" ? "slide-enter" : "slide-enter-back";
    setAnimClass(entering);
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        setAnimClass("slide-active");
        setCurrentIndex((prev) =>
          direction === "forward"
            ? Math.min(prev + 1, totalSlides - 1)
            : Math.max(prev - 1, 0)
        );
        slideRef.current?.scrollTo({ top: 0, behavior: "instant" });
      });
    });
  }

  useEffect(() => {
    function handleKey(e: KeyboardEvent) {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
      if (e.key === "ArrowRight" && currentIndex < totalSlides - 1) navigate("forward");
      if (e.key === "ArrowLeft" && currentIndex > 0) navigate("back");
    }
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [currentIndex, totalSlides]);

  const blockKind = currentBlock?.kind ?? (currentBlock ? inferBlockKind(currentBlock.title) : null);
  const slideHeaderColor =
    blockKind === "common_mistake"
      ? "text-amber-600 dark:text-amber-300"
      : "text-cyan-600 dark:text-cyan-400";
  const slideHeaderIcon =
    blockKind === "common_mistake" ? (
      <AlertTriangle className="h-4 w-4" />
    ) : blockKind === "teach_it_back" ? (
      <GraduationCap className="h-4 w-4" />
    ) : currentIndex === wrapUpIndex ? (
      <FileText className="h-4 w-4" />
    ) : (
      <BookOpen className="h-4 w-4" />
    );
  const slideTitle =
    currentIndex === wrapUpIndex ? "Wrap-up" : currentBlock?.title ?? "";
  const nextButtonLabel = currentCheckpointGated ? "Finish checkpoint" : "Continue";

  return (
    <div>
      {/*
        Content-sized card — no artificial max-height. At normal zoom the full
        slide is visible (page scroll only if needed). Browser zoom shrinks the
        viewport and the dashboard page scroll handles overflow.
      */}
      <div className="card flex flex-col overflow-hidden">
        <div className="flex shrink-0 items-center justify-between gap-3 border-b border-craft-border px-5 py-2.5 sm:px-6">
          <div className="flex items-center gap-2">
            <span className={slideHeaderColor}>{slideHeaderIcon}</span>
            <h2 className="text-base font-bold text-craft-ink">{slideTitle}</h2>
          </div>
          <span className="text-xs font-medium uppercase tracking-[0.18em] text-craft-faint">
            Step {currentIndex + 1} / {totalSlides}
          </span>
        </div>

        <div
          ref={slideRef}
          className={clsx("px-5 py-4 sm:px-6 sm:py-5", animClass)}
        >
          {currentIndex < blockLayouts.length ? (
            <BlockSlide
              block={blockLayouts[currentIndex]}
              blockIndex={currentIndex}
              lesson={lesson}
              completedCheckpointSet={completedCheckpointSet}
              completedTaskSet={completedTaskSet}
              revealedPredictFirstSet={revealedPredictFirstSet}
              checkpointQuestions={checkpointQuestions}
              capstoneAssignment={capstoneAssignment}
              revealPredictFirst={revealPredictFirst}
              markCheckpointComplete={markCheckpointComplete}
              reopenCheckpoint={reopenCheckpoint}
              toggleGuidedTask={toggleGuidedTask}
              recordArtifactInteraction={recordArtifactInteraction}
            />
          ) : (
            <div className="space-y-4">
              {remainingArtifacts.length ? (
                <div className="rounded-xl border border-craft-border bg-craft-soft/70 px-4 py-4">
                  <p className="flex items-center gap-2 text-sm font-semibold text-craft-ink">
                    <Wrench className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />
                    More Practice Files
                  </p>
                  <div className="mt-3">
                    <LessonArtifactPack
                      artifacts={remainingArtifacts}
                      interactionLog={lesson.interaction_log}
                      onRecordInteraction={recordArtifactInteraction}
                    />
                  </div>
                </div>
              ) : null}

              {capstoneAssignment && !hasInlineCapstoneStudio ? (
                <div className="rounded-xl border border-craft-border bg-craft-soft/70 px-4 py-4">
                  <p className="flex items-center gap-2 text-sm font-semibold text-craft-ink">
                    <ClipboardCheck className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />
                    {capstoneAssignment.title}
                  </p>
                  <div className="mt-3">
                    <LessonCapstoneStudio
                      assignment={capstoneAssignment}
                      evaluationRubric={[]}
                      evaluationCases={[]}
                      interactionLog={lesson.interaction_log}
                      onRecordInteraction={recordArtifactInteraction}
                    />
                  </div>
                </div>
              ) : null}

              {!blockLayouts.some((b) => b.checkpoint_after) && checkpointQuestions.length ? (
                <div className="rounded-xl border border-craft-border bg-craft-soft/40 px-4 py-4">
                  <p className="flex items-center gap-2 text-sm font-bold text-craft-ink">
                    <Sparkles className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />
                    Mini Checkpoint
                  </p>
                  <div className="mt-3">
                    <CheckpointQuiz questions={checkpointQuestions} />
                  </div>
                </div>
              ) : null}

              <div className="rounded-xl border border-emerald-400/30 bg-emerald-50/60 px-5 py-4 dark:bg-emerald-500/10">
                <p className="text-sm font-semibold text-emerald-800 dark:text-emerald-300">
                  You&apos;ve worked through every section.
                </p>
                <p className="mt-1 text-sm text-craft-muted">
                  When you&apos;re ready, continue to the next step.
                </p>
                <Link
                  href={lessonStepHref(slug, lessonSlug, nextStep)}
                  className="btn-primary mt-4 inline-flex"
                >
                  {nextLabel}
                  <ChevronRight className="h-4 w-4" />
                </Link>
              </div>
            </div>
          )}
        </div>

        <div className="flex shrink-0 items-center justify-between gap-3 border-t border-craft-border bg-craft-surface/92 px-5 py-2.5 backdrop-blur-sm sm:px-6">
          <button
            type="button"
            onClick={() => navigate("back")}
            disabled={currentIndex === 0}
            className="btn-secondary flex items-center gap-1.5 disabled:pointer-events-none disabled:opacity-40"
          >
            <ChevronLeft className="h-4 w-4" />
            Back
          </button>

          {currentIndex < wrapUpIndex ? (
            <button
              type="button"
              onClick={() => navigate("forward")}
              disabled={!!currentCheckpointGated}
              className="btn-primary flex items-center gap-1.5 disabled:pointer-events-none disabled:opacity-40"
            >
              {nextButtonLabel}
              <ChevronRight className="h-4 w-4" />
            </button>
          ) : <span />}
        </div>
      </div>
    </div>
  );
}
