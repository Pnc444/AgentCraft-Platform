"use client";

import { FormEvent, useCallback, useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { Bot, Send, X } from "lucide-react";
import clsx from "clsx";
import { LogoIcon } from "@/components/shared/Logo";

interface LessonTutorPanelProps {
  lessonTitle: string;
  courseTitle: string;
  open: boolean;
  onClose: () => void;
  onOpen: () => void;
}

type ChatMsg = { role: "assistant" | "user"; text: string };

const FAB_SIZE = 56;
const PANEL_WIDTH = 360;
const PANEL_HEIGHT = 480;
const MARGIN = 16;
const STORAGE_KEY = "agentcraft-tutor-fab-pos";

type Pos = { x: number; y: number };

function clampPos(x: number, y: number): Pos {
  const maxX = Math.max(MARGIN, window.innerWidth - FAB_SIZE - MARGIN);
  const maxY = Math.max(MARGIN, window.innerHeight - FAB_SIZE - MARGIN);
  return {
    x: Math.min(maxX, Math.max(MARGIN, x)),
    y: Math.min(maxY, Math.max(MARGIN, y)),
  };
}

function defaultPos(): Pos {
  return clampPos(window.innerWidth - FAB_SIZE - 24, window.innerHeight - FAB_SIZE - 24);
}

function loadPos(): Pos {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return defaultPos();
    const parsed = JSON.parse(raw) as Pos;
    if (typeof parsed.x === "number" && typeof parsed.y === "number") {
      return clampPos(parsed.x, parsed.y);
    }
  } catch {
    /* ignore */
  }
  return defaultPos();
}

function panelPlacement(pos: Pos) {
  const vw = window.innerWidth;
  const vh = window.innerHeight;
  const panelLeft = Math.min(
    Math.max(MARGIN, pos.x + FAB_SIZE - PANEL_WIDTH),
    vw - PANEL_WIDTH - MARGIN
  );
  const openAbove = pos.y > PANEL_HEIGHT + MARGIN * 2;
  const panelTop = openAbove
    ? Math.max(MARGIN, pos.y - PANEL_HEIGHT - 12)
    : Math.min(pos.y + FAB_SIZE + 12, vh - PANEL_HEIGHT - MARGIN);
  return { panelLeft, panelTop };
}

/** Draggable round help FAB + compact floating chat (portaled to body so it stays on-screen). */
export function LessonTutor({
  lessonTitle,
  courseTitle,
  open,
  onClose,
  onOpen,
}: LessonTutorPanelProps) {
  const [mounted, setMounted] = useState(false);
  // Stable SSR/client initial value — real position applied after mount (avoids hydration errors).
  const [pos, setPos] = useState<Pos>({ x: 24, y: 24 });
  const [draft, setDraft] = useState("");
  const [messages, setMessages] = useState<ChatMsg[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const dragging = useRef(false);
  const didDrag = useRef(false);
  const offset = useRef({ x: 0, y: 0 });
  const posRef = useRef(pos);

  useEffect(() => {
    setPos(loadPos());
    setMounted(true);
  }, []);

  useEffect(() => {
    posRef.current = pos;
  }, [pos]);

  useEffect(() => {
    setMessages([
      {
        role: "assistant",
        text: `I'm your AgentCraft tutor for “${lessonTitle}”. Ask anything you're stuck on. The live AI connection is still being wired up, but this is where help will live.`,
      },
    ]);
    setDraft("");
  }, [lessonTitle]);

  useEffect(() => {
    function onResize() {
      setPos((p) => clampPos(p.x, p.y));
    }
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  const onPointerMove = useCallback((e: PointerEvent) => {
    if (!dragging.current) return;
    didDrag.current = true;
    setPos(clampPos(e.clientX - offset.current.x, e.clientY - offset.current.y));
  }, []);

  const onPointerUp = useCallback(() => {
    if (!dragging.current) return;
    dragging.current = false;
    setIsDragging(false);
    document.body.style.userSelect = "";
    localStorage.setItem(STORAGE_KEY, JSON.stringify(posRef.current));
    window.removeEventListener("pointermove", onPointerMove);
    window.removeEventListener("pointerup", onPointerUp);
  }, [onPointerMove]);

  function startDrag(e: React.PointerEvent) {
    if (e.button !== 0) return;
    dragging.current = true;
    didDrag.current = false;
    setIsDragging(true);
    offset.current = { x: e.clientX - pos.x, y: e.clientY - pos.y };
    document.body.style.userSelect = "none";
    window.addEventListener("pointermove", onPointerMove);
    window.addEventListener("pointerup", onPointerUp);
  }

  function handleFabClick() {
    if (didDrag.current) {
      didDrag.current = false;
      return;
    }
    if (open) onClose();
    else onOpen();
  }

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

  if (!mounted) return null;

  const { panelLeft, panelTop } = open ? panelPlacement(pos) : { panelLeft: 0, panelTop: 0 };

  return createPortal(
    <>
      {open && (
        <button
          type="button"
          aria-label="Close tutor"
          className="fixed inset-0 z-[60] bg-slate-900/20"
          onClick={onClose}
        />
      )}

      {open && (
        <div
          role="dialog"
          aria-label="AI tutor"
          className="fixed z-[70] flex flex-col overflow-hidden rounded-2xl border border-craft-border bg-craft-surface shadow-float ring-1 ring-craft-border/40"
          style={{
            left: panelLeft,
            top: panelTop,
            width: PANEL_WIDTH,
            height: PANEL_HEIGHT,
            maxWidth: `calc(100vw - ${MARGIN * 2}px)`,
            maxHeight: `calc(100dvh - ${MARGIN * 2}px)`,
          }}
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
      )}

      <button
        type="button"
        onPointerDown={startDrag}
        onClick={handleFabClick}
        className={clsx(
          "fixed z-[80] flex h-14 w-14 touch-none items-center justify-center rounded-full transition duration-200",
          "bg-craft-navy text-cyan-300 shadow-navy",
          "ring-2 ring-cyan-400/70 ring-offset-2 ring-offset-craft-canvas",
          "hover:bg-craft-navy-soft hover:shadow-float hover:ring-cyan-300",
          "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-cyan-500",
          "dark:bg-craft-card dark:ring-cyan-400 dark:ring-offset-craft-canvas dark:shadow-[0_0_0_1px_rgba(34,211,238,0.35),0_8px_24px_rgba(0,0,0,0.55)]",
          "dark:hover:bg-craft-soft dark:hover:ring-cyan-300",
          open && "ring-cyan-300 dark:ring-cyan-200"
        )}
        style={{
          left: pos.x,
          top: pos.y,
          cursor: isDragging ? "grabbing" : "grab",
        }}
        aria-label={open ? "Close AI tutor" : "Ask the AI tutor for help"}
        aria-expanded={open}
        title="Drag to move · Click for help"
      >
        {open ? <X className="h-5 w-5 text-cyan-300" /> : <LogoIcon className="h-7 w-7" />}
      </button>
    </>,
    document.body
  );
}
