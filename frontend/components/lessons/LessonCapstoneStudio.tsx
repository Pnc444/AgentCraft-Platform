"use client";

import { useEffect, useMemo, useState } from "react";
import { CheckCircle2, ClipboardCheck, ShieldAlert, Sparkles } from "lucide-react";
import clsx from "clsx";
import { findInteraction } from "@/lib/lesson-interactions";
import type { CapstoneAssignment, LessonInteraction } from "@/types";

interface LessonCapstoneStudioProps {
  assignment: CapstoneAssignment;
  evaluationRubric: Array<{ criterion: string; weight: number; description: string }>;
  evaluationCases: Array<{ name: string; goal: string; expected: string }>;
  interactionLog: LessonInteraction[];
  onRecordInteraction: (event: {
    type: string;
    key: string;
    status?: string;
    details?: Record<string, unknown>;
  }) => void;
}

type ReviewState = Record<string, boolean>;
type SubmissionState = Record<string, string>;

function initializeSubmission(
  assignment: CapstoneAssignment,
  interactionLog: LessonInteraction[]
): SubmissionState {
  const saved = findInteraction(interactionLog, "capstone:submission")?.details?.submission;
  if (!saved || typeof saved !== "object") {
    return Object.fromEntries(assignment.sections.map((section) => [section.key, ""]));
  }

  return Object.fromEntries(
    assignment.sections.map((section) => [
      section.key,
      typeof (saved as Record<string, unknown>)[section.key] === "string"
        ? ((saved as Record<string, unknown>)[section.key] as string)
        : "",
    ])
  );
}

function initializeReview(
  assignment: CapstoneAssignment,
  interactionLog: LessonInteraction[]
): ReviewState {
  const saved = findInteraction(interactionLog, "capstone:review")?.details?.review;
  if (!saved || typeof saved !== "object") {
    return Object.fromEntries(assignment.review_questions.map((_, index) => [`review-${index}`, false]));
  }

  return Object.fromEntries(
    assignment.review_questions.map((_, index) => [
      `review-${index}`,
      Boolean((saved as Record<string, unknown>)[`review-${index}`]),
    ])
  );
}

export function LessonCapstoneStudio({
  assignment,
  evaluationRubric,
  evaluationCases,
  interactionLog,
  onRecordInteraction,
}: LessonCapstoneStudioProps) {
  const [submission, setSubmission] = useState<SubmissionState>(() =>
    initializeSubmission(assignment, interactionLog)
  );
  const [reviewChecks, setReviewChecks] = useState<ReviewState>(() =>
    initializeReview(assignment, interactionLog)
  );
  const savedStatus = findInteraction(interactionLog, "capstone:result")?.status;

  useEffect(() => {
    setSubmission(initializeSubmission(assignment, interactionLog));
    setReviewChecks(initializeReview(assignment, interactionLog));
  }, [assignment, interactionLog]);

  const verifier = useMemo(() => {
    const riskyPhrases = assignment.risky_phrases || [];
    const checks = assignment.sections.map((section) => {
      const value = (submission[section.key] || "").trim();
      const minLength = section.min_length || 0;
      const requiredKeywords = section.required_keywords || [];
      const missingKeywords = requiredKeywords.filter(
        (keyword) => !value.toLowerCase().includes(keyword.toLowerCase())
      );

      return {
        key: section.key,
        label: section.label,
        passed: value.length >= minLength && missingKeywords.length === 0,
        issues: [
          ...(value.length >= minLength ? [] : [`Needs at least ${minLength} characters`]),
          ...missingKeywords.map((keyword) => `Missing keyword or idea: ${keyword}`),
        ],
      };
    });

    const riskyHits = assignment.sections.flatMap((section) => {
      const value = (submission[section.key] || "").toLowerCase();
      return riskyPhrases.filter((phrase) => value.includes(phrase.toLowerCase()));
    });

    const reviewComplete = assignment.review_questions.every((_, index) => reviewChecks[`review-${index}`]);
    const passedChecks = checks.every((check) => check.passed);
    const status = riskyHits.length ? "stop" : passedChecks && reviewComplete ? "pass" : "revise";

    const rubricScores = evaluationRubric.map((criterion) => {
      const normalized = criterion.criterion.toLowerCase();
      let earned = 0;
      if (normalized.includes("helpful") && submission.goal?.trim() && submission.actions?.trim()) earned = criterion.weight;
      if (normalized.includes("truth") && submission.evidence?.toLowerCase().includes("receipt")) earned = criterion.weight;
      if (normalized.includes("harm") && submission.guardrails?.trim() && submission.permissions?.trim()) earned = criterion.weight;
      if (normalized.includes("evaluation") && submission.evidence?.toLowerCase().includes("verifier")) earned = criterion.weight;
      if (normalized.includes("operational") && submission.review_boundary?.trim()) earned = criterion.weight;
      return { ...criterion, earned };
    });

    return { checks, riskyHits, reviewComplete, status, rubricScores };
  }, [assignment, evaluationRubric, reviewChecks, submission]);
  const finalStatus = savedStatus ?? verifier.status;

  function saveDraft() {
    onRecordInteraction({
      type: "capstone_submission",
      key: "capstone:submission",
      status: "saved",
      details: { submission },
    });
    onRecordInteraction({
      type: "capstone_review",
      key: "capstone:review",
      status: "saved",
      details: { review: reviewChecks },
    });
  }

  function runVerifier() {
    saveDraft();
    onRecordInteraction({
      type: "capstone_result",
      key: "capstone:result",
      status: verifier.status,
      details: {
        submission,
        checks: verifier.checks,
        risky_hits: verifier.riskyHits,
        review_complete: verifier.reviewComplete,
        rubric_scores: verifier.rubricScores,
      },
    });
  }

  return (
    <div className="space-y-4 rounded-2xl border border-craft-border bg-craft-surface p-5 shadow-soft">
      <div>
        <p className="text-sm font-semibold text-craft-ink">{assignment.title}</p>
        <p className="mt-1 text-sm text-craft-muted">{assignment.summary}</p>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        {assignment.sections.map((section) => (
          <label key={section.key} className="space-y-2">
            <span className="text-sm font-semibold text-craft-ink">{section.label}</span>
            <p className="text-sm text-craft-muted">{section.prompt}</p>
            <textarea
              value={submission[section.key] || ""}
              onChange={(event) =>
                setSubmission((prev) => ({ ...prev, [section.key]: event.target.value }))
              }
              placeholder={section.placeholder}
              className="min-h-[140px] w-full rounded-xl border border-craft-border bg-craft-soft/60 px-3 py-3 text-sm text-craft-ink shadow-soft focus:border-cyan-500 focus:outline-none"
            />
          </label>
        ))}
      </div>

      <div className="rounded-xl border border-craft-border bg-craft-soft/60 p-4">
        <p className="flex items-center gap-2 text-sm font-semibold text-craft-ink">
          <ClipboardCheck className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />
          Review checklist
        </p>
        <div className="mt-3 space-y-2">
          {assignment.review_questions.map((question, index) => {
            const key = `review-${index}`;
            return (
              <label key={key} className="flex items-start gap-3 rounded-xl border border-craft-border bg-craft-surface px-3 py-3 text-sm text-craft-ink">
                <input
                  type="checkbox"
                  checked={reviewChecks[key]}
                  onChange={(event) =>
                    setReviewChecks((prev) => ({ ...prev, [key]: event.target.checked }))
                  }
                  className="mt-1 h-4 w-4 rounded border-craft-border"
                />
                <span>{question}</span>
              </label>
            );
          })}
        </div>
      </div>

      <div className="flex flex-wrap gap-3">
        <button type="button" onClick={saveDraft} className="btn-secondary">
          <Sparkles className="h-4 w-4" />
          Save draft
        </button>
        <button type="button" onClick={runVerifier} className="btn-primary">
          <CheckCircle2 className="h-4 w-4" />
          Run verifier
        </button>
      </div>

      <div className="grid gap-4 xl:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-xl border border-craft-border bg-craft-soft/60 p-4">
          <p className="text-sm font-semibold text-craft-ink">Verifier results</p>
          <ul className="mt-3 space-y-2 text-sm text-craft-muted">
            {verifier.checks.map((check) => (
              <li key={check.key} className="rounded-xl border border-craft-border bg-craft-surface px-3 py-3">
                <p className={clsx("font-medium", check.passed ? "text-emerald-700 dark:text-emerald-300" : "text-amber-700 dark:text-amber-300")}>
                  {check.label}: {check.passed ? "pass" : "revise"}
                </p>
                {!check.passed ? (
                  <ul className="mt-2 list-disc pl-5">
                    {check.issues.map((issue) => (
                      <li key={issue}>{issue}</li>
                    ))}
                  </ul>
                ) : null}
              </li>
            ))}
          </ul>
          {verifier.riskyHits.length ? (
            <div className="mt-3 rounded-xl border border-rose-300 bg-rose-50 px-4 py-3 text-sm text-rose-800 dark:border-rose-500/30 dark:bg-rose-500/10 dark:text-rose-200">
              <p className="flex items-center gap-2 font-semibold">
                <ShieldAlert className="h-4 w-4" />
                Risk phrases detected
              </p>
              <p className="mt-2">{verifier.riskyHits.join(", ")}</p>
            </div>
          ) : null}
        </div>

        <div className="space-y-4">
          <div className="rounded-xl border border-craft-border bg-craft-soft/60 p-4">
            <p className="text-sm font-semibold text-craft-ink">Rubric snapshot</p>
            <ul className="mt-3 space-y-2 text-sm text-craft-muted">
              {verifier.rubricScores.map((criterion) => (
                <li key={criterion.criterion} className="rounded-xl border border-craft-border bg-craft-surface px-3 py-3">
                  <p className="font-medium text-craft-ink">{criterion.criterion}</p>
                  <p className="mt-1">{criterion.description}</p>
                  <p className="mt-2 text-xs font-semibold text-craft-faint">
                    Score: {criterion.earned} / {criterion.weight}
                  </p>
                </li>
              ))}
            </ul>
          </div>

          <div className="rounded-xl border border-craft-border bg-craft-soft/60 p-4">
            <p className="text-sm font-semibold text-craft-ink">Evaluation case reminders</p>
            <ul className="mt-3 space-y-2 text-sm text-craft-muted">
              {evaluationCases.map((testCase) => (
                <li key={testCase.name} className="rounded-xl border border-craft-border bg-craft-surface px-3 py-3">
                  <p className="font-medium text-craft-ink">{testCase.name}</p>
                  <p className="mt-1">{testCase.goal}</p>
                  <p className="mt-2 text-xs font-semibold text-craft-faint">Expected: {testCase.expected}</p>
                </li>
              ))}
            </ul>
          </div>

          <div
            className={clsx(
              "rounded-xl border px-4 py-4 text-sm",
              finalStatus === "pass"
                ? "border-emerald-300 bg-emerald-50 text-emerald-800 dark:border-emerald-500/30 dark:bg-emerald-500/10 dark:text-emerald-200"
                : finalStatus === "stop"
                  ? "border-rose-300 bg-rose-50 text-rose-800 dark:border-rose-500/30 dark:bg-rose-500/10 dark:text-rose-200"
                  : "border-amber-300 bg-amber-50 text-amber-800 dark:border-amber-500/30 dark:bg-amber-500/10 dark:text-amber-200"
            )}
          >
            <p className="font-semibold">
              Final result: {finalStatus}
            </p>
            <p className="mt-2">
              {finalStatus === "pass"
                ? "This capstone plan is complete enough to pass the lesson verifier."
                : finalStatus === "stop"
                  ? "This plan contains risky language that should stop release until rewritten."
                  : "This plan needs revision before it is ready to pass."}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}