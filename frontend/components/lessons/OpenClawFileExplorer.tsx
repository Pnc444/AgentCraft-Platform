"use client";

import { useMemo, useState } from "react";
import clsx from "clsx";
import {
  BookOpen,
  CheckCircle2,
  FileText,
  Folder,
  FolderOpen,
  Lock,
  Map,
  Pencil,
  Star,
} from "lucide-react";

type NodeBadge = "edit" | "read" | "system";

type ExplorerNode = {
  id: string;
  name: string;
  plainName: string;
  kind: "folder" | "file";
  badge: NodeBadge;
  starred?: boolean;
  blurb: string;
  children?: ExplorerNode[];
};

/**
 * A fixed, finite map of the OpenClaw home. Deliberately not a live filesystem:
 * clicking can never change anything, and the tree never grows or shifts.
 */
const TREE: ExplorerNode = {
  id: "home",
  name: "~ (your home folder)",
  plainName: "Where your personal files live",
  kind: "folder",
  badge: "read",
  blurb:
    "The starting point. Every computer account has a home folder like this one. OpenClaw builds its own small home inside it.",
  children: [
    {
      id: "openclaw-root",
      name: ".openclaw/",
      plainName: "The assistant's home",
      kind: "folder",
      badge: "read",
      blurb:
        "Everything OpenClaw owns lives inside this one folder. If you ever wanted to remove OpenClaw completely, deleting this folder would do it. One folder, whole story.",
      children: [
        {
          id: "openclaw-json",
          name: "openclaw.json",
          plainName: "The control panel",
          kind: "file",
          badge: "edit",
          starred: true,
          blurb:
            "How the system runs: which AI model, which tools are granted, which doors are open. Wrong model? This is the file. It starts nearly empty on purpose, and you add one line at a time.",
        },
        {
          id: "workspace",
          name: "workspace/",
          plainName: "Your assistant's desk",
          kind: "folder",
          badge: "read",
          blurb:
            "The folder your assistant works in. Its job description, its notebook, and its recipe box all sit on this desk.",
          children: [
            {
              id: "soul-md",
              name: "SOUL.md",
              plainName: "The job description",
              kind: "file",
              badge: "edit",
              starred: true,
              blurb:
                "Who your assistant is: its role, rules, and boundaries. Wrong personality? This is the file. It is plain text you can read in one minute.",
            },
            {
              id: "memory",
              name: "memory/",
              plainName: "The notebook",
              kind: "folder",
              badge: "read",
              blurb:
                "What your assistant keeps track of between conversations. You can open and read it anytime, and reading it is the whole interaction. It maintains itself.",
            },
            {
              id: "skills",
              name: "skills/",
              plainName: "The recipe box",
              kind: "folder",
              badge: "read",
              blurb:
                "One folder per skill. Each folder holds one recipe card. Three recipes are all this course uses.",
              children: [
                {
                  id: "research-brief",
                  name: "research-brief/",
                  plainName: "One recipe's folder",
                  kind: "folder",
                  badge: "read",
                  blurb:
                    "Each skill gets its own folder, named after the skill. Inside is always exactly one card.",
                  children: [
                    {
                      id: "skill-md",
                      name: "SKILL.md",
                      plainName: "A recipe card",
                      kind: "file",
                      badge: "edit",
                      starred: true,
                      blurb:
                        "Teaches the assistant one task: a name, a description, and instructions in plain language. This one is Juno's research trick from Module 4, written down as a file.",
                    },
                  ],
                },
              ],
            },
          ],
        },
        {
          id: "credentials",
          name: "credentials/",
          plainName: "Keys the system manages",
          kind: "folder",
          badge: "system",
          blurb:
            "Login tokens and keys, handled entirely by OpenClaw. You never need to open this folder, and never opening it is the correct way to use it.",
        },
        {
          id: "logs",
          name: "logs/",
          plainName: "Receipts of what happened",
          kind: "folder",
          badge: "read",
          blurb:
            "A written record of what the assistant did and when. You will meet these again in Module 8, where receipts become the way you trust unattended work.",
        },
      ],
    },
  ],
};

const BADGE_UI: Record<
  NodeBadge,
  { label: string; note: string; className: string; icon: typeof Pencil }
> = {
  edit: {
    label: "You will edit this",
    note: "One of the three files this module is about.",
    className:
      "border-amber-500/40 bg-amber-50 text-amber-800 dark:bg-amber-500/10 dark:text-amber-200",
    icon: Pencil,
  },
  read: {
    label: "You can read this",
    note: "Open it whenever you like. Looking is the whole interaction.",
    className:
      "border-cyan-500/40 bg-cyan-50 text-cyan-800 dark:bg-cyan-500/10 dark:text-cyan-200",
    icon: BookOpen,
  },
  system: {
    label: "The system manages this",
    note: "You never need to open it. Never opening it is correct.",
    className:
      "border-craft-border bg-craft-soft text-craft-muted",
    icon: Lock,
  },
};

function flattenStarredIds(node: ExplorerNode): string[] {
  const own = node.starred ? [node.id] : [];
  return own.concat(...(node.children ?? []).map(flattenStarredIds));
}

function TreeRow({
  node,
  depth,
  selectedId,
  seenIds,
  onSelect,
}: {
  node: ExplorerNode;
  depth: number;
  selectedId: string;
  seenIds: Set<string>;
  onSelect: (node: ExplorerNode) => void;
}) {
  const isSelected = selectedId === node.id;
  const seen = node.starred && seenIds.has(node.id);
  const Icon =
    node.kind === "folder" ? (isSelected ? FolderOpen : Folder) : FileText;

  return (
    <div>
      <button
        type="button"
        onClick={() => onSelect(node)}
        className={clsx(
          "flex w-full items-center gap-2 rounded-lg px-2 py-1.5 text-left text-sm transition",
          isSelected
            ? "bg-cyan-50 text-craft-ink dark:bg-cyan-500/10"
            : "text-craft-muted hover:bg-craft-soft hover:text-craft-ink"
        )}
        style={{ paddingLeft: `${8 + depth * 18}px` }}
        aria-current={isSelected ? "true" : undefined}
      >
        <Icon className="h-4 w-4 shrink-0 text-cyan-600 dark:text-cyan-400" />
        <span className="font-mono text-xs sm:text-sm">{node.name}</span>
        {node.starred ? (
          seen ? (
            <CheckCircle2 className="h-3.5 w-3.5 shrink-0 text-emerald-500" />
          ) : (
            <Star className="h-3.5 w-3.5 shrink-0 fill-amber-400 text-amber-400" />
          )
        ) : null}
        <span className="ml-auto hidden truncate text-xs text-craft-faint sm:inline">
          {node.plainName}
        </span>
      </button>
      {node.children?.map((child) => (
        <TreeRow
          key={child.id}
          node={child}
          depth={depth + 1}
          selectedId={selectedId}
          seenIds={seenIds}
          onSelect={onSelect}
        />
      ))}
    </div>
  );
}

export function OpenClawFileExplorer() {
  const starredIds = useMemo(() => flattenStarredIds(TREE), []);
  const [selected, setSelected] = useState<ExplorerNode>(TREE);
  const [seenIds, setSeenIds] = useState<Set<string>>(new Set());

  const seenStarredCount = starredIds.filter((id) => seenIds.has(id)).length;
  const allStarredSeen = seenStarredCount === starredIds.length;

  function handleSelect(node: ExplorerNode) {
    setSelected(node);
    if (node.starred) {
      setSeenIds((prev) => {
        if (prev.has(node.id)) return prev;
        const next = new Set(prev);
        next.add(node.id);
        return next;
      });
    }
  }

  const badge = BADGE_UI[selected.badge];
  const BadgeIcon = badge.icon;

  return (
    <div className="rounded-xl border border-craft-border bg-craft-surface">
      <div className="flex items-start gap-2 border-b border-craft-border px-4 py-3">
        <Map className="mt-0.5 h-4 w-4 shrink-0 text-cyan-600 dark:text-cyan-400" />
        <div>
          <p className="text-sm font-semibold text-craft-ink">
            The assistant&apos;s home, mapped
          </p>
          <p className="mt-0.5 text-xs text-craft-muted">
            This is a picture, not your real computer. Clicking cannot change or
            break anything. The three starred files are the only ones this
            module is about.
          </p>
        </div>
      </div>

      <div className="grid gap-0 sm:grid-cols-2">
        <div className="border-b border-craft-border p-2 sm:border-b-0 sm:border-r">
          <TreeRow
            node={TREE}
            depth={0}
            selectedId={selected.id}
            seenIds={seenIds}
            onSelect={handleSelect}
          />
        </div>

        <div className="p-4">
          <div className="flex items-center gap-2">
            <span className="font-mono text-sm font-semibold text-craft-ink">
              {selected.name}
            </span>
            {selected.starred ? (
              <Star className="h-4 w-4 fill-amber-400 text-amber-400" />
            ) : null}
          </div>
          <p className="mt-1 text-sm font-medium text-craft-ink">
            {selected.plainName}
          </p>
          <p className="mt-2 text-sm text-craft-muted">{selected.blurb}</p>

          <div
            className={clsx(
              "mt-4 inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-semibold",
              badge.className
            )}
          >
            <BadgeIcon className="h-3.5 w-3.5" />
            {badge.label}
          </div>
          <p className="mt-2 text-xs text-craft-faint">{badge.note}</p>
        </div>
      </div>

      <div className="border-t border-craft-border px-4 py-3">
        {allStarredSeen ? (
          <p className="flex items-center gap-2 text-sm font-medium text-emerald-700 dark:text-emerald-300">
            <CheckCircle2 className="h-4 w-4" />
            Starred files seen: {seenStarredCount} of {starredIds.length}. This
            map is done. Nothing else here needs opening.
          </p>
        ) : (
          <p className="text-sm text-craft-muted">
            Starred files seen: {seenStarredCount} of {starredIds.length}. Open
            each starred file once and this map is done.
          </p>
        )}
        <p className="mt-1 text-xs text-craft-faint">
          A real install has a few extra system folders. They belong to the
          system and need nothing from you.
        </p>
      </div>
    </div>
  );
}
