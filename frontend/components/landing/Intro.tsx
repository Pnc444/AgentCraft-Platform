const ITEMS = [
  "Short interactive lessons",
  "A path that adapts with you",
  "Hands-on projects",
  "Applicable, connected skills",
  "Clear milestones",
  "Guided practice, then your own work",
];

export function Intro() {
  return (
    <section id="about" className="border-t border-stone-800/50 py-24">
      <div className="mx-auto max-w-4xl px-6 text-center">
        <h2 className="text-3xl font-bold text-white sm:text-4xl">Learn one step at a time</h2>
        <p className="mt-6 text-lg text-slate-400">
          AgentCraft adapts with you. What you learn connects to what you build — guided when you
          need it, independent when you are ready.
        </p>

        <ul className="mt-12 grid gap-4 text-left sm:grid-cols-2 lg:grid-cols-3">
          {ITEMS.map((item) => (
            <li key={item} className="rounded-xl border border-stone-700/40 bg-stone-900/40 p-5 text-stone-300">
              {item}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
