"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { CheckCircle2, RotateCcw, Sparkles, XCircle } from "lucide-react";
import clsx from "clsx";
import type { CheckpointQuestion } from "@/components/lessons/CheckpointQuiz";
import { ConfettiBurst } from "@/components/lessons/ConfettiBurst";

interface RecapQuizProps {
  questions: CheckpointQuestion[];
  passScore?: number;
  onPassed?: (score: number) => void;
  locked?: boolean;
  lockedReason?: string;
  onLockedAction?: () => void;
  label?: string;
}

const PASS_SCORE = 80;
const CELEBRATE_MS = 2200;

type Phase = "answering" | "result";

/** Multi-question recap quiz — pass with PASS_SCORE% or higher. */
export function RecapQuiz({
  questions,
  passScore = PASS_SCORE,
  onPassed,
  locked = false,
  lockedReason,
  onLockedAction,
  label = "Recap Quiz",
}: RecapQuizProps) {
  const bank = useMemo(
    () => questions.filter((q) => q.options?.length && typeof q.answer_index === "number"),
    [questions]
  );

  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [phase, setPhase] = useState<Phase>("answering");
  const [score, setScore] = useState<number | null>(null);
  const [passed, setPassed] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const notifiedPass = useRef(false);
  const onPassedRef = useRef(onPassed);
  onPassedRef.current = onPassed;

  useEffect(() => {
    if (phase !== "result" || !passed || score === null || notifiedPass.current) return;
    const t = window.setTimeout(() => {
      notifiedPass.current = true;
      onPassedRef.current?.(score);
    }, CELEBRATE_MS);
    return () => window.clearTimeout(t);
  }, [phase, passed, score]);

  function reset() {
    setAnswers({});
    setPhase("answering");
    setScore(null);
    setPassed(false);
    setShowConfetti(false);
    notifiedPass.current = false;
  }

  function submit() {
    if (!bank.length || locked || passed) return;
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
  }

  if (!bank.length) {
    return (
      <p className="text-sm text-craft-muted">
        No {label.toLowerCase()} questions are configured for this lesson yet. Add them in the admin panel
        under the lesson’s quiz / sandbox config.
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

  const allAnswered = bank.every((q) => typeof answers[q.id] === "number");
  const showResult = phase === "result";

  return (
    <div className="relative space-y-5">
      <ConfettiBurst active={showConfetti} />

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
                Great work. This lesson is complete. Taking you to progress…
              </p>
            </div>
          </div>
        </div>
      )}

      <p className="text-sm text-craft-muted">
        Answer every question. You need <span className="font-semibold text-craft-ink">{passScore}%</span>{" "}
        or higher to complete this lesson.
      </p>

      {bank.map((question, qi) => {
        const selected = answers[question.id];
        return (
          <div
            key={question.id}
            className="space-y-2 rounded-xl border border-craft-border bg-craft-surface p-4 shadow-soft ring-1 ring-craft-border/40"
          >
            <p className="text-sm font-medium text-craft-ink">
              <span className="mr-2 text-craft-faint">{qi + 1}.</span>
              {question.prompt}
            </p>
            <ul className="space-y-2">
              {question.options.map((option, index) => {
                const chosen = selected === index;
                const isCorrect = index === question.answer_index;
                return (
                  <li key={`${question.id}-${index}`}>
                    <button
                      type="button"
                      disabled={passed}
                      onClick={() => {
                        if (passed) return;
                        setAnswers((prev) => ({ ...prev, [question.id]: index }));
                        if (showResult) {
                          setPhase("answering");
                          setScore(null);
                          setPassed(false);
                          setShowConfetti(false);
                        }
                      }}
                      className={clsx(
                        "w-full rounded-xl border px-4 py-3 text-left text-sm transition",
                        chosen && !showResult && "border-cyan-400 bg-craft-accent-soft text-craft-ink",
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
                          "border-craft-border bg-craft-surface hover:border-craft-border"
                      )}
                    >
                      {option}
                    </button>
                  </li>
                );
              })}
            </ul>
          </div>
        );
      })}

      {showResult && score !== null && !passed && (
        <p className="flex items-center gap-2 text-sm font-medium text-amber-700 dark:text-amber-300 animate-fade-up">
          <XCircle className="h-4 w-4" />
          Score: {score}%. You need {passScore}% to pass. Try again.
        </p>
      )}

      {showResult && passed && score !== null && (
        <p className="flex items-center gap-2 text-sm font-medium text-emerald-700 dark:text-emerald-300">
          <CheckCircle2 className="h-4 w-4" />
          Score: {score}%. Passed (at least {passScore}%).
        </p>
      )}

      <div className="flex flex-wrap gap-3">
        {!passed && (
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
            Retry quiz
          </button>
        )}
      </div>
    </div>
  );
}
