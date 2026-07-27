# CLAUDE.md and Skills

## Two ways to teach an agent
Claude Code learns about your project from files it reads automatically. Today you write both kinds:

- **CLAUDE.md** — always loaded. Standing instructions: what this project is, what the agent must and must not do.
- **Skills** — loaded when relevant. Step-by-step procedures for repeatable jobs. You know this one: it's the same `SKILL.md` idea from OpenClaw, and the format transfers almost line for line.

## How we'll create these files
You're not going to hand-write these in a text editor — **you'll ask the agent to write them.** You already have a working Claude Code session and a permission system that asks before it touches anything, so every file in this lesson gets created the same way: you describe the file, the agent proposes it, you approve.

Two reasons this isn't just laziness. It's another rep on the permission boundary, and the skill file lives in a hidden folder (`.claude/`) that's genuinely awkward to create by hand — Windows Explorer refuses folder names starting with a dot.

Yes, you're using the agent to write the file that configures the agent. That's normal. The new instructions take effect the next time you start a session, which is exactly what you'll do to test them.

## Part 1 — CLAUDE.md
In your `~/agent-practice` folder, start a session with `claude` and ask for the file:

```text
create a file called CLAUDE.md in this folder with exactly this content:

# Practice workspace

This is a sandbox folder for learning Claude Code. Rules:

- Only create or modify files inside this folder.
- Never run commands that touch files outside this folder.
- Keep all writing in English, short and plain.
- When asked to write notes, save them as markdown files in notes/.
```

Approve the write when it asks. Open the file and confirm it says what you expect — **read what the agent wrote before you trust it.** If it paraphrased or reformatted, tell it to fix it.

CLAUDE.md is only read at session start, so exit with `/exit` and start a fresh session (`claude`).

Before testing, confirm the agent is standing where the file is:

```text
run pwd and list the files in this folder
```

You should see your practice folder and `CLAUDE.md` in it. If CLAUDE.md isn't there, it got written somewhere else — move it into this folder before going on, or the test below proves nothing.

Now test:

```text
write a short note about why isolation matters when running AI agents
```

Watch where it goes. The agent should save it under `notes/` as a markdown file — because your CLAUDE.md said so, **not** because you told it to in the prompt. You never mentioned `notes/`. That's the point: **CLAUDE.md is prompt-writing you do once.**

The topic doesn't matter here; the destination does. Ask for a note on anything you like — what you're checking is whether the rule fires on its own.

![Agent following CLAUDE.md rules — note saved to notes/](/images/lessons/claude-claudemd/note-in-notes.png)

Rules of thumb: keep it short (it's loaded every session, and long files get skimmed), make rules concrete ("save notes in notes/" beats "be organized"), and put safety rules here — this is your first guardrail file.

## Part 2 — Your first skill
Skills live in `.claude/skills/<name>/SKILL.md`. Same approach — ask for it:

```text
create the file .claude/skills/daily-log/SKILL.md, making the folders if
they don't exist, with exactly this content:

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

The agent creates the nested folders and the file, and asks permission on the way. Confirm it landed at the right path — the folder names have to match exactly or the skill won't load.

The **description is the trigger** — the agent reads it to decide when the skill applies, exactly like OpenClaw's frontmatter.

**Now close your terminal completely and open a new one**, then `cd` back to your practice folder and run `claude`. Not just `/exit` and restart — a full terminal restart. A newly created skill doesn't always register otherwise: you'll see it work when the agent picks it up on its own, but it won't appear in the `/` command list. Restarting the terminal clears that up.

Then test both invocation paths:

```text
log that I finished the CLAUDE.md lesson
```

(agent picks the skill by itself), and the explicit form: type `/` and find `daily-log` in the command list.

![log.md after two skill invocations — dated heading, bullets appended](/images/lessons/claude-claudemd/daily-log.png)

Run it twice. If the second run rewrites the file instead of appending, your step 4 wasn't clear enough — edit the skill and try again. **Debugging a skill is editing prose.** Let that sink in: that's what "programming" an agent looks like in 2026.

<details>
<summary><strong>🛠️ Common issues — click to expand</strong></summary>

**The agent rewrote or reformatted the content instead of copying it**
Tell it plainly: "replace the file with exactly the content I gave you, no changes." Then re-open the file and check.

**"There's no CLAUDE.md file in this project yet" — but you just made one**
The agent is looking in a different folder than the one the file is in. Run `pwd` in the session and compare it to where the file actually landed. Launch `claude` from the practice folder, or move the file to match.

**The agent answers in chat instead of saving a file**
It read your request as a question, not a writing task. Ask for a note on a plain topic ("write a short note about X") rather than asking it to explain something — explanations invite a chat reply. If it still won't save, your CLAUDE.md rule wording is the thing to sharpen.

**The permission prompts don't look like the screenshots**
Check the bottom of your terminal for the permission mode. If it says anything other than default, press `Shift+Tab` until it cycles back. This module runs in default mode throughout.

**`/` says "No skills found" — but the skill clearly works**
This is the one most people hit. The agent triggers the skill fine from a natural phrase, yet the `/` command list claims there are no skills. **Close the terminal entirely and open a new one**, `cd` back to the folder, and run `claude` again. `/exit` alone isn't always enough. The skill will show up.

**The skill never triggers at all**
Confirm the path first — it must be `.claude/skills/daily-log/SKILL.md`, with `SKILL.md` in capitals. Check with `ls -la .claude/skills/daily-log/`. Then restart the terminal as above. If the path is right and a fresh terminal doesn't fix it, the `description:` line is the problem, not the path.

**You'd rather create the files yourself**
Nothing wrong with that. From your practice folder:

```bash
mkdir -p .claude/skills/daily-log
```

Then open `CLAUDE.md` and `.claude/skills/daily-log/SKILL.md` in any text editor and paste the content in. On Windows, use VS Code or run `mkdir` from PowerShell — Explorer won't create a folder whose name starts with a dot.

**You can't see the `.claude` folder**
It's hidden by design. macOS Finder: `Cmd+Shift+.` to toggle. Windows Explorer: View → Show → Hidden items. Or just run `ls -a` / `dir /a` in the terminal.

</details>

## CLAUDE.md vs skill — which one?
Standing rule, applies always → CLAUDE.md. Procedure, applies when triggered → skill. If you find yourself writing "when asked to X, do Y" in CLAUDE.md, that's a skill trying to escape.

## Self-check
1. Did you read both files after the agent wrote them, and do they match what you asked for?
2. Does a fresh session obey a CLAUDE.md rule without being reminded?
3. Does your skill trigger from a natural phrase (not just `/daily-log`)?
4. Did running it twice append rather than overwrite?

## Takeaway
You configured behavior (CLAUDE.md) and taught a procedure (skill) — all markdown, all written by the agent under your approval. Next lesson: instead of teaching the agent a task, you build it a **colleague**.
