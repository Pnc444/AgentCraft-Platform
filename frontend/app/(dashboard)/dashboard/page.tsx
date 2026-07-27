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
          <div className="grid grid-cols-[minmax(0,1fr)_minmax(8.5rem,10rem)] items-stretch sm:grid-cols-[minmax(0,1.3fr)_minmax(12.5rem,15rem)] lg:grid-cols-[minmax(0,1.45fr)_minmax(17rem,19rem)]">
            <div className="min-w-0 p-3 sm:p-6 lg:p-8">
              <div className="flex items-start gap-2.5 sm:gap-4">
                <UserAvatar size="md" className="shrink-0 sm:hidden" />
                <UserAvatar size="lg" className="hidden shrink-0 sm:flex" />
                <div className="min-w-0 flex-1">
                  <h1 className="text-xl font-bold tracking-tight text-craft-ink sm:text-3xl">
                    {hasStartedAnything ? "Hello," : "Welcome,"}{" "}
                    <span className="break-all">{user?.username ?? "learner"}</span>
                  </h1>
                  <p className="mt-1 line-clamp-2 text-xs leading-snug text-craft-muted sm:line-clamp-none sm:text-sm">
                    {featuredCourse
                      ? hasStartedAnything
                        ? `You are on ${TRACK_LESSON_TITLE} · ${moduleDisplayTitle(featuredCourse)}${
                            primaryTarget ? ` · ${primaryTarget.lesson.title}` : ""
                          }`
                        : `Start ${TRACK_LESSON_TITLE} — first module: ${moduleDisplayTitle(featuredCourse)}.`
                      : "Your learning path is loading…"}
                  </p>
                </div>
              </div>

              {isLoading && (
                <p className="mt-4 animate-pulse text-sm text-craft-faint sm:mt-6">
                  Loading your path…
                </p>
              )}

              {detailsReady && featuredCourse && primaryTarget ? (
                <div className="mt-4 border-t border-craft-border pt-4 sm:mt-6 sm:pt-6">
                  <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-craft-faint sm:text-[11px]">
                    {showStart ? "Start lesson" : "Continue learning"}
                  </p>
                  <div className="mt-2 sm:mt-3">
                    <h2 className="text-base font-bold text-craft-ink sm:text-2xl">
                      {TRACK_LESSON_TITLE}
                    </h2>
                  </div>
                  <p className="mt-1.5 flex flex-wrap items-center gap-2 text-xs text-craft-muted sm:mt-2 sm:text-sm">
                    <span className="line-clamp-2 sm:line-clamp-none">
                      Module · {moduleDisplayTitle(featuredCourse)}
                      {primaryTarget ? ` · Next: ${primaryTarget.lesson.title}` : null}
                    </span>
                    <DifficultyBadge difficulty={featuredCourse.difficulty} />
                  </p>
                  <p className="mt-1.5 hidden text-sm leading-relaxed text-craft-muted sm:mt-2 sm:block">
                    {TRACK_LESSON_BLURB}
                  </p>

                  <div className="mt-4 flex flex-col gap-3 sm:mt-5 sm:gap-5">
                    <div className="flex items-center gap-3 sm:gap-5">
                      <ProgressRing
                        value={lessonPct}
                        size={56}
                        stroke={6}
                        sublabel="Lesson"
                        className="shrink-0 sm:hidden"
                      />
                      <ProgressRing
                        value={lessonPct}
                        size={80}
                        stroke={7}
                        sublabel="Lesson"
                        className="hidden shrink-0 sm:block"
                      />
                      <ul className="min-w-0 flex-1 space-y-1.5 text-xs text-craft-muted sm:space-y-2 sm:text-sm">
                        <LegendRow
                          color="bg-emerald-500"
                          label="Completed"
                          detail={formatModuleProgress(completedModules, courses.length)}
                        />
                        <LegendRow
                          color="bg-violet-500"
                          label="In Progress"
                          detail={
                            inProgressMod ? moduleDisplayTitle(inProgressMod) : "—"
                          }
                        />
                      </ul>
                    </div>
                    <div className="flex w-full flex-col items-stretch gap-2">
                      <Link
                        href={lessonHref(primaryTarget)}
                        className="btn-primary min-h-[44px] w-full sm:min-h-[48px]"
                        onMouseEnter={() => warm(primaryTarget)}
                        onFocus={() => warm(primaryTarget)}
                        onTouchStart={() => warm(primaryTarget)}
                      >
                        {showStart ? "Start" : "Continue"}
                        <ArrowRight className="h-4 w-4" />
                      </Link>
                      <Link
                        href={`/dashboard/courses/${featuredCourse.slug}`}
                        className="text-center text-sm font-semibold text-violet-600 hover:underline dark:text-violet-400"
                      >
                        View lesson
                      </Link>
                    </div>
                  </div>
                </div>
              ) : null}

              {detailsReady && !primaryTarget && (
                <div className="mt-4 border-t border-craft-border pt-4 sm:mt-6 sm:pt-6">
                  <p className="text-sm text-craft-muted">
                    {courses.length
                      ? "All available lessons are complete — nice work."
                      : "No lessons available yet."}
                  </p>
                  {courses.length > 0 ? (
                    <Link href={lessonsHref} className="btn-secondary mt-4 min-h-[44px]">
                      View lessons
                      <ArrowRight className="h-4 w-4" />
                    </Link>
                  ) : null}
                </div>
              )}
            </div>

            <div className="grid grid-cols-2 gap-px self-stretch border-l border-craft-border bg-craft-border">
              <MetricTile
                icon={<Flame className="h-4 w-4 text-orange-400 sm:h-5 sm:w-5 lg:h-6 lg:w-6" />}
                label="Streak"
                labelFull="Daily streak"
                value={`${streak}d`}
                valueFull={`${streak} day${streak === 1 ? "" : "s"}`}
              />
              <MetricTile
                icon={<BookOpen className="h-4 w-4 text-violet-400 sm:h-5 sm:w-5 lg:h-6 lg:w-6" />}
                label="Progress"
                labelFull="Lesson progress"
                value={`${lessonPct}%`}
                valueFull={`${lessonPct}% complete`}
              />
              <MetricTile
                href="/dashboard/certificates"
                icon={<Sparkles className="h-4 w-4 text-violet-400 sm:h-5 sm:w-5 lg:h-6 lg:w-6" />}
                label="Certs"
                labelFull="Certificates"
                value={`${certificatesEarned}`}
                valueFull={`${certificatesEarned} earned`}
              />
              <MetricTile
                href={lessonsHref}
                icon={<GraduationCap className="h-4 w-4 text-sky-400 sm:h-5 sm:w-5 lg:h-6 lg:w-6" />}
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
        <div className="mt-5 space-y-4">
          <h2 className="text-lg font-bold tracking-tight text-craft-ink sm:text-xl">
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
      <div className="flex h-8 w-8 shrink-0 items-center justify-center sm:h-9 sm:w-9 lg:h-10 lg:w-10">
        {icon}
      </div>
      <div className="min-w-0 flex-1">
        <p className="text-[10px] font-semibold uppercase leading-tight tracking-wide text-craft-faint sm:text-[11px] lg:text-xs">
          <span className="sm:hidden">{label}</span>
          <span className="hidden sm:inline">{labelFull ?? label}</span>
        </p>
        <p className="mt-1 text-base font-bold leading-tight text-craft-ink sm:text-lg lg:mt-1.5 lg:text-xl">
          <span className="sm:hidden">{value}</span>
          <span className="hidden sm:inline">{valueFull ?? value}</span>
        </p>
      </div>
    </>
  );

  const className =
    "flex min-h-[4.5rem] flex-col justify-center gap-1.5 overflow-hidden bg-craft-surface p-2.5 transition hover:bg-craft-soft sm:min-h-0 sm:gap-2 sm:p-3.5 lg:gap-2.5 lg:p-5";

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
  detail,
}: {
  color: string;
  label: string;
  detail: string;
}) {
  return (
    <li className="flex items-start gap-2 text-craft-muted">
      <span className={`mt-1.5 h-2 w-2 shrink-0 rounded-full ${color}`} />
      <span>
        {label}{" "}
        <span className="font-medium text-craft-ink">{detail}</span>
      </span>
    </li>
  );
}
