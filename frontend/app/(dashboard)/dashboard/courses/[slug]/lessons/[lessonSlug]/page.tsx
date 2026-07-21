"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";
import { entryStepForLessonType, lessonStepHref } from "@/lib/lesson-steps";

export default function LessonIndexPage() {
  const router = useRouter();
  const { slug, lessonSlug, lesson, isLoading } = useLessonWorkspace();

  useEffect(() => {
    if (!lesson) return;
    router.replace(
      lessonStepHref(slug, lessonSlug, entryStepForLessonType(lesson.lesson_type))
    );
  }, [lesson, lessonSlug, router, slug]);

  if (isLoading || !lesson) return null;

  return null;
}
