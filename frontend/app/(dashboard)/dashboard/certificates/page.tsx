"use client";

import Link from "next/link";
import { useEffect, useMemo } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Award, Lock, ScrollText } from "lucide-react";
import { getCourses } from "@/lib/api/courses";
import { usePageChrome } from "@/stores/pageChrome";
import {
  TRACK_LESSON_TITLE,
  currentModule,
  isModuleComplete,
  trackModulesFrom,
} from "@/lib/learning-track";

/**
 * One certificate per lesson. Right now the site has a single lesson —
 * Creating an AI Agent — so this page always shows that one slot.
 * Unlocks when every module in the lesson is complete.
 * Badge awards stay on Profile. Certificate artwork + typed name overlay come later.
 */
export default function CertificatesPage() {
  const setChrome = usePageChrome((s) => s.setChrome);
  const clearChrome = usePageChrome((s) => s.clearChrome);
  const queryClient = useQueryClient();

  const { data: allCourses, isLoading } = useQuery({
    queryKey: ["courses"],
    queryFn: async () => {
      const list = await getCourses();
      for (const course of list) {
        queryClient.setQueryData(["course", course.slug], course);
      }
      return list;
    },
  });

  const modules = useMemo(() => trackModulesFrom(allCourses ?? []), [allCourses]);
  const hasLesson = modules.length > 0;
  const unlocked = hasLesson && modules.every(isModuleComplete);
  const unlockedCount = unlocked ? 1 : 0;
  const total = hasLesson ? 1 : 0;
  const continueModule = currentModule(modules) ?? modules[0];
  const continueHref = continueModule
    ? `/dashboard/courses/${continueModule.slug}`
    : "/dashboard";

  useEffect(() => {
    setChrome({
      title: "Certificates",
      subtitle: isLoading
        ? "Loading…"
        : total
          ? `${unlockedCount}/${total} certificates`
          : "Complete a lesson to earn one",
      showAskTutor: false,
      onAskTutor: null,
      headerTabs: null,
      activeTab: null,
      onTabChange: null,
    });
    return () => clearChrome();
  }, [clearChrome, isLoading, setChrome, total, unlockedCount]);

  return (
    <div className="mx-auto max-w-4xl">
      <p className="text-sm text-craft-muted">
        Finish {TRACK_LESSON_TITLE} to unlock its certificate. Awards and badges live on your{" "}
        <Link
          href="/dashboard/profile"
          className="font-medium text-violet-600 hover:underline dark:text-violet-400"
        >
          profile
        </Link>
        .
      </p>

      {isLoading && <p className="mt-6 animate-pulse text-craft-faint">Loading…</p>}

      {!isLoading && unlocked && (
        <div className="mt-6 space-y-4">
          <h2 className="text-sm font-semibold uppercase tracking-[0.14em] text-craft-faint">
            Unlocked
          </h2>
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="card overflow-hidden p-0">
              <div
                className="relative flex aspect-[4/3] items-center justify-center bg-gradient-to-br from-[#1e1233] via-[#2e1f4a] to-violet-800"
                aria-hidden
              >
                <ScrollText className="h-12 w-12 text-violet-200/80" />
                <p className="absolute bottom-3 left-3 right-3 text-center text-xs text-violet-100/70">
                  Certificate template coming soon — you&apos;ll type your name to personalize it
                </p>
              </div>
              <div className="p-5">
                <div className="flex items-start gap-3">
                  <Award className="mt-0.5 h-5 w-5 shrink-0 text-violet-600 dark:text-violet-400" />
                  <div className="min-w-0">
                    <h3 className="font-semibold text-craft-ink">{TRACK_LESSON_TITLE}</h3>
                    <p className="mt-2 text-xs font-medium text-emerald-600 dark:text-emerald-400">
                      Unlocked
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {!isLoading && hasLesson && !unlocked && (
        <div className="mt-8 space-y-4">
          <h2 className="text-sm font-semibold uppercase tracking-[0.14em] text-craft-faint">
            In progress
          </h2>
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="card flex items-start gap-4 p-5 opacity-80">
              <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-craft-soft">
                <Lock className="h-5 w-5 text-craft-faint" />
              </span>
              <div className="min-w-0">
                <h3 className="font-semibold text-craft-ink">{TRACK_LESSON_TITLE}</h3>
                <p className="mt-2 text-xs font-medium text-craft-faint">
                  Locked — finish the lesson to unlock
                </p>
                <Link
                  href={continueHref}
                  className="mt-3 inline-flex text-sm font-semibold text-violet-600 hover:underline dark:text-violet-400"
                >
                  Continue lesson
                </Link>
              </div>
            </div>
          </div>
        </div>
      )}

      {!isLoading && !hasLesson && (
        <div className="card mt-8 p-10 text-center">
          <Award className="mx-auto h-10 w-10 text-craft-faint" />
          <p className="mt-3 text-craft-muted">No certificates available yet.</p>
          <Link href="/dashboard" className="btn-primary mt-6">
            Back to dashboard
          </Link>
        </div>
      )}
    </div>
  );
}
