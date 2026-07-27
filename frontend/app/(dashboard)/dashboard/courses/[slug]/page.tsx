"use client";

import Link from "next/link";
import { useEffect, useMemo } from "react";
import { useParams } from "next/navigation";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { getCourses } from "@/lib/api/courses";
import {
  LessonFeatureCard,
  courseHasStarted,
} from "@/components/dashboard/LessonFeatureCard";
import { Reveal } from "@/components/shared/Reveal";
import { usePageChrome } from "@/stores/pageChrome";
import {
  TRACK_LESSON_TITLE,
  currentModule,
  moduleDisplayTitle,
  trackModulesFrom,
} from "@/lib/learning-track";

/** Lessons hub — Creating an AI Agent (modules live on Module overview). */
export default function CourseDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const setChrome = usePageChrome((s) => s.setChrome);
  const clearChrome = usePageChrome((s) => s.clearChrome);
  const queryClient = useQueryClient();

  const { data: allCourses, isLoading } = useQuery({
    queryKey: ["courses"],
    queryFn: async () => {
      const list = await getCourses();
      for (const c of list) {
        queryClient.setQueryData(["course", c.slug], c);
      }
      return list;
    },
  });

  const trackModules = useMemo(
    () => trackModulesFrom(allCourses ?? []),
    [allCourses]
  );

  const active =
    trackModules.find((m) => m.slug === slug) ?? currentModule(trackModules);
  const showStart = !trackModules.some(courseHasStarted);
  const overviewHref = active
    ? `/dashboard/courses/${active.slug}/modules`
    : undefined;

  useEffect(() => {
    setChrome({
      title: "Lessons",
      subtitle: active
        ? `${TRACK_LESSON_TITLE} · ${moduleDisplayTitle(active)}`
        : isLoading
          ? "Loading…"
          : TRACK_LESSON_TITLE,
      showAskTutor: false,
      onAskTutor: null,
      headerTabs: null,
      activeTab: null,
      onTabChange: null,
    });
    return () => clearChrome();
  }, [active, clearChrome, isLoading, setChrome]);

  if (isLoading && !trackModules.length) {
    return <p className="animate-pulse text-craft-faint">Loading…</p>;
  }

  if (!trackModules.length) {
    return (
      <div className="mx-auto mt-16 max-w-md text-center">
        <p className="text-lg font-semibold text-craft-ink">No modules available yet.</p>
        <Link href="/dashboard" className="btn-primary mt-6">
          Back to dashboard
        </Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-6xl">
      <Reveal>
        <h1 className="text-2xl font-bold tracking-tight text-craft-ink sm:text-3xl">
          {showStart ? "Choose a lesson to get started" : "Continue learning"}
        </h1>
      </Reveal>

      {active ? (
        <Reveal delay={40} className="mt-5">
          <LessonFeatureCard
            course={active}
            trackModules={trackModules}
            overviewHref={overviewHref}
          />
        </Reveal>
      ) : null}
    </div>
  );
}
