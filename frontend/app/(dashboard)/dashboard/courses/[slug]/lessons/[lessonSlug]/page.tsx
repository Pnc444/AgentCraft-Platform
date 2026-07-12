"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  AlertTriangle,
  BookOpen,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  ClipboardCheck,
  FileText,
  MonitorPlay,
  Timer,
  Wrench,
} from "lucide-react";
import { getCourse, getLesson, updateLessonProgress } from "@/lib/api/courses";
import {
  invalidateLearningProgress,
  patchLessonStatusInCache,
} from "@/lib/learning-progress";
import type { LessonStatus } from "@/types";
import { LessonContent } from "@/components/lessons/LessonContent";
import { LessonSection } from "@/components/lessons/LessonSection";
import { LessonVideo } from "@/components/lessons/LessonVideo";
import {
  LessonTutorButton,
  LessonTutorPanel,
} from "@/components/lessons/LessonTutorPanel";
import {
  type CheckpointQuestion,
} from "@/components/lessons/CheckpointQuiz";
import { RecapQuiz } from "@/components/lessons/RecapQuiz";
import { ProgressBar } from "@/components/shared/ProgressBar";

function getCheckpointQuestions(config: Record<string, unknown>): CheckpointQuestion[] {
  const raw = config?.questions;
  if (!Array.isArray(raw)) return [];
  return raw.filter(
    (q): q is CheckpointQuestion =>
      !!q &&
      typeof q === "object" &&
      typeof (q as CheckpointQuestion).prompt === "string" &&
      Array.isArray((q as CheckpointQuestion).options)
  );
}

const STATUS_UI = {
  completed: { text: "Completed", pct: 100 },
  in_progress: { text: "In progress", pct: 50 },
  not_started: { text: "Not started", pct: 0 },
  stuck: { text: "Needs help", pct: 50 },
} as const;

type StatusKey = keyof typeof STATUS_UI;

export default function LessonDetailPage() {
  const { slug, lessonSlug } = useParams<{ slug: string; lessonSlug: string }>();
  const queryClient = useQueryClient();
  const [tutorOpen, setTutorOpen] = useState(false);
  const [quizOpen, setQuizOpen] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);
  const autoStartedId = useRef<number | null>(null);
  const videoSectionRef = useRef<HTMLDivElement>(null);
  const quizSectionRef = useRef<HTMLDivElement>(null);

  const { data: lesson, isLoading } = useQuery({
    queryKey: ["lesson", slug, lessonSlug],
    queryFn: () => getLesson(slug, lessonSlug),
    enabled: !!slug && !!lessonSlug,
  });

  const { data: course } = useQuery({
    queryKey: ["course", slug],
    queryFn: () => getCourse(slug),
    enabled: !!slug,
  });

  const progressMutation = useMutation({
    mutationFn: (data: {
      status?: LessonStatus;
      score?: number;
      video_watched?: boolean;
    }) => updateLessonProgress(lesson!.id, data),
    onMutate: async (data) => {
      if (!slug || !lessonSlug || !data.status) return;
      await queryClient.cancelQueries({ queryKey: ["courses"] });
      await queryClient.cancelQueries({ queryKey: ["course", slug] });
      await queryClient.cancelQueries({ queryKey: ["lesson", slug, lessonSlug] });
      patchLessonStatusInCache(queryClient, slug, lessonSlug, data.status);
    },
    onSuccess: (result) => {
      if (!slug || !lessonSlug) return;
      queryClient.setQueryData(["lesson", slug, lessonSlug], (old: typeof lesson) => {
        if (!old) return old;
        return {
          ...old,
          status: result.status,
          score: result.score,
          video_watched: result.video_watched,
        };
      });
    },
    onSettled: () => {
      invalidateLearningProgress(queryClient, { courseSlug: slug, lessonSlug });
    },
  });

  useEffect(() => {
    if (!lesson || lesson.status !== "not_started") return;
    if (autoStartedId.current === lesson.id) return;
    autoStartedId.current = lesson.id;
    progressMutation.mutate({ status: "in_progress" });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lesson?.id, lesson?.status]);

  const markStuck = useCallback(() => {
    if (!lesson) return;
    if (lesson.status === "completed" || lesson.status === "stuck") return;
    progressMutation.mutate({ status: "stuck" });
  }, [lesson, progressMutation]);

  function openTutor() {
    setTutorOpen(true);
    markStuck();
  }

  function scrollTo(el: HTMLElement | null) {
    el?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function handleRecapQuizClick() {
    if (!lesson) return;
    const hasVideo = !!(lesson.video_url || "").trim();
    const videoDone = lesson.video_watched || !hasVideo;

    if (hasVideo && !videoDone) {
      setNotice("Watch the lesson video all the way through before taking the Recap Quiz.");
      setQuizOpen(false);
      scrollTo(videoSectionRef.current);
      return;
    }

    const questions = getCheckpointQuestions(lesson.sandbox_config ?? {});
    if (!questions.length) {
      setNotice(
        "This lesson doesn’t have Recap Quiz questions yet. An instructor needs to add them in the admin panel."
      );
      return;
    }

    setNotice(null);
    setQuizOpen(true);
    requestAnimationFrame(() => scrollTo(quizSectionRef.current));
  }

  function handleVideoWatched() {
    if (!lesson || lesson.video_watched) return;
    progressMutation.mutate({ video_watched: true });
    setNotice(null);
  }

  if (isLoading) return <p className="animate-pulse text-slate-500">Loading lesson…</p>;
  if (!lesson) return <p className="text-slate-500">Lesson not found.</p>;

  const statusUi = STATUS_UI[lesson.status as StatusKey] ?? STATUS_UI.not_started;
  const lessons = course?.lessons ?? [];
  const idx = lessons.findIndex((l) => l.slug === lesson.slug);
  const prev = idx > 0 ? lessons[idx - 1] : null;
  const next = idx >= 0 && idx < lessons.length - 1 ? lessons[idx + 1] : null;
  const checkpointQuestions = getCheckpointQuestions(lesson.sandbox_config ?? {});
  const videoUrl = (lesson.video_url || "").trim();
  const needsVideo = !!videoUrl;
  const videoDone = lesson.video_watched || !needsVideo;
  const showQuiz =
    quizOpen || lesson.status === "completed" || lesson.lesson_type === "quiz";

  return (
    <div className="mx-auto max-w-3xl animate-fade-up">
      <p className="text-sm text-slate-500">
        <Link
          href={`/dashboard/courses/${lesson.course_slug}`}
          className="font-medium text-cyan-600 hover:underline"
        >
          {lesson.course_title}
        </Link>
        <span aria-hidden> · </span>
        <span className="inline-flex items-center gap-1">
          <Timer className="h-3.5 w-3.5" />
          {lesson.estimated_minutes} min
        </span>
        <span aria-hidden> · </span>
        <span className="capitalize">{lesson.lesson_type.replace("_", " ")}</span>
      </p>

      <h1 className="mt-3 text-3xl font-bold tracking-tight text-slate-900">
        {lesson.title}
      </h1>

      <div className="mt-4 flex items-center gap-3">
        <ProgressBar className="flex-1" value={statusUi.pct} />
        <span className="text-sm font-medium text-slate-500">{statusUi.text}</span>
      </div>

      {notice && (
        <div className="mt-4 flex items-start gap-3 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">
          <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" />
          <div className="min-w-0 flex-1">
            <p>{notice}</p>
            {needsVideo && !videoDone && (
              <button
                type="button"
                className="mt-2 text-xs font-semibold underline"
                onClick={() => scrollTo(videoSectionRef.current)}
              >
                Jump to video
              </button>
            )}
          </div>
        </div>
      )}

      <div className="mt-8 space-y-4">
        {videoUrl && (
          <div ref={videoSectionRef}>
            <LessonSection
              title="Video"
              icon={<MonitorPlay className="h-4 w-4 text-cyan-600" />}
            >
              <LessonVideo
                url={videoUrl}
                title={lesson.title}
                watched={lesson.video_watched}
                onWatched={handleVideoWatched}
              />
            </LessonSection>
          </div>
        )}

        {lesson.lesson_type !== "quiz" &&
          (lesson.content ? (
            <LessonSection
              title="Lesson Content"
              icon={<BookOpen className="h-4 w-4 text-cyan-600" />}
            >
              <LessonContent content={lesson.content} />
            </LessonSection>
          ) : !videoUrl ? (
            <LessonSection
              title="Lesson Content"
              icon={<FileText className="h-4 w-4 text-cyan-600" />}
              empty
            />
          ) : null)}

        {lesson.lesson_type === "quiz" && lesson.content ? (
          <LessonSection
            title="Lesson Content"
            icon={<BookOpen className="h-4 w-4 text-cyan-600" />}
          >
            <LessonContent content={lesson.content} />
          </LessonSection>
        ) : null}

        {lesson.lesson_type === "sandbox" && (
          <LessonSection
            title="Interactive Demo"
            icon={<Wrench className="h-4 w-4 text-cyan-600" />}
          >
            <p className="text-sm text-slate-500">Sandbox</p>
            <button
              type="button"
              onClick={() =>
                alert("Sandbox integration coming soon — Diego & Douglas wiring it up.")
              }
              className="btn-primary mt-4"
            >
              <Wrench className="h-4 w-4" />
              Launch Sandbox
            </button>
          </LessonSection>
        )}

        {showQuiz && (
          <div ref={quizSectionRef}>
            <LessonSection
              title="Recap Quiz"
              icon={<ClipboardCheck className="h-4 w-4 text-cyan-600" />}
            >
              <RecapQuiz
                questions={checkpointQuestions}
                locked={needsVideo && !videoDone}
                lockedReason="Watch the lesson video to the end before taking the Recap Quiz."
                onLockedAction={() => {
                  setNotice("Watch the lesson video all the way through before taking the Recap Quiz.");
                  scrollTo(videoSectionRef.current);
                }}
                onPassed={(score) => {
                  if (lesson.status !== "completed") {
                    progressMutation.mutate({ status: "completed", score });
                  }
                  setNotice(null);
                }}
              />
            </LessonSection>
          </div>
        )}

        <div className="card p-6">
          <h2 className="text-base font-semibold text-slate-900">Your progress</h2>
          <p className="mt-1 text-sm text-slate-500">
            {lesson.status === "completed"
              ? `Completed${lesson.score != null ? ` · Recap Quiz ${lesson.score}%` : ""}`
              : needsVideo && !videoDone
                ? "Watch the video, then pass the Recap Quiz (80%+) to finish."
                : "Pass the Recap Quiz with 80% or higher to complete this lesson."}
          </p>
          <div className="mt-4 flex flex-wrap gap-3">
            {lesson.status !== "completed" && (
              <button
                type="button"
                disabled={progressMutation.isPending}
                onClick={handleRecapQuizClick}
                className="btn-primary"
              >
                <ClipboardCheck className="h-4 w-4" />
                Recap Quiz
              </button>
            )}
            {lesson.status === "completed" && (
              <span className="inline-flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-2 text-sm font-medium text-emerald-700">
                <CheckCircle2 className="h-4 w-4" />
                Lesson complete
              </span>
            )}
            {lesson.status === "completed" && (
              <button
                type="button"
                disabled={progressMutation.isPending}
                onClick={() => {
                  setQuizOpen(true);
                  requestAnimationFrame(() => scrollTo(quizSectionRef.current));
                }}
                className="btn-secondary"
              >
                Review Recap Quiz
              </button>
            )}
          </div>
        </div>

        <nav className="flex items-center justify-between gap-4 pt-2">
          {prev ? (
            <Link
              href={`/dashboard/courses/${slug}/lessons/${prev.slug}`}
              className="btn-secondary"
            >
              <ChevronLeft className="h-4 w-4" />
              {prev.title}
            </Link>
          ) : (
            <span />
          )}
          {next ? (
            <Link
              href={`/dashboard/courses/${slug}/lessons/${next.slug}`}
              className="btn-secondary"
            >
              {next.title}
              <ChevronRight className="h-4 w-4" />
            </Link>
          ) : (
            <span />
          )}
        </nav>
      </div>

      {!tutorOpen && <LessonTutorButton onClick={openTutor} />}
      <LessonTutorPanel
        open={tutorOpen}
        onClose={() => setTutorOpen(false)}
        lessonTitle={lesson.title}
        courseTitle={lesson.course_title}
      />
    </div>
  );
}
