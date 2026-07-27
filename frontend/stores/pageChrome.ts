"use client";

import { create } from "zustand";

type PageChromeState = {
  title: string | null;
  subtitle: string | null;
  showAskTutor: boolean;
  onAskTutor: (() => void) | null;
  headerTabs: { id: string; label: string }[] | null;
  activeTab: string | null;
  onTabChange: ((id: string) => void) | null;
  setChrome: (patch: {
    title?: string | null;
    subtitle?: string | null;
    showAskTutor?: boolean;
    onAskTutor?: (() => void) | null;
    headerTabs?: { id: string; label: string }[] | null;
    activeTab?: string | null;
    onTabChange?: ((id: string) => void) | null;
  }) => void;
  clearChrome: () => void;
};

/** Shared topbar title/actions set by lesson (and other) pages. */
export const usePageChrome = create<PageChromeState>((set) => ({
  title: null,
  subtitle: null,
  showAskTutor: false,
  onAskTutor: null,
  headerTabs: null,
  activeTab: null,
  onTabChange: null,
  setChrome: (patch) => set((s) => ({ ...s, ...patch })),
  clearChrome: () =>
    set({
      title: null,
      subtitle: null,
      showAskTutor: false,
      onAskTutor: null,
      headerTabs: null,
      activeTab: null,
      onTabChange: null,
    }),
}));
