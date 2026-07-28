"use client";

import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";
import { Check, ChevronLeft, ChevronRight, Copy, X } from "lucide-react";

interface LessonContentProps {
  content: string;
}

/**
 * Full-screen image overlay. Lesson screenshots render at card width, which
 * makes terminal text in them unreadable — every image is click-to-enlarge.
 *
 * Portaled to <body>: the lesson card is overflow-hidden and pages animate
 * with transforms, either of which would clip or mis-anchor a fixed overlay
 * rendered in place.
 */
function Lightbox({ src, alt, onClose }: { src: string; alt: string; onClose: () => void }) {
  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.key === "Escape") onClose();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  return createPortal(
    <div
      role="dialog"
      aria-modal="true"
      aria-label={alt || "Enlarged image"}
      className="fixed inset-0 z-[100] flex cursor-zoom-out flex-col items-center justify-center gap-3 bg-black/85 p-4 sm:p-8"
      onClick={onClose}
    >
      <button
        type="button"
        onClick={onClose}
        aria-label="Close enlarged image"
        className="absolute right-4 top-4 rounded-full bg-white/10 p-2 text-white transition hover:bg-white/20"
      >
        <X className="h-5 w-5" />
      </button>
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={src}
        alt={alt}
        className="max-h-[85vh] max-w-full rounded-xl object-contain shadow-2xl"
      />
      {alt ? <p className="max-w-2xl text-center text-sm text-white/80">{alt}</p> : null}
    </div>,
    document.body
  );
}

/** Markdown <img> renderer: the image, wrapped in a click-to-enlarge button. */
function ZoomableImage({
  node: _node,
  src,
  alt,
  ...props
}: React.ImgHTMLAttributes<HTMLImageElement> & { node?: unknown }) {
  const [open, setOpen] = useState(false);
  if (!src || typeof src !== "string") return null;
  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        aria-label={`Enlarge image${alt ? `: ${alt}` : ""}`}
        className="block w-full cursor-zoom-in text-left"
        title="Click to enlarge"
      >
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={src} alt={alt ?? ""} {...props} />
      </button>
      {open && <Lightbox src={src} alt={alt ?? ""} onClose={() => setOpen(false)} />}
    </>
  );
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
    <div className="group relative max-w-full min-w-0 overflow-x-auto">
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
  const [zoomed, setZoomed] = useState(false);
  const srcs = (images ?? "").split("|").map((s) => s.trim()).filter(Boolean);
  const caps = (captions ?? "").split("|").map((s) => s.trim());

  if (srcs.length === 0) return null;

  const prev = () => setIndex((i) => (i - 1 + srcs.length) % srcs.length);
  const next = () => setIndex((i) => (i + 1) % srcs.length);

  return (
    <div className="my-6 overflow-hidden rounded-xl border border-craft-border bg-craft-card shadow-card">
      <div className="relative bg-craft-soft">
        <button
          type="button"
          onClick={() => setZoomed(true)}
          aria-label={`Enlarge image: ${caps[index] || `Slide ${index + 1}`}`}
          className="block w-full cursor-zoom-in"
          title="Click to enlarge"
        >
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={srcs[index]}
            alt={caps[index] || `Slide ${index + 1}`}
            className="mx-auto block max-h-[480px] w-auto max-w-full"
          />
        </button>
        {zoomed && (
          <Lightbox
            src={srcs[index]}
            alt={caps[index] || `Slide ${index + 1}`}
            onClose={() => setZoomed(false)}
          />
        )}
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
                  i === index ? "bg-violet-500" : "bg-craft-border hover:bg-craft-faint"
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

/** Anchor renderer: external links open in a new tab; internal links behave normally. */
function MarkdownLink({
  href,
  children,
  ...props
}: React.AnchorHTMLAttributes<HTMLAnchorElement>) {
  const isExternal = /^(https?:)?\/\//i.test(href ?? "");
  return (
    <a
      href={href}
      {...props}
      {...(isExternal ? { target: "_blank", rel: "noopener noreferrer" } : {})}
    >
      {children}
    </a>
  );
}

/**
 * Drop a leading `# Heading` when it just repeats the page's own h1.
 * Nearly every lesson .md opens with its own title, so the old render showed
 * the same words twice ~100px apart (audit B3). A leading h1 that says
 * something different is kept — only the duplicate dies.
 */
export function stripDuplicateTitle(content: string, title: string): string {
  const lines = content.split("\n");
  const first = lines.findIndex((line) => line.trim() !== "");
  if (first === -1) return content;
  const heading = lines[first].match(/^#\s+(.+?)\s*$/);
  if (!heading) return content;
  const norm = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
  if (norm(heading[1]) !== norm(title)) return content;
  return lines.slice(first + 1).join("\n").replace(/^\s*\n+/, "");
}

/** Renders existing lesson Markdown without altering the source string. */
export function LessonContent({ content }: LessonContentProps) {
  return (
    <div className="prose-lesson min-w-0 max-w-full">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw]}
        components={
          {
            pre: CodeBlock,
            carousel: ImageCarousel,
            a: MarkdownLink,
            img: ZoomableImage,
            table: ({ children, ...props }) => (
              <div className="table-scroll">
                <table {...props}>{children}</table>
              </div>
            ),
          } as import("react-markdown").Components
        }
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
