import clsx from "clsx";

const LABELS: Record<number, { label: string; cls: string }> = {
  1: { label: "Beginner", cls: "bg-emerald-500/15 text-emerald-300 border-emerald-500/30" },
  2: { label: "Intermediate", cls: "bg-amber-500/15 text-amber-300 border-amber-500/30" },
  3: { label: "Advanced", cls: "bg-red-500/15 text-red-300 border-red-500/30" },
};

export function DifficultyBadge({ difficulty }: { difficulty: number }) {
  const { label, cls } = LABELS[difficulty] ?? LABELS[1];
  return (
    <span className={clsx("rounded-full border px-2.5 py-0.5 text-xs font-medium", cls)}>
      {label}
    </span>
  );
}
