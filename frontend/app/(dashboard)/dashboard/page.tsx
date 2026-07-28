"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import {
  ArrowRight,
  BookOpen,
  Flame,
  GraduationCap,
  Sparkles,
} from "lucide-react";
import { getCourses } from "@/lib/api/courses";
import { deriveLearningPath, lessonHref, type LessonRef } from "@/lib/learning-path";
import { prefetchLessonNav } from "@/lib/prefetch-lesson";
import { peekVisitStreak, recordAndGetVisitStreak } from "@/lib/visit-streak";
import { useAuthStore } from "@/stores/authStore";
import { usePageChrome } from "@/stores/pageChrome";
import {
  TRACK_LESSON_BLURB,
  TRACK_LESSON_TITLE,
  currentModule,
  formatModuleProgress,
  isModuleComplete,
  lessonProgressPct,
  moduleDisplayTitle,
  moduleHasStarted,
  modulesCompletedCount,
  trackModulesFrom,
} from "@/lib/learning-track";
import {
  LessonFeatureCard,
  courseHasStarted,
} from "@/components/dashboard/LessonFeatureCard";
import { DifficultyBadge } from "@/components/dashboard/DifficultyBadge";
import { ProgressRing } from "@/components/shared/ProgressRing";
import { Reveal } from "@/components/shared/Reveal";
import { UserAvatar } from "@/components/shared/UserAvatar";
import type { CourseDetail } from "@/types";

export default function StudentDashboardPage() {
  const user = useAuthStore((s) => s.user);
  const setChrome = usePageChrome((s) => s.setChrome);
  const clearChrome = usePageChrome((s) => s.clearChrome);
  const queryClient = useQueryClient();
  const router = useRouter();
  const [streak, setStreak] = useState(0);

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

  const courses = useMemo(() => trackModulesFrom(allCourses ?? []), [allCourses]);

  const path = courses.length ? deriveLearningPath(courses, courses) : null;
  const detailsReady = !!allCourses;

  const primaryTarget = path?.continueTarget ?? null;
  const featuredCourse =
    (currentModule(courses) as CourseDetail | null) ??
    ((path?.currentModule ?? courses[0] ?? null) as CourseDetail | null);
  const hasStartedAnything = courses.some(courseHasStarted);
  const showStart = !hasStartedAnything;

  const lessonsHref = useMemo(() => {
    const target = currentModule(courses) ?? courses[0];
    if (target) return `/dashboard/courses/${target.slug}`;
    return "/dashboard";
  }, [courses]);

  const completedModules = modulesCompletedCount(courses);
  const lessonPct = lessonProgressPct(courses);
  const inProgressMod =
    courses.find((m) => moduleHasStarted(m) && !isModuleComplete(m)) ?? null;
  const certificatesEarned = courses.every(isModuleComplete) && courses.length ? 1 : 0;

  useEffect(() => {
    setStreak(recordAndGetVisitStreak() || peekVisitStreak());
  }, []);

  useEffect(() => {
    setChrome({
      title: "Dashboard",
      subtitle: user?.username ? `Welcome back, ${user.username}` : "Your learning home",
      showAskTutor: false,
      onAskTutor: null,
      headerTabs: null,
      activeTab: null,
      onTabChange: null,
    });
    return () => clearChrome();
  }, [clearChrome, setChrome, user?.username]);

  useEffect(() => {
    if (!primaryTarget) return;
    prefetchLessonNav(queryClient, primaryTarget, router);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [primaryTarget?.courseSlug, primaryTarget?.lesson.slug, queryClient, router]);

  function warm(ref: LessonRef) {
    prefetchLessonNav(queryClient, ref, router);
  }

  return (
    <div className="mx-auto w-full max-w-6xl">
      <Reveal>
        <div className="card overflow-hidden p-0">
          {/* Same side-by-side composition as desktop — slim metrics rail on phone */}
          <div className="grid grid-cols-[minmax(0,1fr)_7.25rem] items-stretch sm:grid-cols-[minmax(0,1.3fr)_minmax(12.5rem,15rem)] lg:grid-cols-[minmax(0,1.45fr)_minmax(17rem,19rem)]">
            <div className="relative min-w-0 overflow-hidden bg-gradient-to-br from-violet-50/40 via-transparent to-transparent p-3 dark:from-violet-950/25 sm:bg-none sm:p-6 lg:p-8 sm:dark:from-transparent">
              <div className="pointer-events-none absolute -right-8 -top-10 h-24 w-24 rounded-full bg-violet-400/15 blur-2xl sm:hidden" />

              <div className="relative flex items-center gap-2 sm:items-start sm:gap-4">
                <UserAvatar size="sm" className="shrink-0 sm:hidden" />
                <UserAvatar size="lg" className="hidden shrink-0 sm:flex" />
                <div className="min-w-0 flex-1">
                  <h1 className="truncate text-sm font-bold tracking-tight text-craft-ink sm:text-3xl">
                    {hasStartedAnything ? "Hello," : "Welcome,"}{" "}
                    <span>{user?.username ?? "learner"}</span>
                  </h1>
                  <p className="mt-0.5 truncate text-[10px] leading-snug text-craft-muted sm:mt-1 sm:whitespace-normal sm:text-sm">
                    {featuredCourse
                      ? hasStartedAnything
                        ? `On ${moduleDisplayTitle(featuredCourse)}${
                            primaryTarget ? ` · ${primaryTarget.lesson.title}` : ""
                          }`
                        : `Start with ${moduleDisplayTitle(featuredCourse)}`
                      : "Your learning path is loading…"}
                  </p>
                </div>
              </div>

              {isLoading && (
                <p className="relative mt-3 animate-pulse text-xs text-craft-faint sm:mt-6 sm:text-sm">
                  Loading your path…
                </p>
              )}

              {detailsReady && featuredCourse && primaryTarget ? (
                <div className="relative mt-3 border-t border-craft-border/70 pt-3 sm:mt-6 sm:pt-6">
                  <p className="text-[9px] font-semibold uppercase tracking-[0.16em] text-violet-500/80 dark:text-violet-300/70 sm:text-[11px] sm:text-craft-faint sm:dark:text-craft-faint">
                    {showStart ? "Start lesson" : "Continue learning"}
                  </p>
                  <h2 className="mt-1 text-sm font-bold leading-snug tracking-tight text-craft-ink sm:mt-3 sm:text-2xl">
                    {TRACK_LESSON_TITLE}
                  </h2>
                  <div className="mt-1.5 flex flex-wrap items-center gap-1.5 sm:mt-2 sm:gap-2">
                    <p className="min-w-0 text-[10px] leading-snug text-craft-muted sm:text-sm">
                      <span className="sm:hidden">
                        {moduleDisplayTitle(featuredCourse)}
                        {primaryTarget ? ` · ${primaryTarget.lesson.title}` : null}
                      </span>
                      <span className="hidden sm:inline">
                        Module · {moduleDisplayTitle(featuredCourse)}
                        {primaryTarget ? ` · Next: ${primaryTarget.lesson.title}` : null}
                      </span>
                    </p>
                    <DifficultyBadge difficulty={featuredCourse.difficulty} />
                  </div>
                  <p className="mt-2 hidden text-sm leading-relaxed text-craft-muted sm:block">
                    {TRACK_LESSON_BLURB}
                  </p>

                  <div className="mt-3 flex flex-col gap-2.5 sm:mt-5 sm:gap-5">
                    <div className="flex items-center gap-2 sm:gap-5">
                      <ProgressRing
                        value={lessonPct}
                        size={40}
                        stroke={4}
                        sublabel="done"
                        className="shrink-0 sm:hidden"
                      />
                      <ProgressRing
                        value={lessonPct}
                        size={80}
                        stroke={7}
                        sublabel="Lesson"
                        className="hidden shrink-0 sm:block"
                      />
                      <ul className="min-w-0 flex-1 space-y-0.5 text-[10px] leading-snug text-craft-muted sm:space-y-2 sm:text-sm">
                        <LegendRow
                          color="bg-emerald-500"
                          label="Done"
                          labelFull="Completed"
                          detail={formatModuleProgress(completedModules, courses.length)}
                        />
                        <LegendRow
                          color="bg-violet-500"
                          label="Now"
                          labelFull="In Progress"
                          detail={
                            inProgressMod ? moduleDisplayTitle(inProgressMod) : "—"
                          }
                        />
                      </ul>
                    </div>

                    {/* Continue + View side by side on phone */}
                    <div className="flex items-center gap-2">
                      <Link
                        href={lessonHref(primaryTarget)}
                        className="btn-primary min-h-[36px] flex-1 px-3 text-xs sm:min-h-[48px] sm:flex-none sm:px-5 sm:text-sm"
                        onMouseEnter={() => warm(primaryTarget)}
                        onFocus={() => warm(primaryTarget)}
                        onTouchStart={() => warm(primaryTarget)}
                      >
                        {showStart ? "Start" : "Continue"}
                        <ArrowRight className="h-3.5 w-3.5 sm:h-4 sm:w-4" />
                      </Link>
                      <Link
                        href={`/dashboard/courses/${featuredCourse.slug}`}
                        className="btn-secondary min-h-[36px] flex-1 px-3 text-xs sm:min-h-[48px] sm:flex-none sm:px-5 sm:text-sm"
                      >
                        View lesson
                      </Link>
                    </div>
                  </div>
                </div>
              ) : null}

              {detailsReady && !primaryTarget && (
                <div className="relative mt-3 border-t border-craft-border pt-3 sm:mt-6 sm:pt-6">
                  <p className="text-[11px] text-craft-muted sm:text-sm">
                    {courses.length
                      ? "All available lessons are complete — nice work."
                      : "No lessons available yet."}
                  </p>
                  {courses.length > 0 ? (
                    <Link
                      href={lessonsHref}
                      className="btn-secondary mt-3 min-h-[36px] text-xs sm:mt-4 sm:min-h-[44px] sm:text-sm"
                    >
                      View lessons
                      <ArrowRight className="h-4 w-4" />
                    </Link>
                  ) : null}
                </div>
              )}
            </div>

            <div className="grid grid-cols-2 gap-px self-stretch border-l border-craft-border bg-craft-border">
              <MetricTile
                icon={<Flame className="h-3 w-3 text-orange-400 sm:h-5 sm:w-5 lg:h-6 lg:w-6" />}
                label="Streak"
                labelFull="Daily streak"
                value={`${streak}d`}
                valueFull={`${streak} day${streak === 1 ? "" : "s"}`}
              />
              <MetricTile
                icon={<BookOpen className="h-3 w-3 text-violet-400 sm:h-5 sm:w-5 lg:h-6 lg:w-6" />}
                label="Progress"
                labelFull="Lesson progress"
                value={`${lessonPct}%`}
                valueFull={`${lessonPct}% complete`}
              />
              <MetricTile
                href="/dashboard/certificates"
                icon={<Sparkles className="h-3 w-3 text-violet-400 sm:h-5 sm:w-5 lg:h-6 lg:w-6" />}
                label="Certs"
                labelFull="Certificates"
                value={`${certificatesEarned}`}
                valueFull={`${certificatesEarned} earned`}
              />
              <MetricTile
                href={lessonsHref}
                icon={<GraduationCap className="h-3 w-3 text-sky-400 sm:h-5 sm:w-5 lg:h-6 lg:w-6" />}
                label="Modules"
                labelFull="Modules done"
                value={`${completedModules}/${courses.length || 10}`}
              />
            </div>
          </div>
        </div>
      </Reveal>

      {detailsReady && !hasStartedAnything ? (
        <div className="card mt-5 p-8 text-center sm:p-10">
          <BookOpen className="mx-auto h-10 w-10 text-craft-faint" />
          <p className="mt-3 text-craft-muted">
            You haven&apos;t started a lesson yet. Explore the catalog to begin.
          </p>
          <Link href={lessonsHref} className="btn-primary mt-6 min-h-[44px]">
            View lessons
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      ) : null}

      {detailsReady && hasStartedAnything && featuredCourse ? (
        <div className="mt-4 space-y-3 sm:mt-5 sm:space-y-4">
          <h2 className="text-sm font-bold tracking-tight text-craft-ink sm:text-xl">
            Current lesson
          </h2>
          <Reveal delay={80}>
            <LessonFeatureCard
              course={featuredCourse}
              trackModules={courses}
              overviewHref={`/dashboard/courses/${featuredCourse.slug}/modules`}
              onWarm={() => {
                if (primaryTarget) warm(primaryTarget);
              }}
            />
          </Reveal>
        </div>
      ) : null}
    </div>
  );
}

function MetricTile({
  icon,
  label,
  labelFull,
  value,
  valueFull,
  href,
}: {
  icon: React.ReactNode;
  label: string;
  labelFull?: string;
  value: string;
  valueFull?: string;
  href?: string;
}) {
  const content = (
    <>
      <div className="flex h-5 w-5 shrink-0 items-center justify-center sm:h-9 sm:w-9 lg:h-10 lg:w-10">
        {icon}
      </div>
      <div className="min-w-0">
        <p className="text-[7px] font-semibold uppercase leading-none tracking-wide text-craft-faint sm:text-[11px] lg:text-xs">
          <span className="sm:hidden">{label}</span>
          <span className="hidden sm:inline">{labelFull ?? label}</span>
        </p>
        <p className="mt-0.5 text-[11px] font-bold leading-tight text-craft-ink sm:mt-1 sm:text-lg lg:mt-1.5 lg:text-xl">
          <span className="sm:hidden">{value}</span>
          <span className="hidden sm:inline">{valueFull ?? value}</span>
        </p>
      </div>
    </>
  );

  const className =
    "flex h-full min-h-0 flex-col items-center justify-center gap-0.5 overflow-hidden bg-craft-surface px-1 py-1.5 text-center transition hover:bg-craft-soft sm:items-stretch sm:gap-2 sm:p-3.5 sm:text-left lg:gap-2.5 lg:p-5";

  if (href) {
    return (
      <Link href={href} className={className}>
        {content}
      </Link>
    );
  }

  return <div className={className}>{content}</div>;
}

function LegendRow({
  color,
  label,
  labelFull,
  detail,
}: {
  color: string;
  label: string;
  labelFull?: string;
  detail: string;
}) {
  return (
    <li className="flex items-start gap-1.5 text-craft-muted sm:gap-2">
      <span className={`mt-1 h-1.5 w-1.5 shrink-0 rounded-full sm:mt-1.5 sm:h-2 sm:w-2 ${color}`} />
      <span className="min-w-0 truncate sm:whitespace-normal">
        <span className="sm:hidden">{label} </span>
        <span className="hidden sm:inline">{labelFull ?? label} </span>
        <span className="font-medium text-craft-ink">{detail}</span>
      </span>
    </li>
  );
}
