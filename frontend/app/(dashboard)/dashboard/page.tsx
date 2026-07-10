"use client";

import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { BookOpen, Clock, Inbox } from "lucide-react";
import { getCourses } from "@/lib/api/courses";
import { useAuthStore } from "@/stores/authStore";
import { DifficultyBadge } from "@/components/dashboard/DifficultyBadge";

export default function StudentDashboardPage() {
  const user = useAuthStore((s) => s.user);
  const { data: courses, isLoading } = useQuery({ queryKey: ["courses"], queryFn: getCourses });

  return (
    <div className="mx-auto max-w-4xl">
      <h1 className="text-2xl font-bold text-white">Hello, {user?.username}</h1>
      <p className="mt-1 text-slate-400">Your personalized learning path</p>

      <h2 className="mt-8 flex items-center gap-2 text-lg font-semibold text-white">
        <BookOpen className="h-5 w-5 text-craft-glow" /> Courses
      </h2>

      {isLoading && <p className="mt-6 animate-pulse text-slate-500">Loading courses…</p>}

      <div className="mt-4 space-y-4">
        {courses?.map((course) => (
          <div
            key={course.slug}
            className="flex flex-col gap-4 rounded-2xl border border-white/10 bg-craft-900/60 p-6 sm:flex-row sm:items-center"
          >
            <div className="min-w-0 flex-1">
              <div className="flex flex-wrap items-center gap-3">
                <h3 className="font-semibold text-white">{course.title}</h3>
                <DifficultyBadge difficulty={course.difficulty} />
              </div>
              <p className="mt-2 text-sm text-slate-400">
                {course.description || "No description yet."}
              </p>
              <div className="mt-3 flex items-center gap-4 text-xs text-slate-500">
                <span className="flex items-center gap-1">
                  <Clock className="h-3.5 w-3.5" /> {course.total_minutes ?? "-"} min
                </span>
                <span className="flex items-center gap-1">
                  <BookOpen className="h-3.5 w-3.5" /> {course.total_lessons} lessons
                </span>
              </div>
              <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-craft-800">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-craft-accent to-craft-glow transition-all"
                  style={{ width: `${course.completion_pct}%` }}
                />
              </div>
            </div>
            <Link
              href={`/dashboard/courses/${course.slug}`}
              className="shrink-0 rounded-lg bg-craft-accent px-5 py-2.5 text-center text-sm font-medium text-white transition-colors hover:bg-indigo-500"
            >
              {course.completion_pct > 0 ? "Continue" : "Start"}
            </Link>
          </div>
        ))}

        {courses?.length === 0 && (
          <div className="rounded-2xl border border-white/10 bg-craft-900/60 p-12 text-center">
            <Inbox className="mx-auto h-10 w-10 text-slate-600" />
            <p className="mt-3 text-slate-400">No courses available yet. Check back soon!</p>
          </div>
        )}
      </div>
    </div>
  );
}
