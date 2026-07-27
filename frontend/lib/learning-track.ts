import type { CourseDetail } from "@/types";

/**
 * Product learning hierarchy (frontend display).
 * Lesson = full track (“Creating an AI Agent”);
 * Module = API course;
 * Step = API lesson inside a module.
 */
export const TRACK_LESSON_TITLE = "Creating an AI Agent";
export const TRACK_LESSON_BLURB = "Build your own agent through this lesson!";

/** All curriculum modules in Creating an AI Agent, curriculum order. */
export const TRACK_MODULE_SLUGS = [
  "module-1-introduction-to-ai",
  "module-1-5-how-llms-work",
  "module-2-exploring-llm-models",
  "module-3-prompting",
  "module-4-ai-agents",
  "module-4-5-docker-and-environments",
  "module-5-hermes",
  "module-6-openclaw",
  "module-7-claude",
  "module-8-capstone-safety-evaluation",
] as const;

const DISPLAY_TITLE_OVERRIDES: Record<string, string> = {
  "module-4-ai-agents": "AI Agents",
};

export function isTrackModule(slug: string) {
  return (TRACK_MODULE_SLUGS as readonly string[]).includes(slug);
}

/** Filter + sort API courses into the Creating an AI Agent track. */
export function trackModulesFrom(courses: CourseDetail[]): CourseDetail[] {
  const bySlug = new Map(courses.map((c) => [c.slug, c]));
  return TRACK_MODULE_SLUGS.map((slug) => bySlug.get(slug)).filter(
    (c): c is CourseDetail => !!c
  );
}

/** Strip “Module N:” prefixes and apply display overrides. */
export function moduleDisplayTitle(course: { slug: string; title: string }) {
  if (DISPLAY_TITLE_OVERRIDES[course.slug]) return DISPLAY_TITLE_OVERRIDES[course.slug];
  return course.title.replace(/^Module\s+[\d.]+:\s*/i, "").trim() || course.title;
}

export function isModuleComplete(course: CourseDetail) {
  return (
    course.completion_pct >= 100 ||
    (course.total_lessons > 0 && course.completed_lessons >= course.total_lessons)
  );
}

export function moduleHasStarted(course: CourseDetail) {
  return (
    course.completion_pct > 0 ||
    course.completed_lessons > 0 ||
    (course.lessons ?? []).some((l) => l.status === "in_progress" || l.status === "completed")
  );
}

/** First incomplete module, else last module, else null. */
export function currentModule(modules: CourseDetail[]): CourseDetail | null {
  if (!modules.length) return null;
  return modules.find((m) => !isModuleComplete(m)) ?? modules[modules.length - 1] ?? null;
}

export function modulesCompletedCount(modules: CourseDetail[]) {
  return modules.filter(isModuleComplete).length;
}

export function lessonProgressPct(modules: CourseDetail[]) {
  if (!modules.length) return 0;
  return Math.round((modulesCompletedCount(modules) / modules.length) * 100);
}

/** Compact progress: `0/10 modules` — never `0 of 10`. */
export function formatModuleProgress(completed: number, total: number, noun = "modules") {
  return `${completed}/${total} ${noun}`;
}
