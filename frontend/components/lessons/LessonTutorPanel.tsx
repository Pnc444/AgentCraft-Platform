"use client";

import { FormEvent, useEffect, useState } from "react";
import { createPortal } from "react-dom";
import { Bot, Send, X } from "lucide-react";
import clsx from "clsx";

interface LessonTutorPanelProps {
  lessonTitle: string;
  courseTitle: string;
  open: boolean;
  onClose: () => void;
}

type ChatMsg = { role: "assistant" | "user"; text: string };

export function LessonTutor({
  lessonTitle,
  courseTitle,
  open,
  onClose,
}: LessonTutorPanelProps) {
  const [mounted, setMounted] = useState(false);
  const [draft, setDraft] = useState("");
  const [messages, setMessages] = useState<ChatMsg[]>([]);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    setMessages([
      {
        role: "assistant",
        text: `I'm your AgentCraft tutor for “${lessonTitle}”. Ask anything you're stuck on. The live AI connection is still being wired up, but this is where help will live.`,
      },
    ]);
    setDraft("");
  }, [lessonTitle]);

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const text = draft.trim();
    if (!text) return;
    setMessages((prev) => [
      ...prev,
      { role: "user", text },
      {
        role: "assistant",
        text: "Thanks. The AI tutor isn't connected yet. When it is, I'll answer with this lesson's context. For now, try re-reading the lesson content or marking notes on what confused you.",
      },
    ]);
    setDraft("");
  }

  if (!mounted || !open) return null;

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
        aria-label="AI tutor"
        className="fixed bottom-4 right-4 z-[70] flex h-[min(480px,calc(100dvh-32px))] w-[min(360px,calc(100vw-32px))] flex-col overflow-hidden rounded-2xl border border-craft-border bg-craft-surface shadow-float ring-1 ring-craft-border/40"
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

          <div className="min-h-0 flex-1 space-y-3 overflow-y-auto px-4 py-4">
            {messages.map((msg, i) => (
              <div
                key={`${msg.role}-${i}`}
                className={clsx(
                  "max-w-[90%] rounded-2xl px-3.5 py-2.5 text-sm leading-relaxed",
                  msg.role === "user"
                    ? "ml-auto bg-cyan-500 text-white"
                    : "bg-craft-soft text-craft-ink"
                )}
              >
                {msg.text}
              </div>
            ))}
          </div>

          <form onSubmit={handleSubmit} className="shrink-0 border-t border-craft-border p-3">
            <div className="flex items-end gap-2">
              <textarea
                value={draft}
                onChange={(e) => setDraft(e.target.value)}
                rows={2}
                placeholder="What are you stuck on?"
                className="input-field min-h-[2.75rem] flex-1 resize-none px-3 py-2 text-sm"
              />
              <button
                type="submit"
                disabled={!draft.trim()}
                className="btn-primary shrink-0 px-3 py-2.5"
                aria-label="Send"
              >
                <Send className="h-4 w-4" />
              </button>
            </div>
            <p className="mt-2 text-[11px] text-craft-faint">
              Tutor replies will use this lesson once Anthropic is connected.
            </p>
          </form>
        </div>
    </>,
    document.body
  );
}
