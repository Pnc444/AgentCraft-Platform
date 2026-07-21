"use client";

import { Fragment, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import clsx from "clsx";
import {
  CheckCircle2,
  AlertTriangle,
  BookOpen,
  ClipboardCheck,
  ChevronLeft,
  ChevronRight,
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
import { LessonSection } from "@/components/lessons/LessonSection";
import { OpenClawFileExplorer } from "@/components/lessons/OpenClawFileExplorer";
import { PaginatedLessonContent } from "@/components/lessons/PaginatedLessonContent";
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";
import { ProgressBar } from "@/components/shared/ProgressBar";
import { Reveal } from "@/components/shared/Reveal";
import { completedCheckpointIds, completedInteractionKeys } from "@/lib/lesson-interactions";
import { getCapstoneAssignment, lessonStepHref, stepAfterContent } from "@/lib/lesson-steps";

function inferBlockKind(title: string) {
  const normalized = title.trim().toLowerCase();
  if (normalized === "common mistake") return "common_mistake";
  if (normalized === "teach it back") return "teach_it_back";
  return null;
}

function PredictFirstCard({
  question,
  hint,
  revealed,
  onReveal,
}: {
  question: string;
  hint?: string;
  revealed: boolean;
  onReveal: () => void;
}) {
  return (
    <div className="rounded-xl border-2 border-cyan-500/30 bg-cyan-50/60 px-4 py-4 dark:bg-cyan-500/10">
      <p className="flex items-center gap-2 text-sm font-semibold text-cyan-800 dark:text-cyan-200">
        <Lightbulb className="h-4 w-4" />
        Think first
      </p>
      <p className="mt-2 text-sm text-craft-ink">{question}</p>
      {hint ? (
        <p className="mt-1 text-xs italic text-craft-muted">{hint}</p>
      ) : null}
      {!revealed ? (
        <button
          type="button"
          onClick={onReveal}
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
  );
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
  return Array.from({ length: 3 }, (_, offset) => questions[(start + offset) % questions.length]).filter(
    Boolean
  );
}

export default function LessonContentPage() {
  const {
    slug,
    lessonSlug,
    lesson,
    course,
    videoUrl,
    prev,
    checkpointQuestions,
    guidedBlocks,
    artifactBundle,
    updateProgress,
  } = useLessonWorkspace();

  if (!lesson) return null;

  const nextStep = stepAfterContent(!!videoUrl);
  const nextLabel = nextStep === "video" ? "Continue to Video" : "Continue to Recap Quiz";
  const checkpointBlocks = useMemo(
    () =>
      guidedBlocks
        .map((block, index) => ({
          id: `${lesson.id}:${index}:${block.title}`,
          title: block.title,
          checkpoint_after: !!block.checkpoint_after,
          questions:
            block.checkpoint_questions?.length
              ? block.checkpoint_questions
              : getAdaptiveCheckpointQuestions(checkpointQuestions, index, block.title),
        }))
        .filter((block) => block.checkpoint_after && block.questions.length),
    [guidedBlocks, lesson.id, checkpointQuestions]
  );
  const capstoneAssignment = useMemo(
    () => getCapstoneAssignment(lesson.sandbox_config),
    [lesson.sandbox_config]
  );
  const blockLayouts = useMemo(() => {
    const blockWithArtifactRefs = guidedBlocks.findIndex((block) => block.artifact_paths?.length);
    const defaultInlineArtifactIndex =
      blockWithArtifactRefs >= 0
        ? -1
        : artifactBundle.length === 1
          ? Math.max(
              0,
              guidedBlocks.findIndex((block) => block.try_this?.length || block.checkpoint_after)
            )
          : -1;

    return guidedBlocks.map((block, index) => {
      const inlineArtifacts = block.artifact_paths?.length
        ? artifactBundle.filter((artifact) => block.artifact_paths?.includes(artifact.path))
        : defaultInlineArtifactIndex === index
          ? artifactBundle.slice(0, 1)
          : [];

      return {
        ...block,
        inlineArtifacts,
        inlineCapstoneStudio: block.interactive_widget === "capstone_studio",
        inlineFileExplorer: block.interactive_widget === "openclaw_file_explorer",
      };
    });
  }, [artifactBundle, guidedBlocks]);
  const inlineArtifactPaths = useMemo(
    () => new Set(blockLayouts.flatMap((block) => block.inlineArtifacts.map((artifact) => artifact.path))),
    [blockLayouts]
  );
  const remainingArtifacts = useMemo(
    () => artifactBundle.filter((artifact) => !inlineArtifactPaths.has(artifact.path)),
    [artifactBundle, inlineArtifactPaths]
  );
  const hasInlineCapstoneStudio = useMemo(
    () => blockLayouts.some((block) => block.inlineCapstoneStudio),
    [blockLayouts]
  );
  const [optimisticCheckpointIds, setOptimisticCheckpointIds] = useState<string[]>([]);
  const [optimisticTaskIds, setOptimisticTaskIds] = useState<string[]>([]);
  const [revealedPredictFirstIds, setRevealedPredictFirstIds] = useState<string[]>([]);

  useEffect(() => {
    setOptimisticCheckpointIds(Array.from(completedCheckpointIds(lesson.interaction_log)));
  }, [lesson.interaction_log]);

  useEffect(() => {
    setOptimisticTaskIds(Array.from(completedInteractionKeys(lesson.interaction_log, "guided_task")));
  }, [lesson.interaction_log]);

  const completedCheckpointSet = useMemo(() => new Set(optimisticCheckpointIds), [optimisticCheckpointIds]);
  const completedTaskSet = useMemo(() => new Set(optimisticTaskIds), [optimisticTaskIds]);
  const revealedPredictFirstSet = useMemo(
    () => new Set(revealedPredictFirstIds),
    [revealedPredictFirstIds]
  );
  const checkpointPct = checkpointBlocks.length
    ? Math.round((optimisticCheckpointIds.length / checkpointBlocks.length) * 100)
    : 0;

  function revealPredictFirst(revealId: string) {
    setRevealedPredictFirstIds((prev) => {
      if (prev.includes(revealId)) return prev;
      return [...prev, revealId];
    });
  }

  function markCheckpointComplete(checkpointId: string) {
    setOptimisticCheckpointIds((prev) => {
      if (prev.includes(checkpointId)) return prev;
      return [...prev, checkpointId];
    });
    updateProgress({
      interaction_event: {
        type: "checkpoint",
        key: checkpointId,
        status: "passed",
      },
    });
  }

  function reopenCheckpoint(checkpointId: string) {
    setOptimisticCheckpointIds((prev) => prev.filter((value) => value !== checkpointId));
    updateProgress({
      interaction_event: {
        type: "checkpoint",
        key: checkpointId,
        status: "incomplete",
      },
    });
  }

  function recordArtifactInteraction(event: {
    type: string;
    key: string;
    status?: string;
    details?: Record<string, unknown>;
  }) {
    updateProgress({ interaction_event: event });
  }

  function toggleGuidedTask(taskId: string, blockTitle: string, task: string, done: boolean) {
    setOptimisticTaskIds((prev) => {
      if (done) {
        return prev.includes(taskId) ? prev : [...prev, taskId];
      }
      return prev.filter((value) => value !== taskId);
    });
    updateProgress({
      interaction_event: {
        type: "guided_task",
        key: taskId,
        status: done ? "done" : "incomplete",
        details: { block_title: blockTitle, task },
      },
    });
  }

  const isPaginated =
    blockLayouts.length > 0 ||
    checkpointBlocks.length > 0 ||
    artifactBundle.length > 0 ||
    capstoneAssignment !== null;

  if (isPaginated) {
    return (
      <PaginatedLessonContent
        lesson={lesson}
        slug={slug}
        lessonSlug={lessonSlug}
        videoUrl={videoUrl}
        blockLayouts={blockLayouts}
        checkpointBlocks={checkpointBlocks}
        checkpointPct={checkpointPct}
        optimisticCheckpointIds={optimisticCheckpointIds}
        capstoneAssignment={capstoneAssignment}
        hasInlineCapstoneStudio={hasInlineCapstoneStudio}
        remainingArtifacts={remainingArtifacts}
        checkpointQuestions={checkpointQuestions}
        completedCheckpointSet={completedCheckpointSet}
        completedTaskSet={completedTaskSet}
        revealedPredictFirstSet={revealedPredictFirstSet}
        revealPredictFirst={revealPredictFirst}
        markCheckpointComplete={markCheckpointComplete}
        reopenCheckpoint={reopenCheckpoint}
        toggleGuidedTask={toggleGuidedTask}
        recordArtifactInteraction={recordArtifactInteraction}
      />
    );
  }

  return (
    <div className="space-y-4">
      {checkpointBlocks.length ? (
        <LessonSection
          title="Learning Momentum"
          icon={<Sparkles className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />}
        >
          <div className="space-y-3">
            <p className="text-sm text-craft-muted">
              These mini checkpoints save progress on this device so students feel momentum before the Recap Quiz.
            </p>
            <div className="flex items-center gap-3">
              <ProgressBar value={checkpointPct} className="flex-1" />
              <span className="text-sm font-medium text-craft-ink">
                {optimisticCheckpointIds.length} / {checkpointBlocks.length}
              </span>
            </div>
          </div>
        </LessonSection>
      ) : null}

      {blockLayouts.length ? (
        blockLayouts.map((block, index) => {
          const checkpointId = `${lesson.id}:${index}:${block.title}`;
          const checkpointPassed = completedCheckpointSet.has(checkpointId);
          const revealId = `predict-first:${lesson.id}:${index}:${block.title}`;
          const predictFirstRevealed =
            !block.predict_first || revealedPredictFirstSet.has(revealId);
          const blockCheckpointQuestions =
            block.checkpoint_questions?.length
              ? block.checkpoint_questions
              : getAdaptiveCheckpointQuestions(checkpointQuestions, index, block.title);
          const blockKind = block.kind ?? inferBlockKind(block.title);
          const sectionClassName =
            blockKind === "common_mistake"
              ? "border-amber-500/25 bg-amber-50/70 dark:bg-amber-500/10"
              : blockKind === "teach_it_back"
                ? "border-cyan-500/25 bg-cyan-50/70 dark:bg-cyan-500/10"
                : undefined;
          const sectionIcon =
            blockKind === "common_mistake" ? (
              <AlertTriangle className="h-4 w-4 text-amber-600 dark:text-amber-300" />
            ) : blockKind === "teach_it_back" ? (
              <GraduationCap className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />
            ) : (
              <BookOpen className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />
            );

          return (
          <Fragment key={`${lesson.id}-${block.title}`}>
            <LessonSection
              title={block.title}
              icon={sectionIcon}
              className={sectionClassName}
            >
              <div className="space-y-4">
                {block.predict_first ? (
                  <PredictFirstCard
                    question={block.predict_first.question}
                    hint={block.predict_first.hint}
                    revealed={predictFirstRevealed}
                    onReveal={() => revealPredictFirst(revealId)}
                  />
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
                        const taskId = `task:${lesson.id}:${index}:${taskIndex}`;
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
                      Use the real file below while this idea is still fresh instead of jumping to a separate practice area later.
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

                {predictFirstRevealed && block.inlineFileExplorer ? (
                  <OpenClawFileExplorer />
                ) : null}

                {predictFirstRevealed && block.inlineCapstoneStudio && capstoneAssignment ? (
                  <div className="rounded-xl border border-craft-border bg-craft-soft/70 px-4 py-4">
                    <p className="flex items-center gap-2 text-sm font-semibold text-craft-ink">
                      <ClipboardCheck className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />
                      Build the capstone here
                    </p>
                    <p className="mt-2 text-sm text-craft-muted">
                      The capstone studio is attached to the evaluation block because this is the point where students should actually apply the testing stack, not scroll to a separate tool area later.
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
              </div>
            </LessonSection>

            {predictFirstRevealed && block.checkpoint_after && blockCheckpointQuestions.length ? (
              <LessonSection
                title="Mini Checkpoint"
                icon={<Sparkles className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />}
              >
                {checkpointPassed ? (
                  <div className="space-y-3">
                    <div className="rounded-xl border border-emerald-400/30 bg-emerald-50/80 px-4 py-3 dark:bg-emerald-500/10">
                      <p className="flex items-center gap-2 text-sm font-semibold text-emerald-800 dark:text-emerald-300">
                        <CheckCircle2 className="h-4 w-4" />
                        Checkpoint complete
                      </p>
                      <p className="mt-2 text-sm text-craft-muted">
                        You already locked in the idea from “{block.title}”. Practice again if you want another rep before the recap quiz.
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
              </LessonSection>
            ) : null}
          </Fragment>
          );
        })
      ) : lesson.content ? (
        <LessonSection title="Lesson Content" icon={<BookOpen className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />}>
          <LessonContent content={lesson.content} />
        </LessonSection>
      ) : (
        <LessonSection
          title="Lesson Content"
          icon={<FileText className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />}
          empty
        />
      )}

      {remainingArtifacts.length ? (
        <LessonSection
          title="More Practice Files"
          icon={<Wrench className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />}
        >
          <LessonArtifactPack
            artifacts={remainingArtifacts}
            interactionLog={lesson.interaction_log}
            onRecordInteraction={recordArtifactInteraction}
          />
        </LessonSection>
      ) : null}

      {!guidedBlocks.some((block) => block.checkpoint_after) && checkpointQuestions.length ? (
        <LessonSection
          title="Mini Checkpoint"
          icon={<Sparkles className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />}
        >
          <CheckpointQuiz questions={checkpointQuestions} />
        </LessonSection>
      ) : null}

      {lesson.lesson_type === "sandbox" && (
        <LessonSection
          title="Interactive Demo"
          icon={<Wrench className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />}
        >
          <p className="text-sm text-craft-muted">Sandbox</p>
          <button
            type="button"
            onClick={() =>
              alert("Sandbox integration coming soon. Diego and Douglas are wiring it up.")
            }
            className="btn-primary mt-4"
          >
            <Wrench className="h-4 w-4" />
            Launch Sandbox
          </button>
        </LessonSection>
      )}

      <Reveal delay={80}>
        <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
          {prev ? (
            <Link href={lessonStepHref(slug, prev.slug, "content")} className="btn-secondary">
              <ChevronLeft className="h-4 w-4" />
              {prev.title}
            </Link>
          ) : (
            <span />
          )}
          <Link href={lessonStepHref(slug, lessonSlug, nextStep)} className="btn-primary">
            {nextLabel}
            <ChevronRight className="h-4 w-4" />
          </Link>
        </div>
      </Reveal>
    </div>
  );
}
