"use client";

import { FormEvent, useCallback, useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Bot, RotateCcw, Send, Square, X } from "lucide-react";
import clsx from "clsx";
import {
  getTutorSuggestions,
  streamTutorAnswer,
  type TutorTurn,
} from "@/lib/api/tutor";

interface LessonTutorPanelProps {
  lessonTitle: string;
  courseTitle: string;
  courseSlug: string;
  lessonSlug: string;
  open: boolean;
  onClose: () => void;
}

type ChatMsg = TutorTurn & { streaming?: boolean };

export function LessonTutor({
  lessonTitle,
  courseTitle,
  courseSlug,
  lessonSlug,
  open,
  onClose,
}: LessonTutorPanelProps) {
  const [mounted, setMounted] = useState(false);
  const [draft, setDraft] = useState("");
  const [messages, setMessages] = useState<ChatMsg[]>([]);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const abortRef = useRef<AbortController | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const pinnedRef = useRef(true);
  const lastAskedRef = useRef<string>("");

  useEffect(() => setMounted(true), []);

  // New lesson → new conversation. Cancel anything in flight first.
  useEffect(() => {
    abortRef.current?.abort();
    setMessages([]);
    setDraft("");
    setError(null);
    setBusy(false);
  }, [courseSlug, lessonSlug]);

  useEffect(() => {
    if (!open) return;
    let cancelled = false;
    getTutorSuggestions(courseSlug, lessonSlug)
      .then((res) => !cancelled && setSuggestions(res.suggestions ?? []))
      .catch(() => undefined);
    return () => {
      cancelled = true;
    };
  }, [open, courseSlug, lessonSlug]);

  // Focus the input when opened; stop the stream when closed.
  useEffect(() => {
    if (open) {
      const id = window.setTimeout(() => inputRef.current?.focus(), 60);
      return () => window.clearTimeout(id);
    }
    abortRef.current?.abort();
  }, [open]);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  useEffect(() => () => abortRef.current?.abort(), []);

  // Follow the stream, but stop fighting the user if they scroll up to re-read.
  useEffect(() => {
    if (pinnedRef.current && scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleScroll = () => {
    const el = scrollRef.current;
    if (!el) return;
    pinnedRef.current = el.scrollHeight - el.scrollTop - el.clientHeight < 48;
  };

  const ask = useCallback(
    async (question: string) => {
      const text = question.trim();
      if (!text || busy) return;

      lastAskedRef.current = text;
      setError(null);
      setDraft("");
      pinnedRef.current = true;

      const history = messages
        .filter((m) => !m.streaming)
        .map(({ role, text: t }) => ({ role, text: t }));

      setMessages((prev) => [
        ...prev,
        { role: "user", text },
        { role: "assistant", text: "", streaming: true },
      ]);
      setBusy(true);

      const controller = new AbortController();
      abortRef.current = controller;

      try {
        await streamTutorAnswer({
          message: text,
          courseSlug,
          lessonSlug,
          history,
          signal: controller.signal,
          onToken: (chunk) =>
            setMessages((prev) => {
              const next = [...prev];
              const last = next[next.length - 1];
              if (last?.role === "assistant" && last.streaming) {
                next[next.length - 1] = { ...last, text: last.text + chunk };
              }
              return next;
            }),
        });
        setMessages((prev) =>
          prev.map((m, i) =>
            i === prev.length - 1 ? { ...m, streaming: false } : m
          )
        );
      } catch (err) {
        const aborted = err instanceof DOMException && err.name === "AbortError";
        setMessages((prev) => {
          const next = [...prev];
          const last = next[next.length - 1];
          if (last?.role === "assistant" && last.streaming) {
            if (last.text.trim()) {
              // Keep partial text — half an answer still helps.
              next[next.length - 1] = { ...last, streaming: false };
            } else {
              next.pop();
            }
          }
          return next;
        });
        if (!aborted) {
          setError(err instanceof Error ? err.message : "The tutor failed to answer.");
        }
      } finally {
        setBusy(false);
        abortRef.current = null;
      }
    },
    [busy, messages, courseSlug, lessonSlug]
  );

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    void ask(draft);
  }

  if (!mounted || !open) return null;

  const empty = messages.length === 0;

  return createPortal(
    <>
      <button
        type="button"
        aria-label="Close tutor"
        className="fixed inset-0 z-[60] bg-slate-900/20"
        onClick={onClose}
      />

      <div
        role="dialog"
        aria-modal="true"
        aria-label="AI tutor"
        className="fixed bottom-4 right-4 z-[70] flex h-[min(560px,calc(100dvh-32px))] w-[min(400px,calc(100vw-32px))] flex-col overflow-hidden rounded-2xl border border-craft-border bg-craft-surface shadow-float ring-1 ring-craft-border/40"
      >
        <div className="flex shrink-0 items-start gap-3 border-b border-craft-border bg-craft-navy px-4 py-3 text-white">
          <span className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-cyan-500/20 text-cyan-300">
            <Bot className="h-4 w-4" />
          </span>
          <div className="min-w-0 flex-1">
            <p className="text-sm font-semibold">AI tutor</p>
            <p className="truncate text-xs text-craft-faint">
              {courseTitle} · {lessonTitle}
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-1.5 text-craft-faint transition hover:bg-white/10 hover:text-white"
            aria-label="Close"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <div
          ref={scrollRef}
          onScroll={handleScroll}
          className="min-h-0 flex-1 space-y-3 overflow-y-auto px-4 py-4"
        >
          {empty && (
            <div className="space-y-3">
              <p className="text-sm leading-relaxed text-craft-muted">
                I know this lesson and the rest of the course. Ask me anything
                you&apos;re stuck on.
              </p>
              {suggestions.length > 0 && (
                <div className="flex flex-col items-start gap-2">
                  {suggestions.map((s) => (
                    <button
                      key={s}
                      type="button"
                      onClick={() => void ask(s)}
                      className="rounded-full border border-craft-border bg-craft-soft/60 px-3 py-1.5 text-left text-xs font-medium text-craft-ink transition hover:border-cyan-400 hover:bg-craft-soft"
                    >
                      {s}
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}

          {messages.map((msg, i) => (
            <div
              key={`${msg.role}-${i}`}
              className={clsx(
                "max-w-[92%] rounded-2xl px-3.5 py-2.5 text-sm leading-relaxed",
                msg.role === "user"
                  ? "ml-auto bg-cyan-500 text-white"
                  : "bg-craft-soft text-craft-ink"
              )}
            >
              {msg.role === "assistant" ? (
                <>
                  <div className="prose-tutor" aria-live="polite">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {msg.text}
                    </ReactMarkdown>
                  </div>
                  {msg.streaming && !msg.text && (
                    <span className="flex gap-1 py-1" aria-label="Thinking">
                      {[0, 1, 2].map((d) => (
                        <span
                          key={d}
                          className="h-1.5 w-1.5 animate-pulse rounded-full bg-craft-faint"
                          style={{ animationDelay: `${d * 150}ms` }}
                        />
                      ))}
                    </span>
                  )}
                </>
              ) : (
                msg.text
              )}
            </div>
          ))}

          {error && (
            <div className="rounded-xl border border-amber-500/30 bg-amber-50 px-3 py-2.5 text-xs text-amber-800 dark:bg-amber-500/10 dark:text-amber-200">
              <p>{error}</p>
              <button
                type="button"
                onClick={() => void ask(lastAskedRef.current)}
                className="mt-2 inline-flex items-center gap-1.5 font-semibold underline underline-offset-2"
              >
                <RotateCcw className="h-3 w-3" />
                Try again
              </button>
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="shrink-0 border-t border-craft-border p-3">
          <div className="flex items-end gap-2">
            <textarea
              ref={inputRef}
              value={draft}
              onChange={(e) => setDraft(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  void ask(draft);
                }
              }}
              rows={2}
              maxLength={2000}
              placeholder="What are you stuck on?"
              className="input-field min-h-[2.75rem] flex-1 resize-none px-3 py-2 text-sm"
            />
            {busy ? (
              <button
                type="button"
                onClick={() => abortRef.current?.abort()}
                className="btn-secondary shrink-0 px-3 py-2.5"
                aria-label="Stop generating"
                title="Stop"
              >
                <Square className="h-4 w-4" />
              </button>
            ) : (
              <button
                type="submit"
                disabled={!draft.trim()}
                className="btn-primary shrink-0 px-3 py-2.5"
                aria-label="Send"
              >
                <Send className="h-4 w-4" />
              </button>
            )}
          </div>
          <p className="mt-2 text-[0.6875rem] text-craft-faint">
            Enter to send · Shift+Enter for a new line. AI can be wrong — check
            anything that matters.
          </p>
        </form>
      </div>
    </>,
    document.body
  );
}
