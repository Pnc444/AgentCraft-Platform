export function Features() {
  return (
    <section id="features" className="border-t border-white/5 bg-craft-950 py-24">
      <div className="mx-auto max-w-6xl space-y-24 px-6">
        <div className="grid items-center gap-12 lg:grid-cols-2">
          <div>
            <h3 className="text-2xl font-bold text-white">Learn in Small Steps</h3>
            <p className="mt-4 text-slate-400">
              Students are not expected to understand everything at once. Lessons are broken into
              manageable chunks so each concept builds on the last.
            </p>
          </div>
          <div className="rounded-2xl border border-white/10 bg-craft-900/60 p-8">
            <div className="space-y-3">
              <div className="rounded-lg bg-craft-800 px-4 py-3 text-sm text-slate-300">Lesson 1 — What is an agent?</div>
              <div className="rounded-lg bg-craft-800/60 px-4 py-3 text-sm text-slate-500">Lesson 2 — Tools &amp; memory</div>
              <div className="rounded-lg bg-craft-800/40 px-4 py-3 text-sm text-slate-600">Lesson 3 — Workflows</div>
            </div>
          </div>
        </div>

        <div className="grid items-center gap-12 lg:grid-cols-2">
          <div className="order-2 rounded-2xl border border-white/10 bg-craft-900/60 p-8 lg:order-1">
            <p className="font-mono text-sm text-craft-glow">mini_project.py</p>
            <pre className="mt-4 overflow-x-auto text-sm text-slate-400">
              <code>{`assistant = Agent(
  purpose="summarize notes",
  tools=[read_file, search]
)`}</code>
            </pre>
          </div>
          <div className="order-1 lg:order-2">
            <h3 className="text-2xl font-bold text-white">Build Real Projects</h3>
            <p className="mt-4 text-slate-400">
              Learn by building, not just reading. AgentCraft guides you toward small working
              projects that build confidence step by step.
            </p>
          </div>
        </div>

        <div className="grid items-center gap-12 lg:grid-cols-2">
          <div>
            <h3 className="text-2xl font-bold text-white">Scoped AI Practice</h3>
            <p className="mt-4 text-slate-400">
              Safe, limited-scope AI learning. Students are not thrown into full-access agents
              immediately — the platform teaches structure, constraints, and safe tool use.
            </p>
          </div>
          <div className="rounded-2xl border border-emerald-500/20 bg-emerald-950/20 p-8">
            <p className="text-sm font-medium text-emerald-400">Sandbox workspace</p>
            <ul className="mt-4 space-y-2 text-sm text-slate-400">
              <li>✓ Allowed: read files, search docs</li>
              <li>✗ Blocked: unrestricted web, shell</li>
            </ul>
          </div>
        </div>

        <div className="grid items-center gap-12 lg:grid-cols-2">
          <div className="order-2 rounded-2xl border border-white/10 bg-craft-900/60 p-8 lg:order-1">
            <div className="flex items-center justify-between text-sm text-slate-400">
              <span>Level 4 of 9</span>
              <span className="text-craft-glow">Backend Basics</span>
            </div>
            <div className="mt-4 h-2 rounded-full bg-craft-800">
              <div className="h-full rounded-full bg-craft-accent" style={{ width: "44%" }} />
            </div>
          </div>
          <div className="order-1 lg:order-2">
            <h3 className="text-2xl font-bold text-white">Track Progress</h3>
            <p className="mt-4 text-slate-400">
              See where you are in the learning path and what comes next. Checkpoints keep the
              journey clear and motivating.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
