import { LogoIcon } from "@/components/shared/Logo";

export function SiteFooter() {
  return (
    <footer className="border-t border-white/5 py-10">
      <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-6 text-sm text-slate-500">
        <p className="flex items-center gap-2">
          <LogoIcon className="h-5 w-5" />
          <span>Agent<span className="text-craft-accent">Craft</span> — learn AI agents from zero.</span>
        </p>
        <p>© {new Date().getFullYear()} AgentCraft. Built by students, for students.</p>
      </div>
    </footer>
  );
}
