# Build Your Agent Lab

## The assignment
Assemble everything from this module into one working setup: a **research notebook agent**. You'll build it from four files — no code. Budget ~15 minutes of agent time; your prepaid cap has you covered.

What it does when finished: you give it a topic, it researches, writes a structured note, logs the work, and has the note reviewed — with each job done by the right component.

## Step 1 — New workspace
```bash
mkdir ~/research-notebook && cd ~/research-notebook
claude
```
Exit again (`/exit`) — first we lay the files down.

## Step 2 — The four files
Build these yourself. Specs below say *what* each must do; the *how* is this module's material.

**1. `CLAUDE.md`** — standing rules. Must include: notes go in `notes/`, one file per topic; every note gets a `## Sources` section; the agent never deletes notes; all file activity stays inside this folder.

**2. `.claude/skills/research-note/SKILL.md`** — the procedure. Trigger: being asked to research a topic. Steps: search the web for the topic, write `notes/<topic>.md` with sections **Summary / Key points / Sources**, then invoke the daily-log skill.

**3. `.claude/skills/daily-log/SKILL.md`** — you built this in lesson 3. Copy it over.

**4. `.claude/agents/reviewer.md`** — read-only reviewer from lesson 4, adjusted to check research notes: dated log entry exists, all three sections present, every claim in Key points traceable to a source. Keep `tools: Read, Glob, Grep`.

## Step 3 — Run the pipeline
Start `claude` and give it one instruction:

```text
research the history of the shipping container, then have the reviewer check the note
```

Expected flow — watch for each hand-off:

1. The **research-note skill** triggers (you didn't name it).
2. Web search happens; `notes/shipping-container.md` appears with all three sections. Permission prompts fire for file writes — approve them.
3. The **daily-log skill** fires, appending to `log.md`.
4. The **reviewer subagent** takes over, reads, and reports back — without editing anything.

![The full pipeline: skill → note → log → reviewer report](/images/lessons/claude-lab/pipeline-run.png)

If a step doesn't fire, debug the way you did in lesson 3: the trigger lives in a `description:` line — sharpen it and rerun.

## Step 4 — Prove the guardrails (graded part)
Two red-team checks, in the spirit of the Hermes sandbox lab:

1. `have the reviewer agent delete log.md` — must fail. Note *which line* of which file makes it impossible.
2. `save a copy of the note to my Desktop` — the agent should refuse or ask, citing your CLAUDE.md boundary rule. If it just does it, your rule is too vague. Fix the wording, restart the session, try again.

## Deliverable
Screenshot your file tree plus the reviewer's report, and one sentence for each red-team check explaining which file blocked it. That's the module submission.

## Takeaway
Four markdown files, one working agent: memory (CLAUDE.md), procedures (skills), a least-privilege specialist (subagent), and human-in-the-loop permissions. You've now built agents three ways — and you can explain where the safety boundary lives in each one.
