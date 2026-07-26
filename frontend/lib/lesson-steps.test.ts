import { describe, expect, it } from "vitest";

import {
  assessmentLabelForLessonType,
  entryStepForLessonType,
  isExamLessonType,
  lessonStepHref,
  STEP_AFTER_LESSON,
} from "@/lib/lesson-steps";

describe("entryStepForLessonType", () => {
  it("opens quiz lessons on the quiz step", () => {
    expect(entryStepForLessonType("quiz")).toBe("quiz");
  });

  it("keeps non-quiz lessons on the content step", () => {
    expect(entryStepForLessonType("theory")).toBe("content");
    expect(entryStepForLessonType("interactive")).toBe("content");
    expect(entryStepForLessonType("sandbox")).toBe("content");
    expect(entryStepForLessonType("agent_lab")).toBe("content");
  });

  it("treats quiz lessons as exams for UI labeling", () => {
    expect(isExamLessonType("quiz")).toBe(true);
    expect(isExamLessonType("theory")).toBe(false);
    expect(assessmentLabelForLessonType("quiz")).toBe("Exam");
    expect(assessmentLabelForLessonType("theory")).toBe("Recap Quiz");
  });
});

describe("lesson steps after deleting the Progress step", () => {
  const base = "/dashboard/courses/module-1-introduction-to-ai/lessons/what-is-ai";

  it("routes from the lesson straight to the assessment", () => {
    expect(STEP_AFTER_LESSON).toBe("quiz");
  });

  it("no longer builds links to a progress step", () => {
    // Progress was a report wearing a step's clothes. The type no longer
    // admits it, so a stray link cannot be written by accident.
    expect(lessonStepHref("module-1-introduction-to-ai", "what-is-ai", "content")).toBe(
      `${base}/content`
    );
    expect(lessonStepHref("module-1-introduction-to-ai", "what-is-ai", "quiz")).toBe(
      `${base}/quiz`
    );
    // @ts-expect-error "progress" is not a LessonStep any more
    expect(() => lessonStepHref("c", "l", "progress")).not.toThrow();
  });
});
