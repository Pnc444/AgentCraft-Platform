import { describe, expect, it } from "vitest";

import {
  assessmentLabelForLessonType,
  entryStepForLessonType,
  isExamLessonType,
  lessonStepPosition,
  lessonStepSequence,
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

describe("lesson step sequence", () => {
  it("never treats video as its own destination", () => {
    expect(lessonStepSequence({ isExam: false })).toEqual(["content", "quiz", "progress"]);
    expect(lessonStepSequence({ isExam: false })).not.toContain("video");
    expect(STEP_AFTER_LESSON).toBe("quiz");
  });

  it("drops the lesson step for exams", () => {
    expect(lessonStepSequence({ isExam: true })).toEqual(["quiz", "progress"]);
  });
});

describe("lessonStepPosition", () => {
  const base = "/dashboard/courses/module-1-introduction-to-ai/lessons/what-is-ai";

  it("counts a standard lesson as three steps", () => {
    expect(lessonStepPosition(`${base}/content`, { isExam: false })).toEqual({
      current: 1,
      total: 3,
      label: "Lesson",
    });
    expect(lessonStepPosition(`${base}/quiz`, { isExam: false })).toEqual({
      current: 2,
      total: 3,
      label: "Quiz",
    });
    expect(lessonStepPosition(`${base}/progress`, { isExam: false })).toEqual({
      current: 3,
      total: 3,
      label: "Summary",
    });
  });

  it("treats the retired /video path as the lesson step", () => {
    expect(lessonStepPosition(`${base}/video`, { isExam: false })).toEqual({
      current: 1,
      total: 3,
      label: "Lesson",
    });
  });

  it("counts an exam as two steps starting at the quiz", () => {
    expect(lessonStepPosition(`${base}/quiz`, { isExam: true })).toEqual({
      current: 1,
      total: 2,
      label: "Quiz",
    });
    expect(lessonStepPosition(`${base}/progress`, { isExam: true })).toEqual({
      current: 2,
      total: 2,
      label: "Summary",
    });
  });
});