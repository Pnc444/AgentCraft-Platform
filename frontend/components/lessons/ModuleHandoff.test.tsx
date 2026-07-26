import { act, createElement } from "react";
import { createRoot } from "react-dom/client";
import { afterEach, describe, expect, it, vi } from "vitest";
import { ModuleHandoff } from "@/components/lessons/ModuleHandoff";

vi.mock("next/link", () => ({
  default: ({ href, children }: { href: string; children: React.ReactNode }) =>
    createElement("a", { href }, children),
}));

function render(node: React.ReactElement) {
  const container = document.createElement("div");
  document.body.appendChild(container);
  const root = createRoot(container);
  act(() => root.render(node));
  return { container, root };
}

const nextModule = {
  slug: "module-1-5-how-llms-work",
  title: "Module 1.5: How LLMs Work",
  totalLessons: 3,
  href: "/dashboard/courses/module-1-5-how-llms-work/lessons/context-windows/content",
};

afterEach(() => {
  document.body.innerHTML = "";
});

describe("ModuleHandoff", () => {
  it("gives a finished exam a forward button into the next module", () => {
    const { container } = render(
      createElement(ModuleHandoff, {
        courseTitle: "Module 1: Introduction to AI",
        nextModule,
        isExam: true,
      })
    );

    const link = container.querySelector("a");
    expect(link).not.toBeNull();
    expect(link?.getAttribute("href")).toBe(nextModule.href);
    expect(link?.textContent).toContain("Start Module 1.5: How LLMs Work");
    // The exam is the module's last lesson, so say so.
    expect(container.textContent).toContain("exam passed");
  });

  it("names the next module and its size so the learner knows what they're starting", () => {
    const { container } = render(
      createElement(ModuleHandoff, {
        courseTitle: "Module 4.5: Docker and Environments",
        nextModule,
        isExam: false,
      })
    );

    expect(container.textContent).toContain("Module 4.5: Docker and Environments complete");
    expect(container.textContent).toContain("Module 1.5: How LLMs Work");
    expect(container.textContent).toContain("3 lessons");
  });

  it("never dead-ends on the final module — falls back to the dashboard", () => {
    const { container } = render(
      createElement(ModuleHandoff, {
        courseTitle: "Module 7: Claude (Build #3)",
        nextModule: null,
        isExam: true,
      })
    );

    const link = container.querySelector("a");
    expect(link?.getAttribute("href")).toBe("/dashboard");
    expect(container.textContent).toContain("finished the course");
  });
});
