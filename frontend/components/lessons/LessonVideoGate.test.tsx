import { act, createElement } from "react";
import { createRoot } from "react-dom/client";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

type WorkspaceValue = {
  slug: string;
  lessonSlug: string;
  lesson: {
    id: number;
    title: string;
    content: string;
    course_slug: string;
    course_title: string;
    estimated_minutes: number;
    lesson_type: "theory" | "interactive" | "sandbox" | "quiz" | "agent_lab";
    video_watched: boolean;
    require_full_watch: boolean;
    status: "not_started" | "in_progress" | "completed" | "stuck";
    score: number | null;
    interaction_log: [];
    sandbox_config: Record<string, unknown>;
    beats?: Array<Record<string, unknown>>;
  } | null;
  course: null;
  videoUrl: string;
  needsVideo: boolean;
  videoDone: boolean;
  isLoading: boolean;
  notice: string | null;
  prev: null;
  next: null;
  recapQuestions: [];
  checkpointQuestions: [];
  guidedBlocks: [];
  artifactBundle: [];
  markVideoWatched: () => void;
  setNotice: (value: string | null) => void;
  updateProgress: (payload: { status?: string; score?: number }) => void;
  openTutor: () => void;
};

const pushMock = vi.fn();
const replaceMock = vi.fn();
const setNoticeMock = vi.fn();
const markVideoWatchedMock = vi.fn();
const updateProgressMock = vi.fn();
const openTutorMock = vi.fn();

const LESSON_BASE = "/dashboard/courses/module-1-introduction-to-ai/lessons/what-is-ai";
let pathnameValue = `${LESSON_BASE}/content`;

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

vi.mock("@/components/lessons/LessonContent", () => ({
  LessonContent: ({ content }: { content: string }) => createElement("div", null, content),
  stripDuplicateTitle: (content: string) => content,
}));

vi.mock("@/components/lessons/CheckpointQuiz", () => ({
  CheckpointQuiz: () => createElement("div", null, "checkpoint"),
}));

vi.mock("@/components/lessons/LessonArtifactPack", () => ({
  LessonArtifactPack: () => createElement("div", null, "artifacts"),
}));

vi.mock("@/components/lessons/LessonCapstoneStudio", () => ({
  LessonCapstoneStudio: () => createElement("div", null, "capstone"),
}));

vi.mock("@/components/lessons/OpenClawFileExplorer", () => ({
  OpenClawFileExplorer: () => createElement("div", null, "explorer"),
}));

vi.mock("@/components/lessons/PaginatedLessonContent", () => ({
  PaginatedLessonContent: () => createElement("div", null, "paginated-deck"),
}));

vi.mock("@/components/shared/ProgressBar", () => ({
  ProgressBar: () => createElement("div", null, "progress-bar"),
}));

vi.mock("@/components/shared/Reveal", () => ({
  Reveal: ({ children }: { children: React.ReactNode }) => createElement("div", null, children),
}));

vi.mock("@/components/lessons/PaginatedExam", () => ({
  PaginatedExam: ({ locked }: { locked: boolean }) =>
    createElement("div", null, locked ? "quiz-locked" : "quiz-open"),
}));

import LessonContentPage from "@/app/(dashboard)/dashboard/courses/[slug]/lessons/[lessonSlug]/content/page";
import LessonQuizPage from "@/app/(dashboard)/dashboard/courses/[slug]/lessons/[lessonSlug]/quiz/page";
import LessonVideoPage from "@/app/(dashboard)/dashboard/courses/[slug]/lessons/[lessonSlug]/video/page";
import { LessonShell } from "@/components/lessons/LessonShell";

function mount() {
  const container = document.createElement("div");
  document.body.appendChild(container);
  return { container, root: createRoot(container) };
}

async function render(node: React.ReactElement) {
  const { container, root } = mount();
  await act(async () => {
    root.render(node);
  });
  return { container, root };
}

describe("lesson video gating", () => {
  beforeEach(() => {
    workspaceValue = {
      slug: "module-1-introduction-to-ai",
      lessonSlug: "what-is-ai",
      lesson: {
        id: 1,
        title: "What is AI?",
        content: "# What is AI?\n\nWatch for three things.",
        course_slug: "module-1-introduction-to-ai",
        course_title: "Module 1: Introduction to AI",
        estimated_minutes: 8,
        lesson_type: "theory",
        video_watched: false,
        require_full_watch: true,
        status: "in_progress",
        score: null,
        interaction_log: [],
        sandbox_config: {},
        beats: [
          { type: "explain", title: "Watch for three things", body: "Intro." },
          { type: "do", action: "video", title: "Watch the video", video_url: "https://www.youtube-nocookie.com/embed/x" },
          { type: "recap", title: "Remember", bullets: ["AI is narrow."] },
        ],
      },
      course: null,
      videoUrl: "https://www.youtube-nocookie.com/embed/c0m6yaGlZh4",
      needsVideo: true,
      videoDone: false,
      isLoading: false,
      notice: null,
      prev: null,
      next: null,
      recapQuestions: [],
      checkpointQuestions: [],
      guidedBlocks: [],
      artifactBundle: [],
      markVideoWatched: markVideoWatchedMock,
      setNotice: setNoticeMock,
      updateProgress: updateProgressMock,
      openTutor: openTutorMock,
    };
    pushMock.mockReset();
    replaceMock.mockReset();
    setNoticeMock.mockReset();
    markVideoWatchedMock.mockReset();
    updateProgressMock.mockReset();
    openTutorMock.mockReset();
    pathnameValue = `${LESSON_BASE}/content`;
  });

  afterEach(() => {
    document.body.innerHTML = "";
  });

  it("plays the video inside the lesson step instead of behind its own tab", async () => {
    const { container, root } = await render(createElement(LessonContentPage));

    try {
      // The player shows one beat at a time: advance past the intro explain.
      const cont = () =>
        Array.from(container.querySelectorAll("button")).filter((b) =>
          b.textContent?.includes("Continue")
        ).pop();
      await act(async () => {
        cont()!.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      });
      expect(container.textContent).toContain("video-player");
      // No hand-off to a separate video destination.
      const videoLinks = Array.from(container.querySelectorAll("a")).filter((anchor) =>
        anchor.getAttribute("href")?.endsWith("/video")
      );
      expect(videoLinks).toHaveLength(0);
    } finally {
      root.unmount();
      container.remove();
    }
  });

  it("keeps the lesson-step CTA from advancing to the quiz before the video is finished", async () => {
    const { container, root } = await render(createElement(LessonContentPage));

    try {
      const cont = () =>
        Array.from(container.querySelectorAll("button")).filter((b) =>
          b.textContent?.includes("Continue")
        ).pop();
      // advance onto the video beat, where the gate lives
      await act(async () => {
        cont()!.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      });
      expect(container.textContent).toContain("video-player");
      // videoDone=false: the gate holds Continue shut
      expect((cont() as HTMLButtonElement).disabled).toBe(true);
      await act(async () => {
        cont()!.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      });
      expect(container.textContent).toContain("video-player");
      expect(pushMock).not.toHaveBeenCalled();
    } finally {
      root.unmount();
      container.remove();
    }
  });

  it("offers the quiz once the video is done", async () => {
    workspaceValue.lesson!.video_watched = true;
    workspaceValue.videoDone = true;

    const { container, root } = await render(createElement(LessonContentPage));

    try {
      const cont = () =>
        Array.from(container.querySelectorAll("button")).filter((b) =>
          b.textContent?.includes("Continue")
        ).pop();
      // explain -> video (ungated now) -> recap; the last beat routes to the quiz
      await act(async () => {
        cont()!.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      });
      await act(async () => {
        cont()!.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      });
      expect(cont()!.textContent).toContain("Continue to Recap Quiz");
      await act(async () => {
        cont()!.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      });
      expect(pushMock).toHaveBeenCalledWith(`${LESSON_BASE}/quiz`);
    } finally {
      root.unmount();
      container.remove();
    }
  });

  it("redirects direct quiz navigation back to the lesson step while the quiz is locked", async () => {
    pathnameValue = `${LESSON_BASE}/quiz`;
    const { container, root } = await render(createElement(LessonQuizPage));

    try {
      expect(replaceMock).toHaveBeenCalledWith(`${LESSON_BASE}/content`);
      expect(setNoticeMock).toHaveBeenCalledWith(
        "Watch the lesson video all the way through before taking the Recap Quiz."
      );
      expect(container.textContent).toContain("quiz-locked");
    } finally {
      root.unmount();
      container.remove();
    }
  });

  it("sends the retired /video route back to the lesson step", async () => {
    pathnameValue = `${LESSON_BASE}/video`;
    const { container, root } = await render(createElement(LessonVideoPage));

    try {
      expect(replaceMock).toHaveBeenCalledWith(`${LESSON_BASE}/content`);
    } finally {
      root.unmount();
      container.remove();
    }
  });

  it("shows linear step orientation and no step-tab navigation in the shell", async () => {
    const { container, root } = await render(
      createElement(LessonShell, null, createElement("div", null, "body"))
    );

    try {
      // Player courses carry their own beat counter, so the shell's step chip
      // stays off the content step (one position signal per screen, audit B1).
      expect(container.textContent).not.toContain("step 1 of 3");

      const stepLinks = Array.from(container.querySelectorAll("a")).filter((anchor) => {
        const href = anchor.getAttribute("href") ?? "";
        return (
          href.endsWith("/content") ||
          href.endsWith("/video") ||
          href.endsWith("/quiz") ||
          href.endsWith("/progress")
        );
      });
      expect(stepLinks).toHaveLength(0);
    } finally {
      root.unmount();
      container.remove();
    }
  });
});
