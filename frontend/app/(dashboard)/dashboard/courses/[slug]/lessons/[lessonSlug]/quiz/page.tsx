"use client";

import { useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ArrowRight, ChevronLeft } from "lucide-react";
import { PaginatedExam } from "@/components/lessons/PaginatedExam";
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";
import {
  assessmentLabelForLessonType,
  isExamLessonType,
  lessonStepHref,
} from "@/lib/lesson-steps";
import { useCanBypassGates } from "@/lib/gates";

/**
 * The assessment step, and the last screen of a lesson.
 *
 * There is no Progress step after this one. Progress was a report wearing a
 * step's clothes: it restated "complete" four times and then hid the only
 * forward button in its bottom-right corner, so finishing a mid-module quiz
 * meant being routed to a dashboard to hunt for the way on. The forward action
 * now lives on this card, where the result is.
 */
export default function LessonQuizPage() {
  const router = useRouter();
  const canBypassGates = useCanBypassGates();
  const {
    slug,
    lessonSlug,
    lesson,
    prev,
    next,
    recapQuestions,
    needsVideo,
    videoDone,
    setNotice,
    updateProgress,
    atModuleEnd,
    nextModule,
  } = useLessonWorkspace();

  useEffect(() => {
    if (!lesson || !needsVideo || videoDone) return;
    setNotice("Watch the lesson video all the way through before taking the Recap Quiz.");
    // Back to the lesson step — that is where the video now lives.
    router.replace(lessonStepHref(slug, lessonSlug, "content"));
  }, [lesson, needsVideo, videoDone, lessonSlug, router, setNotice, slug]);

  if (!lesson) return null;

  const isExamLesson = isExamLessonType(lesson.lesson_type);
  const assessmentLabel = assessmentLabelForLessonType(lesson.lesson_type);
  // Finishing the module's last lesson hands off to the next module instead.
  const endsModule = atModuleEnd;

  /*
    One primary action, always present, named after where it goes. Every branch
    resolves to something real — a passed assessment is never a dead end.
  */
  const forwardAction = endsModule ? (
    nextModule ? (
      <Link href={nextModule.href} className="btn-primary">
        Start {nextModule.title}
        <ArrowRight className="h-4 w-4 shrink-0" />
      </Link>
    ) : nextModule === undefined ? (
      // The course list has not resolved yet — never claim "course complete"
      // on unknown data.
      <Link href="/dashboard" className="btn-primary">
        Back to dashboard
        <ArrowRight className="h-4 w-4 shrink-0" />
      </Link>
    ) : (
      <Link href="/dashboard" className="btn-primary">
        You finished the course — back to dashboard
        <ArrowRight className="h-4 w-4 shrink-0" />
      </Link>
    )
  ) : next ? (
    <Link href={lessonStepHref(slug, next.slug, "content")} className="btn-primary">
      Next: {next.title}
      <ArrowRight className="h-4 w-4 shrink-0" />
    </Link>
  ) : (
    <Link href={`/dashboard/courses/${slug}`} className="btn-primary">
      Back to the module
      <ArrowRight className="h-4 w-4 shrink-0" />
    </Link>
  );

  return (
    <div className="flex h-full min-h-0 flex-col gap-3">
      <div className="min-h-0 flex-1">
        <PaginatedExam
          questions={recapQuestions}
          label={assessmentLabel}
          previouslyPassed={lesson.status === "completed"}
          previousScore={lesson.score}
          storageKey={`agentcraft-quiz-draft:${lesson.id}`}
          locked={needsVideo && !videoDone && !canBypassGates}
          lockedReason={`Watch the lesson video to the end before taking the ${assessmentLabel}.`}
          onLockedAction={() => {
            setNotice(
              `Watch the lesson video all the way through before taking the ${assessmentLabel}.`
            );
            router.push(lessonStepHref(slug, lessonSlug, "content"));
          }}
          onPassed={(score) => {
            if (lesson.status !== "completed") {
              updateProgress({ status: "completed", score });
            }
            setNotice(null);
          }}
          completionAction={forwardAction}
          reviewLessonHref={
            isExamLesson ? undefined : lessonStepHref(slug, lessonSlug, "content")
          }
        />
      </div>

      <div className="flex shrink-0 flex-wrap items-center justify-between gap-2">
        {isExamLesson ? (
          prev ? (
            <Link
              href={lessonStepHref(slug, prev.slug, "content")}
              className="inline-flex items-center gap-1 text-sm text-craft-muted transition hover:text-craft-ink"
            >
              <ChevronLeft className="h-4 w-4" />
              {prev.title}
            </Link>
          ) : (
            <Link
              href={`/dashboard/courses/${slug}`}
              className="inline-flex items-center gap-1 text-sm text-craft-muted transition hover:text-craft-ink"
            >
              <ChevronLeft className="h-4 w-4" />
              Back to Module
            </Link>
          )
        ) : (
          <Link
            href={lessonStepHref(slug, lessonSlug, "content")}
            className="inline-flex items-center gap-1 text-sm text-craft-muted transition hover:text-craft-ink"
          >
            <ChevronLeft className="h-4 w-4" />
            Back to Lesson
          </Link>
        )}
      </div>
    </div>
  );
}
