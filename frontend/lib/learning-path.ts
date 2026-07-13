import type { Course, CourseDetail, LessonSummary } from "@/types";

export interface LessonRef {
  courseSlug: string;
  courseTitle: string;
  lesson: LessonSummary;
}

/** Derive continue / recent / upcoming targets from real course detail data only. */
export function deriveLearningPath(courses: Course[], details: CourseDetail[]) {
  const bySlug = new Map(details.map((d) => [d.slug, d]));

  const all: LessonRef[] = [];
  for (const course of courses) {
    const detail = bySlug.get(course.slug);
    if (!detail) continue;
    for (const lesson of detail.lessons) {
      all.push({ courseSlug: course.slug, courseTitle: course.title, lesson });
    }
  }

  const continueTarget =
    all.find((x) => x.lesson.status === "in_progress") ??
    all.find((x) => x.lesson.status === "not_started") ??
    null;

  const recentCompleted = all.filter((x) => x.lesson.status === "completed").slice(-5).reverse();

  let upcoming: LessonRef[] = [];
  if (continueTarget) {
    const idx = all.findIndex(
      (x) =>
        x.courseSlug === continueTarget.courseSlug && x.lesson.slug === continueTarget.lesson.slug
    );
    upcoming = all
      .slice(idx + 1)
      .filter((x) => x.lesson.status === "not_started")
      .slice(0, 4);
  } else {
    upcoming = all.filter((x) => x.lesson.status === "not_started").slice(0, 4);
  }

  const currentModule =
    (continueTarget && courses.find((c) => c.slug === continueTarget.courseSlug)) ??
    courses.find((c) => c.completion_pct < 100) ??
    courses[0] ??
    null;

  return { continueTarget, recentCompleted, upcoming, currentModule, all };
}

export function lessonHref(ref: LessonRef) {
  return `/dashboard/courses/${ref.courseSlug}/lessons/${ref.lesson.slug}/content`;
}
