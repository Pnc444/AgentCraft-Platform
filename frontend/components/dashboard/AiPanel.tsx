"use client";

import Link from "next/link";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Send } from "lucide-react";
import clsx from "clsx";
import { getRecommendations } from "@/lib/api/courses";
import { useAuthStore } from "@/stores/authStore";

interface AiPanelProps {
  mobileOpen: boolean;
  onMobileClose: () => void;
}

interface ChatMessage {
  from: "bot" | "user";
  text: string;
}

export function AiPanel({ mobileOpen }: AiPanelProps) {
  const user = useAuthStore((s) => s.user);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      from: "bot",
      text: `Hi${user ? `, ${user.username}` : ""}! Ask about your courses, get hints, or find what to learn next.`,
    },
  ]);
  const [draft, setDraft] = useState("");

  const { data: recommendations } = useQuery({
    queryKey: ["recommendations"],
    queryFn: getRecommendations,
  });

  function handleSend() {
    const text = draft.trim();
    if (!text) return;
    setMessages((prev) => [
      ...prev,
      { from: "user", text },
      { from: "bot", text: "The AI Tutor connects once the Anthropic API is wired up — coming soon!" },
    ]);
    setDraft("");
  }

  return (
    <aside
      className={clsx(
        "fixed inset-y-0 right-0 z-40 flex w-80 flex-col border-l border-white/5 bg-craft-900 transition-transform xl:static xl:translate-x-0",
        mobileOpen ? "translate-x-0" : "translate-x-full xl:translate-x-0"
      )}
      aria-label="AI assistant"
    >
      <div className="flex items-center justify-between border-b border-white/5 px-5 py-4">
        <div>
          <p className="text-xs uppercase tracking-wide text-slate-500">AI Assistant</p>
          <h2 className="font-semibold text-white">Tutor</h2>
        </div>
        <span className="flex items-center gap-2 text-xs text-emerald-400">
          <span className="h-2 w-2 rounded-full bg-emerald-400" />
          Ready
        </span>
      </div>

      <div className="flex-1 space-y-3 overflow-y-auto p-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={clsx(
              "max-w-[85%] rounded-xl px-4 py-3 text-sm",
              msg.from === "bot"
                ? "bg-craft-800 text-slate-300"
                : "ml-auto bg-craft-accent/20 text-slate-200"
            )}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <div className="border-t border-white/5 p-4">
        <p className="text-xs uppercase tracking-wide text-slate-500">Recommendations</p>
        <div className="mt-2 space-y-2">
          {recommendations?.map((rec) => (
            <Link
              key={rec.id}
              href={`/dashboard/courses/${rec.course_slug}/lessons/${rec.lesson_slug}`}
              className="block rounded-lg border border-white/10 p-3 text-sm transition-colors hover:border-craft-accent/50"
            >
              <span className="text-slate-200">
                {rec.course_title} → {rec.lesson_title}
              </span>
              {rec.reason && <span className="mt-1 block text-xs text-slate-500">{rec.reason}</span>}
            </Link>
          ))}
          {(!recommendations || recommendations.length === 0) && (
            <p className="text-sm text-slate-600">Complete a lesson to get personalized recommendations.</p>
          )}
        </div>
      </div>

      <div className="border-t border-white/5 p-4">
        <textarea
          rows={3}
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
          placeholder="Ask me anything…"
          aria-label="Message to AI tutor"
          className="w-full resize-none rounded-lg border border-white/10 bg-craft-950 px-3 py-2 text-sm text-white placeholder:text-slate-600 focus:border-craft-accent focus:outline-none"
        />
        <button
          type="button"
          onClick={handleSend}
          className="mt-2 flex w-full items-center justify-center gap-2 rounded-lg bg-craft-accent px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-500"
        >
          <Send className="h-4 w-4" />
          Send
        </button>
      </div>
    </aside>
  );
}
