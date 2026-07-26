"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { LessonPlayer } from "@/components/lessons/LessonPlayer";
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";
import { lessonStepHref } from "@/lib/lesson-steps";

/**
 * The lesson content step IS the player (plan step 7: the stacked page, the
 * old deck, and the per-module flag are gone — one lesson UI exists).
 * Exam-type lessons have no content step; they go straight to the quiz.
 */
export default function LessonContentPage() {
  const router = useRouter();
  const { slug, lessonSlug, lesson } = useLessonWorkspace();

  useEffect(() => {
    if (!lesson || lesson.lesson_type !== "quiz") return;
    router.replace(lessonStepHref(slug, lessonSlug, "quiz"));
  }, [lesson, lessonSlug, router, slug]);

  if (!lesson || lesson.lesson_type === "quiz") return null;

  return <LessonPlayer />;
}
