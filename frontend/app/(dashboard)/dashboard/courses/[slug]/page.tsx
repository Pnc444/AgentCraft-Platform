"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { Check } from "lucide-react";
import clsx from "clsx";
import { getCourse } from "@/lib/api/courses";
import { DifficultyBadge } from "@/components/dashboard/DifficultyBadge";

export default function CourseDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const { data: course, isLoading } = useQuery({
    queryKey: ["course", slug],
    queryFn: () => getCourse(slug),
    enabled: !!slug,
  });

  if (isLoading) return <p className="animate-pulse text-slate-500">Loading course…</p>;
  if (!course) return <p className="text-slate-400">Course not found.</p>;

  return (
    <div className="mx-auto max-w-4xl">
      <p className="text-sm text-slate-500">
        <Link href="/dashboard" className="text-craft-glow hover:underline">Dashboard</Link>
        <span aria-hidden> / </span>
        {course.lessons.length} lessons
      </p>
      <div className="mt-2 flex flex-wrap items-center gap-3">
        <h1 className="text-2xl font-bold text-white">{course.title}</h1>
        <DifficultyBadge difficulty={course.difficulty} />
      </div>
      {course.description && <p className="mt-3 max-w-2xl text-slate-400">{course.description}</p>}

      <h2 className="mt-10 text-lg font-semibold text-white">Lessons</h2>
      <div className="mt-4 space-y-3">
        {course.lessons.map((lesson, i) => {
          const completed = lesson.status === "completed";
          return (
            <div
              key={lesson.id}
              className={clsx(
                "flex items-center gap-4 rounded-xl border p-4",
                completed
                  ? "border-emerald-500/30 bg-emerald-950/10"
                  : "border-white/10 bg-craft-900/60"
              )}
            >
              <span
                className={clsx(
                  "flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-sm font-bold",
                  completed ? "bg-emerald-500/20 text-emerald-300" : "bg-craft-800 text-slate-300"
                )}
              >
                {completed ? <Check className="h-4 w-4" /> : i + 1}
              </span>
              <span className="min-w-0 flex-1 truncate font-medium text-white">{lesson.title}</span>
              <span className="shrink-0 text-xs text-slate-500">{lesson.estimated_minutes} min</span>
              <Link
                href={`/dashboard/courses/${course.slug}/lessons/${lesson.slug}`}
                className="shrink-0 rounded-lg border border-white/15 px-4 py-2 text-sm text-slate-200 transition-colors hover:border-craft-accent hover:text-white"
              >
                {completed ? "Review" : "Start"}
              </Link>
            </div>
          );
        })}

        {course.lessons.length === 0 && (
          <div className="rounded-2xl border border-white/10 bg-craft-900/60 p-12 text-center">
            <p className="text-4xl">📝</p>
            <p className="mt-3 text-slate-400">No lessons in this course yet.</p>
          </div>
        )}
      </div>
    </div>
  );
}
