# What Hermes Is

## Not a model — an orchestrator
Hermes doesn't run AI on your machine. It's a program that sits between you and a model provider: it takes your task, sends API calls to an LLM, and **executes actions** based on the responses — running shell commands, reading and writing files, calling other services. The heavy thinking happens on the provider's servers; the *doing* happens on yours. That last part is why this module cares so much about safety.

## The three-box diagram
Remember this picture — we reuse it in every lesson this module.

<div class="lesson-diagram">
  <div class="ld-box">
    <div class="ld-title">Gateways</div>
    <div class="ld-sub">CLI, Telegram, web UI</div>
  </div>
  <div class="ld-arrow">→</div>
  <div class="ld-box ld-accent">
    <div class="ld-title">Agent loop + tools</div>
    <div class="ld-sub">Hermes: shell, files, memory, skills</div>
  </div>
  <div class="ld-arrow">→</div>
  <div class="ld-box">
    <div class="ld-title">Model provider</div>
    <div class="ld-sub">OpenRouter → any model</div>
  </div>
  <div class="ld-caption">Tasks flow left to right; results flow back. The middle box is the one that runs on <em>your</em> machine.</div>
</div>

- **Gateways** — how tasks get in: the CLI for now, chat apps later.
- **Agent loop + tools** — Hermes itself: receives a task, asks the model what to do, runs the tool call, feeds the result back, repeats until done.
- **Model provider** — where the intelligence lives. We use OpenRouter so we can swap models without changing anything else.

## Why the three-box split matters
Because every safety decision in this module lives on a **boundary between boxes**. The spending cap lives on the arrow to the model provider — that's where money flows. The Docker sandbox wraps the middle box — that's where commands run. And the gateway is where tasks get in — which is why we keep it to just the CLI until you trust the setup. When something goes wrong with any agent, ever, your first question should be: *which box, or which arrow?*

## Takeaway
Hermes is an orchestrator, not a model: thinking happens on the provider's servers, doing happens on your machine. Keep the three boxes in your head — the rest of this module is just hardening them one at a time.