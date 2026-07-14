"use client";

import Link from "next/link";
import { ChevronLeft, ChevronRight, ClipboardCheck, MonitorPlay } from "lucide-react";
import { LessonContent } from "@/components/lessons/LessonContent";
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";
import { Reveal } from "@/components/shared/Reveal";
import { lessonStepHref, stepAfterContent } from "@/lib/lesson-steps";

export default function LessonContentPage() {
  const { slug, lessonSlug, lesson, videoUrl, prev, next } = useLessonWorkspace();

  if (!lesson) return null;

  const nextStep = stepAfterContent(!!videoUrl);
  const hasVideo = nextStep === "video";

  return (
    <div className="space-y-10">
      {lesson.content ? (
        <LessonContent content={lesson.content} />
      ) : (
        <p className="text-sm text-craft-faint">No content yet.</p>
      )}

      {/* End-of-lesson: quiz prompt + navigation */}
      <Reveal delay={80}>
        <div className="border-t border-craft-border pt-8">
          <div className="flex flex-col items-center gap-3 text-center">
            <h2 className="text-lg font-bold text-craft-ink">
              {hasVideo ? "Up next: the lesson video" : "Ready to check your understanding?"}
            </h2>
            <p className="max-w-md text-sm text-craft-muted">
              {hasVideo
                ? "Watch the video, then take the recap quiz to finish this lesson."
                : "Pass the recap quiz (80%+) to complete this lesson and move on."}
            </p>
            <Link href={lessonStepHref(slug, lessonSlug, nextStep)} className="btn-primary mt-1">
              {hasVideo ? (
                <>
                  <MonitorPlay className="h-4 w-4" />
                  Watch Video
                </>
              ) : (
                <>
                  <ClipboardCheck className="h-4 w-4" />
                  Start Recap Quiz
                </>
              )}
            </Link>
          </div>

          <div className="mt-8 flex flex-wrap items-center justify-between gap-3">
            {prev ? (
              <Link href={lessonStepHref(slug, prev.slug, "content")} className="btn-secondary">
                <ChevronLeft className="h-4 w-4" />
                {prev.title}
              </Link>
            ) : (
              <span />
            )}
            {next && (
              <Link href={lessonStepHref(slug, next.slug, "content")} className="btn-secondary">
                {next.title}
                <ChevronRight className="h-4 w-4" />
              </Link>
            )}
          </div>
        </div>
      </Reveal>
    </div>
  );
}
