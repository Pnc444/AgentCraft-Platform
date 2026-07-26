"use client";

import Link from "next/link";
import { ArrowRight, PartyPopper, Trophy } from "lucide-react";

interface ModuleHandoffProps {
  /** Module just finished. */
  courseTitle: string;
  /** Null when this was the last module in the course. */
  nextModule: { slug: string; title: string; totalLessons: number; href: string } | null;
  /** Exams get a louder headline than an ordinary final lesson. */
  isExam: boolean;
}

/**
 * The forward step after finishing a module.
 *
 * Passing a module exam used to be a dead end: the exam is the module's last
 * lesson, so the prev/next footer had no `next` to render and the only way on
 * was the sidebar. Finishing something and being shown nothing reads as "the
 * course stops here".
 *
 * Deliberately the single loudest thing on the page at that moment — one
 * obvious action, named after where it goes, so the learner never has to work
 * out what happens next.
 */
export function ModuleHandoff({ courseTitle, nextModule, isExam }: ModuleHandoffProps) {
  if (!nextModule) {
    return (
      <div className="rounded-2xl border border-amber-500/30 bg-gradient-to-br from-amber-50 to-craft-surface px-5 py-5 shadow-soft dark:from-amber-500/10 dark:to-craft-surface">
        <div className="flex items-start gap-3">
          <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-amber-500/15 text-amber-600 dark:text-amber-300">
            <Trophy className="h-5 w-5" />
          </span>
          <div className="min-w-0 flex-1">
            <p className="text-base font-bold text-craft-ink">
              That&apos;s the last module — you finished the course.
            </p>
            <p className="mt-1 text-sm text-craft-muted">
              You went from no AI background to building and evaluating real agents.
            </p>
            <Link href="/dashboard" className="btn-primary mt-4">
              Back to dashboard
              <ArrowRight className="h-4 w-4 shrink-0" />
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-cyan-500/30 bg-gradient-to-br from-cyan-50 to-craft-surface px-5 py-5 shadow-soft dark:from-cyan-500/10 dark:to-craft-surface">
      <div className="flex items-start gap-3">
        <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-cyan-500/15 text-cyan-600 dark:text-cyan-300">
          <PartyPopper className="h-5 w-5" />
        </span>
        <div className="min-w-0 flex-1">
          <p className="text-base font-bold text-craft-ink">
            {isExam ? `${courseTitle} — exam passed.` : `${courseTitle} complete.`}
          </p>
          <p className="mt-1 text-sm text-craft-muted">
            Up next: <span className="font-medium text-craft-ink">{nextModule.title}</span>
            {nextModule.totalLessons > 0 && ` · ${nextModule.totalLessons} lessons`}
          </p>
          <Link href={nextModule.href} className="btn-primary mt-4">
            Start {nextModule.title}
            <ArrowRight className="h-4 w-4 shrink-0" />
          </Link>
        </div>
      </div>
    </div>
  );
}
