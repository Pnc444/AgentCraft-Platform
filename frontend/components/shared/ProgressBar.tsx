import clsx from "clsx";

interface ProgressBarProps {
  value: number;
  className?: string;
  barClassName?: string;
}

/** Outline track + purple fill driven by a real 0–100 percentage. */
export function ProgressBar({ value, className, barClassName }: ProgressBarProps) {
  const pct = Math.max(0, Math.min(100, value));
  const shine = 0.25 + (pct / 100) * 0.55;

  return (
    <div
      className={clsx(
        "h-1.5 overflow-hidden rounded-full border border-craft-border bg-craft-soft shadow-[inset_0_1px_3px_rgba(20,18,26,0.12)] dark:shadow-[inset_0_1px_3px_rgba(0,0,0,0.45)]",
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
                  #6D28D9 0%,
                  #7C3AED ${Math.max(20, 55 - pct * 0.25)}%,
                  #8B5CF6 ${65 + pct * 0.2}%,
                  #C4B5FD 100%)`,
                boxShadow: `0 0 ${6 + pct * 0.08}px rgba(124, 58, 237, ${shine})`,
              }),
        }}
      />
    </div>
  );
}
