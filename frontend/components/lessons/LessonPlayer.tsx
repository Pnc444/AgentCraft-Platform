"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import clsx from "clsx";
import {
  BookOpen,
  Check,
  ChevronLeft,
  ChevronRight,
  ClipboardCheck,
  Lightbulb,
  ListChecks,
  Sparkles,
} from "lucide-react";
import { LessonContent } from "@/components/lessons/LessonContent";
import { LessonVideo } from "@/components/lessons/LessonVideo";
import { LessonWorkbench } from "@/components/lessons/LessonWorkbench";
import { LessonCapstoneStudio } from "@/components/lessons/LessonCapstoneStudio";
import { LessonSandbox } from "@/components/lessons/LessonSandbox";
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";
import { getCapstoneAssignment, lessonStepHref } from "@/lib/lesson-steps";
import { useCanBypassGates } from "@/lib/gates";
import type { Beat, CheckpointQuestion, LessonArtifact, SandboxSpec } from "@/types";

/**
 * The zero-scroll lesson player. One beat on screen; the card fills the
 * available viewport under app chrome. Only the beat pane may scroll.
 */
export function LessonPlayer() {
  const router = useRouter();
  const canBypassGates = useCanBypassGates();
  const { slug, lessonSlug, lesson, course, needsVideo, videoDone, markVideoWatched, artifactBundle } =
    useLessonWorkspace();
  const beats = (lesson?.beats ?? []) as Beat[];
  const moduleSteps = course?.lessons ?? [];
  const stepIndex = moduleSteps.findIndex((l) => l.slug === lessonSlug);
  const stepOrdinal = stepIndex >= 0 ? stepIndex + 1 : 1;
  const storageKey = lesson ? `agentcraft-player:${lesson.id}` : "";

  const [index, setIndex] = useState(0);
  const [revealed, setRevealed] = useState<Record<number, boolean>>({});
  const [picks, setPicks] = useState<Record<number, number>>({});
  const [workDone, setWorkDone] = useState<Record<number, boolean>>({});

  /*
    Resume where the learner left off (session-scoped, like quiz drafts).
    One effect owns both restore and persist: the restore pass never writes,
    so StrictMode's double-invoke cannot clobber a saved draft with index 0
    before the restored state commits.
  */
  const restored = useRef(false);
  useEffect(() => {
    if (!storageKey || !beats.length) return;
    if (!restored.current) {
      restored.current = true;
      try {
        const raw = window.sessionStorage.getItem(storageKey);
        if (raw) {
          const saved = JSON.parse(raw) as { index?: number };
          setIndex(Math.min(Math.max(saved.index ?? 0, 0), beats.length - 1));
        }
      } catch {
        /* fresh start */
      }
      return;
    }
    try {
      window.sessionStorage.setItem(storageKey, JSON.stringify({ index }));
    } catch {
      /* non-persistent is fine */
    }
  }, [index, storageKey, beats.length]);

  const beat = beats[index];
  const isLast = index === beats.length - 1;

  const checkQuestion =
    beat?.type === "check" && typeof beat.question === "object"
      ? (beat.question as CheckpointQuestion)
      : null;
  const pickedCorrect =
    !!checkQuestion && picks[index] === checkQuestion.answer_index;

  // Staff step through beats freely. Every condition below is a teaching
  // device — commit a guess, answer correctly, watch to the end, open the
  // files — and all of them are obstacles when the job is reading the lesson
  // rather than learning it.
  const satisfied =
    !beat ||
    canBypassGates ||
    (beat.type === "predict"
      ? !!revealed[index]
      : beat.type === "check"
        ? pickedCorrect
        : beat.type === "do" && beat.action === "video"
          ? videoDone || !needsVideo
          : beat.type === "do" && beat.action === "workbench"
            ? !!workDone[index]
            : true);

  const goForward = useCallback(() => {
    if (!satisfied) return;
    if (isLast) {
      router.push(lessonStepHref(slug, lessonSlug, "quiz"));
      return;
    }
    setIndex((i) => Math.min(i + 1, beats.length - 1));
  }, [satisfied, isLast, router, slug, lessonSlug, beats.length]);

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement)
        return;
      if (event.key === "ArrowRight") goForward();
      if (event.key === "ArrowLeft") setIndex((i) => Math.max(i - 1, 0));
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [goForward]);

  if (!lesson) return null;
  if (!beats.length) return <p className="text-craft-muted">This lesson has no content yet.</p>;

  return (
    /*
      Sized to content with a viewport cap, not h-full. Forcing full height
      made a two-bullet recap float in a screen of empty card with the Next
      button a monitor's-height away — the same defect the pre-redesign player
      fixed and documented. Compact beats get a compact card; long beats cap at
      the available height and scroll internally. "No page scrollbar" never
      required the card to be tall, only never taller than the viewport.
    */
    <div className="card flex min-h-0 max-h-full flex-col overflow-hidden">
      {/* Module step progress — all steps in this module, not beats inside one step. */}
      <div className="flex shrink-0 items-center gap-3 border-b border-craft-border/80 px-3 py-2 sm:gap-4 sm:px-4">
        <div className="flex min-w-0 flex-1 gap-1" aria-hidden>
          {moduleSteps.map((step, i) => {
            const done = step.status === "completed";
            const current = i === stepIndex;
            return (
              <span
                key={step.slug}
                className={clsx(
                  "h-1.5 flex-1 rounded-full",
                  done
                    ? "bg-violet-500"
                    : current
                      ? "bg-violet-300"
                      : "bg-craft-border"
                )}
                title={step.title}
              />
            );
          })}
        </div>
        <span className="shrink-0 whitespace-nowrap text-[10px] font-medium uppercase tracking-[0.14em] text-craft-faint sm:text-xs">
          {stepOrdinal}/{moduleSteps.length || "—"}
        </span>
      </div>

      {/* One beat. Only this pane scrolls — the page never does. */}
      <div className="min-h-0 flex-1 overflow-y-auto overscroll-contain px-4 py-3 sm:px-5 sm:py-4 lg:px-6">
        <div className="mx-auto w-full max-w-3xl">
          <h2 className="mb-3 text-lg font-bold tracking-tight text-craft-ink sm:mb-4 sm:text-xl">
            {beat.title || lesson.title}
          </h2>
          {beat.type === "do" && beat.action === "terminal" ? (
            <TerminalBeat />
          ) : beat.type === "do" && beat.action === "studio" ? (
            <StudioBeat beat={beat} />
          ) : (
            <BeatView
              beat={beat}
              revealed={!!revealed[index]}
              onReveal={() => setRevealed((r) => ({ ...r, [index]: true }))}
              pick={picks[index]}
              onPick={(option) => setPicks((p) => ({ ...p, [index]: option }))}
              videoDone={videoDone}
              markVideoWatched={markVideoWatched}
              artifacts={artifactBundle}
              onWorkDone={() => setWorkDone((w) => ({ ...w, [index]: true }))}
              needsVideo={needsVideo}
              lessonVideoUrl={lesson.video_url || ""}
            />
          )}
        </div>
      </div>

      <div className="flex shrink-0 flex-col gap-2 border-t border-craft-border px-3 py-2.5 sm:px-4 sm:py-3">
        {!satisfied && beat?.type === "do" && beat.action === "video" ? (
          <p className="text-center text-xs text-amber-700 dark:text-amber-300">
            Watch the video all the way through to unlock the Recap Quiz.
          </p>
        ) : null}
        <div className="flex items-center justify-between gap-2">
          <button
            type="button"
            onClick={() => setIndex((i) => Math.max(i - 1, 0))}
            disabled={index === 0}
            className="btn-secondary min-h-[40px] px-3 text-xs disabled:pointer-events-none disabled:opacity-40 sm:min-h-[44px] sm:px-5 sm:text-sm"
          >
            <ChevronLeft className="h-4 w-4 shrink-0" />
            <span className="hidden sm:inline">Back</span>
          </button>
          <button
            type="button"
            onClick={goForward}
            disabled={!satisfied}
            className="btn-primary min-h-[40px] px-3 text-xs disabled:pointer-events-none disabled:opacity-40 sm:min-h-[44px] sm:px-5 sm:text-sm"
          >
            {isLast ? (
              <>
                <ClipboardCheck className="h-4 w-4 shrink-0" />
                <span className="sm:hidden">Quiz</span>
                <span className="hidden sm:inline">Continue to Recap Quiz</span>
              </>
            ) : (
              <>
                Continue
                <ChevronRight className="h-4 w-4 shrink-0" />
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

function BeatView({
  beat,
  revealed,
  onReveal,
  pick,
  onPick,
  videoDone,
  markVideoWatched,
  artifacts,
  onWorkDone,
  needsVideo,
  lessonVideoUrl,
}: {
  beat: Beat;
  revealed: boolean;
  onReveal: () => void;
  pick: number | undefined;
  onPick: (option: number) => void;
  videoDone: boolean;
  markVideoWatched: Parameters<typeof LessonVideo>[0]["onWatched"];
  artifacts: LessonArtifact[];
  onWorkDone: () => void;
  needsVideo: boolean;
  lessonVideoUrl: string;
}) {
  if (beat.type === "do" && beat.action === "workbench") {
    return (
      <LessonWorkbench
        artifacts={artifacts}
        paths={beat.artifact_paths ?? []}
        instructions={beat.instructions ?? []}
        onAllOpened={onWorkDone}
      />
    );
  }

  if (beat.type === "predict") {
    return (
      <div className="space-y-4">
        <div className="rounded-xl border-2 border-violet-500/30 bg-violet-50/60 px-4 py-4 dark:bg-violet-500/10">
          <p className="flex items-center gap-2 text-sm font-semibold text-violet-800 dark:text-violet-200">
            <Lightbulb className="h-4 w-4 shrink-0" />
            Think first
          </p>
          <p className="mt-2 text-sm text-craft-ink">{String(beat.question ?? "")}</p>
          {beat.hint ? <p className="mt-1 text-xs italic text-craft-muted">{beat.hint}</p> : null}
          {!revealed && (
            <button type="button" onClick={onReveal} className="btn-secondary mt-3 px-3 py-2 text-xs">
              I&apos;ve thought about it. Show the explanation
            </button>
          )}
        </div>
        {revealed && <ExplainBody beat={beat} />}
      </div>
    );
  }

  if (beat.type === "check") {
    const question = typeof beat.question === "object" ? (beat.question as CheckpointQuestion) : null;
    if (!question) return <p className="text-craft-muted">This checkpoint is missing its question.</p>;
    const correct = pick === question.answer_index;
    return (
      <div className="space-y-4">
        <p className="text-base font-medium leading-relaxed text-craft-ink sm:text-lg">
          {question.prompt}
        </p>
        <ul className="space-y-2">
          {question.options.map((option, i) => (
            <li key={i}>
              <button
                type="button"
                onClick={() => onPick(i)}
                disabled={correct}
                className={clsx(
                  "w-full rounded-xl border px-4 py-3 text-left text-sm transition sm:text-base",
                  pick === i && i === question.answer_index
                    ? "border-emerald-400 bg-emerald-50 text-emerald-800 dark:bg-emerald-500/15 dark:text-emerald-200"
                    : pick === i
                      ? "border-amber-400 bg-amber-50 text-amber-800 dark:bg-amber-500/15 dark:text-amber-200"
                      : "border-craft-border bg-craft-surface text-craft-ink hover:border-craft-faint"
                )}
              >
                {option}
              </button>
            </li>
          ))}
        </ul>
        {pick !== undefined &&
          (correct ? (
            <p className="flex items-center gap-1.5 text-sm font-medium text-emerald-700 dark:text-emerald-300">
              <Check className="h-4 w-4 shrink-0" /> Right — carry on.
            </p>
          ) : (
            <p className="text-sm text-amber-700 dark:text-amber-300">
              Not quite — retries are free. Look at the idea again and pick another answer.
            </p>
          ))}
      </div>
    );
  }

  if (beat.type === "recap") {
    return (
      <div className="space-y-3">
        <p className="flex items-center gap-2 text-sm font-semibold text-craft-ink">
          <Sparkles className="h-4 w-4 shrink-0 text-violet-600 dark:text-violet-400" />
          What you now know
        </p>
        <ul className="space-y-2">
          {(beat.bullets ?? []).map((line, i) => (
            <li key={i} className="flex items-start gap-2 text-sm text-craft-ink">
              <Check className="mt-0.5 h-4 w-4 shrink-0 text-emerald-500" />
              {line}
            </li>
          ))}
        </ul>
      </div>
    );
  }

  if (beat.type === "do" && beat.action === "video") {
    return (
      <LessonVideo
        url={(beat.video_url || lessonVideoUrl || "").trim()}
        title={beat.title}
        watched={videoDone}
        requireFullWatch={needsVideo}
        onWatched={markVideoWatched}
      />
    );
  }

  // explain — and the honest fallback for do-actions not yet built.
  return <ExplainBody beat={beat} />;
}

function ExplainBody({ beat }: { beat: Beat }) {
  return (
    <div className="space-y-4">
      {beat.body ? <LessonContent content={beat.body} /> : null}
      {beat.analogy ? (
        <div className="rounded-xl bg-craft-soft px-4 py-3 ring-1 ring-craft-border">
          <p className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-craft-muted">
            <BookOpen className="h-3.5 w-3.5 shrink-0" />
            Analogy
          </p>
          <p className="mt-1.5 text-sm text-craft-ink">{beat.analogy}</p>
        </div>
      ) : null}
      {beat.try_this?.length ? (
        <div className="rounded-xl border border-violet-500/25 px-4 py-3">
          <p className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-violet-700 dark:text-violet-300">
            <ListChecks className="h-3.5 w-3.5 shrink-0" />
            Try this now
          </p>
          <ul className="mt-2 space-y-1.5">
            {beat.try_this.map((task, i) => (
              <li key={i} className="text-sm text-craft-ink">
                {task}
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </div>
  );
}


function StudioBeat({ beat }: { beat: Beat }) {
  const { lesson, updateProgress } = useLessonWorkspace();
  if (!lesson) return null;
  const assignment = getCapstoneAssignment(lesson.sandbox_config);
  if (!assignment) {
    return (
      <p className="text-sm text-craft-muted">
        The capstone assignment for this step is missing from the lesson config.
      </p>
    );
  }
  return (
    <div className="space-y-3">
      {beat.instructions?.length ? (
        <ul className="space-y-1.5">
          {beat.instructions.map((task, i) => (
            <li key={i} className="text-sm text-craft-ink">
              {task}
            </li>
          ))}
        </ul>
      ) : null}
      <LessonCapstoneStudio
        assignment={assignment}
        evaluationRubric={
          Array.isArray(lesson.sandbox_config.evaluation_rubric)
            ? (lesson.sandbox_config.evaluation_rubric as Array<{
                criterion: string;
                weight: number;
                description: string;
              }>)
            : []
        }
        evaluationCases={
          Array.isArray(lesson.sandbox_config.evaluation_cases)
            ? (lesson.sandbox_config.evaluation_cases as Array<{
                name: string;
                goal: string;
                expected: string;
              }>)
            : []
        }
        interactionLog={lesson.interaction_log}
        onRecordInteraction={(event) => updateProgress({ interaction_event: event })}
      />
    </div>
  );
}


function TerminalBeat() {
  const { lesson, updateProgress } = useLessonWorkspace();
  if (!lesson) return null;
  const spec = lesson.sandbox_config?.sandbox as SandboxSpec | undefined;
  if (!spec) {
    return (
      <p className="text-sm text-craft-muted">
        This practice step&apos;s terminal spec is missing from the lesson config.
      </p>
    );
  }
  return (
    <LessonSandbox
      spec={spec}
      lessonId={lesson.id}
      interactionLog={lesson.interaction_log}
      onRecordInteraction={(event) => updateProgress({ interaction_event: event })}
    />
  );
}
