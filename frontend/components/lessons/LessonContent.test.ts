import { describe, expect, it } from "vitest";
import { stripDuplicateTitle } from "@/components/lessons/LessonContent";

describe("stripDuplicateTitle", () => {
  it("drops a leading h1 that repeats the page title", () => {
    const md = "# What is AI?\n\nBody text here.";
    expect(stripDuplicateTitle(md, "What is AI?")).toBe("Body text here.");
  });

  it("matches loosely across case and punctuation", () => {
    const md = "# Your First Containers\n\nRun something.";
    expect(stripDuplicateTitle(md, "your first CONTAINERS!")).toBe("Run something.");
  });

  it("keeps a leading h1 that says something different", () => {
    const md = "# A Different Heading\n\nBody.";
    expect(stripDuplicateTitle(md, "What is AI?")).toBe(md);
  });

  it("keeps content with no leading h1", () => {
    const md = "Plain intro paragraph.\n\n## Section";
    expect(stripDuplicateTitle(md, "What is AI?")).toBe(md);
  });

  it("skips leading blank lines before the h1", () => {
    const md = "\n\n# Tokens\n\nBody.";
    expect(stripDuplicateTitle(md, "Tokens")).toBe("Body.");
  });

  it("does not touch a matching heading deeper in the document", () => {
    const md = "Intro.\n\n# Tokens\n\nBody.";
    expect(stripDuplicateTitle(md, "Tokens")).toBe(md);
  });
});
