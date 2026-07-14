"use client";

import { useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";
import { Check, Copy } from "lucide-react";

interface LessonContentProps {
  content: string;
}

/** <pre> renderer with a copy-to-clipboard button in the top-right corner. */
function CodeBlock(props: React.HTMLAttributes<HTMLPreElement>) {
  const preRef = useRef<HTMLPreElement>(null);
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    const text = preRef.current?.innerText ?? "";
    try {
      await navigator.clipboard.writeText(text.trimEnd());
    } catch {
      // Clipboard API unavailable (e.g. non-HTTPS); fall back silently.
      const ta = document.createElement("textarea");
      ta.value = text.trimEnd();
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
    }
    setCopied(true);
    window.setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="group relative">
      <pre ref={preRef} {...props} />
      <button
        type="button"
        onClick={handleCopy}
        aria-label={copied ? "Copied" : "Copy to clipboard"}
        className="absolute right-2 top-2 inline-flex items-center gap-1 rounded-md border border-craft-border bg-craft-soft/80 px-2 py-1 text-xs text-craft-muted opacity-0 transition-opacity hover:text-craft-ink focus:opacity-100 group-hover:opacity-100"
      >
        {copied ? (
          <>
            <Check className="h-3.5 w-3.5 text-emerald-500" />
            Copied
          </>
        ) : (
          <>
            <Copy className="h-3.5 w-3.5" />
            Copy
          </>
        )}
      </button>
    </div>
  );
}

/** Renders existing lesson Markdown without altering the source string. */
export function LessonContent({ content }: LessonContentProps) {
  return (
    <div className="prose-lesson">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw]}
        components={{ pre: CodeBlock }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
