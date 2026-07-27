import { describe, expect, it } from "vitest";
import { frontierIndex, isLessonReachable } from "./lesson-access";
import type { LessonSummary } from "@/types";

function step(status: LessonSummary["status"]): LessonSummary {
  return {
    id: 1,
    title: "t",
    slug: "s",
    lesson_type: "theory",
    type_label: "Read",
    type_promise: "",
    order: 0,
    estimated_minutes: 5,
    status,
  };
}

describe("frontierIndex", () => {
  it("is the first not-completed step", () => {
    expect(frontierIndex([step("completed"), step("in_progress"), step("not_started")])).toBe(1);
  });

  it("is -1 when the module is fully complete", () => {
    expect(frontierIndex([step("completed"), step("completed")])).toBe(-1);
  });

  it("counts a stuck step as the frontier, not as done", () => {
    expect(frontierIndex([step("completed"), step("stuck"), step("not_started")])).toBe(1);
  });
});

describe("isLessonReachable", () => {
  const lessons = [step("completed"), step("in_progress"), step("not_started"), step("not_started")];

  it("opens completed steps and the frontier, locks what follows", () => {
    expect(isLessonReachable(lessons, 0, true)).toBe(true); // review
    expect(isLessonReachable(lessons, 1, true)).toBe(true); // continue
    expect(isLessonReachable(lessons, 2, true)).toBe(false); // not yet
    expect(isLessonReachable(lessons, 3, true)).toBe(false);
  });

  it("opens everything in a finished module", () => {
    const done = [step("completed"), step("completed")];
    expect(isLessonReachable(done, 0, true)).toBe(true);
    expect(isLessonReachable(done, 1, true)).toBe(true);
  });

  it("locks every step of a locked module", () => {
    expect(isLessonReachable(lessons, 0, false)).toBe(false);
  });

  it("staff bypass opens everything, locked modules included", () => {
    expect(isLessonReachable(lessons, 3, false, true)).toBe(true);
  });
});
