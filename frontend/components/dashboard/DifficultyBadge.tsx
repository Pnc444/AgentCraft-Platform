import clsx from "clsx";

const LABELS: Record<number, { label: string; cls: string }> = {
  1: { label: "Beginner", cls: "bg-emerald-50 text-emerald-700 border-emerald-200" },
  2: { label: "Intermediate", cls: "bg-amber-50 text-amber-700 border-amber-200" },
  3: { label: "Advanced", cls: "bg-sky-50 text-sky-700 border-sky-200" },
};

export function DifficultyBadge({ difficulty }: { difficulty: number }) {
  const { label, cls } = LABELS[difficulty] ?? LABELS[1];
  return (
    <span className={clsx("rounded-full border px-2.5 py-0.5 text-xs font-semibold", cls)}>
      {label}
    </span>
  );
}
