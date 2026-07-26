"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";
import { lessonStepHref } from "@/lib/lesson-steps";

/**
 * The video step no longer exists as its own destination — the player renders
 * inline in the lesson step. This route is kept only so existing links,
 * bookmarks, and browser history land somewhere real instead of 404ing.
 */
export default function LessonVideoPage() {
  const router = useRouter();
  const { slug, lessonSlug } = useLessonWorkspace();

  useEffect(() => {
    router.replace(lessonStepHref(slug, lessonSlug, "content"));
  }, [router, slug, lessonSlug]);

  return <p className="text-sm text-craft-muted">Taking you to the lesson…</p>;
}
