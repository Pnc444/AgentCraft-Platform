"use client";

import { useEffect, useMemo, useState, type ReactNode } from "react";
import { CheckCircle2, Lightbulb, RefreshCw, Sparkles, XCircle } from "lucide-react";
import clsx from "clsx";

/** Tip / myth / try callout used in lesson markdown. */
export function LessonCallout({
  type = "tip",
  children,
}: {
  type?: string;
  children?: ReactNode;
}) {
  const kind = (type || "tip").toLowerCase();
  const meta =
    kind === "myth"
      ? {
          label: "Myth check",
          cls: "border-amber-400/40 bg-amber-50 text-amber-950 dark:bg-amber-500/10 dark:text-amber-100",
          Icon: XCircle,
        }
      : kind === "try"
        ? {
            label: "Try this",
            cls: "border-cyan-400/40 bg-cyan-50 text-cyan-950 dark:bg-cyan-500/10 dark:text-cyan-100",
            Icon: Sparkles,
          }
        : {
            label: "Quick tip",
            cls: "border-emerald-400/40 bg-emerald-50 text-emerald-950 dark:bg-emerald-500/10 dark:text-emerald-100",
            Icon: Lightbulb,
          };

  return (
    <aside className={clsx("my-5 rounded-xl border px-4 py-3 text-sm leading-relaxed", meta.cls)}>
      <p className="mb-1 flex items-center gap-1.5 text-xs font-bold uppercase tracking-wide opacity-80">
        <meta.Icon className="h-3.5 w-3.5" />
        {meta.label}
      </p>
      <div className="[&_p]:mb-0">{children}</div>
    </aside>
  );
}

/** Instant multiple-choice check with reveal — no server round-trip. */
export function PickOne({
  prompt,
  options,
  answer,
  children,
}: {
  prompt?: string;
  options?: string;
  answer?: string;
  children?: ReactNode;
}) {
  const choices = useMemo(
    () => (options ?? "").split("|").map((s) => s.trim()).filter(Boolean),
    [options]
  );
  const correct = Number.parseInt(answer ?? "0", 10);
  const [selected, setSelected] = useState<number | null>(null);
  const [revealed, setRevealed] = useState(false);

  if (!choices.length) return null;

  const isCorrect = selected !== null && selected === correct;

  function reset() {
    setSelected(null);
    setRevealed(false);
  }

  return (
    <div className="my-6 rounded-2xl border border-craft-border bg-craft-card p-4 shadow-soft ring-1 ring-craft-border/40">
      <p className="text-xs font-bold uppercase tracking-wide text-cyan-600 dark:text-cyan-400">
        Quick check
      </p>
      <p className="mt-1 text-sm font-semibold text-craft-ink">{prompt}</p>
      <ul className="mt-3 space-y-2">
        {choices.map((choice, i) => {
          const chosen = selected === i;
          return (
            <li key={choice}>
              <button
                type="button"
                disabled={revealed}
                onClick={() => {
                  setSelected(i);
                  setRevealed(true);
                }}
                className={clsx(
                  "w-full rounded-xl border px-3 py-2.5 text-left text-sm transition",
                  !revealed && "border-craft-border hover:border-cyan-400/50 hover:bg-craft-accent-soft",
                  revealed && chosen && isCorrect && "border-emerald-400 bg-emerald-50 dark:bg-emerald-500/15",
                  revealed && chosen && !isCorrect && "border-amber-400 bg-amber-50 dark:bg-amber-500/15",
                  revealed && !chosen && i === correct && "border-emerald-300/80 bg-emerald-50/60 dark:bg-emerald-500/10",
                  revealed && !chosen && i !== correct && "opacity-60"
                )}
              >
                {choice}
              </button>
            </li>
          );
        })}
      </ul>
      {revealed && (
        <div
          className={clsx(
            "mt-3 flex flex-col gap-2 text-sm animate-fade-up",
            isCorrect ? "text-emerald-700 dark:text-emerald-300" : "text-amber-800 dark:text-amber-200"
          )}
        >
          <p className="flex items-start gap-2">
            {isCorrect ? (
              <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0" />
            ) : (
              <XCircle className="mt-0.5 h-4 w-4 shrink-0" />
            )}
            <span>
              {isCorrect ? "Nice — you got it." : "Not quite — here’s the idea:"}
              {children ? (
                <span className="mt-1 block text-craft-muted">{children}</span>
              ) : null}
            </span>
          </p>
          <button
            type="button"
            onClick={reset}
            className="inline-flex w-fit items-center gap-1.5 rounded-lg border border-craft-border px-2.5 py-1 text-xs font-medium text-craft-muted transition hover:border-cyan-400/50 hover:text-craft-ink"
          >
            <RefreshCw className="h-3 w-3" />
            Try again
          </button>
        </div>
      )}
    </div>
  );
}

/** Myth vs fact flip — tap a side, then reveal. */
export function MythBust({
  claim,
  answer = "myth",
  children,
}: {
  claim?: string;
  answer?: string;
  children?: ReactNode;
}) {
  const truth = (answer || "myth").toLowerCase() === "fact" ? "fact" : "myth";
  const [pick, setPick] = useState<"myth" | "fact" | null>(null);

  const revealed = pick !== null;
  const isCorrect = pick === truth;

  return (
    <div className="my-6 rounded-2xl border border-craft-border bg-craft-card p-4 shadow-soft">
      <p className="text-xs font-bold uppercase tracking-wide text-amber-600 dark:text-amber-400">
        Myth or fact?
      </p>
      <p className="mt-2 text-sm font-semibold text-craft-ink">{claim}</p>
      <div className="mt-3 grid grid-cols-2 gap-2">
        {(["myth", "fact"] as const).map((side) => (
          <button
            key={side}
            type="button"
            disabled={revealed}
            onClick={() => setPick(side)}
            className={clsx(
              "rounded-xl border px-3 py-3 text-sm font-semibold capitalize transition",
              !revealed && "border-craft-border hover:border-amber-400/50 hover:bg-amber-50/80 dark:hover:bg-amber-500/10",
              revealed && pick === side && isCorrect && "border-emerald-400 bg-emerald-50 dark:bg-emerald-500/15",
              revealed && pick === side && !isCorrect && "border-amber-400 bg-amber-50 dark:bg-amber-500/15",
              revealed && pick !== side && truth === side && "border-emerald-300/80 bg-emerald-50/50 dark:bg-emerald-500/10",
              revealed && pick !== side && truth !== side && "opacity-50"
            )}
          >
            {side}
          </button>
        ))}
      </div>
      {revealed && (
        <div className="mt-3 space-y-2 animate-fade-up">
          <p
            className={clsx(
              "flex items-start gap-2 text-sm",
              isCorrect ? "text-emerald-700 dark:text-emerald-300" : "text-amber-800 dark:text-amber-200"
            )}
          >
            {isCorrect ? (
              <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0" />
            ) : (
              <XCircle className="mt-0.5 h-4 w-4 shrink-0" />
            )}
            <span>
              {isCorrect ? "Correct — " : "Close — "}
              it’s a <strong className="capitalize">{truth}</strong>.
              {children ? <span className="mt-1 block text-craft-muted">{children}</span> : null}
            </span>
          </p>
          <button
            type="button"
            onClick={() => setPick(null)}
            className="inline-flex items-center gap-1.5 rounded-lg border border-craft-border px-2.5 py-1 text-xs font-medium text-craft-muted transition hover:border-cyan-400/50 hover:text-craft-ink"
          >
            <RefreshCw className="h-3 w-3" />
            Try again
          </button>
        </div>
      )}
    </div>
  );
}

function shuffleIndices(n: number): number[] {
  const arr = Array.from({ length: n }, (_, i) => i);
  for (let i = arr.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  // Avoid the trivial “already sorted” layout when possible
  if (n > 2 && arr.every((v, i) => v === i)) {
    [arr[0], arr[1]] = [arr[1], arr[0]];
  }
  return arr;
}

/** Click steps in order — shuffled display, correct sequence underneath. */
export function OrderSteps({
  prompt,
  steps,
  children,
}: {
  prompt?: string;
  steps?: string;
  children?: ReactNode;
}) {
  const items = useMemo(
    () => (steps ?? "").split("|").map((s) => s.trim()).filter(Boolean),
    [steps]
  );
  const [order, setOrder] = useState<number[]>([]);
  const [picked, setPicked] = useState<number[]>([]);
  const [done, setDone] = useState(false);

  useEffect(() => {
    if (items.length < 2) return;
    setOrder(shuffleIndices(items.length));
    setPicked([]);
    setDone(false);
  }, [items]);

  if (items.length < 2) return null;

  const display = order.length === items.length ? order : items.map((_, i) => i);
  const nextExpected = picked.length;
  const complete = picked.length === items.length;

  function onTap(originalIndex: number) {
    if (done || picked.includes(originalIndex)) return;
    if (originalIndex === nextExpected) {
      const next = [...picked, originalIndex];
      setPicked(next);
      if (next.length === items.length) setDone(true);
    } else {
      setPicked([]);
    }
  }

  function reset() {
    setPicked([]);
    setDone(false);
    setOrder(shuffleIndices(items.length));
  }

  return (
    <div className="my-6 rounded-2xl border border-craft-border bg-craft-card p-4 shadow-soft">
      <p className="text-xs font-bold uppercase tracking-wide text-cyan-600 dark:text-cyan-400">
        Order the steps
      </p>
      <p className="mt-1 text-sm font-semibold text-craft-ink">
        {prompt || "Tap in the right order."}
      </p>
      <p className="mt-1 text-xs text-craft-muted">
        {done
          ? "Sequence complete."
          : `Next: step ${nextExpected + 1} of ${items.length} (wrong tap resets)`}
      </p>
      <ul className="mt-3 space-y-2">
        {display.map((originalIndex) => {
          const label = items[originalIndex];
          const rank = picked.indexOf(originalIndex);
          const locked = rank !== -1;
          return (
            <li key={`${originalIndex}-${label}`}>
              <button
                type="button"
                disabled={done || locked}
                onClick={() => onTap(originalIndex)}
                className={clsx(
                  "flex w-full items-center gap-3 rounded-xl border px-3 py-2.5 text-left text-sm transition",
                  locked
                    ? "border-cyan-400/50 bg-cyan-50 dark:bg-cyan-500/10"
                    : "border-craft-border hover:border-cyan-400/50 hover:bg-craft-accent-soft",
                  done && "opacity-90"
                )}
              >
                <span
                  className={clsx(
                    "flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-bold",
                    locked
                      ? "bg-cyan-500 text-white"
                      : "bg-craft-soft text-craft-muted ring-1 ring-craft-border"
                  )}
                >
                  {locked ? rank + 1 : "·"}
                </span>
                {label}
              </button>
            </li>
          );
        })}
      </ul>
      {(done || picked.length > 0) && (
        <div className="mt-3 flex flex-wrap items-center gap-2 animate-fade-up">
          {complete && (
            <p className="flex items-center gap-2 text-sm text-emerald-700 dark:text-emerald-300">
              <CheckCircle2 className="h-4 w-4 shrink-0" />
              <span>{children || "Perfect order."}</span>
            </p>
          )}
          <button
            type="button"
            onClick={reset}
            className="inline-flex items-center gap-1.5 rounded-lg border border-craft-border px-2.5 py-1 text-xs font-medium text-craft-muted transition hover:border-cyan-400/50 hover:text-craft-ink"
          >
            <RefreshCw className="h-3 w-3" />
            Reset
          </button>
        </div>
      )}
    </div>
  );
}

/** Silly local “token splitter” so students can tap chips. */
export function TokenDemo({ text = "Hello agents" }: { text?: string }) {
  const [input, setInput] = useState(text);
  const tokens = useMemo(() => {
    const raw = input.trim() || "Hello agents";
    // Rough, fun approximation — not a real tokenizer
    return raw.match(/\w+|[^\w\s]/g) ?? [raw];
  }, [input]);
  const [lit, setLit] = useState<number | null>(null);

  return (
    <div className="my-6 rounded-2xl border border-craft-border bg-craft-navy p-4 text-slate-100 shadow-navy">
      <p className="text-xs font-bold uppercase tracking-wide text-cyan-300">Token playground</p>
      <p className="mt-1 text-sm text-slate-300">
        Type a phrase, then tap a chip. Real models often split into sub-words — this is a friendly demo.
      </p>
      <label className="mt-3 block">
        <span className="sr-only">Phrase to tokenize</span>
        <input
          value={input}
          onChange={(e) => {
            setInput(e.target.value);
            setLit(null);
          }}
          className="w-full rounded-lg border border-white/10 bg-slate-900/80 px-3 py-2 font-mono text-sm text-cyan-50 placeholder:text-slate-500 focus:border-cyan-400/50 focus:outline-none focus:ring-1 focus:ring-cyan-400/40"
          placeholder="Type something fun…"
        />
      </label>
      <div className="mt-3 flex flex-wrap gap-2">
        {tokens.map((tok, i) => (
          <button
            key={`${tok}-${i}`}
            type="button"
            onClick={() => setLit(i)}
            className={clsx(
              "rounded-lg px-2.5 py-1.5 font-mono text-sm transition",
              lit === i
                ? "scale-105 bg-cyan-400 text-slate-900 shadow-soft"
                : "bg-slate-800 text-cyan-100 ring-1 ring-white/10 hover:bg-slate-700"
            )}
          >
            {tok}
          </button>
        ))}
      </div>
      <p className="mt-2 text-xs text-slate-400">
        {tokens.length} chip{tokens.length === 1 ? "" : "s"} (demo count — not a real tokenizer)
      </p>
      {lit !== null && (
        <p className="mt-2 text-sm text-cyan-200/90 animate-fade-up">
          Token #{lit + 1}: <span className="font-mono text-white">{JSON.stringify(tokens[lit])}</span>
        </p>
      )}
    </div>
  );
}

type ReplyMap = Record<string, string>;

function parseReplies(raw?: string): ReplyMap {
  const map: ReplyMap = {};
  for (const part of (raw ?? "").split("|")) {
    const idx = part.indexOf("::");
    if (idx === -1) continue;
    map[part.slice(0, idx).trim().toLowerCase()] = part.slice(idx + 2).trim();
  }
  return map;
}

/** Local pretend-assistant for Module 1 — no API keys required. */
export function PromptPlayground({
  hint,
  replies,
  examples,
}: {
  hint?: string;
  replies?: string;
  examples?: string;
}) {
  const replyMap = useMemo(() => parseReplies(replies), [replies]);
  const chips = useMemo(() => {
    if (examples?.trim()) {
      return examples.split("|").map((s) => s.trim()).filter(Boolean);
    }
    return Object.keys(replyMap).filter((k) => k !== "default").slice(0, 4);
  }, [examples, replyMap]);
  const [prompt, setPrompt] = useState("");
  const [output, setOutput] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  function run(override?: string) {
    const q = (override ?? prompt).trim();
    if (!q) return;
    if (override) setPrompt(override);
    setBusy(true);
    setOutput(null);
    window.setTimeout(() => {
      const lower = q.toLowerCase();
      let text =
        replyMap.default ||
        "Hmm — try a clearer ask (summarize, list, or explain). Models love specifics.";
      for (const [key, value] of Object.entries(replyMap)) {
        if (key !== "default" && lower.includes(key)) {
          text = value;
          break;
        }
      }
      setOutput(text);
      setBusy(false);
    }, 450 + Math.random() * 350);
  }

  return (
    <div className="my-6 overflow-hidden rounded-2xl border border-craft-border bg-craft-card shadow-elevated">
      <div className="border-b border-craft-border bg-craft-soft/80 px-4 py-2.5">
        <p className="text-xs font-bold uppercase tracking-wide text-cyan-600 dark:text-cyan-400">
          Mini playground
        </p>
        <p className="text-xs text-craft-muted">
          {hint || "Type a tiny prompt — this is a pretend model for practice."}
        </p>
      </div>
      <div className="space-y-3 p-4">
        {chips.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {chips.map((chip) => (
              <button
                key={chip}
                type="button"
                onClick={() => run(chip)}
                className="rounded-lg border border-craft-border bg-craft-soft px-2.5 py-1 text-xs font-medium text-craft-muted transition hover:border-cyan-400/50 hover:text-craft-ink"
              >
                {chip}
              </button>
            ))}
          </div>
        )}
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          rows={3}
          placeholder='e.g. "Summarize pizza in 3 bullets"'
          className="input-field resize-y text-sm"
        />
        <button type="button" onClick={() => run()} disabled={busy || !prompt.trim()} className="btn-primary text-xs">
          {busy ? "Thinking…" : "Run prompt"}
        </button>
        {output && (
          <div className="rounded-xl border border-cyan-500/25 bg-craft-accent-soft px-3 py-3 text-sm text-craft-ink animate-fade-up">
            <p className="mb-1 text-[11px] font-semibold uppercase tracking-wide text-cyan-700 dark:text-cyan-300">
              Pretend reply
            </p>
            <p className="whitespace-pre-wrap leading-relaxed">{output}</p>
          </div>
        )}
      </div>
    </div>
  );
}
