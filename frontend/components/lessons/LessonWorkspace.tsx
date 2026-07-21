"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";
import { useParams, usePathname } from "next/navigation";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { getCourse, getLesson, updateLessonProgress } from "@/lib/api/courses";
import {
  invalidateLearningProgress,
  patchLessonStatusInCache,
} from "@/lib/learning-progress";
import type { VideoCompletionDetails } from "@/components/lessons/LessonVideo";
import {
  getCheckpointQuestions,
  getGuidedLessonBlocks,
  getLessonArtifacts,
  getRecapQuestions,
} from "@/lib/lesson-steps";
import type {
  CourseDetail,
  GuidedLessonBlock,
  LessonArtifact,
  LessonDetail,
  LessonStatus,
} from "@/types";
import { LessonTutor } from "@/components/lessons/LessonTutorPanel";

type ProgressPayload = {
  status?: LessonStatus;
  score?: number;
  video_watched?: boolean;
  interaction_event?: {
    type: string;
    key: string;
    status?: string;
    details?: Record<string, unknown>;
  };
};

type LessonWorkspaceValue = {
  slug: string;
  lessonSlug: string;
  lesson: LessonDetail | undefined;
  course: CourseDetail | undefined;
  isLoading: boolean;
  notice: string | null;
  setNotice: (value: string | null) => void;
  recapQuestions: ReturnType<typeof getRecapQuestions>;
  checkpointQuestions: ReturnType<typeof getCheckpointQuestions>;
  guidedBlocks: GuidedLessonBlock[];
  artifactBundle: LessonArtifact[];
  videoUrl: string;
  needsVideo: boolean;
  videoDone: boolean;
  prev: { slug: string; title: string } | null;
  next: { slug: string; title: string } | null;
  progressPending: boolean;
  updateProgress: (data: ProgressPayload) => void;
  markVideoWatched: (details: VideoCompletionDetails) => void;
  openTutor: () => void;
};

const LessonWorkspaceContext = createContext<LessonWorkspaceValue | null>(null);

export function LessonWorkspaceProvider({ children }: { children: ReactNode }) {
  const { slug, lessonSlug } = useParams<{ slug: string; lessonSlug: string }>();
  const pathname = usePathname();
  const queryClient = useQueryClient();
  const [tutorOpen, setTutorOpen] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);
  const autoStartedId = useRef<number | null>(null);

  // The dashboard scrolls inside <main>, so reset both document and panel scroll
  // whenever the lesson route changes.
  useEffect(() => {
    window.scrollTo(0, 0);
    document.querySelector("main")?.scrollTo(0, 0);
  }, [pathname]);

  const { data: lesson, isLoading } = useQuery({
    queryKey: ["lesson", slug, lessonSlug],
    queryFn: () => getLesson(slug, lessonSlug),
    enabled: !!slug && !!lessonSlug,
    staleTime: 5 * 60_000,
  });

  const cachedCourse = slug ? queryClient.getQueryData<CourseDetail>(["course", slug]) : undefined;
  const { data: course } = useQuery({
    queryKey: ["course", slug],
    queryFn: () => getCourse(slug),
    enabled: !!slug,
    staleTime: 5 * 60_000,
    initialData: cachedCourse,
    initialDataUpdatedAt: cachedCourse
      ? queryClient.getQueryState(["course", slug])?.dataUpdatedAt
      : undefined,
  });

  // Prefetch neighbor lessons for snappy prev/next
  useEffect(() => {
    if (!course?.lessons?.length || !lessonSlug) return;
    const idx = course.lessons.findIndex((l) => l.slug === lessonSlug);
    const neighbors = [course.lessons[idx - 1], course.lessons[idx + 1]].filter(Boolean);
    for (const neighbor of neighbors) {
      void queryClient.prefetchQuery({
        queryKey: ["lesson", slug, neighbor!.slug],
        queryFn: () => getLesson(slug, neighbor!.slug),
        staleTime: 5 * 60_000,
      });
    }
  }, [course, lessonSlug, queryClient, slug]);

  const progressMutation = useMutation({
    mutationFn: (data: ProgressPayload) => updateLessonProgress(lesson!.id, data),
    onMutate: async (data) => {
      if (!slug || !lessonSlug || !data.status) return;
      await queryClient.cancelQueries({ queryKey: ["courses"] });
      await queryClient.cancelQueries({ queryKey: ["course", slug] });
      await queryClient.cancelQueries({ queryKey: ["lesson", slug, lessonSlug] });
      patchLessonStatusInCache(queryClient, slug, lessonSlug, data.status);
    },
    onSuccess: (result, variables) => {
      if (!slug || !lessonSlug) return;
      queryClient.setQueryData(["lesson", slug, lessonSlug], (old: LessonDetail | undefined) => {
        if (!old) return old;
        return {
          ...old,
          status: result.status,
          score: result.score,
          video_watched: result.video_watched,
          interaction_log: result.interaction_log,
        };
      });
      if (variables.status) {
        patchLessonStatusInCache(queryClient, slug, lessonSlug, result.status);
      }
    },
    onSettled: (_data, _error, variables) => {
      if (
        variables?.status === "in_progress" ||
        (variables?.video_watched === true && !variables?.status)
      ) {
        return;
      }
      invalidateLearningProgress(queryClient, {
        courseSlug: slug,
        lessonSlug,
        light: true,
      });
    },
  });

  useEffect(() => {
    if (!lesson || lesson.status !== "not_started") return;
    if (autoStartedId.current === lesson.id) return;
    autoStartedId.current = lesson.id;
    progressMutation.mutate({ status: "in_progress" });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lesson?.id, lesson?.status]);

  const markStuck = useCallback(() => {
    if (!lesson) return;
    if (lesson.status === "completed" || lesson.status === "stuck") return;
    progressMutation.mutate({ status: "stuck" });
  }, [lesson, progressMutation]);

  const openTutor = useCallback(() => {
    setTutorOpen(true);
    markStuck();
  }, [markStuck]);

  const updateProgress = useCallback(
    (data: ProgressPayload) => {
      progressMutation.mutate(data);
    },
    [progressMutation]
  );

  const markVideoWatched = useCallback((details: VideoCompletionDetails) => {
    if (!lesson || lesson.video_watched) return;
    progressMutation.mutate({
      video_watched: true,
      interaction_event: {
        type: "video_completion",
        key: `video:${lesson.id}:completion`,
        status: "done",
        details: {
          source: details.source,
          duration_seconds: Number(details.durationSeconds.toFixed(2)),
          watched_seconds: Number(details.watchedSeconds.toFixed(2)),
        },
      },
    });
    setNotice(null);
  }, [lesson, progressMutation]);

  const lessons = course?.lessons ?? [];
  const idx = lesson ? lessons.findIndex((l) => l.slug === lesson.slug) : -1;
  const prev = idx > 0 ? lessons[idx - 1] : null;
  const next = idx >= 0 && idx < lessons.length - 1 ? lessons[idx + 1] : null;

  const videoUrl = (lesson?.video_url || "").trim();
  // Admin toggle: require_full_watch locks the quiz until the video ends.
  const needsVideo = !!videoUrl && (lesson?.require_full_watch ?? true);
  const videoDone = !!lesson && (lesson.video_watched || !needsVideo);
  const recapQuestions = getRecapQuestions(lesson?.sandbox_config ?? {});
  const checkpointQuestions = getCheckpointQuestions(lesson?.sandbox_config ?? {});
  const guidedBlocks = getGuidedLessonBlocks(lesson?.sandbox_config ?? {});
  const artifactBundle = getLessonArtifacts(lesson?.sandbox_config ?? {});

  const value = useMemo<LessonWorkspaceValue>(
    () => ({
      slug,
      lessonSlug,
      lesson,
      course,
      isLoading,
      notice,
      setNotice,
      recapQuestions,
      checkpointQuestions,
      guidedBlocks,
      artifactBundle,
      videoUrl,
      needsVideo,
      videoDone,
      prev: prev ? { slug: prev.slug, title: prev.title } : null,
      next: next ? { slug: next.slug, title: next.title } : null,
      progressPending: progressMutation.isPending,
      updateProgress,
      markVideoWatched,
      openTutor,
    }),
    [
      slug,
      lessonSlug,
      lesson,
      course,
      isLoading,
      notice,
      recapQuestions,
      checkpointQuestions,
      guidedBlocks,
      artifactBundle,
      videoUrl,
      needsVideo,
      videoDone,
      prev,
      next,
      progressMutation.isPending,
      updateProgress,
      markVideoWatched,
      openTutor,
    ]
  );

  return (
    <LessonWorkspaceContext.Provider value={value}>
      {children}
      {lesson && (
        <LessonTutor
          open={tutorOpen}
          onClose={() => setTutorOpen(false)}
          lessonTitle={lesson.title}
          courseTitle={lesson.course_title}
        />
      )}
    </LessonWorkspaceContext.Provider>
  );
}

export function useLessonWorkspace() {
  const ctx = useContext(LessonWorkspaceContext);
  if (!ctx) {
    throw new Error("useLessonWorkspace must be used within LessonWorkspaceProvider");
  }
  return ctx;
}
