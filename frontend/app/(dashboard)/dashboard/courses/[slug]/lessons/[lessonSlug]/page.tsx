"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { BookOpen, CheckCircle2, FileText, LifeBuoy, MapPin, PlayCircle, RefreshCw, Timer, Wrench } from "lucide-react";
import { getLesson, updateLessonProgress } from "@/lib/api/courses";
import type { LessonStatus } from "@/types";

const STATUS_UI = {
  completed: { text: "You've completed this lesson!", pct: 100, Icon: CheckCircle2, cls: "text-emerald-400" },
  in_progress: { text: "In progress — keep going!", pct: 50, Icon: RefreshCw, cls: "text-craft-glow" },
  not_started: { text: "Not started yet", pct: 0, Icon: Timer, cls: "text-slate-500" },
  stuck: { text: "Marked as needing help", pct: 50, Icon: LifeBuoy, cls: "text-amber-400" },
} as const;

type StatusKey = keyof typeof STATUS_UI;

export default function LessonDetailPage() {
  const { slug, lessonSlug } = useParams<{ slug: string; lessonSlug: string }>();
  const queryClient = useQueryClient();

  const { data: lesson, isLoading } = useQuery({
    queryKey: ["lesson", slug, lessonSlug],
    queryFn: () => getLesson(slug, lessonSlug),
    enabled: !!slug && !!lessonSlug,
  });

  const progressMutation = useMutation({
    mutationFn: (status: LessonStatus) => updateLessonProgress(lesson!.id, status),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["lesson", slug, lessonSlug] });
      queryClient.invalidateQueries({ queryKey: ["course", slug] });
      queryClient.invalidateQueries({ queryKey: ["courses"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard-stats"] });
    },
  });

  if (isLoading) return <p className="animate-pulse text-slate-500">Loading lesson…</p>;
  if (!lesson) return <p className="text-slate-400">Lesson not found.</p>;

  const statusUi = STATUS_UI[lesson.status as StatusKey] ?? STATUS_UI.not_started;

  return (
    <div className="mx-auto max-w-4xl">
      <p className="text-sm text-slate-500">
        <Link href={`/dashboard/courses/${lesson.course_slug}`} className="text-craft-glow hover:underline">
          {lesson.course_title}
        </Link>
        <span aria-hidden> · </span>
        {lesson.estimated_minutes} min
      </p>
      <h1 className="mt-2 text-2xl font-bold text-white">{lesson.title}</h1>

      <div className="mt-8 space-y-6">
        {lesson.content ? (
          <div className="rounded-2xl border border-white/10 bg-craft-900/60 p-6">
            <h2 className="flex items-center gap-2 text-lg font-semibold text-white">
              <BookOpen className="h-5 w-5 text-craft-glow" /> Lesson Content
            </h2>
            <div className="mt-4 whitespace-pre-wrap text-slate-300">{lesson.content}</div>
          </div>
        ) : (
          <div className="rounded-2xl border border-white/10 bg-craft-900/60 p-12 text-center">
            <FileText className="mx-auto h-10 w-10 text-slate-600" />
            <p className="mt-3 text-slate-400">Lesson content coming soon.</p>
          </div>
        )}

        {lesson.lesson_type === "sandbox" && (
          <div className="rounded-2xl border border-white/10 bg-craft-900/60 p-6">
            <h2 className="flex items-center gap-2 text-lg font-semibold text-white">
              <Wrench className="h-5 w-5 text-craft-glow" /> Sandbox
            </h2>
            <p className="mt-2 text-sm text-slate-400">
              Launch a hands-on environment to practice what you learn.
            </p>
            <button
              type="button"
              onClick={() => alert("Sandbox integration coming soon — Diego & Douglas wiring it up.")}
              className="mt-4 flex items-center gap-2 rounded-lg bg-craft-accent px-5 py-2.5 text-sm font-medium text-white transition-colors hover:bg-indigo-500"
            >
              <Wrench className="h-4 w-4" />
              Launch Sandbox →
            </button>
          </div>
        )}

        <div className="rounded-2xl border border-white/10 bg-craft-900/60 p-6">
          <h2 className="flex items-center gap-2 text-lg font-semibold text-white">
            <MapPin className="h-5 w-5 text-craft-glow" /> Your Progress
          </h2>
          <p className="mt-2 flex items-center gap-2 text-sm text-slate-300">
            <statusUi.Icon className={"h-4 w-4 " + statusUi.cls} />
            {statusUi.text}
          </p>
          <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-craft-800">
            <div
              className="h-full rounded-full bg-gradient-to-r from-craft-accent to-craft-glow transition-all"
              style={{ width: `${statusUi.pct}%` }}
            />
          </div>

          <div className="mt-5 flex flex-wrap gap-3">
            {lesson.status === "not_started" && (
              <button
                type="button"
                disabled={progressMutation.isPending}
                onClick={() => progressMutation.mutate("in_progress")}
                className="flex items-center gap-2 rounded-lg bg-craft-accent px-5 py-2.5 text-sm font-medium text-white transition-colors hover:bg-indigo-500 disabled:opacity-50"
              >
                <PlayCircle className="h-4 w-4" />
                Start lesson
              </button>
            )}
            {lesson.status !== "completed" && (
              <button
                type="button"
                disabled={progressMutation.isPending}
                onClick={() => progressMutation.mutate("completed")}
                className="flex items-center gap-2 rounded-lg border border-emerald-500/40 px-5 py-2.5 text-sm font-medium text-emerald-300 transition-colors hover:bg-emerald-950/30 disabled:opacity-50"
              >
                <CheckCircle2 className="h-4 w-4" />
                Mark complete
              </button>
            )}
            {lesson.status === "completed" && (
              <button
                type="button"
                disabled={progressMutation.isPending}
                onClick={() => progressMutation.mutate("in_progress")}
                className="rounded-lg border border-white/15 px-5 py-2.5 text-sm text-slate-300 transition-colors hover:border-white/30 disabled:opacity-50"
              >
                Restart lesson
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
