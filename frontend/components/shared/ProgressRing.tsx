"use client";

import clsx from "clsx";

interface ProgressRingProps {
  value: number;
  size?: number;
  stroke?: number;
  className?: string;
  label?: string;
  sublabel?: string;
}

/** Circular progress from a real 0–100 percentage. */
export function ProgressRing({
  value,
  size = 88,
  stroke = 8,
  className,
  label,
  sublabel,
}: ProgressRingProps) {
  const pct = Math.max(0, Math.min(100, Math.round(value || 0)));
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const offset = c - (pct / 100) * c;

  return (
    <div className={clsx("relative inline-flex items-center justify-center", className)}>
      <svg width={size} height={size} className="-rotate-90" aria-hidden>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke="currentColor"
          strokeWidth={stroke}
          className="text-craft-soft"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke="currentColor"
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={c}
          strokeDashoffset={offset}
          className="text-violet-600 transition-[stroke-dashoffset] duration-700 ease-out dark:text-violet-400"
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <span className="text-lg font-bold tabular-nums text-craft-ink">{label ?? `${pct}%`}</span>
        {sublabel ? <span className="text-[10px] text-craft-faint">{sublabel}</span> : null}
      </div>
    </div>
  );
}
