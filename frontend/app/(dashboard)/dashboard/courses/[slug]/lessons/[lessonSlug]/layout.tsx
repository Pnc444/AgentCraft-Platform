"use client";

import { LessonWorkspaceProvider } from "@/components/lessons/LessonWorkspace";
import { LessonShell } from "@/components/lessons/LessonShell";

export default function LessonLayout({ children }: { children: React.ReactNode }) {
  return (
    <LessonWorkspaceProvider>
      <LessonShell>{children}</LessonShell>
    </LessonWorkspaceProvider>
  );
}
