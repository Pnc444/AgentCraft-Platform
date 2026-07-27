"use client";

import { useState } from "react";
import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";
import { AcademyBackdrop } from "@/components/shared/AcademyBackdrop";

export function DashboardShell({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen overflow-hidden bg-craft-canvas">
      <Sidebar mobileOpen={sidebarOpen} onMobileClose={() => setSidebarOpen(false)} />

      <div className="relative flex min-h-0 min-w-0 flex-1 flex-col">
        <Topbar onOpenSidebar={() => setSidebarOpen(true)} />
        <main className="relative min-h-0 min-w-0 flex-1 overflow-y-auto">
          <AcademyBackdrop subtle />
          {/*
            h-full (not min-h-full) bounds this box to main's height, which is
            what lets the lesson player's flex-1 card SHRINK to the space that
            is actually left. With min-h-full the box grew instead, so short
            viewports — landscape phones especially — scrolled the page.
            Pages with genuinely tall content still overflow this box and main's
            overflow-y-auto scrolls them as before.
          */}
          <div className="relative z-10 flex h-full flex-col p-5 lg:px-8 lg:py-6">
            {children}
          </div>
        </main>
      </div>

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
