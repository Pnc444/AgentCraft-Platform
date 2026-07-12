import type { ReactNode } from "react";

export function Features() {
  return (
    <section id="features" className="border-t border-slate-200 bg-white py-24">
      <div className="mx-auto max-w-6xl space-y-20 px-6">
        <FeatureRow
          title="Learn in small steps"
          body="Students are not expected to understand everything at once. Lessons are broken into manageable chunks so each concept builds on the last."
          visual={
            <div className="space-y-2">
              <div className="rounded-xl bg-cyan-50 px-4 py-3 text-sm font-medium text-cyan-800">
                Lesson 1 — What is an agent?
              </div>
              <div className="rounded-xl bg-slate-50 px-4 py-3 text-sm text-slate-500">
                Lesson 2 — Tools &amp; memory
              </div>
              <div className="rounded-xl bg-slate-50/70 px-4 py-3 text-sm text-slate-400">
                Lesson 3 — Workflows
              </div>
            </div>
          }
        />

        <FeatureRow
          reverse
          title="Build real projects"
          body="Learn by building, not just reading. AgentCraft guides you toward small working projects that build confidence step by step."
          visual={
            <div>
              <p className="font-mono text-sm font-medium text-cyan-600">mini_project.py</p>
              <pre className="mt-3 overflow-x-auto rounded-xl bg-slate-900 p-4 text-sm text-slate-200">
                <code>{`assistant = Agent(
  purpose="summarize notes",
  tools=[read_file, search]
)`}</code>
              </pre>
            </div>
          }
        />

        <FeatureRow
          title="Scoped practice"
          body="Safe, limited-scope AI learning. Students are not thrown into full-access agents immediately — the platform teaches structure, constraints, and safe tool use."
          visual={
            <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-6">
              <p className="text-sm font-semibold text-emerald-800">Sandbox workspace</p>
              <ul className="mt-3 space-y-2 text-sm text-emerald-900/80">
                <li>Allowed: read files, search docs</li>
                <li>Blocked: unrestricted web, shell</li>
              </ul>
            </div>
          }
        />

        <FeatureRow
          reverse
          title="Track progress"
          body="See where you are in the learning path and what comes next. Checkpoints keep the journey clear and motivating."
          visual={
            <div>
              <div className="flex items-center justify-between text-sm text-slate-500">
                <span>Level 4 of 9</span>
                <span className="font-medium text-cyan-600">Backend Basics</span>
              </div>
              <div className="mt-4 h-2 rounded-full bg-slate-100">
                <div className="h-full rounded-full bg-cyan-500" style={{ width: "44%" }} />
              </div>
            </div>
          }
        />
      </div>
    </section>
  );
}

function FeatureRow({
  title,
  body,
  visual,
  reverse = false,
}: {
  title: string;
  body: string;
  visual: ReactNode;
  reverse?: boolean;
}) {
  return (
    <div className="grid items-center gap-10 lg:grid-cols-2">
      <div className={reverse ? "lg:order-2" : undefined}>
        <h3 className="text-2xl font-bold tracking-tight text-slate-900">{title}</h3>
        <p className="mt-4 leading-relaxed text-slate-500">{body}</p>
      </div>
      <div className={`landing-card p-6 ${reverse ? "lg:order-1" : ""}`}>{visual}</div>
    </div>
  );
}
