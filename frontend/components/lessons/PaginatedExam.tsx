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
import type { CheckpointQuestion } from "@/components/lessons/CheckpointQuiz";
import { ConfettiBurst } from "@/components/lessons/ConfettiBurst";

interface PaginatedExamProps {
  questions: CheckpointQuestion[];
  passScore?: number;
  onPassed?: (score: number) => void;
  locked?: boolean;
  lockedReason?: string;
  onLockedAction?: () => void;
  label?: string;
}

const DEFAULT_PASS_SCORE = 80;
const CELEBRATE_MS = 2200;

type Phase = "answering" | "result";

/**
 * One-question-per-slide assessment UI (Module 1 Exam + recap quizzes).
 * Mirrors PaginatedLessonContent: fixed viewport card, step counter,
 * Back/Next footer — designed so neurodivergent students never face a
 * long scrolling wall of questions.
 */
export function PaginatedExam({
  questions,
  passScore = DEFAULT_PASS_SCORE,
  onPassed,
  locked = false,
  lockedReason,
  onLockedAction,
  label = "Exam",
}: PaginatedExamProps) {
  const bank = useMemo(
    () => questions.filter((q) => q.options?.length && typeof q.answer_index === "number"),
    [questions]
  );

  // Question slides (0..n-1) + one final review/results slide (n)
  const totalSlides = bank.length + 1;
  const reviewIndex = bank.length;

  const [currentIndex, setCurrentIndex] = useState(0);
  const [animClass, setAnimClass] = useState<"slide-active" | "slide-enter" | "slide-enter-back">(
    "slide-active"
  );
  const slideRef = useRef<HTMLDivElement>(null);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [phase, setPhase] = useState<Phase>("answering");
  const [score, setScore] = useState<number | null>(null);
  const [passed, setPassed] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const notifiedPass = useRef(false);
  const onPassedRef = useRef(onPassed);
  onPassedRef.current = onPassed;

  const showResult = phase === "result";
  const isReviewSlide = currentIndex === reviewIndex;
  const currentQuestion = !isReviewSlide ? bank[currentIndex] : null;
  const currentAnswered =
    !!currentQuestion && typeof answers[currentQuestion.id] === "number";
  const allAnswered = bank.every((q) => typeof answers[q.id] === "number");
  const answeredCount = bank.filter((q) => typeof answers[q.id] === "number").length;

  function navigate(direction: "forward" | "back") {
    if (direction === "forward" && currentIndex >= totalSlides - 1) return;
    if (direction === "back" && currentIndex <= 0) return;
    // Soft gate: must answer the current question before Next
    if (direction === "forward" && !isReviewSlide && !currentAnswered) return;

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
  }, [currentIndex, totalSlides, currentAnswered, isReviewSlide]);

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
              {answeredCount}/{bank.length} answered
            </span>
            <span className="text-xs font-medium uppercase tracking-[0.18em] text-craft-faint">
              Step {currentIndex + 1} / {totalSlides}
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
                      <p className="mt-1 text-sm text-emerald-700/80 dark:text-emerald-200/80">
                        Great work. This {label.toLowerCase()} is complete. Taking you to
                        progress…
                      </p>
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
              {!currentAnswered && (
                <p className="text-xs text-craft-faint">
                  Select an answer to continue to the next question.
                </p>
              )}
            </div>
          ) : null}
        </div>

        {/* Footer navigation — same chrome as PaginatedLessonContent */}
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
              disabled={!currentAnswered}
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
