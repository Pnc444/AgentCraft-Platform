# What Claude Code Is

## Same picture, third time
Claude Code is Anthropic's agent. Like Hermes and OpenClaw, it is **not a model** — it's an orchestrator that takes your task, calls a model, and executes actions on your machine. The three-box diagram from Module 5 still applies:

<div class="lesson-diagram">
  <div class="ld-box">
    <div class="ld-title">Gateways</div>
    <div class="ld-sub">Terminal, VS Code, web, Slack</div>
  </div>
  <div class="ld-arrow">→</div>
  <div class="ld-box ld-accent">
    <div class="ld-title">Agent loop + tools</div>
    <div class="ld-sub">Claude Code: shell, files, search, subagents</div>
  </div>
  <div class="ld-arrow">→</div>
  <div class="ld-box">
    <div class="ld-title">Model provider</div>
    <div class="ld-sub">Anthropic → Claude models</div>
  </div>
  <div class="ld-caption">By build #3 you should be able to draw this from memory. Only the labels change.</div>
</div>

One difference from the previous builds: the middle and right box come from the **same company**. There's no OpenRouter-style model swapping — Claude Code talks to Claude models only.

## How it differs from Hermes and OpenClaw
- **First-party.** Built by the same lab that trains the model, so the agent loop and the model are tuned for each other. This is the most polished of the three builds.
- **Still no code required.** Everything we customize in this module is markdown and config files — the same SKILL.md format you met in OpenClaw carries over almost unchanged.
- **Safety is built in, not bolted on.** Hermes needed us to bring our own Docker sandbox before first run. Claude Code ships with a **permission system**: by default it asks before editing files or running commands, and its shell tool can be sandboxed. We'll still apply Module 4.5 thinking — but this time we're configuring guardrails, not building them.
- **It's aimed at code, but not only code.** The tools are general: read/write files, run commands, search the web. People use it for research, file wrangling, and automation too.

## The vocabulary for this module
Four file-based concepts do all the work. Each gets its own lesson:

- **CLAUDE.md** — persistent instructions the agent reads at the start of every session. Its memory about your project.
- **Skills** — folders with a `SKILL.md` teaching the agent a repeatable procedure. Same idea as OpenClaw skills.
- **Subagents** — markdown files defining specialist agents (a reviewer, a researcher) that the main agent can delegate to. This is the new concept — neither previous build had it.
- **The `.claude/` directory** — where all of the above lives inside a project.

## Takeaway
Claude Code is build #3: same architecture, first-party polish, and configuration by markdown. The one genuinely new idea is **subagents** — agents defining and delegating to other agents — and it's where this module ends up.
