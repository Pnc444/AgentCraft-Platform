export function SiteFooter() {
  return (
    <footer className="border-t border-white/5 py-10">
      <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-6 text-sm text-slate-500">
        <p>
          <span aria-hidden>⚡</span> Agent<span className="text-craft-accent">Craft</span> — learn AI agents from zero.
        </p>
        <p>© {new Date().getFullYear()} AgentCraft. Built by students, for students.</p>
      </div>
    </footer>
  );
}
