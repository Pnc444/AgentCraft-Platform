import type { QueryClient } from "@tanstack/react-query";
import type { CourseDetail, LessonDetail, LessonStatus } from "@/types";

type InvalidateOpts = {
  courseSlug?: string;
  lessonSlug?: string;
  /** When true, only refresh list/stats counts — skip refetching course/lesson detail. */
  light?: boolean;
};

/** Refresh learning/progress caches after a status change (scoped by default). */
export function invalidateLearningProgress(queryClient: QueryClient, opts?: InvalidateOpts) {
  void queryClient.invalidateQueries({ queryKey: ["dashboard-stats"] });

  if (opts?.light) return;

  void queryClient.invalidateQueries({ queryKey: ["courses"] });
  if (opts?.courseSlug) {
    void queryClient.invalidateQueries({ queryKey: ["course", opts.courseSlug] });
  }
  if (opts?.courseSlug && opts?.lessonSlug) {
    void queryClient.invalidateQueries({
      queryKey: ["lesson", opts.courseSlug, opts.lessonSlug],
    });
  }
}

/** Optimistically patch lesson status in course + courses list caches. */
export function patchLessonStatusInCache(
  queryClient: QueryClient,
  courseSlug: string,
  lessonSlug: string,
  nextStatus: LessonStatus
) {
  let previousStatus: LessonStatus | undefined;

  queryClient.setQueryData<LessonDetail>(["lesson", courseSlug, lessonSlug], (old) => {
    if (!old) return old;
    previousStatus = old.status;
    return { ...old, status: nextStatus };
  });

  queryClient.setQueryData<CourseDetail>(["course", courseSlug], (old) => {
    if (!old) return old;
    const lessons = old.lessons.map((lesson) => {
      if (lesson.slug !== lessonSlug) return lesson;
      previousStatus = previousStatus ?? lesson.status;
      return { ...lesson, status: nextStatus };
    });
    const completed_lessons = lessons.filter((l) => l.status === "completed").length;
    const total_lessons = lessons.length;
    return {
      ...old,
      lessons,
      completed_lessons,
      completion_pct: total_lessons ? Math.round((completed_lessons / total_lessons) * 100) : 0,
    };
  });

  queryClient.setQueryData<CourseDetail[]>(["courses"], (old) => {
    if (!old) return old;
    return old.map((course) => {
      if (course.slug !== courseSlug) return course;
      const lessons = course.lessons?.map((lesson) => {
        if (lesson.slug !== lessonSlug) return lesson;
        previousStatus = previousStatus ?? lesson.status;
        return { ...lesson, status: nextStatus };
      });
      let completed = course.completed_lessons;
      const wasCompleted = previousStatus === "completed";
      const nowCompleted = nextStatus === "completed";
      if (!wasCompleted && nowCompleted) completed += 1;
      if (wasCompleted && !nowCompleted) completed = Math.max(0, completed - 1);
      const total = course.total_lessons || 1;
      return {
        ...course,
        lessons: lessons ?? course.lessons,
        completed_lessons: completed,
        completion_pct: Math.round((completed / total) * 100),
      };
    });
  });
}
