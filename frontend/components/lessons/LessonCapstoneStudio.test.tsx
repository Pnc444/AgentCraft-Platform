import { act, createElement } from "react";
import { createRoot } from "react-dom/client";
import { describe, expect, it, vi } from "vitest";
import { LessonCapstoneStudio } from "@/components/lessons/LessonCapstoneStudio";
import type { CapstoneAssignment, LessonInteraction } from "@/types";

const assignment: CapstoneAssignment = {
  title: "Capstone Studio",
  summary: "Practice the release decision.",
  review_questions: [
    "Would this workflow stay safe if someone misunderstood one step?",
  ],
  sections: [
    {
      key: "goal",
      label: "Goal",
      prompt: "Describe the goal.",
      min_length: 10,
    },
    {
      key: "evidence",
      label: "Receipts and evidence",
      prompt: "Describe the receipts.",
      min_length: 10,
    },
  ],
};

const savedGoal =
  "Review a release candidate before it can widen access or ship a risky change.";
const savedEvidence =
  "Every run leaves a receipt and verifier output that can be checked first.";

const hydratedInteractionLog: LessonInteraction[] = [
  {
    type: "capstone_submission",
    key: "capstone:submission",
    status: "saved",
    details: {
      submission: {
        goal: savedGoal,
        evidence: savedEvidence,
      },
    },
  },
  {
    type: "capstone_review",
    key: "capstone:review",
    status: "saved",
    details: {
      review: {
        "review-0": true,
      },
    },
  },
  {
    type: "capstone_result",
    key: "capstone:result",
    status: "pass",
    details: {},
  },
];

describe("LessonCapstoneStudio", () => {
  it("hydrates saved verifier state after the interaction log reloads", async () => {
    const onRecordInteraction = vi.fn();
    const container = document.createElement("div");
    document.body.appendChild(container);
    const root = createRoot(container);

    try {
      await act(async () => {
        root.render(
          createElement(LessonCapstoneStudio, {
            assignment,
            evaluationRubric: [],
            evaluationCases: [],
            interactionLog: [],
            onRecordInteraction,
          })
        );
      });

      expect(container.textContent).toContain("Final result: revise");

      await act(async () => {
        root.render(
          createElement(LessonCapstoneStudio, {
            assignment,
            evaluationRubric: [],
            evaluationCases: [],
            interactionLog: hydratedInteractionLog,
            onRecordInteraction,
          })
        );
      });

      const textareaValues = Array.from(container.querySelectorAll("textarea")).map(
        (textarea) => (textarea as HTMLTextAreaElement).value
      );
      const reviewCheckbox = container.querySelector(
        'input[type="checkbox"]'
      ) as HTMLInputElement | null;

      expect(textareaValues).toEqual([savedGoal, savedEvidence]);
      expect(reviewCheckbox?.checked).toBe(true);
      expect(container.textContent).toContain("Goal: pass");
      expect(container.textContent).toContain("Receipts and evidence: pass");
      expect(container.textContent).toContain("Final result: pass");
      expect(container.textContent).toContain(
        "This capstone plan is complete enough to pass the lesson verifier."
      );
      expect(container.textContent).not.toContain(
        "This plan needs revision before it is ready to pass."
      );
    } finally {
      root.unmount();
      container.remove();
    }
  });
});