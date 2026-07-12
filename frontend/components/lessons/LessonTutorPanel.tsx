"use client";

import { FormEvent, useEffect, useState } from "react";
import { Bot, MessageCircleQuestion, Send, X } from "lucide-react";
import clsx from "clsx";

interface LessonTutorPanelProps {
  lessonTitle: string;
  courseTitle: string;
  open: boolean;
  onClose: () => void;
}

type ChatMsg = { role: "assistant" | "user"; text: string };

export function LessonTutorButton({ onClick }: { onClick: () => void }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="fixed bottom-6 right-6 z-40 inline-flex items-center gap-2 rounded-full bg-[#0F172A] px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-slate-900/20 transition hover:bg-slate-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-cyan-500"
      aria-label="Ask the AI tutor for help"
    >
      <MessageCircleQuestion className="h-4 w-4 text-cyan-300" />
      Get help
    </button>
  );
}

export function LessonTutorPanel({
  lessonTitle,
  courseTitle,
  open,
  onClose,
}: LessonTutorPanelProps) {
  const [draft, setDraft] = useState("");
  const [messages, setMessages] = useState<ChatMsg[]>([
    {
      role: "assistant",
      text: `I'm your AgentCraft tutor for “${lessonTitle}”. Ask anything you're stuck on — the live AI connection is still being wired up, but this is where help will live.`,
    },
  ]);

  useEffect(() => {
    setMessages([
      {
        role: "assistant",
        text: `I'm your AgentCraft tutor for “${lessonTitle}”. Ask anything you're stuck on — the live AI connection is still being wired up, but this is where help will live.`,
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
        text: "Thanks — the AI tutor isn't connected yet. When it is, I'll answer with this lesson's context. For now, try re-reading the lesson content or marking notes on what confused you.",
      },
    ]);
    setDraft("");
  }

  return (
    <>
      <button
        type="button"
        aria-label="Close tutor"
        className={clsx(
          "fixed inset-0 z-40 bg-slate-900/30 transition",
          open ? "opacity-100" : "pointer-events-none opacity-0"
        )}
        onClick={onClose}
      />
      <aside
        className={clsx(
          "fixed inset-y-0 right-0 z-50 flex w-full max-w-md flex-col border-l border-slate-200 bg-white shadow-2xl transition-transform duration-300",
          open ? "translate-x-0" : "translate-x-full"
        )}
        aria-hidden={!open}
      >
        <div className="flex items-start gap-3 border-b border-slate-200 bg-[#0F172A] px-4 py-4 text-white">
          <span className="mt-0.5 flex h-9 w-9 items-center justify-center rounded-full bg-cyan-500/20 text-cyan-300">
            <Bot className="h-5 w-5" />
          </span>
          <div className="min-w-0 flex-1">
            <p className="text-sm font-semibold">AI tutor</p>
            <p className="truncate text-xs text-slate-400">
              {courseTitle} · {lessonTitle}
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-1.5 text-slate-400 transition hover:bg-white/10 hover:text-white"
            aria-label="Close"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <div className="flex-1 space-y-3 overflow-y-auto px-4 py-4">
          {messages.map((msg, i) => (
            <div
              key={`${msg.role}-${i}`}
              className={clsx(
                "max-w-[90%] rounded-2xl px-3.5 py-2.5 text-sm leading-relaxed",
                msg.role === "user"
                  ? "ml-auto bg-cyan-500 text-white"
                  : "bg-slate-100 text-slate-700"
              )}
            >
              {msg.text}
            </div>
          ))}
        </div>

        <form onSubmit={handleSubmit} className="border-t border-slate-200 p-3">
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
          <p className="mt-2 text-[11px] text-slate-400">
            Tutor replies will use this lesson once Anthropic is connected.
          </p>
        </form>
      </aside>
    </>
  );
}
