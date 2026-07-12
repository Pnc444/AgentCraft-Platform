"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface LessonContentProps {
  content: string;
}

/** Renders existing lesson Markdown without altering the source string. */
export function LessonContent({ content }: LessonContentProps) {
  return (
    <div className="prose-lesson">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
    </div>
  );
}
