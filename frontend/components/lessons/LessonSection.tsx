import type { ReactNode } from "react";
import clsx from "clsx";

interface LessonSectionProps {
  title: string;
  icon?: ReactNode;
  children?: ReactNode;
  empty?: boolean;
  className?: string;
}

/** Labeled lesson section. When empty, shows only the section label as a placeholder. */
export function LessonSection({ title, icon, children, empty, className }: LessonSectionProps) {
  return (
    <section className={clsx("card p-6", className)}>
      <h2 className="flex items-center gap-2 text-base font-bold text-slate-900">
        {icon}
        {title}
      </h2>
      {empty || !children ? (
        <p className="mt-4 text-sm text-slate-400">—</p>
      ) : (
        <div className="mt-4">{children}</div>
      )}
    </section>
  );
}
