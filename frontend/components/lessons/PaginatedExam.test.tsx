import { act, createElement } from "react";
import { createRoot } from "react-dom/client";
import { afterEach, describe, expect, it, vi } from "vitest";
import { PaginatedExam } from "@/components/lessons/PaginatedExam";
import type { CheckpointQuestion } from "@/types";

vi.mock("@/components/lessons/ConfettiBurst", () => ({
  ConfettiBurst: () => null,
}));

const questions: CheckpointQuestion[] = [
  {
    id: "q1",
    prompt: "What is AI?",
    options: ["Human-like judgment software", "A toaster brand", "A spreadsheet formula"],
    answer_index: 0,
  },
  {
    id: "q2",
    prompt: "What is an LLM?",
    options: ["Next-token predictor", "A database table", "A CSS framework"],
    answer_index: 0,
  },
];

function render(node: React.ReactElement) {
  const container = document.createElement("div");
  document.body.appendChild(container);
  const root = createRoot(container);
  return { container, root };
}

describe("PaginatedExam", () => {
  afterEach(() => {
    document.body.innerHTML = "";
  });

  it("opens a already-passed exam on its standing result, not a blank attempt", async () => {
    const onPassed = vi.fn();
    const { container, root } = render(
      createElement(PaginatedExam, {
        questions,
        label: "Exam",
        previouslyPassed: true,
        previousScore: 90,
        onPassed,
      })
    );

    try {
      await act(async () => {
        root.render(
          createElement(PaginatedExam, {
            questions,
            label: "Exam",
            previouslyPassed: true,
            previousScore: 90,
            onPassed,
          })
        );
      });

      // The standing result, with the score preserved.
      expect(container.textContent).toContain("Exam already complete");
      expect(container.textContent).toContain("90%");
      expect(container.textContent).toContain("nothing here has been reset");

      // Crucially: NOT a fresh attempt.
      expect(container.textContent).not.toContain("Question 1");
      expect(container.textContent).not.toContain("What is AI?");

      // Retaking must be a deliberate press, never the default.
      expect(container.textContent).toContain("Retake exam");

      // Re-entering a finished exam must not re-report completion.
      expect(onPassed).not.toHaveBeenCalled();
    } finally {
      root.unmount();
      container.remove();
    }
  });

  it("starts a genuinely fresh attempt only when retake is pressed", async () => {
    const { container, root } = render(
      createElement(PaginatedExam, {
        questions,
        label: "Exam",
        previouslyPassed: true,
        previousScore: 90,
      })
    );

    try {
      await act(async () => {
        root.render(
          createElement(PaginatedExam, {
            questions,
            label: "Exam",
            previouslyPassed: true,
            previousScore: 90,
          })
        );
      });

      const retake = Array.from(container.querySelectorAll("button")).find((b) =>
        b.textContent?.includes("Retake exam")
      );
      expect(retake).toBeDefined();

      await act(async () => {
        retake!.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      });

      expect(container.textContent).toContain("Question 1");
      expect(container.textContent).toContain("What is AI?");
      expect(container.textContent).not.toContain("Exam already complete");
    } finally {
      root.unmount();
      container.remove();
    }
  });

  it("restores a mid-attempt draft after unmount instead of wiping it (F1)", async () => {
    sessionStorage.clear();
    const key = "agentcraft-quiz-draft:test";

    // First mount: answer question 1.
    const first = render(createElement(PaginatedExam, { questions, storageKey: key }));
    try {
      await act(async () => {
        first.root.render(createElement(PaginatedExam, { questions, storageKey: key }));
      });
      const option = Array.from(first.container.querySelectorAll("ul li button")).find((b) =>
        b.textContent?.includes("Human-like judgment software")
      );
      expect(option).toBeDefined();
      await act(async () => {
        option!.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      });
      expect(first.container.textContent).toContain("1/2 answered");
    } finally {
      first.root.unmount();
      first.container.remove();
    }

    // Simulated navigation away and back: a fresh mount restores the draft.
    const second = render(createElement(PaginatedExam, { questions, storageKey: key }));
    try {
      await act(async () => {
        second.root.render(createElement(PaginatedExam, { questions, storageKey: key }));
      });
      expect(second.container.textContent).toContain("1/2 answered");
    } finally {
      second.root.unmount();
      second.container.remove();
      sessionStorage.clear();
    }
  });

  it("lets you page through a review instead of trapping you on question 1", async () => {
    const { container, root } = render(
      createElement(PaginatedExam, {
        questions,
        label: "Exam",
        previouslyPassed: true,
        previousScore: 100,
      })
    );

    try {
      await act(async () => {
        root.render(
          createElement(PaginatedExam, {
            questions,
            label: "Exam",
            previouslyPassed: true,
            previousScore: 100,
          })
        );
      });

      const byText = (t: string) =>
        Array.from(container.querySelectorAll("button")).find((b) =>
          b.textContent?.includes(t)
        );

      await act(async () => {
        byText("Review questions")!.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      });

      // A previously-passed exam has no stored answers, so the answer gate must
      // stand down — otherwise Review is a dead end on question 1.
      expect(container.textContent).toContain("What is AI?");
      expect(container.textContent).toContain("Reviewing");
      expect(container.textContent).not.toContain("Select an answer to continue");

      const advance = byText("Review") ?? byText("Next");
      expect((advance as HTMLButtonElement).disabled).toBe(false);
    } finally {
      root.unmount();
      container.remove();
    }
  });

  it("offers only a retake on the passed results slide — no Done reviewing", async () => {
    const { container, root } = render(
      createElement(PaginatedExam, {
        questions,
        label: "Exam",
        previouslyPassed: true,
        previousScore: 100,
        completionAction: createElement("a", { href: "/next" }, "Start Module 1.5"),
      })
    );

    try {
      const rerender = () =>
        act(async () => {
          root.render(
            createElement(PaginatedExam, {
              questions,
              label: "Exam",
              previouslyPassed: true,
              previousScore: 100,
              completionAction: createElement("a", { href: "/next" }, "Start Module 1.5"),
            })
          );
        });
      await rerender();

      const byText = (t: string) =>
        Array.from(container.querySelectorAll("button")).find((b) =>
          b.textContent?.includes(t)
        );

      await act(async () => {
        byText("Review questions")!.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      });

      // Page to the results slide. navigate() defers with a double
      // requestAnimationFrame, which jsdom only fires on a timer — so each
      // click needs a real flush, not just an await.
      const flush = () =>
        act(async () => {
          await new Promise((resolve) => setTimeout(resolve, 60));
        });
      for (let i = 0; i < 5; i += 1) {
        const advance = byText("Review") ?? byText("Next");
        if (!advance || (advance as HTMLButtonElement).disabled) break;
        await act(async () => {
          advance.dispatchEvent(new MouseEvent("click", { bubbles: true }));
        });
        await flush();
        if (container.textContent?.includes("You passed with")) break;
      }

      expect(container.textContent).toContain("You passed with 100%!");
      expect(container.textContent).toContain("Start Module 1.5");
      // Back already pages to the questions, so a "stop looking" button was one
      // more thing to read for no new destination.
      expect(container.textContent).not.toContain("Done reviewing");
      expect(byText("Retake exam")).toBeDefined();
    } finally {
      root.unmount();
      container.remove();
    }
  });

  it("shows one question at a time with step chrome", async () => {
    const { container, root } = render(
      createElement(PaginatedExam, { questions, label: "Exam" })
    );

    try {
      await act(async () => {
        root.render(createElement(PaginatedExam, { questions, label: "Exam" }));
      });

      expect(container.textContent).toContain("Question 1");
      // Counter counts questions (2 here), never slides — the review slide is
      // a state, not a step (audit B8).
      expect(container.textContent).toContain("1 / 2");
      expect(container.textContent).not.toContain("1 / 3");
      expect(container.textContent).toContain("What is AI?");
      expect(container.textContent).not.toContain("What is an LLM?");
      expect(container.textContent).toContain("Select an answer to continue");
    } finally {
      root.unmount();
      container.remove();
    }
  });

  it("requires an answer before Next is enabled", async () => {
    const { container, root } = render(
      createElement(PaginatedExam, { questions, label: "Exam" })
    );

    try {
      await act(async () => {
        root.render(createElement(PaginatedExam, { questions, label: "Exam" }));
      });

      const next = Array.from(container.querySelectorAll("button")).find((b) =>
        b.textContent?.includes("Next")
      );
      expect(next?.disabled || next?.className.includes("disabled")).toBeTruthy();

      const option = Array.from(container.querySelectorAll("button")).find((b) =>
        b.textContent?.includes("Human-like judgment software")
      );
      await act(async () => {
        option?.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      });

      const nextAfter = Array.from(container.querySelectorAll("button")).find((b) =>
        b.textContent?.includes("Next")
      );
      expect(nextAfter?.disabled).toBeFalsy();
    } finally {
      root.unmount();
      container.remove();
    }
  });

  it("shows empty state when no valid questions exist", async () => {
    const { container, root } = render(
      createElement(PaginatedExam, { questions: [], label: "Exam" })
    );

    try {
      await act(async () => {
        root.render(createElement(PaginatedExam, { questions: [], label: "Exam" }));
      });

      expect(container.textContent).toContain("No exam questions are configured");
    } finally {
      root.unmount();
      container.remove();
    }
  });
});
