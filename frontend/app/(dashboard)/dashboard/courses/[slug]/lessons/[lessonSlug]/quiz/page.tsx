"use client";

import { useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { PaginatedExam } from "@/components/lessons/PaginatedExam";
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";
import {
  assessmentLabelForLessonType,
  isExamLessonType,
  lessonStepHref,
} from "@/lib/lesson-steps";

export default function LessonQuizPage() {
  const router = useRouter();
  const {
    slug,
    lessonSlug,
    lesson,
    prev,
    recapQuestions,
    needsVideo,
    videoDone,
    setNotice,
    updateProgress,
  } = useLessonWorkspace();

  useEffect(() => {
    if (!lesson || !needsVideo || videoDone) return;
    setNotice("Watch the lesson video all the way through before taking the Recap Quiz.");
    router.replace(lessonStepHref(slug, lessonSlug, "video"));
  }, [lesson, needsVideo, videoDone, lessonSlug, router, setNotice, slug]);

  if (!lesson) return null;

  const isExamLesson = isExamLessonType(lesson.lesson_type);
  const assessmentLabel = assessmentLabelForLessonType(lesson.lesson_type);

  return (
    <div className="space-y-3">
      {/*
        Paginated one-question-per-slide UI — content-sized card (same as
        Modules 4 / 6 / 8). One focused question, no full-screen empty space.
      */}
      <PaginatedExam
        questions={recapQuestions}
        label={assessmentLabel}
        locked={needsVideo && !videoDone}
        lockedReason={`Watch the lesson video to the end before taking the ${assessmentLabel}.`}
        onLockedAction={() => {
          setNotice(
            `Watch the lesson video all the way through before taking the ${assessmentLabel}.`
          );
          router.push(lessonStepHref(slug, lessonSlug, "video"));
        }}
        onPassed={(score) => {
          if (lesson.status !== "completed") {
            updateProgress({ status: "completed", score });
          }
          setNotice(null);
          router.push(lessonStepHref(slug, lessonSlug, "progress"));
        }}
      />

      <div className="flex flex-wrap items-center justify-between gap-2 pt-0.5">
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
            Back to Content
          </Link>
        )}
        <Link
          href={lessonStepHref(slug, lessonSlug, "progress")}
          className="inline-flex items-center gap-1 text-sm text-craft-muted transition hover:text-craft-ink"
        >
          Progress
          <ChevronRight className="h-4 w-4" />
        </Link>
      </div>
    </div>
  );
}
