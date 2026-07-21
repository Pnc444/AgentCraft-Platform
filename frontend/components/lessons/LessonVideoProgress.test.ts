import { describe, expect, it } from "vitest";

import {
  hasMetRequiredWatchTime,
  isForwardSeekBeyondAllowed,
  resumePlaybackSeconds,
  videoCompletionThresholdSeconds,
} from "@/components/lessons/LessonVideo";

describe("LessonVideo progress helpers", () => {
  it("requires near-end watch coverage before marking a video complete", () => {
    expect(videoCompletionThresholdSeconds(100)).toBe(97);
    expect(hasMetRequiredWatchTime(96.5, 100)).toBe(false);
    expect(hasMetRequiredWatchTime(97, 100)).toBe(true);
  });

  it("allows ordinary playback drift but blocks large forward seeks", () => {
    expect(isForwardSeekBeyondAllowed(12, 13.4)).toBe(false);
    expect(isForwardSeekBeyondAllowed(12, 15)).toBe(true);
  });

  it("rewinds blocked seeks to the last watched point", () => {
    expect(resumePlaybackSeconds(0)).toBe(0);
    expect(resumePlaybackSeconds(24)).toBeCloseTo(23.75);
  });
});