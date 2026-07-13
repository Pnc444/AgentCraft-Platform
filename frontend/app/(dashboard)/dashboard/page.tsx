"use client";

import { useState } from "react";
import Link from "next/link";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { ArrowRight, BookOpen, CheckCircle2, ChevronDown, Clock, Inbox } from "lucide-react";
import { getCourses, getDashboardStats } from "@/lib/api/courses";
import { deriveLearningPath, lessonHref } from "@/lib/learning-path";
import { useAuthStore } from "@/stores/authStore";
import { DifficultyBadge } from "@/components/dashboard/DifficultyBadge";
import { ProgressBar } from "@/components/shared/ProgressBar";
import { Reveal } from "@/components/shared/Reveal";

export default function StudentDashboardPage() {
  const user = useAuthStore((s) => s.user);
  const queryClient = useQueryClient();
  const [pathOpen, setPathOpen] = useState(false);
  const { data: courses, isLoading } = useQuery({
    queryKey: ["courses"],
    queryFn: async () => {
      const list = await getCourses();
      for (const course of list) {
        queryClient.setQueryData(["course", course.slug], course);
      }
      return list;
    },
  });
  const { data: stats } = useQuery({ queryKey: ["dashboard-stats"], queryFn: getDashboardStats });

  const path = courses ? deriveLearningPath(courses, courses) : null;
  const detailsReady = !!courses;

  return (
    <div className="mx-auto max-w-5xl">
      <Reveal>
        <h1 className="text-3xl font-bold tracking-tight text-craft-ink">
          Hello, {user?.username}
        </h1>
        <p className="mt-1 text-craft-muted">Pick up where you left off</p>
      </Reveal>

      <div className="mt-8 grid gap-4 lg:grid-cols-3">
        <Reveal className="lg:col-span-2" delay={60}>
          <div className="card card-interactive p-6 h-full">
            <p className="text-xs font-bold uppercase tracking-wide text-cyan-600 dark:text-cyan-400">
              Continue learning
            </p>
            {!detailsReady && <p className="mt-4 animate-pulse text-sm text-craft-faint">Loading…</p>}
            {detailsReady && path?.continueTarget ? (
              <div className="mt-3">
                <p className="text-sm text-craft-muted">{path.continueTarget.courseTitle}</p>
                <h2 className="mt-1 text-xl font-bold text-craft-ink">
                  {path.continueTarget.lesson.title}
                </h2>
                <p className="mt-2 text-sm text-craft-muted">
                  {path.continueTarget.lesson.estimated_minutes} min ·{" "}
                  {path.continueTarget.lesson.lesson_type.replace("_", " ")}
                </p>
                <Link href={lessonHref(path.continueTarget)} className="btn-primary mt-5">
                  Continue <ArrowRight className="h-4 w-4" />
                </Link>
              </div>
            ) : null}
            {detailsReady && !path?.continueTarget && (
              <p className="mt-4 text-sm text-craft-muted">
                {courses?.length
                  ? "All available lessons are complete."
                  : "No lessons available yet."}
              </p>
            )}
          </div>
        </Reveal>

        <Reveal delay={140} variant="scale">
          <div className="rounded-2xl bg-craft-navy p-6 text-white shadow-navy ring-1 ring-white/10 h-full">
            <p className="text-xs font-bold uppercase tracking-wide text-craft-faint">
              Overall progress
            </p>
            <p className="mt-3 text-4xl font-bold text-white">
              {stats?.overall_progress_pct ?? 0}%
            </p>
            <ProgressBar
              className="mt-4 border-slate-500 bg-slate-800 shadow-none"
              value={stats?.overall_progress_pct ?? 0}
            />
            <p className="mt-3 text-sm text-craft-faint">
              {stats
                ? `${stats.lessons_completed} completed · ${stats.lessons_in_progress} in progress`
                : "—"}
            </p>
          </div>
        </Reveal>
      </div>

      <div className="mt-4 grid gap-4 md:grid-cols-2">
        <Reveal delay={100}>
          <div className="card card-interactive p-6 h-full">
            <p className="text-xs font-bold uppercase tracking-wide text-cyan-600 dark:text-cyan-400">
              Current module
            </p>
            {path?.currentModule ? (
              <div className="mt-3">
                <div className="flex flex-wrap items-center gap-2">
                  <h3 className="font-bold text-craft-ink">{path.currentModule.title}</h3>
                  <DifficultyBadge difficulty={path.currentModule.difficulty} />
                </div>
                <ProgressBar className="mt-4" value={path.currentModule.completion_pct} />
                <p className="mt-2 text-sm text-craft-muted">
                  {path.currentModule.completed_lessons} of {path.currentModule.total_lessons}{" "}
                  lessons
                </p>
                <Link
                  href={`/dashboard/courses/${path.currentModule.slug}`}
                  className="mt-4 inline-flex text-sm font-semibold text-cyan-600 hover:underline dark:text-cyan-400"
                >
                  View module
                </Link>
              </div>
            ) : (
              <p className="mt-4 text-sm text-craft-muted">No module in progress.</p>
            )}
          </div>
        </Reveal>

        <Reveal delay={180}>
          <div className="card card-interactive p-6 h-full">
            <p className="text-xs font-bold uppercase tracking-wide text-cyan-600 dark:text-cyan-400">
              Recently completed
            </p>
            {detailsReady && path && path.recentCompleted.length > 0 ? (
              <ul className="mt-3 space-y-2">
                {path.recentCompleted.map((ref) => (
                  <li key={`${ref.courseSlug}-${ref.lesson.id}`}>
                    <Link
                      href={lessonHref(ref)}
                      className="flex items-start gap-2 rounded-xl px-2 py-2 text-sm transition hover:bg-craft-soft"
                    >
                      <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-600" />
                      <span>
                        <span className="font-medium text-craft-ink">{ref.lesson.title}</span>
                        <span className="block text-xs text-craft-faint">{ref.courseTitle}</span>
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="mt-4 text-sm text-craft-muted">No completed lessons yet.</p>
            )}
          </div>
        </Reveal>
      </div>

      <Reveal delay={120} className="mt-4">
        <div className="card card-interactive p-6">
          <p className="text-xs font-bold uppercase tracking-wide text-cyan-600 dark:text-cyan-400">
            Upcoming lessons
          </p>
          {detailsReady && path && path.upcoming.length > 0 ? (
            <ul className="mt-3 divide-y divide-craft-border">
              {path.upcoming.map((ref) => (
                <li key={`${ref.courseSlug}-${ref.lesson.id}`}>
                  <Link
                    href={lessonHref(ref)}
                    className="flex items-center justify-between gap-4 py-3 transition hover:opacity-80"
                  >
                    <span>
                      <span className="font-medium text-craft-ink">{ref.lesson.title}</span>
                      <span className="mt-0.5 block text-xs text-craft-faint">{ref.courseTitle}</span>
                    </span>
                    <span className="shrink-0 text-xs text-craft-faint">
                      {ref.lesson.estimated_minutes} min
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          ) : (
            <p className="mt-4 text-sm text-craft-muted">No upcoming lessons.</p>
          )}
        </div>
      </Reveal>

      <Reveal className="mt-10" delay={80}>
        <button
          type="button"
          onClick={() => setPathOpen((open) => !open)}
          aria-expanded={pathOpen}
          className="flex w-full items-center justify-between gap-3 text-left"
        >
          <h2 className="flex items-center gap-2 text-lg font-bold text-craft-ink">
            <BookOpen className="h-5 w-5 text-cyan-600 dark:text-cyan-400" /> Create an AI Agent
          </h2>
          <span className="flex shrink-0 items-center gap-1.5 text-sm font-medium text-craft-muted">
            {pathOpen ? "View less" : "View more"}
            <ChevronDown
              className={`h-5 w-5 text-craft-faint transition-transform ${
                pathOpen ? "rotate-180" : ""
              }`}
            />
          </span>
        </button>
      </Reveal>

        {pathOpen && (
          <div className="mt-1">
            <p className="text-sm text-craft-muted">Modules 1–8 in this learning path</p>

            {isLoading && <p className="mt-6 animate-pulse text-craft-faint">Loading courses…</p>}

            <div className="mt-4 space-y-3">
              {courses?.map((course, i) => (
                <Reveal key={course.slug} delay={i * 60}>
                  <div className="card card-interactive flex flex-col gap-4 p-5 sm:flex-row sm:items-center">
                    <div className="min-w-0 flex-1">
                      <div className="flex flex-wrap items-center gap-3">
                        <h3 className="font-bold text-craft-ink">{course.title}</h3>
                        <DifficultyBadge difficulty={course.difficulty} />
                      </div>
                      <p className="mt-2 text-sm text-craft-muted">
                        {course.description || "No description yet."}
                      </p>
                      <div className="mt-3 flex items-center gap-4 text-xs text-craft-faint">
                        <span className="flex items-center gap-1">
                          <Clock className="h-3.5 w-3.5" /> {course.total_minutes ?? "—"} min
                        </span>
                        <span className="flex items-center gap-1">
                          <BookOpen className="h-3.5 w-3.5" /> {course.total_lessons} lessons
                        </span>
                      </div>
                      <ProgressBar className="mt-3" value={course.completion_pct} />
                    </div>
                    <Link
                      href={`/dashboard/courses/${course.slug}`}
                      className="btn-primary shrink-0"
                    >
                      {course.completion_pct > 0 ? "Continue" : "Start"}
                    </Link>
                  </div>
                </Reveal>
              ))}

              {courses?.length === 0 && (
                <div className="card p-12 text-center">
                  <Inbox className="mx-auto h-10 w-10 text-craft-faint" />
                  <p className="mt-3 text-craft-muted">
                    No courses available yet. Check back soon!
                  </p>
                </div>
              )}
            </div>
          </div>
        )}
    </div>
  );
}
