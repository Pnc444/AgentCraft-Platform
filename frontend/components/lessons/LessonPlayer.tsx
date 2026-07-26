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
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";
import { lessonStepHref } from "@/lib/lesson-steps";
import type { CheckpointQuestion } from "@/components/lessons/CheckpointQuiz";
import type { Beat } from "@/types";

/**
 * Courses that render lessons through the player instead of the stacked
 * content page (plan step 1: Module 4 proves it; later steps widen the set,
 * step 7 deletes the flag and the old page together).
 */
const PLAYER_COURSES = new Set(["module-4-ai-agents"]);

export function isPlayerCourse(courseSlug: string): boolean {
  return PLAYER_COURSES.has(courseSlug);
}

/**
 * The zero-scroll lesson player (plan §3). One beat on screen; nothing renders
 * below the card. The card owns the viewport height minus the app chrome —
 * only the beat's own pane may scroll, never the page.
 */
export function LessonPlayer() {
  const router = useRouter();
  const { slug, lessonSlug, lesson, needsVideo, videoDone, markVideoWatched } =
    useLessonWorkspace();
  const beats = (lesson?.beats ?? []) as Beat[];
  const storageKey = lesson ? `agentcraft-player:${lesson.id}` : "";

  const [index, setIndex] = useState(0);
  const [revealed, setRevealed] = useState<Record<number, boolean>>({});
  const [picks, setPicks] = useState<Record<number, number>>({});

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

  const satisfied =
    !beat ||
    (beat.type === "predict"
      ? !!revealed[index]
      : beat.type === "check"
        ? pickedCorrect
        : beat.type === "do" && beat.action === "video"
          ? videoDone || !needsVideo
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
    <div className="card flex h-[calc(100dvh-19.5rem)] min-h-[22rem] flex-col overflow-hidden sm:h-[calc(100dvh-16rem)] sm:min-h-[26rem]">
      {/* Header: beat title + ONE position signal (segmented bar + count). */}
      <div className="flex shrink-0 items-center justify-between gap-4 border-b border-craft-border px-5 py-3 sm:px-6">
        <h2 className="min-w-0 truncate text-base font-bold text-craft-ink">
          {beat.title || lesson.title}
        </h2>
        <div className="flex shrink-0 items-center gap-3">
          <div className="hidden w-32 gap-1 sm:flex" aria-hidden>
            {beats.map((_, i) => (
              <span
                key={i}
                className={clsx(
                  "h-1 flex-1 rounded-full",
                  i < index ? "bg-cyan-500" : i === index ? "bg-cyan-300" : "bg-craft-border"
                )}
              />
            ))}
          </div>
          <span className="whitespace-nowrap text-xs font-medium uppercase tracking-[0.18em] text-craft-faint">
            {index + 1} / {beats.length}
          </span>
        </div>
      </div>

      {/* One beat. The pane may scroll internally; the page never does. */}
      <div className="min-h-0 flex-1 overflow-y-auto px-5 py-5 sm:px-8 sm:py-6">
        <div className="mx-auto max-w-2xl">
          <BeatView
            beat={beat}
            revealed={!!revealed[index]}
            onReveal={() => setRevealed((r) => ({ ...r, [index]: true }))}
            pick={picks[index]}
            onPick={(option) => setPicks((p) => ({ ...p, [index]: option }))}
            videoDone={videoDone}
            markVideoWatched={markVideoWatched}
          />
        </div>
      </div>

      <div className="flex shrink-0 items-center justify-between gap-3 border-t border-craft-border px-5 py-3 sm:px-6">
        <button
          type="button"
          onClick={() => setIndex((i) => Math.max(i - 1, 0))}
          disabled={index === 0}
          className="btn-secondary disabled:pointer-events-none disabled:opacity-40"
        >
          <ChevronLeft className="h-4 w-4 shrink-0" />
          Back
        </button>
        <button
          type="button"
          onClick={goForward}
          disabled={!satisfied}
          className="btn-primary disabled:pointer-events-none disabled:opacity-40"
        >
          {isLast ? (
            <>
              <ClipboardCheck className="h-4 w-4 shrink-0" />
              Continue to Recap Quiz
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
}: {
  beat: Beat;
  revealed: boolean;
  onReveal: () => void;
  pick: number | undefined;
  onPick: (option: number) => void;
  videoDone: boolean;
  markVideoWatched: Parameters<typeof LessonVideo>[0]["onWatched"];
}) {
  if (beat.type === "predict") {
    return (
      <div className="space-y-4">
        <div className="rounded-xl border-2 border-cyan-500/30 bg-cyan-50/60 px-4 py-4 dark:bg-cyan-500/10">
          <p className="flex items-center gap-2 text-sm font-semibold text-cyan-800 dark:text-cyan-200">
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
          <Sparkles className="h-4 w-4 shrink-0 text-cyan-600 dark:text-cyan-400" />
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
        url={beat.video_url ?? ""}
        title={beat.title}
        watched={videoDone}
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
        <div className="rounded-xl border border-cyan-500/25 px-4 py-3">
          <p className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-cyan-700 dark:text-cyan-300">
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
