"use client";

import { useEffect } from "react";
import Link from "next/link";
import { ChevronRight } from "lucide-react";
import {
  TRACK_LESSON_TITLE,
  moduleDisplayTitle,
} from "@/lib/learning-track";
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";
import { usePageChrome } from "@/stores/pageChrome";

/** Lesson chrome: breadcrumb + main content. Ask Tutor stays in the topbar. */
export function LessonStudioLayout({ children }: { children: React.ReactNode }) {
  const { lesson, course, openTutor, isLoading } = useLessonWorkspace();
  const setChrome = usePageChrome((s) => s.setChrome);
  const clearChrome = usePageChrome((s) => s.clearChrome);

  const lessons = course?.lessons ?? [];
  const lessonIndex = lessons.findIndex((l) => l.slug === lesson?.slug);
  const stepOrdinal = lessonIndex >= 0 ? lessonIndex + 1 : 1;
  const moduleTitle = course ? moduleDisplayTitle(course) : "";

  useEffect(() => {
    if (!lesson) {
      clearChrome();
      return;
    }
    setChrome({
      title: lesson.title,
      subtitle: `${lesson.estimated_minutes} min · Step ${stepOrdinal}/${lessons.length || "—"}`,
      showAskTutor: true,
      onAskTutor: openTutor,
      headerTabs: null,
      activeTab: null,
      onTabChange: null,
    });
    return () => clearChrome();
  }, [lesson, stepOrdinal, lessons.length, openTutor, setChrome, clearChrome]);

  if (isLoading || !lesson) {
    return <>{children}</>;
  }

  const hubHref = course ? `/dashboard/courses/${course.slug}` : "/dashboard";

  return (
    <div className="mx-auto flex h-full min-h-0 w-full max-w-[1400px] flex-col">
      <nav
        className="mb-2 flex shrink-0 flex-wrap items-center gap-1 text-xs text-craft-muted sm:gap-1.5 sm:text-sm"
        aria-label="Breadcrumb"
      >
        <Link href={hubHref} className="hover:text-violet-600 dark:hover:text-violet-400">
          Lessons
        </Link>
        <ChevronRight className="h-3.5 w-3.5 shrink-0 text-craft-faint" />
        <Link
          href={hubHref}
          className="max-w-[40%] truncate hover:text-violet-600 dark:hover:text-violet-400 sm:max-w-none"
        >
          {TRACK_LESSON_TITLE}
        </Link>
        {moduleTitle ? (
          <>
            <ChevronRight className="h-3.5 w-3.5 shrink-0 text-craft-faint" />
            <span className="max-w-[40%] truncate text-craft-ink sm:max-w-none">
              {moduleTitle}
            </span>
          </>
        ) : null}
      </nav>

      <div className="flex min-h-0 flex-1 flex-col">{children}</div>
    </div>
  );
}
