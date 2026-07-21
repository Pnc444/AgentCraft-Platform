# Teach It Skills

*Lesson 2 of 4 · about 12 minutes · your assistant learns its first three tricks.*

Your gateway is healthy and your assistant has a job description. Today it learns how to actually do things, through **skills**.

## A skill is a recipe card, literally

In OpenClaw, a skill is not hidden code. It is a markdown file, always named `SKILL.md`, that teaches the assistant when and how to use a capability. You can open one in any text editor and read every word. Here is a complete, real one:

```markdown
---
name: research-brief
description: Turn raw source material into a short, cited summary.
---

When the user asks for a short research brief, gather the source material,
summarize only supported claims, and label unknowns explicitly.
```

That is the entire format: a name, a description, and instructions in plain language. Recognize it? That is Juno's core trick from Module 4, written down as a file.

## If two skills share a name: closest wins

Skills can live in a few places: your project's workspace, your home folder, and a set that ships with OpenClaw. When names collide, **the skill closest to your current project wins.** That one sentence is the entire rule you need for this course. The full lookup order lives in the docs for the day a real collision sends you there.

## Skills from strangers: read the recipe before cooking

OpenClaw has a public library of skills called ClawHub. A skill is instructions your assistant will follow, so a downloaded one deserves the same treatment as a recipe from a stranger: read it before you cook it. OpenClaw builds the caution in as a command:

```bash
openclaw skills install @owner/some-skill   # fetch it
openclaw skills verify @owner/some-skill    # the built-in checker inspects its trust record
```

Fetch, verify, read it once, then trust it. After those three steps the trust question is settled.

## Your three skills

This module uses exactly three:

- **research-brief**: Juno's trick. Summarize sources without losing the evidence trail.
- **channel-policy-check**: double-checks the door settings you will create in Lesson 3.
- **security-audit-helper**: turns Lesson 4's safety sweep into a tidy to-do list.

Notice what the second and third ones are: skills that check things for you. From its first week, your assistant helps keep itself trustworthy.

## Done means done

You are done when you can:

- say what file makes a skill exist
- state the collision rule in one sentence
- say what `verify` is for, in recipe-from-a-stranger terms

Three skills understood beats fifty installed. You have three.