# Custom Subagents

## The new idea in build #3
Neither Hermes nor OpenClaw had this: Claude Code can **delegate work to other agents it spawns**. A subagent is a specialist — its own instructions, its own restricted toolset, its own separate context — that the main agent hands a task to and gets a result back from.

Why bother?

- **Focus.** A subagent defined as "you review text for clarity" does that job better than a general agent juggling everything.
- **Isolation.** The subagent's reading and exploring doesn't clutter the main conversation — only its final answer comes back.
- **Least privilege.** This is the safety payoff: you choose which tools each subagent gets. A reviewer that can only *read* files cannot damage anything — the Module 4.5 principle, applied per-agent instead of per-container.

## Anatomy of a subagent
One markdown file in `.claude/agents/`. Same routine as last lesson — ask the agent to write it, approve the permission prompt, then check what landed:

```text
create the file .claude/agents/reviewer.md, making the folder if it doesn't
exist, with exactly this content:

---
name: reviewer
description: Reviews notes and log entries for clarity and completeness. Use after writing or updating any note.
tools: Read, Glob, Grep
---

You are a careful reviewing assistant for a learning journal.

When given a file to review:
1. Read it fully.
2. Check: is each entry dated? Is the writing clear to a stranger?
3. Report at most three concrete improvements, quoting the line each applies to.

You never edit files. You only report.
```

Open the file and read it before moving on. The `tools:` line is a security boundary — if the agent paraphrased it or added tools that weren't in your list, the rest of this lesson proves nothing.

Read the frontmatter like a security badge:

- `name` / `description` — identity and **trigger**, same pattern as skills.
- `tools: Read, Glob, Grep` — the whole permission story. No Write, no Edit, no Bash. This subagent is **physically unable** to modify your files or run commands, no matter what it's asked or how it misbehaves.

The body is the subagent's system prompt — the job description it wakes up with.

## Run it
**Close your terminal completely and open a new one**, `cd` back to your practice folder, and run `claude`. Same reason as the skill in the last lesson: a newly created subagent doesn't reliably register until the terminal restarts, and `/exit` alone isn't always enough.

Confirm it registered by running `/agents` — `reviewer` should be listed. Then:

```text
use the reviewer agent to review my notes and log
```

Watch the delegation happen: the main agent hands off, the reviewer works in its own context, and a tidy report comes back.

![Main agent delegating to the reviewer subagent](/images/lessons/claude-subagents/delegation.png)

Now verify the cage. Ask directly:

```text
use the reviewer agent to fix the problems it found
```

It can't — the reviewer has no Write tool. The main agent (which does have Write) has to apply fixes itself, with your permission prompt still in the loop. **Restriction lives in the file; you can audit it by reading one line.**

You can also run `/agents` to see and manage every subagent available in this project.

<details>
<summary><strong>🛠️ Common issues — click to expand</strong></summary>

**`/agents` doesn't list `reviewer`**
Close the terminal entirely and open a new one, then `cd` back and relaunch `claude`. New agent files often don't register until a full terminal restart — `/exit` alone isn't enough. Same behaviour you saw with the skill last lesson.

**"No such agent" when you ask for the reviewer**
Check the path with `ls -la .claude/agents/`. It must be `.claude/agents/reviewer.md`, and the `name:` in the frontmatter must be `reviewer` — the agent is called by its `name:`, not by its filename.

**The agent rewrote the content instead of copying it**
Tell it: "replace the file with exactly the content I gave you, no changes." Pay particular attention to the `tools:` line — that's the one that matters here.

**The reviewer edits files anyway**
Re-read the `tools:` line in the file. If `Write`, `Edit`, or `Bash` appear there, remove them and restart the terminal. If the line is correct and it still edits, you're likely watching the *main* agent apply fixes after the reviewer reported — which is the expected behaviour, not a broken cage.

**You can't see the `.claude` folder**
It's hidden. macOS Finder: `Cmd+Shift+.` to toggle. Windows Explorer: View → Show → Hidden items. Or `ls -a` / `dir /a` in the terminal.

</details>

## Where this generalizes
One reviewer is a demo. The pattern — *split the job into specialists, give each the minimum tools* — is how real agent systems are built, and it's exactly what the capstone lab asks you to do next.

## Self-check
1. Does `use the reviewer agent...` visibly delegate (not just answer inline)?
2. Can you explain why the reviewer cannot edit files, and point to the exact line that guarantees it?
3. Did the review come back as a report while your main conversation stayed clean?

## Takeaway
A subagent is a job description with a badge: markdown body for the job, one `tools:` line for the badge. Least privilege went from a principle to a line you can read.
