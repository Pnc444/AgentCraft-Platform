import type { QueryClient } from "@tanstack/react-query";
import { getCourse, getLesson } from "@/lib/api/courses";
import type { LessonRef } from "@/lib/learning-path";
import { lessonHref } from "@/lib/learning-path";

const STALE = 5 * 60_000;

/** Warm React Query + Next route for a lesson before navigation. */
export function prefetchLessonNav(
  queryClient: QueryClient,
  ref: Pick<LessonRef, "courseSlug" | "lesson">,
  router?: { prefetch: (href: string) => void }
) {
  const href = lessonHref({
    courseSlug: ref.courseSlug,
    courseTitle: "",
    lesson: ref.lesson,
  });
  router?.prefetch(href);

  void queryClient.prefetchQuery({
    queryKey: ["course", ref.courseSlug],
    queryFn: () => getCourse(ref.courseSlug),
    staleTime: STALE,
  });
  void queryClient.prefetchQuery({
    queryKey: ["lesson", ref.courseSlug, ref.lesson.slug],
    queryFn: () => getLesson(ref.courseSlug, ref.lesson.slug),
    staleTime: STALE,
  });
}
