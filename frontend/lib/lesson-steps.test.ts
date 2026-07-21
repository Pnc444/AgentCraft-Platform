import { describe, expect, it } from "vitest";

import {
  assessmentLabelForLessonType,
  entryStepForLessonType,
  isExamLessonType,
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