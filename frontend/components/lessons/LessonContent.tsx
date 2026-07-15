"use client";

import { useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";
import { Check, ChevronLeft, ChevronRight, Copy } from "lucide-react";

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

/**
 * Image carousel usable from lesson markdown via a raw HTML tag:
 *
 *   <carousel
 *     images="/images/lessons/docker-install/step-1.png|/images/lessons/docker-install/step-2.png"
 *     captions="Step 1: download page|Step 2: installer options">
 *   </carousel>
 *
 * `images` is required (pipe-separated paths); `captions` is optional.
 */
function ImageCarousel({ images, captions }: { images?: string; captions?: string }) {
  const [index, setIndex] = useState(0);
  const srcs = (images ?? "").split("|").map((s) => s.trim()).filter(Boolean);
  const caps = (captions ?? "").split("|").map((s) => s.trim());

  if (srcs.length === 0) return null;

  const prev = () => setIndex((i) => (i - 1 + srcs.length) % srcs.length);
  const next = () => setIndex((i) => (i + 1) % srcs.length);

  return (
    <div className="my-6 overflow-hidden rounded-xl border border-craft-border bg-craft-card shadow-card">
      <div className="relative bg-craft-soft">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={srcs[index]}
          alt={caps[index] || `Slide ${index + 1}`}
          className="mx-auto block max-h-[480px] w-auto max-w-full"
        />
        {srcs.length > 1 && (
          <>
            <button
              type="button"
              onClick={prev}
              aria-label="Previous image"
              className="absolute left-2 top-1/2 -translate-y-1/2 rounded-full border border-craft-border bg-craft-surface/90 p-2 text-craft-ink shadow-soft transition hover:bg-craft-surface"
            >
              <ChevronLeft className="h-4 w-4" />
            </button>
            <button
              type="button"
              onClick={next}
              aria-label="Next image"
              className="absolute right-2 top-1/2 -translate-y-1/2 rounded-full border border-craft-border bg-craft-surface/90 p-2 text-craft-ink shadow-soft transition hover:bg-craft-surface"
            >
              <ChevronRight className="h-4 w-4" />
            </button>
          </>
        )}
      </div>
      <div className="flex items-center justify-between gap-2 px-4 py-2.5">
        <span className="text-xs text-craft-muted">
          {caps[index] || ""}
        </span>
        <span className="flex items-center gap-2">
          {srcs.length > 1 &&
            srcs.map((_, i) => (
              <button
                key={i}
                type="button"
                aria-label={`Go to image ${i + 1}`}
                onClick={() => setIndex(i)}
                className={`h-2 w-2 rounded-full transition ${
                  i === index ? "bg-cyan-500" : "bg-craft-border hover:bg-craft-faint"
                }`}
              />
            ))}
          <span className="text-xs tabular-nums text-craft-faint">
            {index + 1}/{srcs.length}
          </span>
        </span>
      </div>
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
        components={
          {
            pre: CodeBlock,
            carousel: ImageCarousel,
          } as import("react-markdown").Components
        }
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
