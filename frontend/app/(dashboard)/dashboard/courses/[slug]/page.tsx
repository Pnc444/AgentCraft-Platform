"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Check, CircleDashed, FileText } from "lucide-react";
import clsx from "clsx";
import { getCourse } from "@/lib/api/courses";
import type { CourseDetail } from "@/types";
import { DifficultyBadge } from "@/components/dashboard/DifficultyBadge";
import { ProgressBar } from "@/components/shared/ProgressBar";

export default function CourseDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const queryClient = useQueryClient();
  const cached = slug
    ? queryClient.getQueryData<CourseDetail>(["course", slug])
    : undefined;
  const { data: course, isLoading } = useQuery({
    queryKey: ["course", slug],
    queryFn: () => getCourse(slug),
    enabled: !!slug,
    initialData: cached,
    initialDataUpdatedAt: cached
      ? queryClient.getQueryState(["course", slug])?.dataUpdatedAt
      : undefined,
  });

  if (isLoading && !course) return <p className="animate-pulse text-slate-400">Loading course…</p>;
  if (!course) return <p className="text-slate-500">Course not found.</p>;

  return (
    <div className="mx-auto max-w-3xl animate-fade-up">
      <p className="text-sm text-slate-500">
        <Link href="/dashboard" className="font-medium text-cyan-600 hover:underline">
          Dashboard
        </Link>
        <span aria-hidden> / </span>
        {course.lessons.length} lessons
      </p>

      <div className="mt-3 flex flex-wrap items-center gap-3">
        <h1 className="text-3xl font-bold tracking-tight text-slate-900">{course.title}</h1>
        <DifficultyBadge difficulty={course.difficulty} />
      </div>

      {course.description && (
        <p className="mt-3 max-w-2xl leading-relaxed text-slate-500">{course.description}</p>
      )}

      <div className="mt-6 rounded-2xl bg-[#0F172A] p-5 text-white">
        <div className="mb-2 flex justify-between text-sm text-slate-400">
          <span>
            {course.completed_lessons} of {course.total_lessons} complete
          </span>
          <span className="font-semibold text-cyan-400">{course.completion_pct}%</span>
        </div>
        <ProgressBar
          className="bg-slate-700"
          barClassName="bg-cyan-400"
          value={course.completion_pct}
        />
      </div>

      <h2 className="mt-10 text-lg font-bold text-slate-900">Lessons</h2>
      <div className="mt-4 space-y-2">
        {course.lessons.map((lesson, i) => {
          const completed = lesson.status === "completed";
          const inProgress = lesson.status === "in_progress";
          const cta = completed ? "Review" : inProgress ? "Continue" : "Start";

          return (
            <div
              key={lesson.id}
              className={clsx(
                "card flex items-center gap-4 p-4 transition duration-300 hover:-translate-y-0.5 hover:shadow-elevated",
                completed && "border-emerald-200 bg-emerald-50/50"
              )}
            >
              <span
                className={clsx(
                  "flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-sm font-bold",
                  completed
                    ? "bg-emerald-100 text-emerald-700"
                    : inProgress
                      ? "bg-cyan-50 text-cyan-700"
                      : "bg-slate-100 text-slate-600"
                )}
              >
                {completed ? (
                  <Check className="h-4 w-4" />
                ) : inProgress ? (
                  <CircleDashed className="h-4 w-4" />
                ) : (
                  i + 1
                )}
              </span>
              <div className="min-w-0 flex-1">
                <p className="truncate font-semibold text-slate-900">{lesson.title}</p>
                <p className="mt-0.5 text-xs capitalize text-slate-400">
                  {lesson.lesson_type.replace("_", " ")} · {lesson.estimated_minutes} min
                </p>
              </div>
              <Link
                href={`/dashboard/courses/${course.slug}/lessons/${lesson.slug}/content`}
                className="btn-secondary shrink-0 px-4 py-2"
              >
                {cta}
              </Link>
            </div>
          );
        })}

        {course.lessons.length === 0 && (
          <div className="card p-12 text-center">
            <FileText className="mx-auto h-10 w-10 text-slate-300" />
            <p className="mt-3 text-slate-500">No lessons in this course yet.</p>
          </div>
        )}
      </div>
    </div>
  );
}
