"use client";

import { useMemo, useState } from "react";
import clsx from "clsx";
import { Check, FileText, ListChecks, RotateCcw } from "lucide-react";
import type { LessonArtifact } from "@/types";

interface LessonWorkbenchProps {
  /** The lesson's full artifact bundle (bodies already hydrated server-side). */
  artifacts: LessonArtifact[];
  /** Paths this beat is about; empty means the whole bundle. */
  paths: string[];
  /** The beat's task instructions, shown above the files. */
  instructions: string[];
  /** Fires once every listed file has been opened. */
  onAllOpened: () => void;
}

function basename(path: string): string {
  return path.split("/").pop() ?? path;
}

function bodyText(artifact: LessonArtifact): string {
  if (typeof artifact.body === "string") return artifact.body;
  if (artifact.body == null) return "";
  try {
    return JSON.stringify(artifact.body, null, 2);
  } catch {
    return String(artifact.body);
  }
}

/**
 * The workbench do-beat (plan §4): the real files, openable and safely
 * editable. The old explorer was a hardcoded picture that never showed file
 * contents while the real bodies sat unused in the payload — this renders
 * those bodies. Edits live in a per-file scratch buffer, never the server;
 * Reset restores the shipped text. Deliberately not an IDE: no highlighting,
 * no filesystem, one closed widget.
 */
export function LessonWorkbench({ artifacts, paths, instructions, onAllOpened }: LessonWorkbenchProps) {
  const files = useMemo(() => {
    const scoped = paths.length
      ? paths
          .map((p) => artifacts.find((a) => a.path === p))
          .filter((a): a is LessonArtifact => !!a)
      : artifacts;
    return scoped;
  }, [artifacts, paths]);

  const [active, setActive] = useState<string | null>(null);
  const [opened, setOpened] = useState<Set<string>>(new Set());
  const [buffers, setBuffers] = useState<Record<string, string>>({});

  const activeFile = files.find((f) => f.path === active) ?? null;
  const activeText = activeFile
    ? (buffers[activeFile.path] ?? bodyText(activeFile))
    : "";
  const activeEdited = !!activeFile && buffers[activeFile.path] !== undefined;

  function open(file: LessonArtifact) {
    setActive(file.path);
    setOpened((prev) => {
      if (prev.has(file.path)) return prev;
      const next = new Set(prev);
      next.add(file.path);
      if (next.size === files.length) onAllOpened();
      return next;
    });
  }

  if (!files.length) {
    return <p className="text-sm text-craft-muted">This step&apos;s practice files are missing from the lesson bundle.</p>;
  }

  return (
    <div className="space-y-3">
      {instructions.length > 0 && (
        <div className="rounded-xl border border-violet-500/25 px-4 py-3">
          <p className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-violet-700 dark:text-violet-300">
            <ListChecks className="h-3.5 w-3.5 shrink-0" />
            Try this now
          </p>
          <ul className="mt-2 space-y-1.5">
            {instructions.map((task, i) => (
              <li key={i} className="text-sm text-craft-ink">
                {task}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="overflow-hidden rounded-xl border border-craft-border">
        <div className="flex flex-col sm:flex-row">
          {/* The tree: data, not a hardcoded constant. */}
          <ul className="flex shrink-0 flex-row gap-1 overflow-x-auto border-b border-craft-border bg-craft-soft/60 p-2 sm:w-56 sm:flex-col sm:border-b-0 sm:border-r">
            {files.map((file) => (
              <li key={file.path}>
                <button
                  type="button"
                  onClick={() => open(file)}
                  title={file.path}
                  className={clsx(
                    "flex w-full items-center gap-1.5 whitespace-nowrap rounded-lg px-2.5 py-1.5 text-left font-mono text-xs transition",
                    active === file.path
                      ? "bg-craft-accent-soft text-violet-800 dark:text-violet-200"
                      : "text-craft-ink hover:bg-craft-soft"
                  )}
                >
                  {opened.has(file.path) ? (
                    <Check className="h-3.5 w-3.5 shrink-0 text-emerald-500" />
                  ) : (
                    <FileText className="h-3.5 w-3.5 shrink-0 text-craft-faint" />
                  )}
                  {basename(file.path)}
                </button>
              </li>
            ))}
          </ul>

          <div className="min-w-0 flex-1">
            {activeFile ? (
              <div className="flex flex-col">
                <div className="flex items-center justify-between gap-2 border-b border-craft-border px-3 py-1.5">
                  <p className="truncate text-xs text-craft-muted" title={activeFile.path}>
                    {activeFile.summary || activeFile.path}
                  </p>
                  {activeEdited && (
                    <button
                      type="button"
                      onClick={() =>
                        setBuffers(({ [activeFile.path]: _dropped, ...rest }) => rest)
                      }
                      className="inline-flex shrink-0 items-center gap-1 rounded-md px-2 py-1 text-xs text-craft-muted transition hover:bg-craft-soft hover:text-craft-ink"
                    >
                      <RotateCcw className="h-3 w-3 shrink-0" />
                      Reset file
                    </button>
                  )}
                </div>
                <textarea
                  value={activeText}
                  spellCheck={false}
                  onChange={(e) =>
                    setBuffers((prev) => ({ ...prev, [activeFile.path]: e.target.value }))
                  }
                  // Shorter on phones: at 375x667 a 14rem editor pushed the
                  // widget's own footer past the beat pane. The pane scrolls
                  // internally either way, but a clipped footer reads as broken.
                  className="h-36 w-full resize-none bg-craft-surface p-3 font-mono text-xs leading-relaxed text-craft-ink outline-none sm:h-64"
                  aria-label={`Contents of ${basename(activeFile.path)}`}
                />
              </div>
            ) : (
              <div className="flex h-36 items-center justify-center p-6 text-center text-sm text-craft-muted sm:h-64">
                Open each file on the left. Looking inside is the whole exercise.
              </div>
            )}
          </div>
        </div>
        <p className="border-t border-craft-border bg-craft-soft/50 px-3 py-1.5 text-[11px] text-craft-faint">
          {opened.size}/{files.length} files opened · This is a practice copy — you can&apos;t break
          anything. Reset puts a file back.
        </p>
      </div>
    </div>
  );
}
