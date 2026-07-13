"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { CheckCircle2, ChevronLeft, ChevronRight, ClipboardCheck } from "lucide-react";
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";
import { lessonStepHref } from "@/lib/lesson-steps";

export default function LessonProgressPage() {
  const router = useRouter();
  const {
    slug,
    lessonSlug,
    lesson,
    videoUrl,
    needsVideo,
    videoDone,
    setNotice,
    progressPending,
    prev,
    next,
  } = useLessonWorkspace();

  if (!lesson) return null;

  function goToQuiz() {
    if (needsVideo && !videoDone) {
      setNotice("Watch the lesson video all the way through before taking the Recap Quiz.");
      router.push(lessonStepHref(slug, lessonSlug, "video"));
      return;
    }
    setNotice(null);
    router.push(lessonStepHref(slug, lessonSlug, "quiz"));
  }

  return (
    <div className="space-y-4">
      <div className="card p-6">
        <h2 className="text-base font-semibold text-slate-900">Your progress</h2>
        <p className="mt-1 text-sm text-slate-500">
          {lesson.status === "completed"
            ? `Completed${lesson.score != null ? ` · Recap Quiz ${lesson.score}%` : ""}`
            : needsVideo && !videoDone
              ? "Watch the video, then pass the Recap Quiz (80%+) to finish."
              : "Pass the Recap Quiz with 80% or higher to complete this lesson."}
        </p>

        <dl className="mt-5 grid gap-3 sm:grid-cols-3">
          <div className="rounded-xl bg-slate-50 px-3 py-3 ring-1 ring-slate-200/70">
            <dt className="text-[11px] font-medium uppercase tracking-wide text-slate-400">
              Video
            </dt>
            <dd className="mt-1 text-sm font-semibold text-slate-800">
              {!videoUrl
                ? "No video"
                : !needsVideo
                  ? videoDone && lesson.video_watched
                    ? "Optional · watched"
                    : "Optional · can skip"
                  : videoDone
                    ? "Watched"
                    : "Not finished"}
            </dd>
          </div>
          <div className="rounded-xl bg-slate-50 px-3 py-3 ring-1 ring-slate-200/70">
            <dt className="text-[11px] font-medium uppercase tracking-wide text-slate-400">
              Recap Quiz
            </dt>
            <dd className="mt-1 text-sm font-semibold text-slate-800">
              {lesson.score != null ? `${lesson.score}%` : "Not taken"}
            </dd>
          </div>
          <div className="rounded-xl bg-slate-50 px-3 py-3 ring-1 ring-slate-200/70">
            <dt className="text-[11px] font-medium uppercase tracking-wide text-slate-400">
              Status
            </dt>
            <dd className="mt-1 text-sm font-semibold capitalize text-slate-800">
              {lesson.status.replace("_", " ")}
            </dd>
          </div>
        </dl>

        <div className="mt-5 flex flex-wrap gap-3">
          {lesson.status !== "completed" && (
            <button
              type="button"
              disabled={progressPending}
              onClick={goToQuiz}
              className="btn-primary"
            >
              <ClipboardCheck className="h-4 w-4" />
              Take Recap Quiz
            </button>
          )}
          {lesson.status === "completed" && (
            <>
              <span className="inline-flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-2 text-sm font-medium text-emerald-700">
                <CheckCircle2 className="h-4 w-4" />
                Lesson complete
              </span>
              <Link href={lessonStepHref(slug, lessonSlug, "quiz")} className="btn-secondary">
                Review Recap Quiz
              </Link>
            </>
          )}
          <Link href={lessonStepHref(slug, lessonSlug, "content")} className="btn-secondary">
            Review content
          </Link>
          {videoUrl && (
            <Link href={lessonStepHref(slug, lessonSlug, "video")} className="btn-secondary">
              {lesson.video_watched ? "Review video" : needsVideo ? "Watch video" : "Watch video (optional)"}
            </Link>
          )}
        </div>
      </div>

      <nav className="flex items-center justify-between gap-4 pt-2">
        {prev ? (
          <Link href={lessonStepHref(slug, prev.slug, "content")} className="btn-secondary">
            <ChevronLeft className="h-4 w-4" />
            {prev.title}
          </Link>
        ) : (
          <span />
        )}
        {next ? (
          <Link href={lessonStepHref(slug, next.slug, "content")} className="btn-secondary">
            {next.title}
            <ChevronRight className="h-4 w-4" />
          </Link>
        ) : (
          <span />
        )}
      </nav>
    </div>
  );
}
