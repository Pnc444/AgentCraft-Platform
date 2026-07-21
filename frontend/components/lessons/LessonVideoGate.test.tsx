import { act, createElement } from "react";
import { createRoot } from "react-dom/client";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

type WorkspaceValue = {
  slug: string;
  lessonSlug: string;
  lesson: {
    title: string;
    course_slug: string;
    course_title: string;
    estimated_minutes: number;
    lesson_type: "theory" | "interactive" | "sandbox" | "quiz" | "agent_lab";
    video_watched: boolean;
    require_full_watch: boolean;
    status: "not_started" | "in_progress" | "completed" | "stuck";
  } | null;
  videoUrl: string;
  needsVideo: boolean;
  videoDone: boolean;
  recapQuestions: [];
  markVideoWatched: () => void;
  setNotice: (value: string | null) => void;
  updateProgress: (payload: { status?: string; score?: number }) => void;
};

const pushMock = vi.fn();
const replaceMock = vi.fn();
const setNoticeMock = vi.fn();
const markVideoWatchedMock = vi.fn();
const updateProgressMock = vi.fn();
let pathnameValue = "/dashboard/courses/module-1-introduction-to-ai/lessons/what-is-ai/video";

let workspaceValue: WorkspaceValue;

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: pushMock, replace: replaceMock }),
  usePathname: () => pathnameValue,
}));

vi.mock("next/link", () => ({
  default: ({ href, children, ...props }: { href: string; children: React.ReactNode }) =>
    createElement("a", { href, ...props }, children),
}));

vi.mock("@/components/lessons/LessonWorkspace", () => ({
  useLessonWorkspace: () => workspaceValue,
}));

vi.mock("@/components/lessons/LessonSection", () => ({
  LessonSection: ({ children }: { children: React.ReactNode }) =>
    createElement("section", null, children),
}));

vi.mock("@/components/lessons/LessonVideo", () => ({
  LessonVideo: () => createElement("div", null, "video-player"),
}));

vi.mock("@/components/shared/Reveal", () => ({
  Reveal: ({ children }: { children: React.ReactNode }) => createElement("div", null, children),
}));

vi.mock("@/components/lessons/RecapQuiz", () => ({
  RecapQuiz: ({ locked }: { locked: boolean }) =>
    createElement("div", null, locked ? "quiz-locked" : "quiz-open"),
}));

vi.mock("@/components/lessons/PaginatedExam", () => ({
  PaginatedExam: ({ locked }: { locked: boolean }) =>
    createElement("div", null, locked ? "quiz-locked" : "quiz-open"),
}));

import LessonVideoPage from "@/app/(dashboard)/dashboard/courses/[slug]/lessons/[lessonSlug]/video/page";
import LessonQuizPage from "@/app/(dashboard)/dashboard/courses/[slug]/lessons/[lessonSlug]/quiz/page";
import { LessonShell } from "@/components/lessons/LessonShell";

function render(node: React.ReactElement) {
  const container = document.createElement("div");
  document.body.appendChild(container);
  const root = createRoot(container);
  return { container, root };
}

describe("lesson video gating", () => {
  beforeEach(() => {
    workspaceValue = {
      slug: "module-1-introduction-to-ai",
      lessonSlug: "what-is-ai",
      lesson: {
        title: "What is AI?",
        course_slug: "module-1-introduction-to-ai",
        course_title: "Module 1: Introduction to AI",
        estimated_minutes: 8,
        lesson_type: "theory",
        video_watched: false,
        require_full_watch: true,
        status: "in_progress",
      },
      videoUrl: "https://www.youtube-nocookie.com/embed/c0m6yaGlZh4",
      needsVideo: true,
      videoDone: false,
      recapQuestions: [],
      markVideoWatched: markVideoWatchedMock,
      setNotice: setNoticeMock,
      updateProgress: updateProgressMock,
    };
    pushMock.mockReset();
    replaceMock.mockReset();
    setNoticeMock.mockReset();
    markVideoWatchedMock.mockReset();
    updateProgressMock.mockReset();
    pathnameValue = "/dashboard/courses/module-1-introduction-to-ai/lessons/what-is-ai/video";
  });

  afterEach(() => {
    document.body.innerHTML = "";
  });

  it("keeps the video-page CTA from advancing to the quiz before the video is finished", async () => {
    const { container, root } = render(createElement(LessonVideoPage));

    try {
      await act(async () => {
        root.render(createElement(LessonVideoPage));
      });

      const button = Array.from(container.querySelectorAll("button")).find((candidate) =>
        candidate.textContent?.includes("Finish Video to Unlock Quiz")
      );

      expect(button?.textContent).toContain("Finish Video to Unlock Quiz");

      await act(async () => {
        button?.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      });

      expect(setNoticeMock).toHaveBeenCalledWith(
        "Watch the lesson video all the way through before taking the Recap Quiz."
      );
      expect(pushMock).not.toHaveBeenCalled();
    } finally {
      root.unmount();
      container.remove();
    }
  });

  it("redirects direct quiz navigation back to the video step while the quiz is locked", async () => {
    const { container, root } = render(createElement(LessonQuizPage));

    try {
      await act(async () => {
        root.render(createElement(LessonQuizPage));
      });

      expect(replaceMock).toHaveBeenCalledWith(
        "/dashboard/courses/module-1-introduction-to-ai/lessons/what-is-ai/video"
      );
      expect(setNoticeMock).toHaveBeenCalledWith(
        "Watch the lesson video all the way through before taking the Recap Quiz."
      );
      expect(container.textContent).toContain("quiz-locked");
    } finally {
      root.unmount();
      container.remove();
    }
  });

  it("routes the locked Recap Quiz tab back to the video step", async () => {
    const { container, root } = render(createElement(LessonShell, null, createElement("div", null, "body")));

    try {
      await act(async () => {
        root.render(createElement(LessonShell, null, createElement("div", null, "body")));
      });

      const button = Array.from(container.querySelectorAll("button")).find((candidate) =>
        candidate.textContent?.includes("Recap Quiz")
      );

      expect(button?.getAttribute("aria-disabled")).toBe("true");

      await act(async () => {
        button?.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      });

      expect(setNoticeMock).toHaveBeenCalledWith(
        "Watch the lesson video all the way through before taking the Recap Quiz."
      );
      expect(pushMock).toHaveBeenCalledWith(
        "/dashboard/courses/module-1-introduction-to-ai/lessons/what-is-ai/video"
      );
    } finally {
      root.unmount();
      container.remove();
    }
  });
});