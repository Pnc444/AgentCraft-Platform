"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BookOpen, ClipboardCheck, Gauge, MonitorPlay, Timer } from "lucide-react";
import clsx from "clsx";
import { lessonStepHref, statusUiFor, type LessonStep } from "@/lib/lesson-steps";
import { ProgressBar } from "@/components/shared/ProgressBar";
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";

export function LessonShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { lesson, isLoading, notice, slug, lessonSlug, videoUrl } = useLessonWorkspace();

  if (isLoading) return <p className="animate-pulse text-slate-500">Loading lesson…</p>;
  if (!lesson) return <p className="text-slate-500">Lesson not found.</p>;

  const statusUi = statusUiFor(lesson.status);
  const hasVideo = !!videoUrl;

  const steps: { id: LessonStep; label: string; icon: typeof BookOpen }[] = [
    { id: "content", label: "Content", icon: BookOpen },
    ...(hasVideo ? [{ id: "video" as const, label: "Video", icon: MonitorPlay }] : []),
    { id: "quiz", label: "Recap Quiz", icon: ClipboardCheck },
    { id: "progress", label: "Progress", icon: Gauge },
  ];

  const active =
    steps.find((step) => pathname.endsWith(`/${step.id}`))?.id ?? ("content" as LessonStep);

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

      <h1 className="mt-3 text-3xl font-bold tracking-tight text-slate-900">{lesson.title}</h1>

      <div className="mt-4 flex items-center gap-3">
        <ProgressBar className="flex-1" value={statusUi.pct} />
        <span className="text-sm font-medium text-slate-500">{statusUi.text}</span>
      </div>

      <nav
        className="mt-6 flex gap-1 rounded-2xl border border-slate-200/80 bg-white p-1 shadow-soft ring-1 ring-black/[0.02]"
        aria-label="Lesson steps"
      >
        {steps.map(({ id, label, icon: Icon }) => {
          const href = lessonStepHref(slug, lessonSlug, id);
          const isActive = active === id;
          return (
            <Link
              key={id}
              href={href}
              className={clsx(
                "flex flex-1 items-center justify-center gap-2 rounded-xl px-3 py-2.5 text-sm font-medium transition",
                isActive
                  ? "bg-cyan-50 text-cyan-800 shadow-soft ring-1 ring-cyan-100"
                  : "text-slate-500 hover:bg-slate-50 hover:text-slate-900"
              )}
              aria-current={isActive ? "page" : undefined}
            >
              <Icon className="h-4 w-4 shrink-0" />
              <span className="hidden sm:inline">{label}</span>
            </Link>
          );
        })}
      </nav>

      {notice && (
        <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">
          {notice}
        </div>
      )}

      <div className="mt-6">{children}</div>
    </div>
  );
}
