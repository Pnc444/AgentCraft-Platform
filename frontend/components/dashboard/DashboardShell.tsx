"use client";

import { useState } from "react";
import { usePathname } from "next/navigation";
import clsx from "clsx";
import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";
import { MobileBottomNav } from "./MobileBottomNav";
import { AcademyBackdrop } from "@/components/shared/AcademyBackdrop";

export function DashboardShell({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const pathname = usePathname();
  const isLessonView = /\/lessons\/[^/]+\//.test(pathname);

  return (
    <div className="flex h-screen overflow-hidden bg-craft-canvas">
      <Sidebar mobileOpen={sidebarOpen} onMobileClose={() => setSidebarOpen(false)} />

      <div className="relative flex min-h-0 min-w-0 flex-1 flex-col">
        <Topbar onOpenSidebar={() => setSidebarOpen(true)} />
        <main
          className={clsx(
            "relative min-h-0 min-w-0 flex-1",
            isLessonView ? "overflow-hidden" : "overflow-y-auto"
          )}
        >
          <AcademyBackdrop subtle />
          <div
            className={clsx(
              "relative z-10",
              isLessonView
                ? "flex h-full min-h-0 flex-col p-3 sm:p-4 lg:px-6 lg:py-4"
                : "p-4 pb-[calc(4.75rem+env(safe-area-inset-bottom))] sm:p-5 lg:px-8 lg:py-6 lg:pb-6"
            )}
          >
            {children}
          </div>
        </main>
      </div>

      <MobileBottomNav />

      {sidebarOpen && (
        <button
          type="button"
          aria-label="Close menu"
          className="fixed inset-0 z-30 bg-craft-navy/40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
}
