"use client";

import { useState } from "react";
import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";
import { AiPanel } from "./AiPanel";

export function DashboardShell({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [aiPanelOpen, setAiPanelOpen] = useState(false);

  return (
    <div className="flex min-h-screen">
      <Sidebar mobileOpen={sidebarOpen} onMobileClose={() => setSidebarOpen(false)} />

      <div className="flex min-w-0 flex-1 flex-col">
        <Topbar onOpenSidebar={() => setSidebarOpen(true)} onToggleAiPanel={() => setAiPanelOpen((v) => !v)} />

        <div className="flex min-h-0 flex-1">
          <main className="min-w-0 flex-1 overflow-y-auto p-6 lg:p-8">{children}</main>
          <AiPanel mobileOpen={aiPanelOpen} onMobileClose={() => setAiPanelOpen(false)} />
        </div>
      </div>

      {(sidebarOpen || aiPanelOpen) && (
        <button
          type="button"
          aria-label="Close panels"
          className="fixed inset-0 z-30 bg-black/60 lg:hidden"
          onClick={() => {
            setSidebarOpen(false);
            setAiPanelOpen(false);
          }}
        />
      )}
    </div>
  );
}
