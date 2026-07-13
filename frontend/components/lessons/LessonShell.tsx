"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BookOpen, ClipboardCheck, Gauge, MonitorPlay, Timer } from "lucide-react";
import clsx from "clsx";
import { lessonStepHref, lessonStepProgress, type LessonStep } from "@/lib/lesson-steps";
import { ProgressBar } from "@/components/shared/ProgressBar";
import { Reveal } from "@/components/shared/Reveal";
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";

export function LessonShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { lesson, isLoading, notice, slug, lessonSlug, videoUrl, needsVideo } =
    useLessonWorkspace();

  if (isLoading) return <p className="animate-pulse text-craft-faint">Loading lesson…</p>;
  if (!lesson) return <p className="text-craft-muted">Lesson not found.</p>;

  const statusUi = lessonStepProgress(lesson, { needsVideo });
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
    <div className="mx-auto max-w-3xl">
      <Reveal>
        <p className="flex flex-wrap items-center gap-x-2 gap-y-1 text-sm text-craft-muted">
          <Link
            href={`/dashboard/courses/${lesson.course_slug}`}
            className="font-medium text-cyan-600 hover:underline dark:text-cyan-400"
          >
            {lesson.course_title}
          </Link>
          <span aria-hidden className="text-craft-faint">
            ·
          </span>
          <span className="inline-flex items-center gap-1">
            <Timer className="h-3.5 w-3.5" />
            {lesson.estimated_minutes} min
          </span>
          <span aria-hidden className="text-craft-faint">
            ·
          </span>
          <span className="capitalize">{lesson.lesson_type.replace("_", " ")}</span>
        </p>

        <h1 className="mt-3 text-3xl font-bold tracking-tight text-craft-ink">{lesson.title}</h1>

        <div className="mt-4 flex items-center gap-3">
          <ProgressBar className="flex-1" value={statusUi.pct} />
          <span className="text-sm font-medium text-craft-muted">{statusUi.text}</span>
        </div>
      </Reveal>

      <Reveal delay={80} variant="scale">
        <nav
          className="mt-6 flex gap-1 rounded-2xl border border-craft-border bg-craft-surface p-1 shadow-soft"
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
                    ? "bg-craft-accent-soft text-cyan-800 shadow-soft ring-1 ring-cyan-500/20 dark:text-cyan-200"
                    : "text-craft-muted hover:bg-craft-soft hover:text-craft-ink"
                )}
                aria-current={isActive ? "page" : undefined}
              >
                <Icon className="h-4 w-4 shrink-0" />
                <span className="hidden sm:inline">{label}</span>
              </Link>
            );
          })}
        </nav>
      </Reveal>

      {notice && (
        <div className="mt-4 rounded-xl border border-amber-500/30 bg-amber-50 px-4 py-3 text-sm text-amber-800 dark:bg-amber-500/10 dark:text-amber-200">
          {notice}
        </div>
      )}

      <div className="mt-6">{children}</div>
    </div>
  );
}
