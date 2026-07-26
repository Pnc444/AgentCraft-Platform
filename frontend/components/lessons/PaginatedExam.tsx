"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import clsx from "clsx";
import {
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  ClipboardCheck,
  RotateCcw,
  Sparkles,
  XCircle,
} from "lucide-react";
import type { CheckpointQuestion } from "@/types";
import { ConfettiBurst } from "@/components/lessons/ConfettiBurst";

interface PaginatedExamProps {
  questions: CheckpointQuestion[];
  passScore?: number;
  onPassed?: (score: number) => void;
  locked?: boolean;
  lockedReason?: string;
  onLockedAction?: () => void;
  label?: string;
  /**
   * Rendered inside the pass card instead of the "taking you to progress…"
   * line. Supplied when finishing this assessment also finishes the module, so
   * the learner presses a real button to move on rather than being auto-moved
   * off their own result.
   */
  completionAction?: React.ReactNode;
  /**
   * This learner has already passed. Opens on a record of that result instead
   * of a blank question 1 — returning to a finished exam must not look like
   * the attempt was wiped.
   */
  previouslyPassed?: boolean;
  /** Score from that earlier pass, when the server recorded one. */
  previousScore?: number | null;
  /**
   * sessionStorage key for the in-progress draft (answers + position). With a
   * key set, navigating away and back mid-attempt restores the attempt instead
   * of silently wiping it. Cleared on pass and on deliberate retry.
   */
  storageKey?: string;
}

const DEFAULT_PASS_SCORE = 80;
const CELEBRATE_MS = 2200;

/**
 * `completed` is the entry state for an exam this learner already passed: a
 * record of the result, not a fresh attempt. From there they can review the
 * questions (read-only, correct answers shown) or deliberately retake.
 */
type Phase = "answering" | "result" | "completed";

/**
 * One-question-per-slide assessment UI (module exams + recap quizzes):
 * fixed viewport card, question counter, Back/Next footer — designed so
 * neurodivergent students never face a long scrolling wall of questions.
 */
export function PaginatedExam({
  questions,
  passScore = DEFAULT_PASS_SCORE,
  onPassed,
  locked = false,
  lockedReason,
  onLockedAction,
  label = "Exam",
  completionAction,
  previouslyPassed = false,
  previousScore = null,
  storageKey,
}: PaginatedExamProps) {
  const bank = useMemo(
    () => questions.filter((q) => q.options?.length && typeof q.answer_index === "number"),
    [questions]
  );

  // Question slides (0..n-1) + one final review/results slide (n)
  const totalSlides = bank.length + 1;
  const reviewIndex = bank.length;

  /*
    Mid-attempt answers survive navigation (audit F1). Answering 15 of 20 and
    glancing at Progress used to wipe everything silently. The draft lives in
    sessionStorage under `storageKey`, restored once on mount, cleared on pass
    or on a deliberate retry. Not hydrated over an already-passed exam — the
    standing result stays the entry state.
  */
  const draft = useMemo(() => {
    if (!storageKey || previouslyPassed || typeof window === "undefined") return null;
    try {
      const raw = window.sessionStorage.getItem(storageKey);
      if (!raw) return null;
      const parsed = JSON.parse(raw) as { answers?: Record<string, number>; index?: number };
      const valid: Record<string, number> = {};
      for (const q of bank) {
        if (typeof parsed.answers?.[q.id] === "number") valid[q.id] = parsed.answers[q.id];
      }
      return {
        answers: valid,
        index: Math.min(Math.max(parsed.index ?? 0, 0), bank.length),
      };
    } catch {
      return null;
    }
    // One-time read; the bank is stable for the life of the mount.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const [currentIndex, setCurrentIndex] = useState(draft?.index ?? 0);
  const [animClass, setAnimClass] = useState<"slide-active" | "slide-enter" | "slide-enter-back">(
    "slide-active"
  );
  const slideRef = useRef<HTMLDivElement>(null);
  const [answers, setAnswers] = useState<Record<string, number>>(draft?.answers ?? {});
  // Entry state is decided once, on mount: an already-passed exam opens on its
  // result, never on a blank question 1.
  const [phase, setPhase] = useState<Phase>(previouslyPassed ? "completed" : "answering");
  const [score, setScore] = useState<number | null>(previouslyPassed ? previousScore : null);
  const [passed, setPassed] = useState(previouslyPassed);
  const [showConfetti, setShowConfetti] = useState(false);
  // Already reported — re-entering a finished exam must not re-fire completion.
  const notifiedPass = useRef(previouslyPassed);
  const onPassedRef = useRef(onPassed);
  onPassedRef.current = onPassed;

  const showResult = phase === "result";
  /*
    Reviewing a result that already stands. A previously-passed exam stores no
    answers, so every "did you answer this one?" gate must stand down — the
    review is read-only paging, not an attempt. Without this, Review questions
    opened on question 1 with Next disabled: a dead end.
  */
  const reviewing = showResult && passed;
  const isReviewSlide = currentIndex === reviewIndex;
  const currentQuestion = !isReviewSlide ? bank[currentIndex] : null;
  const currentAnswered =
    !!currentQuestion && typeof answers[currentQuestion.id] === "number";
  const allAnswered = bank.every((q) => typeof answers[q.id] === "number");
  const answeredCount = bank.filter((q) => typeof answers[q.id] === "number").length;

  function navigate(direction: "forward" | "back") {
    if (direction === "forward" && currentIndex >= totalSlides - 1) return;
    if (direction === "back" && currentIndex <= 0) return;
    // Soft gate: must answer the current question before Next — but never
    // while reviewing a standing result (there are no answers to have given).
    if (direction === "forward" && !isReviewSlide && !currentAnswered && !reviewing) return;

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
      if (e.key === "ArrowRight") navigate("forward");
      if (e.key === "ArrowLeft") navigate("back");
    }
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
    // eslint-disable-next-line react-hooks/exhaustive-deps
    // `reviewing` included so arrow keys page through a review too.
  }, [currentIndex, totalSlides, currentAnswered, isReviewSlide, reviewing]);

  // Write the draft through; drop it the moment the attempt passes (F1).
  useEffect(() => {
    if (!storageKey) return;
    try {
      if (passed) {
        window.sessionStorage.removeItem(storageKey);
      } else if (phase === "answering" && Object.keys(answers).length > 0) {
        window.sessionStorage.setItem(
          storageKey,
          JSON.stringify({ answers, index: currentIndex })
        );
      }
    } catch {
      // Storage blocked or full — degrade silently to non-persistent behavior.
    }
  }, [answers, currentIndex, phase, passed, storageKey]);

  useEffect(() => {
    if (phase !== "result" || !passed || score === null || notifiedPass.current) return;
    const t = window.setTimeout(() => {
      notifiedPass.current = true;
      onPassedRef.current?.(score);
    }, CELEBRATE_MS);
    return () => window.clearTimeout(t);
  }, [phase, passed, score]);

  function submit() {
    if (!bank.length || locked || passed || !allAnswered) return;
    let correct = 0;
    for (const q of bank) {
      if (answers[q.id] === q.answer_index) correct += 1;
    }
    const pct = Math.round((correct / bank.length) * 100);
    const didPass = pct >= passScore;
    setScore(pct);
    setPassed(didPass);
    setShowConfetti(didPass);
    setPhase("result");
    setCurrentIndex(reviewIndex);
  }

  function reset() {
    // Deliberate fresh start — the draft goes with it.
    if (storageKey) {
      try {
        window.sessionStorage.removeItem(storageKey);
      } catch {
        /* ignore */
      }
    }
    setAnswers({});
    setPhase("answering");
    setScore(null);
    setPassed(false);
    setShowConfetti(false);
    notifiedPass.current = false;
    setCurrentIndex(0);
    setAnimClass("slide-active");
  }

  function selectAnswer(questionId: string, index: number) {
    if (passed) return;
    setAnswers((prev) => ({ ...prev, [questionId]: index }));
    if (showResult) {
      // Changing an answer after a failed attempt returns to answering mode
      setPhase("answering");
      setScore(null);
      setPassed(false);
      setShowConfetti(false);
    }
  }

  if (!bank.length) {
    return (
      <p className="text-sm text-craft-muted">
        No {label.toLowerCase()} questions are configured for this lesson yet. Add them in the admin
        panel under the lesson&apos;s quiz / sandbox config.
      </p>
    );
  }

  /*
    Already passed. Show the standing result, not a blank attempt — returning
    to a finished exam previously looked identical to never having taken it,
    which reads as "your progress was wiped". Retaking is available, but it is
    a deliberate press, never the default.
  */
  if (phase === "completed") {
    return (
      <div className="card px-5 py-6 sm:px-6">
        <div className="mx-auto max-w-2xl">
          <div className="flex items-start gap-3">
            <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-emerald-500 text-white shadow-soft">
              <CheckCircle2 className="h-5 w-5" />
            </span>
            <div className="min-w-0 flex-1">
              <p className="text-base font-bold text-craft-ink">
                {label} already complete
              </p>
              <p className="mt-1 text-sm text-craft-muted">
                {typeof score === "number"
                  ? `You passed this ${label.toLowerCase()} with ${score}%. That result stands — nothing here has been reset.`
                  : `You've already passed this ${label.toLowerCase()}. That result stands — nothing here has been reset.`}
              </p>

              {completionAction && <div className="mt-4">{completionAction}</div>}

              <div className="mt-4 flex flex-wrap gap-2">
                <button
                  type="button"
                  onClick={() => {
                    // Read-only walkthrough: the existing result rendering
                    // already marks correct answers, so reuse it as-is.
                    setPhase("result");
                    setCurrentIndex(0);
                    setAnimClass("slide-active");
                  }}
                  className="btn-secondary"
                >
                  Review questions
                </button>
                <button
                  type="button"
                  onClick={reset}
                  className="inline-flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm font-medium text-craft-muted transition hover:bg-craft-soft hover:text-craft-ink"
                >
                  <RotateCcw className="h-4 w-4" />
                  Retake {label.toLowerCase()}
                </button>
              </div>
              <p className="mt-2 text-xs text-craft-faint">
                Retaking starts a fresh attempt. Your passing result is kept either way.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (locked) {
    return (
      <div className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800 dark:border-amber-500/30 dark:bg-amber-500/10 dark:text-amber-200">
        <p>{lockedReason || `Finish the required steps before taking the ${label}.`}</p>
        {onLockedAction && (
          <button type="button" onClick={onLockedAction} className="btn-secondary mt-3 text-xs">
            Take me there
          </button>
        )}
      </div>
    );
  }

  const slideTitle = isReviewSlide
    ? showResult
      ? `${label} Results`
      : `Review & Submit`
    : `Question ${currentIndex + 1}`;

  const nextLabel =
    currentIndex === bank.length - 1
      ? "Review"
      : "Next";

  return (
    <div>
      <ConfettiBurst active={showConfetti} />

      <div className="card flex flex-col overflow-hidden">
        {/* Header: title + step counter */}
        <div className="flex shrink-0 items-center justify-between gap-3 border-b border-craft-border px-5 py-2.5 sm:px-6">
          <div className="flex items-center gap-2">
            <span className="text-cyan-600 dark:text-cyan-400">
              <ClipboardCheck className="h-4 w-4" />
            </span>
            <h2 className="text-base font-bold text-craft-ink">{slideTitle}</h2>
          </div>
          <div className="flex items-center gap-3">
            <span className="hidden text-xs text-craft-muted sm:inline">
              {reviewing ? "Reviewing — answers shown" : `${answeredCount}/${bank.length} answered`}
            </span>
            {/*
              Counts questions, not slides — "Step 1 / 6" on a 5-question quiz
              read as a lie (audit B8). The review slide is a state, not a step.
            */}
            <span className="whitespace-nowrap text-xs font-medium uppercase tracking-[0.18em] text-craft-faint">
              {isReviewSlide ? "Review" : `${currentIndex + 1} / ${bank.length}`}
            </span>
          </div>
        </div>

        {/*
          Slide body — no max-height, no inner scrollbar at normal size.
          Card grows with content; page/browser scroll only when zoomed or
          content truly exceeds the viewport.
        */}
        <div
          ref={slideRef}
          className={clsx("px-5 py-4 sm:px-6 sm:py-5", animClass)}
        >
          {isReviewSlide ? (
            <div className="mx-auto max-w-2xl space-y-4">
              {showResult && passed && (
                <div className="overflow-hidden rounded-2xl border border-emerald-400/40 bg-gradient-to-br from-emerald-50 to-cyan-50 p-5 shadow-elevated dark:from-emerald-500/15 dark:to-cyan-500/10 animate-fade-up">
                  <div className="flex items-start gap-3">
                    <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-emerald-500 text-white shadow-soft">
                      <Sparkles className="h-5 w-5" />
                    </span>
                    <div>
                      <p className="text-base font-bold text-emerald-800 dark:text-emerald-300">
                        You passed with {score}%!
                      </p>
                      {completionAction ? (
                        <>
                          <p className="mt-1 text-sm text-emerald-700/80 dark:text-emerald-200/80">
                            Great work — that finishes this module.
                          </p>
                          <div className="mt-4">{completionAction}</div>
                        </>
                      ) : (
                        <p className="mt-1 text-sm text-emerald-700/80 dark:text-emerald-200/80">
                          Great work. This {label.toLowerCase()} is complete. Taking you to
                          progress…
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {showResult && score !== null && !passed && (
                <div className="rounded-2xl border border-amber-400/40 bg-amber-50/80 p-5 dark:bg-amber-500/10 animate-fade-up">
                  <p className="flex items-center gap-2 text-base font-bold text-amber-800 dark:text-amber-200">
                    <XCircle className="h-5 w-5" />
                    Score: {score}%
                  </p>
                  <p className="mt-2 text-sm text-amber-700/90 dark:text-amber-200/80">
                    You need {passScore}% to pass. Use Back to revisit questions, or retry from
                    the start.
                  </p>
                </div>
              )}

              {!showResult && (
                <>
                  <p className="text-sm text-craft-muted">
                    You&apos;ve answered{" "}
                    <span className="font-semibold text-craft-ink">
                      {answeredCount} of {bank.length}
                    </span>{" "}
                    questions. You need{" "}
                    <span className="font-semibold text-craft-ink">{passScore}%</span> or higher
                    to pass.
                  </p>

                  {/* Compact question checklist — no full re-render of options */}
                  <ul className="space-y-2">
                    {bank.map((q, i) => {
                      const answered = typeof answers[q.id] === "number";
                      return (
                        <li key={q.id}>
                          <button
                            type="button"
                            onClick={() => {
                              setAnimClass("slide-enter-back");
                              requestAnimationFrame(() => {
                                requestAnimationFrame(() => {
                                  setAnimClass("slide-active");
                                  setCurrentIndex(i);
                                  slideRef.current?.scrollTo({ top: 0, behavior: "instant" });
                                });
                              });
                            }}
                            className={clsx(
                              "flex w-full items-center gap-3 rounded-xl border px-4 py-3 text-left text-sm transition",
                              answered
                                ? "border-emerald-300/60 bg-emerald-50/50 dark:border-emerald-500/30 dark:bg-emerald-500/10"
                                : "border-craft-border bg-craft-surface hover:border-craft-faint"
                            )}
                          >
                            <span
                              className={clsx(
                                "inline-flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-semibold",
                                answered
                                  ? "bg-emerald-500 text-white"
                                  : "border border-craft-faint text-craft-faint"
                              )}
                            >
                              {answered ? <CheckCircle2 className="h-3.5 w-3.5" /> : i + 1}
                            </span>
                            <span className="line-clamp-1 text-craft-ink">{q.prompt}</span>
                          </button>
                        </li>
                      );
                    })}
                  </ul>
                </>
              )}

              {showResult && score !== null && (
                <p
                  className={clsx(
                    "flex items-center gap-2 text-sm font-medium",
                    passed
                      ? "text-emerald-700 dark:text-emerald-300"
                      : "text-amber-700 dark:text-amber-300"
                  )}
                >
                  {passed ? (
                    <CheckCircle2 className="h-4 w-4" />
                  ) : (
                    <XCircle className="h-4 w-4" />
                  )}
                  Score: {score}%. {passed ? `Passed (at least ${passScore}%).` : `Need ${passScore}% to pass.`}
                </p>
              )}

              <div className="flex flex-wrap gap-3">
                {!passed && !showResult && (
                  <button
                    type="button"
                    disabled={!allAnswered}
                    onClick={submit}
                    className="btn-primary"
                  >
                    {`Submit ${label}`}
                  </button>
                )}
                {showResult && !passed && (
                  <button type="button" onClick={reset} className="btn-secondary">
                    <RotateCcw className="h-4 w-4" />
                    Retry {label.toLowerCase()}
                  </button>
                )}
                {previouslyPassed && showResult && passed && (
                  <button
                    type="button"
                    onClick={() => setPhase("completed")}
                    className="btn-secondary"
                  >
                    Done reviewing
                  </button>
                )}
              </div>
            </div>
          ) : currentQuestion ? (
            <div className="mx-auto max-w-2xl space-y-4">
              <p className="text-base font-medium leading-relaxed text-craft-ink sm:text-lg">
                <span className="mr-2 text-craft-faint">{currentIndex + 1}.</span>
                {currentQuestion.prompt}
              </p>
              <ul className="space-y-2">
                {currentQuestion.options.map((option, index) => {
                  const chosen = answers[currentQuestion.id] === index;
                  const isCorrect = index === currentQuestion.answer_index;
                  return (
                    <li key={`${currentQuestion.id}-${index}`}>
                      <button
                        type="button"
                        disabled={passed}
                        onClick={() => selectAnswer(currentQuestion.id, index)}
                        className={clsx(
                          "w-full rounded-xl border px-4 py-3 text-left text-sm transition sm:text-base",
                          chosen &&
                            !showResult &&
                            "border-cyan-400 bg-craft-accent-soft text-craft-ink ring-1 ring-cyan-400/30",
                          showResult &&
                            chosen &&
                            isCorrect &&
                            "border-emerald-400 bg-emerald-50 text-emerald-800 dark:bg-emerald-500/15 dark:text-emerald-200",
                          showResult &&
                            chosen &&
                            !isCorrect &&
                            "border-amber-400 bg-amber-50 text-amber-800 dark:bg-amber-500/15 dark:text-amber-200",
                          showResult &&
                            !chosen &&
                            isCorrect &&
                            "border-emerald-300 bg-emerald-50/70 dark:bg-emerald-500/10",
                          !chosen &&
                            !showResult &&
                            "border-craft-border bg-craft-surface hover:border-cyan-400/50 hover:bg-craft-soft"
                        )}
                      >
                        {option}
                      </button>
                    </li>
                  );
                })}
              </ul>
              {!currentAnswered && !reviewing && (
                <p className="text-xs text-craft-faint">
                  Select an answer to continue to the next question.
                </p>
              )}
              {reviewing && (
                <p className="text-xs text-craft-faint">
                  The correct answer is highlighted. Use Next and Back to page through.
                </p>
              )}
              {/* After submission, say WHY the right answer is right and which
                  lesson teaches it — never a bare score (plan §6). */}
              {showResult && currentQuestion.explanation && (
                <div className="rounded-xl bg-craft-soft px-4 py-3 text-sm text-craft-ink ring-1 ring-craft-border">
                  {currentQuestion.explanation}
                </div>
              )}
            </div>
          ) : null}
        </div>

        {/* Footer navigation — same chrome as the lesson player */}
        <div className="flex shrink-0 items-center justify-between gap-3 border-t border-craft-border bg-craft-surface/90 px-5 py-2.5 backdrop-blur-sm sm:px-6">
          <button
            type="button"
            onClick={() => navigate("back")}
            disabled={currentIndex === 0}
            className="btn-secondary flex items-center gap-1.5 disabled:pointer-events-none disabled:opacity-40"
          >
            <ChevronLeft className="h-4 w-4" />
            Back
          </button>

          {/* Progress dots for quick orientation */}
          <div
            className="hidden max-w-[40%] flex-wrap items-center justify-center gap-1.5 sm:flex"
            aria-hidden
          >
            {Array.from({ length: totalSlides }, (_, i) => {
              const isQ = i < bank.length;
              const qAnswered = isQ && typeof answers[bank[i].id] === "number";
              return (
                <span
                  key={i}
                  className={clsx(
                    "h-1.5 w-1.5 rounded-full transition",
                    i === currentIndex
                      ? "w-4 bg-cyan-500"
                      : qAnswered
                        ? "bg-emerald-400"
                        : i === reviewIndex
                          ? "bg-craft-faint/60"
                          : "bg-craft-border"
                  )}
                />
              );
            })}
          </div>

          {isReviewSlide ? (
            !passed && !showResult ? (
              <button
                type="button"
                disabled={!allAnswered}
                onClick={submit}
                className="btn-primary flex items-center gap-1.5 disabled:pointer-events-none disabled:opacity-40"
              >
                {`Submit ${label}`}
              </button>
            ) : showResult && !passed ? (
              <button type="button" onClick={reset} className="btn-secondary flex items-center gap-1.5">
                <RotateCcw className="h-4 w-4" />
                Retry
              </button>
            ) : (
              <span className="min-w-[5rem]" />
            )
          ) : (
            <button
              type="button"
              onClick={() => navigate("forward")}
              disabled={!currentAnswered && !reviewing}
              className="btn-primary flex items-center gap-1.5 disabled:pointer-events-none disabled:opacity-40"
            >
              {nextLabel}
              <ChevronRight className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
