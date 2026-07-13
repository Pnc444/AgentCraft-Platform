"use client";

import Link from "next/link";
import { BookOpen, ChevronLeft, ChevronRight, FileText, Wrench } from "lucide-react";
import { LessonContent } from "@/components/lessons/LessonContent";
import { LessonSection } from "@/components/lessons/LessonSection";
import { useLessonWorkspace } from "@/components/lessons/LessonWorkspace";
import { lessonStepHref, stepAfterContent } from "@/lib/lesson-steps";

export default function LessonContentPage() {
  const { slug, lessonSlug, lesson, videoUrl, prev } = useLessonWorkspace();

  if (!lesson) return null;

  const nextStep = stepAfterContent(!!videoUrl);
  const nextLabel = nextStep === "video" ? "Continue to Video" : "Continue to Recap Quiz";

  return (
    <div className="space-y-4">
      {lesson.content ? (
        <LessonSection title="Lesson Content" icon={<BookOpen className="h-4 w-4 text-cyan-600" />}>
          <LessonContent content={lesson.content} />
        </LessonSection>
      ) : (
        <LessonSection
          title="Lesson Content"
          icon={<FileText className="h-4 w-4 text-cyan-600" />}
          empty
        />
      )}

      {lesson.lesson_type === "sandbox" && (
        <LessonSection
          title="Interactive Demo"
          icon={<Wrench className="h-4 w-4 text-cyan-600" />}
        >
          <p className="text-sm text-slate-500">Sandbox</p>
          <button
            type="button"
            onClick={() =>
              alert("Sandbox integration coming soon — Diego & Douglas wiring it up.")
            }
            className="btn-primary mt-4"
          >
            <Wrench className="h-4 w-4" />
            Launch Sandbox
          </button>
        </LessonSection>
      )}

      <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
        {prev ? (
          <Link href={lessonStepHref(slug, prev.slug, "content")} className="btn-secondary">
            <ChevronLeft className="h-4 w-4" />
            {prev.title}
          </Link>
        ) : (
          <span />
        )}
        <Link href={lessonStepHref(slug, lessonSlug, nextStep)} className="btn-primary">
          {nextLabel}
          <ChevronRight className="h-4 w-4" />
        </Link>
      </div>
    </div>
  );
}
