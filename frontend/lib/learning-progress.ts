import type { QueryClient } from "@tanstack/react-query";
import type { Course, CourseDetail, LessonDetail, LessonStatus } from "@/types";

/** Refresh all learning/progress caches after a status change. */
export function invalidateLearningProgress(
  queryClient: QueryClient,
  opts?: { courseSlug?: string; lessonSlug?: string }
) {
  void queryClient.invalidateQueries({ queryKey: ["courses"] });
  void queryClient.invalidateQueries({ queryKey: ["dashboard-stats"] });
  void queryClient.invalidateQueries({ queryKey: ["course"] });
  void queryClient.invalidateQueries({ queryKey: ["lesson"] });
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

  queryClient.setQueryData<Course[]>(["courses"], (old) => {
    if (!old) return old;
    return old.map((course) => {
      if (course.slug !== courseSlug) return course;
      let completed = course.completed_lessons;
      const wasCompleted = previousStatus === "completed";
      const nowCompleted = nextStatus === "completed";
      if (!wasCompleted && nowCompleted) completed += 1;
      if (wasCompleted && !nowCompleted) completed = Math.max(0, completed - 1);
      const total = course.total_lessons || 1;
      return {
        ...course,
        completed_lessons: completed,
        completion_pct: Math.round((completed / total) * 100),
      };
    });
  });
}
