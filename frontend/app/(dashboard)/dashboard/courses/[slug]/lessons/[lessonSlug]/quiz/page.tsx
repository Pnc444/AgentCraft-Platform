"use client";

import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { PaginatedExam } from "@/components/lessons/PaginatedExam";
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";
import {
  assessmentLabelForLessonType,
  isExamLessonType,
  lessonStepHref,
} from "@/lib/lesson-steps";

/**
 * The assessment step, and the last screen of a lesson.
 *
 * Learners may skip without answering. Skip navigates onward but does not
 * mark the lesson completed — so certificates and badges stay locked until
 * they actually pass.
 */
export default function LessonQuizPage() {
  const {
    slug,
    lessonSlug,
    lesson,
    next,
    recapQuestions,
    setNotice,
    updateProgress,
    atModuleEnd,
    nextModule,
  } = useLessonWorkspace();

  if (!lesson) return null;

  const isExamLesson = isExamLessonType(lesson.lesson_type);
  const assessmentLabel = assessmentLabelForLessonType(lesson.lesson_type);
  // Finishing the module's last lesson hands off to the next module instead.
  const endsModule = atModuleEnd;
  const alreadyPassed = lesson.status === "completed";

  /*
    One primary action, always present, named after where it goes. Every branch
    resolves to something real — a passed assessment is never a dead end.
  */
  const forwardHref = endsModule
    ? nextModule
      ? nextModule.href
      : "/dashboard"
    : next
      ? lessonStepHref(slug, next.slug, "content")
      : `/dashboard/courses/${slug}`;

  const forwardLabel = endsModule
    ? nextModule
      ? `Start ${nextModule.title}`
      : nextModule === undefined
        ? "Back to dashboard"
        : "You finished the course — back to dashboard"
    : next
      ? `Next: ${next.title}`
      : "Back to the module";

  const skipLabel = "Skip";
  const skipTitle = endsModule
    ? nextModule
      ? `Skip without credit — go to ${moduleDisplayTitleSafe(nextModule.title)}`
      : "Skip without credit"
    : next
      ? `Skip without credit — next: ${next.title}`
      : "Skip without credit";

  const forwardAction = (
    <Link href={forwardHref} className="btn-primary">
      {forwardLabel}
      <ArrowRight className="h-4 w-4 shrink-0" />
    </Link>
  );

  const skipAction = alreadyPassed ? null : (
    <Link
      href={forwardHref}
      title={skipTitle}
      className="inline-flex items-center gap-1"
      onClick={() => {
        try {
          window.sessionStorage.removeItem(`agentcraft-quiz-draft:${lesson.id}`);
        } catch {
          /* ignore */
        }
        setNotice(
          `Skipped ${assessmentLabel.toLowerCase()} — it won’t count toward your certificate until you pass it.`
        );
      }}
    >
      {skipLabel}
      <ArrowRight className="h-3 w-3 shrink-0" />
    </Link>
  );

  return (
    <div className="flex h-full min-h-0 flex-col">
      <div className="min-h-0 flex-1">
        <PaginatedExam
          questions={recapQuestions}
          label={assessmentLabel}
          previouslyPassed={alreadyPassed}
          previousScore={lesson.score}
          storageKey={`agentcraft-quiz-draft:${lesson.id}`}
          locked={false}
          onPassed={(score) => {
            if (lesson.status !== "completed") {
              updateProgress({ status: "completed", score });
            }
            setNotice(null);
          }}
          completionAction={forwardAction}
          skipAction={skipAction}
          reviewLessonHref={
            isExamLesson ? undefined : lessonStepHref(slug, lessonSlug, "content")
          }
        />
      </div>
    </div>
  );
}

function moduleDisplayTitleSafe(title: string) {
  return title.replace(/^Module\s+[\d.]+:\s*/i, "").trim() || title;
}
