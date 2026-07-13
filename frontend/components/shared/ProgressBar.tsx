import clsx from "clsx";

interface ProgressBarProps {
  value: number;
  className?: string;
  barClassName?: string;
}

/** Outline track + fill that shifts blue → shiny cyan as progress grows. */
export function ProgressBar({ value, className, barClassName }: ProgressBarProps) {
  const pct = Math.max(0, Math.min(100, value));
  const shine = 0.25 + (pct / 100) * 0.55;

  return (
    <div
      className={clsx(
        "h-1.5 overflow-hidden rounded-full border border-craft-border bg-craft-soft shadow-[inset_0_1px_3px_rgba(15,23,42,0.12)] dark:shadow-[inset_0_1px_3px_rgba(0,0,0,0.45)]",
        className
      )}
      role="progressbar"
      aria-valuenow={pct}
      aria-valuemin={0}
      aria-valuemax={100}
    >
      <div
        className={clsx(
          "h-full rounded-full transition-[width,box-shadow] duration-500 ease-out",
          barClassName
        )}
        style={{
          width: `${pct}%`,
          ...(barClassName
            ? undefined
            : {
                background: `linear-gradient(90deg,
                  #1D4ED8 0%,
                  #2563EB ${Math.max(20, 55 - pct * 0.25)}%,
                  #06B6D4 ${65 + pct * 0.2}%,
                  #A5F3FC 100%)`,
                boxShadow: `0 0 ${6 + pct * 0.08}px rgba(34, 211, 238, ${shine})`,
              }),
        }}
      />
    </div>
  );
}
