"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { ChevronLeft, ChevronRight, ClipboardCheck } from "lucide-react";
import { LessonSection } from "@/components/lessons/LessonSection";
import { RecapQuiz } from "@/components/lessons/RecapQuiz";
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";
import { lessonStepHref } from "@/lib/lesson-steps";

export default function LessonQuizPage() {
  const router = useRouter();
  const {
    slug,
    lessonSlug,
    lesson,
    recapQuestions,
    needsVideo,
    videoDone,
    setNotice,
    updateProgress,
  } = useLessonWorkspace();

  if (!lesson) return null;

  return (
    <div className="space-y-4">
      <LessonSection
        title="Recap Quiz"
        icon={<ClipboardCheck className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />}
      >
        <RecapQuiz
          questions={recapQuestions}
          locked={needsVideo && !videoDone}
          lockedReason="Watch the lesson video to the end before taking the Recap Quiz."
          onLockedAction={() => {
            setNotice("Watch the lesson video all the way through before taking the Recap Quiz.");
            router.push(lessonStepHref(slug, lessonSlug, "video"));
          }}
          onPassed={(score) => {
            if (lesson.status !== "completed") {
              updateProgress({ status: "completed", score });
            }
            setNotice(null);
            router.push(lessonStepHref(slug, lessonSlug, "progress"));
          }}
        />
      </LessonSection>

      <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
        <Link href={lessonStepHref(slug, lessonSlug, "content")} className="btn-secondary">
          <ChevronLeft className="h-4 w-4" />
          Back to Content
        </Link>
        <Link href={lessonStepHref(slug, lessonSlug, "progress")} className="btn-secondary">
          Progress
          <ChevronRight className="h-4 w-4" />
        </Link>
      </div>
    </div>
  );
}
