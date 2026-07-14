"use client";

import { useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ChevronLeft, ChevronRight, MonitorPlay } from "lucide-react";
import { LessonSection } from "@/components/lessons/LessonSection";
import { LessonVideo } from "@/components/lessons/LessonVideo";
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";
import { lessonStepHref } from "@/lib/lesson-steps";

export default function LessonVideoPage() {
  const router = useRouter();
  const { slug, lessonSlug, lesson, videoUrl, markVideoWatched } = useLessonWorkspace();

  useEffect(() => {
    if (lesson && !videoUrl) {
      router.replace(lessonStepHref(slug, lessonSlug, "content"));
    }
  }, [lesson, videoUrl, router, slug, lessonSlug]);

  if (!lesson || !videoUrl) return null;

  return (
    <div className="space-y-4">
      <LessonSection title="Video" icon={<MonitorPlay className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />}>
        <LessonVideo
          url={videoUrl}
          title={lesson.title}
          watched={lesson.video_watched}
          onWatched={markVideoWatched}
        />
        {lesson.video_watched ? (
          <p className="mt-3 text-sm text-emerald-700">Video watched. You can take the Recap Quiz.</p>
        ) : lesson.require_full_watch ? (
          <p className="mt-3 text-sm text-craft-muted">
            Watch all the way through to unlock the Recap Quiz.
          </p>
        ) : (
          <p className="mt-3 text-sm text-craft-muted">
            This video is optional. You can skip ahead to the Recap Quiz anytime.
          </p>
        )}
      </LessonSection>

      <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
        <Link href={lessonStepHref(slug, lessonSlug, "content")} className="btn-secondary">
          <ChevronLeft className="h-4 w-4" />
          Back to Content
        </Link>
        <Link href={lessonStepHref(slug, lessonSlug, "quiz")} className="btn-primary">
          Continue to Recap Quiz
          <ChevronRight className="h-4 w-4" />
        </Link>
      </div>
    </div>
  );
}
