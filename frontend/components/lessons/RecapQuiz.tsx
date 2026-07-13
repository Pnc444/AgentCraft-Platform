"use client";

import { useMemo, useState } from "react";
import { CheckCircle2, RotateCcw, XCircle } from "lucide-react";
import clsx from "clsx";
import type { CheckpointQuestion } from "@/components/lessons/CheckpointQuiz";

interface RecapQuizProps {
  questions: CheckpointQuestion[];
  passScore?: number;
  onPassed?: (score: number) => void;
  locked?: boolean;
  lockedReason?: string;
  onLockedAction?: () => void;
}

const PASS_SCORE = 80;

/** Multi-question recap quiz — pass with PASS_SCORE% or higher. */
export function RecapQuiz({
  questions,
  passScore = PASS_SCORE,
  onPassed,
  locked = false,
  lockedReason,
  onLockedAction,
}: RecapQuizProps) {
  const bank = useMemo(
    () => questions.filter((q) => q.options?.length && typeof q.answer_index === "number"),
    [questions]
  );

  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState<number | null>(null);
  const [passed, setPassed] = useState(false);

  function reset() {
    setAnswers({});
    setSubmitted(false);
    setScore(null);
    setPassed(false);
  }

  function submit() {
    if (!bank.length || locked) return;
    let correct = 0;
    for (const q of bank) {
      if (answers[q.id] === q.answer_index) correct += 1;
    }
    const pct = Math.round((correct / bank.length) * 100);
    setScore(pct);
    setSubmitted(true);
    if (pct >= passScore) {
      setPassed(true);
      onPassed?.(pct);
    }
  }

  if (!bank.length) {
    return (
      <p className="text-sm text-slate-500">
        No recap quiz questions are configured for this lesson yet. Add them in the admin panel
        under the lesson’s quiz / sandbox config.
      </p>
    );
  }

  if (locked) {
    return (
      <div className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">
        <p>{lockedReason || "Finish the required steps before taking the Recap Quiz."}</p>
        {onLockedAction && (
          <button type="button" onClick={onLockedAction} className="btn-secondary mt-3 text-xs">
            Take me there
          </button>
        )}
      </div>
    );
  }

  const allAnswered = bank.every((q) => typeof answers[q.id] === "number");

  return (
    <div className="space-y-5">
      <p className="text-sm text-slate-500">
        Answer every question. You need <span className="font-semibold text-slate-700">{passScore}%</span>{" "}
        or higher to complete this lesson.
      </p>

      {bank.map((question, qi) => {
        const selected = answers[question.id];
        return (
          <div key={question.id} className="space-y-2 rounded-xl border border-slate-200/80 bg-white p-4 shadow-soft ring-1 ring-black/[0.02]">
            <p className="text-sm font-medium text-slate-900">
              <span className="mr-2 text-slate-400">{qi + 1}.</span>
              {question.prompt}
            </p>
            <ul className="space-y-2">
              {question.options.map((option, index) => {
                const chosen = selected === index;
                const showResult = submitted;
                const isCorrect = index === question.answer_index;
                return (
                  <li key={`${question.id}-${index}`}>
                    <button
                      type="button"
                      disabled={passed}
                      onClick={() => {
                        if (passed) return;
                        setAnswers((prev) => ({ ...prev, [question.id]: index }));
                        if (submitted) {
                          setSubmitted(false);
                          setScore(null);
                        }
                      }}
                      className={clsx(
                        "w-full rounded-xl border px-4 py-3 text-left text-sm transition",
                        chosen && !showResult && "border-cyan-400 bg-cyan-50 text-slate-900",
                        showResult &&
                          chosen &&
                          isCorrect &&
                          "border-emerald-400 bg-emerald-50 text-emerald-800",
                        showResult &&
                          chosen &&
                          !isCorrect &&
                          "border-amber-400 bg-amber-50 text-amber-800",
                        showResult &&
                          !chosen &&
                          isCorrect &&
                          "border-emerald-300 bg-emerald-50/70",
                        !chosen && !showResult && "border-slate-200 bg-white hover:border-slate-300"
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

      {submitted && score !== null && (
        <p
          className={clsx(
            "flex items-center gap-2 text-sm font-medium",
            passed ? "text-emerald-700" : "text-amber-700"
          )}
        >
          {passed ? <CheckCircle2 className="h-4 w-4" /> : <XCircle className="h-4 w-4" />}
          Score: {score}%{" "}
          {passed
            ? `— passed (≥ ${passScore}%). Lesson complete.`
            : `— need ${passScore}% to pass. Try again.`}
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
            Submit Recap Quiz
          </button>
        )}
        {submitted && !passed && (
          <button type="button" onClick={reset} className="btn-secondary">
            <RotateCcw className="h-4 w-4" />
            Retry quiz
          </button>
        )}
      </div>
    </div>
  );
}
