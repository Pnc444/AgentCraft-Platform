"use client";

import { useMemo, useState } from "react";
import { CheckCircle2, RotateCcw, XCircle } from "lucide-react";
import clsx from "clsx";

export interface CheckpointQuestion {
  id: string;
  prompt: string;
  options: string[];
  answer_index: number;
}

interface CheckpointQuizProps {
  questions: CheckpointQuestion[];
  onPassed?: () => void;
}

function pickRandom(questions: CheckpointQuestion[]): CheckpointQuestion | null {
  if (!questions.length) return null;
  return questions[Math.floor(Math.random() * questions.length)] ?? null;
}

/** Random single-question checkpoint with unlimited retries. */
export function CheckpointQuiz({ questions, onPassed }: CheckpointQuizProps) {
  const bank = useMemo(
    () => questions.filter((q) => q.options?.length && typeof q.answer_index === "number"),
    [questions]
  );

  const [question, setQuestion] = useState<CheckpointQuestion | null>(() => pickRandom(bank));
  const [selected, setSelected] = useState<number | null>(null);
  const [revealed, setRevealed] = useState(false);
  const [passed, setPassed] = useState(false);

  function nextQuestion() {
    setSelected(null);
    setRevealed(false);
    setQuestion(pickRandom(bank));
  }

  function submit() {
    if (selected === null || !question) return;
    setRevealed(true);
    if (selected === question.answer_index) {
      setPassed(true);
      onPassed?.();
    }
  }

  if (!bank.length) {
    return <p className="text-sm text-craft-muted">—</p>;
  }

  if (!question) {
    return <p className="text-sm text-craft-muted">No checkpoint question available.</p>;
  }

  const isCorrect = revealed && selected === question.answer_index;
  const isWrong = revealed && selected !== null && selected !== question.answer_index;

  return (
    <div className="space-y-4">
      <p className="text-sm text-craft-muted">
        Answer correctly to pass. You can retry as many times as you need.
      </p>

      <p className="text-base font-medium text-craft-ink">{question.prompt}</p>

      <ul className="space-y-2">
        {question.options.map((option, index) => {
          const chosen = selected === index;
          return (
            <li key={`${question.id}-${index}`}>
              <button
                type="button"
                disabled={revealed && passed}
                onClick={() => {
                  if (revealed && passed) return;
                  setSelected(index);
                  setRevealed(false);
                }}
                className={clsx(
                  "w-full rounded-xl border px-4 py-3 text-left text-sm transition",
                  chosen && !revealed && "border-cyan-400 bg-craft-accent-soft text-craft-ink",
                  chosen && isCorrect && "border-emerald-400 bg-emerald-50 text-emerald-800",
                  chosen && isWrong && "border-amber-400 bg-amber-50 text-amber-800",
                  !chosen && "border-craft-border bg-craft-surface text-craft-ink hover:border-craft-border",
                  revealed &&
                    index === question.answer_index &&
                    !chosen &&
                    "border-emerald-300 bg-emerald-50/70"
                )}
              >
                {option}
              </button>
            </li>
          );
        })}
      </ul>

      {isCorrect && (
        <p className="flex items-center gap-2 text-sm font-medium text-emerald-700">
          <CheckCircle2 className="h-4 w-4" /> Correct — checkpoint passed.
        </p>
      )}
      {isWrong && (
        <p className="flex items-center gap-2 text-sm font-medium text-amber-700">
          <XCircle className="h-4 w-4" /> Not quite — try again anytime.
        </p>
      )}

      <div className="flex flex-wrap gap-3">
        {!passed && (
          <button
            type="button"
            disabled={selected === null}
            onClick={submit}
            className="btn-primary"
          >
            Check answer
          </button>
        )}
        <button type="button" onClick={nextQuestion} className="btn-secondary">
          <RotateCcw className="h-4 w-4" />
          {passed ? "Try another question" : "New question"}
        </button>
      </div>
    </div>
  );
}
