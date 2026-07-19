# CLAUDE.md and Skills

## Two ways to teach an agent
Claude Code learns about your project from files it reads automatically. Today you write both kinds:

- **CLAUDE.md** — always loaded. Standing instructions: what this project is, what the agent must and must not do.
- **Skills** — loaded when relevant. Step-by-step procedures for repeatable jobs. You know this one: it's the same `SKILL.md` idea from OpenClaw, and the format transfers almost line for line.

## Part 1 — CLAUDE.md
In your `~/agent-practice` folder, create a file named `CLAUDE.md`:

```markdown
# Practice workspace

This is a sandbox folder for learning Claude Code. Rules:

- Only create or modify files inside this folder.
- Never run commands that touch files outside this folder.
- Keep all writing in English, short and plain.
- When asked to write notes, save them as markdown files in notes/.
```

Start a fresh session (`claude`) and test it:

```text
write a note about what CLAUDE.md does
```

The agent should create it under `notes/` as markdown — because your CLAUDE.md said so, not because you told it in the prompt. That's the point: **CLAUDE.md is prompt-writing you do once.**

![Agent following CLAUDE.md rules — note saved to notes/](/images/lessons/claude-claudemd/note-in-notes.png)

Rules of thumb: keep it short (it's loaded every session, and long files get skimmed), make rules concrete ("save notes in notes/" beats "be organized"), and put safety rules here — this is your first guardrail file.

## Part 2 — Your first skill
Skills live in `.claude/skills/<name>/SKILL.md`. Create `.claude/skills/daily-log/SKILL.md`:

```markdown
---
name: daily-log
description: Append a dated entry to the practice log. Use when asked to log progress or record what was done today.
---

# Daily log

1. Open log.md in the project root (create it if missing).
2. Add a heading with today's date if there isn't one yet.
3. Under it, append the entry the user described, as a single bullet.
4. Do not rewrite or delete previous entries.
```

The **description is the trigger** — the agent reads it to decide when the skill applies, exactly like OpenClaw's frontmatter. Test both invocation paths in a fresh session:

```text
log that I finished the CLAUDE.md lesson
```

(agent picks the skill by itself), and the explicit form: type `/` and find `daily-log` in the command list.

![log.md after two skill invocations — dated heading, bullets appended](/images/lessons/claude-claudemd/daily-log.png)

Run it twice. If the second run rewrites the file instead of appending, your step 4 wasn't clear enough — edit the skill and try again. **Debugging a skill is editing prose.** Let that sink in: that's what "programming" an agent looks like in 2026.

## CLAUDE.md vs skill — which one?
Standing rule, applies always → CLAUDE.md. Procedure, applies when triggered → skill. If you find yourself writing "when asked to X, do Y" in CLAUDE.md, that's a skill trying to escape.

## Self-check
1. Does a fresh session obey a CLAUDE.md rule without being reminded?
2. Does your skill trigger from a natural phrase (not just `/daily-log`)?
3. Did running it twice append rather than overwrite?

## Takeaway
You configured behavior (CLAUDE.md) and taught a procedure (skill) — all markdown. Next lesson: instead of teaching the agent a task, you build it a **colleague**.
