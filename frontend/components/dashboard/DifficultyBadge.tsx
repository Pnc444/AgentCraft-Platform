import clsx from "clsx";

const LABELS: Record<number, { label: string; cls: string }> = {
  1: {
    label: "Beginner",
    cls: "bg-emerald-500/15 text-emerald-700 border-emerald-500/25 dark:text-emerald-300",
  },
  2: {
    label: "Intermediate",
    cls: "bg-amber-500/15 text-amber-700 border-amber-500/25 dark:text-amber-300",
  },
  3: {
    label: "Advanced",
    cls: "bg-sky-500/15 text-sky-700 border-sky-500/25 dark:text-sky-300",
  },
};

export function DifficultyBadge({ difficulty }: { difficulty: number }) {
  const { label, cls } = LABELS[difficulty] ?? LABELS[1];
  return (
    <span className={clsx("rounded-full border px-2.5 py-0.5 text-xs font-semibold", cls)}>
      {label}
    </span>
  );
}
