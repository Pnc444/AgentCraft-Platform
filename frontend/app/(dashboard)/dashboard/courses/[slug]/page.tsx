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
import { Reveal } from "@/components/shared/Reveal";

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

  if (isLoading && !course) return <p className="animate-pulse text-craft-faint">Loading course…</p>;
  if (!course) return <p className="text-craft-muted">Course not found.</p>;

  return (
    <div className="mx-auto max-w-3xl">
      <Reveal>
        <p className="text-sm text-craft-muted">
          <Link
            href="/dashboard"
            className="font-medium text-cyan-600 hover:underline dark:text-cyan-400"
          >
            Dashboard
          </Link>
          <span aria-hidden> / </span>
          {course.lessons.length} lessons
        </p>

        <div className="mt-3 flex flex-wrap items-center gap-3">
          <h1 className="text-3xl font-bold tracking-tight text-craft-ink">{course.title}</h1>
          <DifficultyBadge difficulty={course.difficulty} />
        </div>

        {course.description && (
          <p className="mt-3 max-w-2xl leading-relaxed text-craft-muted">{course.description}</p>
        )}
      </Reveal>

      <Reveal delay={80} variant="scale" className="mt-6">
        <div className="card p-5">
          <div className="mb-2 flex justify-between text-sm text-craft-muted">
            <span>
              {course.completed_lessons} of {course.total_lessons} complete
            </span>
            <span className="font-semibold text-craft-ink">
              {course.completion_pct}%
            </span>
          </div>
          <ProgressBar value={course.completion_pct} />
        </div>
      </Reveal>

      <Reveal delay={100} className="mt-10">
        <h2 className="text-lg font-bold text-craft-ink">Lessons</h2>
      </Reveal>
      <div className="mt-4 space-y-2">
        {course.lessons.map((lesson, i) => {
          const completed = lesson.status === "completed";
          const inProgress = lesson.status === "in_progress";
          const cta = completed ? "Review" : inProgress ? "Continue" : "Start";

          return (
            <Reveal key={lesson.id} delay={Math.min(i * 50, 280)} as="div">
              <div
                className={clsx(
                  "card flex items-center gap-4 p-4",
                  completed && "border-emerald-300/40 bg-emerald-50/30 dark:border-emerald-500/20 dark:bg-emerald-500/5"
                )}
              >
                <span
                  className={clsx(
                    "flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-sm font-bold",
                    completed
                      ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-300"
                      : inProgress
                        ? "bg-craft-accent-soft text-cyan-700 dark:text-cyan-300"
                        : "bg-craft-soft text-craft-muted"
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
                  <p className="truncate font-semibold text-craft-ink">{lesson.title}</p>
                  <p className="mt-0.5 text-xs capitalize text-craft-faint">
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
            </Reveal>
          );
        })}

        {course.lessons.length === 0 && (
          <div className="card p-12 text-center">
            <FileText className="mx-auto h-10 w-10 text-craft-faint" />
            <p className="mt-3 text-craft-muted">No lessons in this course yet.</p>
          </div>
        )}
      </div>
    </div>
  );
}
