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
  /**
   * Link back to the lesson content, shown on the standing-result card. The
   * Progress step used to host "Review lesson"; it lives here now.
   */
  reviewLessonHref?: string;
  /**
   * Leave without passing. Shown while the learner is still in an attempt —
   * skipping must not call onPassed, so it never counts toward certificates
   * or badges.
   */
  skipAction?: React.ReactNode;
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
  reviewLessonHref,
  skipAction,
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
                {reviewLessonHref && (
                  <a href={reviewLessonHref} className="btn-secondary">
                    Review lesson
                  </a>
                )}
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
    <div className="flex h-full min-h-0 flex-col">
      <ConfettiBurst active={showConfetti} />

      <div className="card flex min-h-0 flex-1 flex-col overflow-hidden">
        {/* Header: title + step counter */}
        <div className="flex shrink-0 items-center justify-between gap-2 border-b border-craft-border px-3 py-2 sm:gap-3 sm:px-6 sm:py-3.5">
          <div className="flex min-w-0 items-center gap-1.5 sm:gap-2">
            <span className="shrink-0 text-violet-600 dark:text-violet-400">
              <ClipboardCheck className="h-4 w-4" />
            </span>
            <h2 className="truncate text-sm font-bold text-craft-ink sm:text-lg">{slideTitle}</h2>
          </div>
          <span className="shrink-0 whitespace-nowrap text-[10px] font-medium uppercase tracking-[0.14em] text-craft-faint sm:text-sm">
            {isReviewSlide ? "Review" : `${currentIndex + 1} / ${bank.length}`}
          </span>
        </div>

        {/*
          Slide body fills remaining card height; content stays readable with
          generous padding that scales up on larger screens.
        */}
        <div
          ref={slideRef}
          className={clsx(
            "min-h-0 flex-1 overflow-y-auto overscroll-contain scrollbar-hide px-3 py-3 sm:px-8 sm:py-8 lg:px-10 lg:py-10",
            animClass
          )}
        >
          {isReviewSlide ? (
            <div className="mx-auto max-w-3xl space-y-4 sm:space-y-5">
              {showResult && passed && (
                <div className="overflow-hidden rounded-2xl border border-emerald-400/40 bg-gradient-to-br from-emerald-50 to-violet-50 p-5 shadow-elevated dark:from-emerald-500/15 dark:to-violet-500/10 animate-fade-up">
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
                            {`Great work. This ${label.toLowerCase()} is complete.`}
                          </p>
                          {/* The forward action lives here now — nothing
                              auto-navigates off the learner's own result. */}
                          <div className="mt-4">{completionAction}</div>
                        </>
                      ) : (
                        <p className="mt-1 text-sm text-emerald-700/80 dark:text-emerald-200/80">
                          {`Great work. This ${label.toLowerCase()} is complete.`}
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
                {/*
                  A passed result offers exactly two things: the forward action
                  (inside the pass card above) and a deliberate retake. There is
                  no "Done reviewing" — Back already pages to the questions, so
                  a button whose only job is "stop looking" was one more thing
                  to read for no new destination.
                */}
                {showResult && passed && (
                  <button
                    type="button"
                    onClick={reset}
                    className="inline-flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm font-medium text-craft-muted transition hover:bg-craft-soft hover:text-craft-ink"
                  >
                    <RotateCcw className="h-4 w-4" />
                    Retake {label.toLowerCase()}
                  </button>
                )}
              </div>
            </div>
          ) : currentQuestion ? (
            <div className="mx-auto flex h-full max-w-3xl flex-col justify-center space-y-3 sm:space-y-6 lg:space-y-7">
              <p className="text-sm font-medium leading-snug text-craft-ink sm:text-xl sm:leading-relaxed lg:text-2xl">
                <span className="mr-1.5 text-craft-faint sm:mr-2">{currentIndex + 1}.</span>
                {currentQuestion.prompt}
              </p>
              <ul className="space-y-2 sm:space-y-3.5">
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
                          "w-full rounded-xl border px-3 py-2.5 text-left text-xs transition sm:px-5 sm:py-4 sm:text-base lg:text-lg",
                          chosen &&
                            !showResult &&
                            "border-violet-400 bg-craft-accent-soft text-craft-ink ring-1 ring-violet-400/30",
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
                            "border-craft-border bg-craft-surface hover:border-violet-400/50 hover:bg-craft-soft"
                        )}
                      >
                        {option}
                      </button>
                    </li>
                  );
                })}
              </ul>
              {!currentAnswered && !reviewing && (
                <p className="text-[11px] text-craft-faint sm:text-sm">
                  Select an answer, or Next / Skip to move on.
                </p>
              )}
              {reviewing && (
                <p className="text-[11px] text-craft-faint sm:text-sm">
                  The correct answer is highlighted. Use Next and Back to page through.
                </p>
              )}
              {showResult && currentQuestion.explanation && (
                <div className="rounded-xl bg-craft-soft px-3 py-2.5 text-xs text-craft-ink ring-1 ring-craft-border sm:px-5 sm:py-4 sm:text-base">
                  {currentQuestion.explanation}
                </div>
              )}
            </div>
          ) : null}
        </div>

        {/* Footer — single compact row so it always fits on phone */}
        <div className="flex shrink-0 items-center gap-1.5 border-t border-craft-border bg-craft-surface/95 px-2.5 py-2 sm:gap-3 sm:px-6 sm:py-3">
          <button
            type="button"
            onClick={() => navigate("back")}
            disabled={currentIndex === 0}
            className="btn-secondary min-h-[36px] flex-1 px-2 text-xs disabled:pointer-events-none disabled:opacity-40 sm:min-h-[44px] sm:flex-none sm:px-5 sm:text-sm"
          >
            <ChevronLeft className="h-4 w-4 shrink-0" />
            <span className="sm:inline">Back</span>
          </button>

          {skipAction && !previouslyPassed && !(showResult && passed) ? (
            <div
              className="min-w-0 flex-[1.2] text-center text-[11px] font-semibold text-craft-muted [&_a]:inline-flex [&_a]:max-w-full [&_a]:items-center [&_a]:justify-center [&_a]:gap-0.5 [&_a]:truncate [&_a]:px-1 [&_a]:py-2 [&_a]:text-craft-muted hover:[&_a]:text-violet-600 dark:hover:[&_a]:text-violet-400 sm:text-sm"
              title="Skipping does not count toward your certificate or badges"
            >
              {skipAction}
            </div>
          ) : (
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
                        ? "w-4 bg-violet-500"
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
          )}

          {isReviewSlide ? (
            !passed && !showResult ? (
              <button
                type="button"
                disabled={!allAnswered}
                onClick={submit}
                className="btn-primary min-h-[36px] flex-1 px-2 text-xs disabled:pointer-events-none disabled:opacity-40 sm:min-h-[44px] sm:flex-none sm:px-5 sm:text-sm"
              >
                Submit
              </button>
            ) : showResult && !passed ? (
              <button
                type="button"
                onClick={reset}
                className="btn-secondary min-h-[36px] flex-1 px-2 text-xs sm:min-h-[44px] sm:flex-none sm:px-5 sm:text-sm"
              >
                <RotateCcw className="h-4 w-4" />
                Retry
              </button>
            ) : (
              <span className="min-w-[3rem] flex-1 sm:flex-none" />
            )
          ) : (
            <button
              type="button"
              onClick={() => navigate("forward")}
              className="btn-primary min-h-[36px] flex-1 px-2 text-xs sm:min-h-[44px] sm:flex-none sm:px-5 sm:text-sm"
            >
              {nextLabel}
              <ChevronRight className="h-4 w-4 shrink-0" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
