"use client";

import { useMemo, useState } from "react";
import clsx from "clsx";
import { Check, Copy, Eye, FileCode2, PencilLine, RotateCcw, Search } from "lucide-react";
import type { LessonArtifact } from "@/types";
import { interactionDone } from "@/lib/lesson-interactions";
import type { LessonInteraction } from "@/types";

interface LessonArtifactPackProps {
  artifacts: LessonArtifact[];
  interactionLog: LessonInteraction[];
  variant?: "default" | "inline";
  onRecordInteraction: (event: {
    type: string;
    key: string;
    status?: string;
    details?: Record<string, unknown>;
  }) => void;
}

function getDisplayPath(path: string) {
  const parts = path.split("/").filter(Boolean);
  if (!parts.length) return path;
  if (parts[0].endsWith("artifacts") && parts.length > 1) {
    return parts.slice(1).join("/");
  }
  return path;
}

function serializeArtifactBody(artifact: LessonArtifact) {
  if (artifact.body == null) return "";
  if (artifact.format === "json" && typeof artifact.body !== "string") {
    return JSON.stringify(artifact.body, null, 2);
  }
  return typeof artifact.body === "string"
    ? artifact.body
    : JSON.stringify(artifact.body, null, 2);
}

function ArtifactCard({
  artifact,
  interactionLog,
  variant,
  onRecordInteraction,
}: {
  artifact: LessonArtifact;
  interactionLog: LessonInteraction[];
  variant: "default" | "inline";
  onRecordInteraction: (event: {
    type: string;
    key: string;
    status?: string;
    details?: Record<string, unknown>;
  }) => void;
}) {
  const [activePane, setActivePane] = useState<null | "preview" | "practice">(null);
  const [copiedValue, setCopiedValue] = useState<"path" | "body" | "draft" | null>(null);
  const initialDraft = useMemo(() => serializeArtifactBody(artifact), [artifact]);
  const [draft, setDraft] = useState(initialDraft);
  const displayPath = useMemo(() => getDisplayPath(artifact.path), [artifact.path]);
  const fileName = displayPath.split("/").pop() || displayPath;
  const previewKey = `artifact:${artifact.path}:preview`;
  const copyKey = `artifact:${artifact.path}:copy`;
  const practiceKey = `artifact:${artifact.path}:practice`;
  const previewed = interactionDone(interactionLog, previewKey);
  const practiced = interactionDone(interactionLog, practiceKey);
  const previewOpen = activePane === "preview";
  const practiceOpen = activePane === "practice";
  const canPractice = previewed || previewOpen || practiced;

  async function copyValue(kind: "path" | "body" | "draft", value: string) {
    if (!value.trim()) return;
    try {
      await navigator.clipboard.writeText(value);
      setCopiedValue(kind);
      onRecordInteraction({
        type: "artifact_action",
        key: copyKey,
        status: "done",
        details: { artifact_path: artifact.path, action: kind },
      });
      window.setTimeout(() => {
        setCopiedValue((current) => (current === kind ? null : current));
      }, 1600);
    } catch {
      setCopiedValue(null);
    }
  }

  const hasBody = initialDraft.trim().length > 0;

  return (
    <article
      className={clsx(
        "rounded-2xl border border-craft-border bg-craft-surface shadow-soft",
        variant === "inline" ? "p-3" : "p-4"
      )}
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="text-sm font-semibold text-craft-ink">{artifact.summary}</h3>
          <p className="mt-1 text-xs font-medium uppercase tracking-wide text-craft-faint">
            {artifact.format === "json" ? "JSON artifact" : "Text artifact"}
          </p>
          <p className="mt-2 rounded-lg bg-craft-soft px-3 py-2 font-mono text-xs text-craft-ink break-all">
            {fileName}
          </p>
          <p className="mt-1 text-xs text-craft-faint">Lesson file path: {displayPath}</p>
        </div>
        <button
          type="button"
          onClick={() => copyValue("path", displayPath)}
          className="btn-secondary px-3 py-2 text-xs"
        >
          {copiedValue === "path" ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
          {copiedValue === "path" ? "Path copied" : "Copy path"}
        </button>
      </div>

      <div className="mt-4 rounded-xl border border-craft-border bg-craft-soft/60 p-3">
        <div className="flex flex-wrap items-center gap-2">
          <button
            type="button"
            onClick={() => {
              setActivePane("preview");
              onRecordInteraction({
                type: "artifact_action",
                key: previewKey,
                status: "done",
                details: { artifact_path: artifact.path, action: "preview" },
              });
            }}
            className={clsx("px-3 py-2 text-xs", previewOpen ? "btn-primary" : "btn-secondary")}
          >
            <Search className="h-3.5 w-3.5" />
            1. Inspect example
          </button>
          <button
            type="button"
            onClick={() => {
              if (!canPractice) return;
              setActivePane("practice");
              onRecordInteraction({
                type: "artifact_action",
                key: practiceKey,
                status: "done",
                details: { artifact_path: artifact.path, action: "practice_opened" },
              });
            }}
            disabled={!canPractice}
            className={clsx("px-3 py-2 text-xs", practiceOpen ? "btn-primary" : "btn-secondary")}
          >
            <PencilLine className="h-3.5 w-3.5" />
            2. Try a safe edit
          </button>
        </div>

        <div className="mt-3 flex flex-wrap gap-2 text-xs">
          <span className={clsx("rounded-full px-2.5 py-1", previewed ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-500/15 dark:text-emerald-300" : "bg-craft-surface text-craft-faint")}>Inspect {previewed ? "done" : "next"}</span>
          <span className={clsx("rounded-full px-2.5 py-1", practiced ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-500/15 dark:text-emerald-300" : "bg-craft-surface text-craft-faint")}>Practice {practiced ? "done" : "later"}</span>
        </div>

        {!previewOpen && !practiceOpen ? (
          <p className="mt-3 text-sm text-craft-muted">
            {artifact.inspect_prompt || artifact.summary}
          </p>
        ) : null}
      </div>

      {hasBody ? (
        <div className="mt-4 space-y-3 rounded-xl border border-craft-border bg-craft-soft/70 p-3">
          {previewOpen ? (
            <div className="space-y-3">
              <p className="text-sm text-craft-muted">{artifact.inspect_prompt || artifact.summary}</p>
              <pre className="max-h-72 overflow-auto rounded-xl bg-craft-navy px-4 py-3 text-xs text-craft-inverse">
                <code>{initialDraft}</code>
              </pre>
              <button
                type="button"
                onClick={() => copyValue("body", initialDraft)}
                className="btn-secondary px-3 py-2 text-xs"
              >
                {copiedValue === "body" ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
                {copiedValue === "body" ? "Example copied" : "Copy example"}
              </button>
            </div>
          ) : null}

          {practiceOpen ? (
            <div className="space-y-3">
              <p className="text-sm text-craft-muted">
                {artifact.change_prompt ||
                  "Change one safe detail in a practice copy and explain what behavior you expect to change."}
              </p>
              <textarea
                value={draft}
                onChange={(event) => setDraft(event.target.value)}
                className="min-h-[220px] w-full rounded-xl border border-craft-border bg-craft-surface px-3 py-3 font-mono text-xs text-craft-ink shadow-soft focus:border-cyan-500 focus:outline-none"
                spellCheck={false}
              />
              <div className="flex flex-wrap gap-2">
                <button
                  type="button"
                  onClick={() => copyValue("draft", draft)}
                  className="btn-primary px-3 py-2 text-xs"
                >
                  {copiedValue === "draft" ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
                  {copiedValue === "draft" ? "Practice copy copied" : "Copy your edited version"}
                </button>
                <button
                  type="button"
                  onClick={() => setDraft(initialDraft)}
                  className="btn-secondary px-3 py-2 text-xs"
                >
                  <RotateCcw className="h-3.5 w-3.5" />
                  Reset practice copy
                </button>
              </div>
              <p className="text-xs text-craft-faint">
                This is a safe in-browser practice copy. It does not change the real project file.
              </p>
            </div>
          ) : null}
        </div>
      ) : null}
    </article>
  );
}

export function LessonArtifactPack({
  artifacts,
  interactionLog,
  variant = "default",
  onRecordInteraction,
}: LessonArtifactPackProps) {
  if (!artifacts.length) return null;

  return (
    <div className={clsx("grid gap-4", variant === "inline" ? "grid-cols-1" : "md:grid-cols-2")}>
      {artifacts.map((artifact) => (
        <ArtifactCard
          key={artifact.path}
          artifact={artifact}
          interactionLog={interactionLog}
          variant={variant}
          onRecordInteraction={onRecordInteraction}
        />
      ))}
    </div>
  );
}