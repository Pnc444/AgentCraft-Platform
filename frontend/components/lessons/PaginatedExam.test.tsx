import { act, createElement } from "react";
import { createRoot } from "react-dom/client";
import { afterEach, describe, expect, it, vi } from "vitest";
import { PaginatedExam } from "@/components/lessons/PaginatedExam";
import type { CheckpointQuestion } from "@/components/lessons/CheckpointQuiz";

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

  it("shows one question at a time with step chrome", async () => {
    const { container, root } = render(
      createElement(PaginatedExam, { questions, label: "Exam" })
    );

    try {
      await act(async () => {
        root.render(createElement(PaginatedExam, { questions, label: "Exam" }));
      });

      expect(container.textContent).toContain("Question 1");
      expect(container.textContent).toContain("Step 1 / 3");
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
