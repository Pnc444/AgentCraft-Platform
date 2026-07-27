"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { CheckCircle2, ChevronRight, Lightbulb, RotateCcw, TerminalSquare } from "lucide-react";
import clsx from "clsx";
import type { LessonInteraction, SandboxSpec, SandboxTask } from "@/types";
import { completedInteractionKeys } from "@/lib/lesson-interactions";

interface LessonSandboxProps {
  spec: SandboxSpec;
  lessonId: number;
  interactionLog?: LessonInteraction[];
  onRecordInteraction: (event: {
    type: string;
    key: string;
    status?: string;
    details?: Record<string, unknown>;
  }) => void;
}

type Line =
  | { kind: "command"; text: string }
  | { kind: "output"; text: string }
  | { kind: "coach"; text: string }
  | { kind: "success"; text: string };

function matches(patterns: string[], command: string): boolean {
  return patterns.some((pattern) => {
    try {
      return new RegExp(pattern, "i").test(command);
    } catch {
      return pattern.trim().toLowerCase() === command.toLowerCase();
    }
  });
}

export function LessonSandbox({
  spec,
  lessonId,
  interactionLog,
  onRecordInteraction,
}: LessonSandboxProps) {
  const tasks = useMemo(() => spec.tasks ?? [], [spec.tasks]);
  const storageKey = `agentcraft-sandbox-${lessonId}`;

  const persisted = useMemo(
    () => completedInteractionKeys(interactionLog, "sandbox"),
    [interactionLog]
  );
  const [done, setDone] = useState<Set<string>>(persisted);
  const [lines, setLines] = useState<Line[]>([]);
  const [draft, setDraft] = useState("");
  const [hintFor, setHintFor] = useState<string | null>(null);
  const [history, setHistory] = useState<string[]>([]);
  const [historyIdx, setHistoryIdx] = useState<number | null>(null);

  const streamRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Server progress is the source of truth once it arrives.
  useEffect(() => {
    setDone((prev) => {
      const merged = new Set(prev);
      persisted.forEach((key) => merged.add(key));
      return merged;
    });
  }, [persisted]);

  // Transcript is deliberately session-only — it is scratch work, not progress.
  useEffect(() => {
    const saved = sessionStorage.getItem(storageKey);
    if (saved) {
      try {
        setLines(JSON.parse(saved));
      } catch {
        /* ignore malformed scratch state */
      }
    }
  }, [storageKey]);

  useEffect(() => {
    if (lines.length) sessionStorage.setItem(storageKey, JSON.stringify(lines));
  }, [lines, storageKey]);

  useEffect(() => {
    if (streamRef.current) {
      streamRef.current.scrollTop = streamRef.current.scrollHeight;
    }
  }, [lines]);

  const nextTask: SandboxTask | undefined = tasks.find((t) => !done.has(t.id));
  const allDone = tasks.length > 0 && !nextTask;

  function push(...added: Line[]) {
    setLines((prev) => [...prev, ...added]);
  }

  function run(rawCommand: string) {
    const command = rawCommand.trim();
    if (!command) return;

    setHistory((prev) => [...prev, command]);
    setHistoryIdx(null);
    setDraft("");
    push({ kind: "command", text: command });

    if (command === "clear") {
      setLines([]);
      sessionStorage.removeItem(storageKey);
      return;
    }

    // 1. Does it complete the current task?
    if (nextTask && matches(nextTask.accept, command)) {
      const output = nextTask.output?.trim();
      push(
        ...(output ? [{ kind: "output" as const, text: output }] : []),
        { kind: "success", text: nextTask.success ?? "Correct." }
      );
      const updated = new Set(done).add(nextTask.id);
      setDone(updated);
      setHintFor(null);
      onRecordInteraction({
        type: "sandbox",
        key: nextTask.id,
        status: "done",
        details: { command },
      });
      return;
    }

    // 2. Already-completed task re-run — still show its output.
    const earlier = tasks.find((t) => done.has(t.id) && matches(t.accept, command));
    if (earlier?.output) {
      push({ kind: "output", text: earlier.output.trim() });
      return;
    }

    // 3. A known near-miss gets specific coaching, not a generic error.
    const misfire = (spec.misfires ?? []).find((m) => matches(m.match, command));
    if (misfire) {
      push({ kind: "coach", text: misfire.message });
      return;
    }

    // 4. Commands the lesson recognises but that aren't a task step.
    const extra = (spec.extras ?? []).find((e) => matches(e.match, command));
    if (extra) {
      push({ kind: "output", text: extra.output.trim() });
      return;
    }

    push({
      kind: "coach",
      text: nextTask
        ? `Not what this step needs. Goal: ${nextTask.goal}`
        : "Unrecognised command in this practice terminal.",
    });
  }

  function reset() {
    setLines([]);
    setDraft("");
    setHintFor(null);
    sessionStorage.removeItem(storageKey);
  }

  return (
    <div className="space-y-4">
      {spec.intro && <p className="text-sm text-craft-muted">{spec.intro}</p>}

      {/* Task checklist — the learner always knows what they're aiming at. */}
      <ol className="space-y-2">
        {tasks.map((task, index) => {
          const complete = done.has(task.id);
          const active = !complete && task.id === nextTask?.id;
          return (
            <li
              key={task.id}
              className={clsx(
                "rounded-xl border px-3.5 py-3 transition",
                complete
                  ? "border-emerald-500/30 bg-emerald-50/60 dark:bg-emerald-500/10"
                  : active
                    ? "border-violet-500/40 bg-craft-surface shadow-soft"
                    : "border-craft-border bg-craft-surface/50 opacity-70"
              )}
            >
              <div className="flex items-start gap-2.5">
                {complete ? (
                  <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-600 dark:text-emerald-400" />
                ) : (
                  <span
                    className={clsx(
                      "mt-0.5 flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-[10px] font-bold",
                      active
                        ? "bg-violet-500 text-white"
                        : "bg-craft-soft text-craft-faint"
                    )}
                  >
                    {index + 1}
                  </span>
                )}
                <div className="min-w-0 flex-1">
                  <p
                    className={clsx(
                      "text-sm font-medium",
                      complete ? "text-craft-muted line-through" : "text-craft-ink"
                    )}
                  >
                    {task.goal}
                  </p>
                  {active && task.detail && (
                    <p className="mt-1 text-xs text-craft-muted">{task.detail}</p>
                  )}
                  {active && task.hint && (
                    <div className="mt-2">
                      {hintFor === task.id ? (
                        <p className="inline-flex items-center gap-1.5 rounded-lg bg-craft-soft px-2.5 py-1.5 font-mono text-xs text-craft-ink">
                          <Lightbulb className="h-3 w-3 shrink-0 text-amber-500" />
                          {task.hint}
                        </p>
                      ) : (
                        <button
                          type="button"
                          onClick={() => setHintFor(task.id)}
                          className="text-xs font-medium text-violet-700 underline underline-offset-2 dark:text-violet-300"
                        >
                          Show hint
                        </button>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </li>
          );
        })}
      </ol>

      <div className="overflow-hidden rounded-xl border border-craft-border bg-craft-navy shadow-elevated">
        <div className="flex items-center gap-2 border-b border-white/10 px-3.5 py-2">
          <TerminalSquare className="h-3.5 w-3.5 text-violet-300" />
          <p className="text-xs font-medium text-slate-200">Practice terminal</p>
          <p className="ml-auto text-[11px] text-slate-400">
            Simulated · nothing runs on your machine
          </p>
        </div>

        <div
          ref={streamRef}
          className="max-h-72 min-h-[9rem] overflow-y-auto px-3.5 py-3 font-mono text-xs leading-relaxed"
        >
          {lines.length === 0 && (
            <p className="text-slate-500">
              Type the command for step 1 and press Enter.
            </p>
          )}
          {lines.map((line, i) => {
            if (line.kind === "command") {
              return (
                <p key={i} className="text-slate-100">
                  <span className="select-none text-violet-400">$ </span>
                  {line.text}
                </p>
              );
            }
            if (line.kind === "success") {
              return (
                <p key={i} className="mt-1 text-emerald-400">
                  ✓ {line.text}
                </p>
              );
            }
            if (line.kind === "coach") {
              return (
                <p key={i} className="mt-1 whitespace-pre-wrap text-amber-300">
                  {line.text}
                </p>
              );
            }
            return (
              <pre key={i} className="whitespace-pre-wrap text-slate-300">
                {line.text}
              </pre>
            );
          })}
        </div>

        <form
          onSubmit={(e) => {
            e.preventDefault();
            run(draft);
          }}
          className="flex items-center gap-2 border-t border-white/10 px-3.5 py-2.5"
        >
          <span className="select-none font-mono text-xs text-violet-400">$</span>
          <input
            ref={inputRef}
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={(e) => {
              // Shell-style history. Expected by anyone who has used a terminal.
              if (e.key === "ArrowUp") {
                e.preventDefault();
                if (!history.length) return;
                const idx = historyIdx === null ? history.length - 1 : Math.max(0, historyIdx - 1);
                setHistoryIdx(idx);
                setDraft(history[idx]);
              } else if (e.key === "ArrowDown") {
                e.preventDefault();
                if (historyIdx === null) return;
                const idx = historyIdx + 1;
                if (idx >= history.length) {
                  setHistoryIdx(null);
                  setDraft("");
                } else {
                  setHistoryIdx(idx);
                  setDraft(history[idx]);
                }
              }
            }}
            spellCheck={false}
            autoComplete="off"
            autoCapitalize="off"
            aria-label="Practice terminal command"
            placeholder={allDone ? "All steps complete — experiment freely" : "Type a command…"}
            className="min-w-0 flex-1 bg-transparent font-mono text-xs text-slate-100 placeholder:text-slate-500 focus:outline-none"
          />
          <button
            type="button"
            onClick={reset}
            className="shrink-0 rounded-md p-1 text-slate-400 transition hover:bg-white/10 hover:text-slate-100"
            aria-label="Clear terminal"
            title="Clear"
          >
            <RotateCcw className="h-3.5 w-3.5" />
          </button>
        </form>
      </div>

      {allDone && (
        <div className="flex items-start gap-2.5 rounded-xl border border-emerald-500/30 bg-emerald-50/60 px-4 py-3 dark:bg-emerald-500/10">
          <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-600 dark:text-emerald-400" />
          <div>
            <p className="text-sm font-semibold text-craft-ink">
              {spec.completion?.title ?? "Every step done."}
            </p>
            <p className="mt-0.5 text-sm text-craft-muted">
              {spec.completion?.body ??
                "Run these for real in your own terminal — the commands are identical."}
            </p>
          </div>
        </div>
      )}

      {!allDone && nextTask && (
        <p className="flex items-center gap-1.5 text-xs text-craft-faint">
          <ChevronRight className="h-3 w-3" />
          Step {tasks.indexOf(nextTask) + 1} of {tasks.length}
        </p>
      )}
    </div>
  );
}
