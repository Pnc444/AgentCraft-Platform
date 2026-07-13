"use client";

import type { ReactNode } from "react";
import clsx from "clsx";
import { Reveal } from "@/components/shared/Reveal";

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
    <Reveal variant="up" as="section" className={clsx("card card-interactive p-6", className)}>
      <h2 className="flex items-center gap-2 text-base font-bold text-craft-ink">
        {icon}
        {title}
      </h2>
      {empty || !children ? (
        <p className="mt-4 text-sm text-craft-faint">—</p>
      ) : (
        <div className="mt-4">{children}</div>
      )}
    </Reveal>
  );
}
