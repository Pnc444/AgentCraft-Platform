from __future__ import annotations

from copy import deepcopy

from apps.courses.module4_missions import MODULE_4_MISSION_PACK


def _ai_tutor_prompt(lesson_title: str, deliverable: str, focus: str) -> str:
    return f"""You are the AgentCraft course tutor for the lesson "{lesson_title}".

Who you are teaching: an intelligent adult beginner with zero AI background. Assume they can think clearly. Never assume they know jargon — introduce every technical word with a plain-English anchor the first time it appears.

How to behave:
- Attempt-first: start by asking what they have already configured, drafted, or tried, then build on their own words.
- One idea per reply. End every reply with the single next step — never a menu of possible next steps.
- Keep the learner moving toward the deliverable: {deliverable}.
- Use the course's running example (Juno, the research helper from Module 4) when an example is needed.
- If the learner answers correctly and then asks whether they are really sure, confirm once, in one plain sentence, and move forward. Do not reopen a settled point — re-explaining a correct answer teaches doubt.
- If they are wrong or stuck, name what was right first, then give the one adjustment. Being stuck is information, never a verdict.
- Never dramatize risk. If something can go wrong, say exactly what would happen and how it is undone. Prefer "here is the command that checks this for you" over lists of things to worry about.
- If they already have a draft, review it against the lesson's finish line instead of replacing their work.
- When the learner can do what the lesson's "Done means done" list asks, say so explicitly and tell them it is safe to stop.

Focus for this lesson: {focus}
"""


def _artifact(
    path: str,
    summary: str,
    artifact_format: str,
    *,
    inspect_prompt: str | None = None,
    change_prompt: str | None = None,
) -> dict:
    artifact = {
        "path": path,
        "summary": summary,
        "format": artifact_format,
    }
    if inspect_prompt is not None:
        artifact["inspect_prompt"] = inspect_prompt
    if change_prompt is not None:
        artifact["change_prompt"] = change_prompt
    return artifact


MISSION_PACKS = [
    MODULE_4_MISSION_PACK,
    {
        "title": "Module 6: Build Your Assistant a Home (OpenClaw)",
        "slug": "module-6-openclaw",
        "description": (
            "Give the agent you designed a real home: set up OpenClaw the official way, "
            "teach it three skills, open one front door, and run the built-in safety sweep. "
            "Everything here is reversible, and one command always tells you the system is healthy."
        ),
        "difficulty": 2,
        "order": 8,
        "publish_rules": [
            "requires_non_placeholder_content",
            "requires_tutor_prompts",
            "requires_valid_quiz_banks",
            "requires_openclaw_artifacts",
            "requires_skill_templates",
            "requires_channel_templates",
            "requires_safety_checks",
        ],
        "lessons": [
            {
                "title": "Set Up the Home Base",
                "slug": "configuration",
                "lesson_type": "agent_lab",
                "estimated_minutes": 15,
                "content": """# Set Up the Home Base

*Lesson 1 of 4 · about 15 minutes · your Module 4 blueprint gets a real home today.*

In Module 4 you designed an agent on paper. This module gives it an actual home on your own computer, using a tool called **OpenClaw** — a program that runs a personal AI assistant on your own devices. Your machine, your rules, your files.

## First, the question worth answering before any command

*"What can go wrong here?"* — Honestly: very little, and nothing permanent. Every step below is undone by editing a text file or re-running a command. OpenClaw's defaults are private: nothing you do in this lesson is visible to anyone else, and nobody can talk to your assistant until you explicitly allow them (that is Lesson 3, and it is opt-in). You cannot wander into danger by typing the wrong thing on this page.

## Three commands, in order

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
openclaw gateway status
```

One line each:

1. **Install** puts the OpenClaw program on your computer (npm is a standard installer for software like this).
2. **Onboard** is a guided setup that asks you questions in the right order — model, workspace, and so on — instead of making you hand-edit settings on day one. The `--install-daemon` part sets up a *daemon*: a small background program that keeps your assistant awake even when you close the window.
3. **Status** asks the *Gateway* — the front desk of the whole building, the part that stays running — one question: "are you healthy?"

## The one health question

`openclaw gateway status` is worth a moment of appreciation. After **any** change you make in this module, this single command answers "is everything okay?" If it says healthy, it is healthy — the command does the checking so you don't have to wonder or re-verify by hand. One run, one answer, move on. It is the first of several places where OpenClaw carries the checking for you.

## Three files, three jobs

Only three files matter this week:

| File | Job | Plain name |
| --- | --- | --- |
| `~/.openclaw/openclaw.json` | How the system runs: which AI model, which tools, which doors | The control panel |
| `SOUL.md` | Who your assistant is: its role, rules, and boundaries | The job description |
| `<workspace>/skills/<name>/SKILL.md` | How to do one specific task well | A recipe card |

The one distinction that makes every later lesson easier: **the control panel changes how the system runs; the job description changes who the assistant is.** Wrong model? Control panel. Wrong personality? Job description. That routing rule answers most questions you will ever have about OpenClaw configuration.

The starter files below are yours to open and poke at. The control panel starts nearly empty on purpose — a model line and little else — because a small config that works beats a big config you can't reason about. You will add to it layer by layer across this module, proving health after each layer.

## Done means done

You are done with this lesson when you can:

- say what the Gateway is in one sentence
- route two problems correctly: "wrong model" → which file? "wrong personality" → which file?
- name the command that answers "is everything okay?"

That is the whole foundation. Lesson 2 adds recipe cards; nothing there requires re-reading this page.
""",
                "ai_tutor_prompt": _ai_tutor_prompt(
                    "Set Up the Home Base",
                    "a healthy OpenClaw gateway and a working grasp of the three files (control panel, job description, recipe card)",
                    "the official onboarding path (install, onboard, status), the gateway as the one health check they can always trust, and routing problems to the right file: openclaw.json for how it runs, SOUL.md for who it is.",
                ),
                "questions": [
                    {
                        "id": "openclaw-config-q1",
                        "prompt": "A colleague says: 'Skip onboarding — just open openclaw.json and start editing.' What is the gentle correction?",
                        "options": [
                            "Run openclaw onboard first — it sets up the gateway and workspace in the right order before any hand-editing",
                            "They are right — onboarding is just a convenience for people who are not comfortable editing files",
                            "openclaw.json cannot be edited by hand at all",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-config-q2",
                        "prompt": "You edit SOUL.md to change your assistant's personality, but it still uses the wrong AI model. Where does the model actually live?",
                        "options": [
                            "In SOUL.md — the job description covers everything about the assistant, including its model",
                            "In ~/.openclaw/openclaw.json — the control panel decides how the system runs, including the model",
                            "In a SKILL.md file — skills choose the model",
                        ],
                        "answer_index": 1,
                    },
                    {
                        "id": "openclaw-config-q3",
                        "prompt": "openclaw gateway status reports healthy. What exactly do you now know?",
                        "options": [
                            "Every skill is installed, verified, and ready for the assistant to use in every channel",
                            "All channels are connected and approved",
                            "The gateway is running and can talk to your model — the foundation is solid to build on",
                        ],
                        "answer_index": 2,
                    },
                    {
                        "id": "openclaw-config-q4",
                        "prompt": "Someone's assistant works fine but sounds completely wrong for its role. Which file is the first place to look?",
                        "options": [
                            "SOUL.md — the job description defines identity, tone, and rules",
                            "openclaw.json — personality lives in the runtime settings",
                            "The daemon logs — personality is set at install time",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-config-q5",
                        "prompt": "A student wants to add every channel and skill on day one, before running anything. What is the better path, and why?",
                        "options": [
                            "Add everything at once — seeing the full system working together is the fastest way to learn it",
                            "Channels must come first or the gateway will not start",
                            "Prove the gateway healthy first, then add one layer at a time, so you always know which layer changed",
                        ],
                        "answer_index": 2,
                    },
                ],
                "guided_blocks": [
                    {
                        "title": "The office, not the worker",
                        "predict_first": {
                            "question": "You are setting up an assistant on your own computer. Two things need configuring: who the assistant is, and the system that keeps it running. Which do you think lives in which file — and does mixing them up sound easy to do?",
                            "hint": "One file is a control panel. One is a job description. The whole trick is never confusing them.",
                        },
                        "body": "OpenClaw is the office; your assistant is the worker inside it. The Gateway is the front desk that keeps the office open. `openclaw.json` is the office's control panel, `SOUL.md` is the worker's job description, and each `SKILL.md` is a recipe card the worker can reach for. Every question in this module routes to one of those four things.",
                        "analogy": "Control panel, job description, recipe card, front desk. Four objects — that is the entire building.",
                    },
                    {
                        "title": "Three commands, one pass",
                        "body": "Install, onboard, status. The onboarding wizard asks its questions in the right order so you do not have to know the right order — answer them plainly and it builds a correct starting point. Then `openclaw gateway status` gives you your first 'healthy.' That word is the finish line for this block.",
                        "artifact_paths": ["lesson_artifacts/openclaw/config/onboard-checklist.md"],
                        "remember": "One run of each command is enough. 'Healthy' means healthy — the command checked so you don't have to.",
                        "try_this": [
                            "Open the onboarding checklist below and read it once, noticing that channels come last on purpose.",
                        ],
                    },
                    {
                        "title": "The routing rule",
                        "body": "Wrong model → control panel (`openclaw.json`). Wrong personality → job description (`SOUL.md`). Wrong way of doing one task → recipe card (`SKILL.md`). Practice that routing three times and this lesson's hardest idea is permanently yours.",
                        "artifact_paths": [
                            "lesson_artifacts/openclaw/config/openclaw.json.template.json5",
                            "lesson_artifacts/openclaw/config/SOUL.md",
                        ],
                        "try_this": [
                            "Open the control panel template and find the model line.",
                            "Open SOUL.md and find the Mission line.",
                            "Say which file you would touch if the assistant were rude, and which if it were slow to answer.",
                        ],
                        "checkpoint_after": True,
                    },
                    {
                        "title": "Small config, big calm",
                        "body": "The starter control panel is nearly empty — a model line and two safe defaults. That is deliberate. Each lesson in this module adds one layer, and after each layer you run one status check. Built this way, you always know exactly which change caused anything, because you only ever changed one thing.",
                        "remember": "One layer, one health check, then the next layer. The order is doing the worrying for you.",
                    },
                    {
                        "title": "If the two files blur together",
                        "body": "Everyone briefly mixes up the control panel and the job description — the names are new. If it happens, nothing is broken: ask 'is this about how the system runs, or who the assistant is?' and the answer routes you. That one question re-derives the whole distinction, so there is nothing to memorize.",
                        "remember": "How it runs → openclaw.json. Who it is → SOUL.md.",
                        "kind": "common_mistake",
                    },
                    {
                        "title": "Say it back, once",
                        "body": "A classmate asks, 'Why are there so many files?' Your answer: one file runs the system, one describes the worker, one teaches a task — and one command tells you the whole thing is healthy. If you can say that, this lesson is finished.",
                        "try_this": [
                            "Say it once, using 'control panel, job description, recipe card' if the names help.",
                        ],
                        "kind": "teach_it_back",
                    },
                ],
                "checkpoint_questions": [
                    {
                        "id": "openclaw-config-cp1",
                        "prompt": "You want to change who the assistant is. Which file?",
                        "options": [
                            "SOUL.md",
                            "openclaw.json",
                            "The daemon settings",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-config-cp2",
                        "prompt": "Which file is the runtime control panel?",
                        "options": [
                            "The workspace SOUL.md file",
                            "A skill's SKILL.md file",
                            "~/.openclaw/openclaw.json",
                        ],
                        "answer_index": 2,
                    },
                    {
                        "id": "openclaw-config-cp3",
                        "prompt": "Which command answers 'is everything okay?' after a change?",
                        "options": [
                            "openclaw skills update --all",
                            "openclaw gateway status",
                            "openclaw pairing approve",
                        ],
                        "answer_index": 1,
                    },
                ],
                "skill_templates": [],
                "channel_templates": [],
                "safety_checks": [
                    "Deny-by-default tool access",
                    "Human review for destructive operations",
                    "Run receipts persisted to disk",
                ],
                "permission_matrix": [],
                "evaluation_rubric": [],
                "evaluation_cases": [],
                "artifacts": [
                    _artifact(
                        "lesson_artifacts/openclaw/config/openclaw.json.template.json5",
                        "The nearly-empty starter control panel: a model line and two safe defaults, with plain-English comments.",
                        "text",
                        inspect_prompt="Find the model line, the DM session setting, and the sandbox mode. Say in plain English what each one controls.",
                        change_prompt="Replace the model placeholder with the provider and model you would try first. One edit is the whole exercise.",
                    ),
                    _artifact(
                        "lesson_artifacts/openclaw/config/SOUL.md",
                        "A starter job description (SOUL.md) for a study-buddy research assistant, modeled on Juno.",
                        "text",
                        inspect_prompt="Read the Mission and Rules sections. Would a stranger know what this assistant is for?",
                        change_prompt="Rewrite the Mission line in your own words, as if writing a job ad for a very reliable intern.",
                    ),
                    _artifact(
                        "lesson_artifacts/openclaw/config/onboard-checklist.md",
                        "The setup path as a finite checklist: install, onboard, status, then one layer at a time.",
                        "text",
                        inspect_prompt="Notice the order: health is proven before anything is added, and channels come last. Say why that ordering is kind to the builder.",
                        change_prompt="Mark which steps you could do today. Any unmarked step is simply the next thing, not a problem.",
                    ),
                ],
            },
            {
                "title": "Teach It Skills",
                "slug": "adding-skills",
                "lesson_type": "agent_lab",
                "estimated_minutes": 12,
                "content": """# Teach It Skills

*Lesson 2 of 4 · about 12 minutes · your assistant learns its first three tricks.*

Your gateway is healthy and your assistant has a job description. Today it learns how to actually do things — through **skills**.

## A skill is a recipe card, literally

In OpenClaw, a skill is not hidden code. It is a markdown file — always named `SKILL.md` — that teaches the assistant when and how to use a capability. You can open one in any text editor and read every word of it. Here is a complete, real one:

```markdown
---
name: research-brief
description: Turn raw source material into a short, cited summary.
---

When the user asks for a short research brief, gather the source material,
summarize only supported claims, and label unknowns explicitly.
```

That is the entire format: a name, a description, and instructions in plain language. Recognize it? That is Juno's core trick from Module 4, written down as a file. Your paper blueprint and this file are the same idea at two altitudes.

## If two skills share a name: closest wins

Skills can live in a few places (your project's workspace, your home folder, built-in ones that ship with OpenClaw). The rule when names collide is one sentence: **the skill closest to your current project wins.** That is the entire rule you need this module. The precise lookup order exists in the docs for the day you want it — you can build everything in this course without ever reading it.

## Skills from strangers: read the recipe before cooking

OpenClaw has a public library of skills called ClawHub. Because a skill is instructions your assistant will follow, a downloaded skill deserves the same treatment as a recipe from a stranger: read it before you cook it. OpenClaw builds the caution in as a command:

```bash
openclaw skills install @owner/some-skill   # fetch it
openclaw skills verify @owner/some-skill    # the built-in checker inspects its trust record
```

`verify` is this lesson's version of the status command — a machine that does the checking so you don't have to hold the worry. Fetch, verify, read it once, then trust it.

## Your three skills

This module uses exactly three — a deliberately small set:

- **research-brief** — Juno's trick: summarize sources without losing the evidence trail.
- **channel-policy-check** — double-checks the door settings you will create in Lesson 3.
- **security-audit-helper** — turns Lesson 4's safety sweep into a tidy to-do list.

Notice what the second and third ones are: *skills that check things for you.* Your assistant's first tricks include helping keep itself trustworthy.

## Done means done

You are done with this lesson when you can:

- say what file makes a skill exist (name and format)
- state the collision rule in one sentence
- say what `verify` is for, in the recipe-from-a-stranger terms

Three skills understood beats fifty installed. You have three.
""",
                "ai_tutor_prompt": _ai_tutor_prompt(
                    "Teach It Skills",
                    "three understood skills (research-brief, channel-policy-check, security-audit-helper) and a working grasp of SKILL.md, the closest-wins rule, and install-then-verify",
                    "the SKILL.md format as a readable recipe card, the one-sentence precedence rule (closest to the project wins), and verify as the built-in checker that carries the trust question for the learner.",
                ),
                "questions": [
                    {
                        "id": "openclaw-skills-q1",
                        "prompt": "You write skill instructions in a file called skills-info.txt inside workspace/skills/. OpenClaw ignores it. Why?",
                        "options": [
                            "The gateway must be restarted twice after adding text files",
                            "Skills are discovered by their exact filename — it must be SKILL.md",
                            "Text files need to be registered in openclaw.json first",
                        ],
                        "answer_index": 1,
                    },
                    {
                        "id": "openclaw-skills-q2",
                        "prompt": "The same skill name exists in your project workspace and in your home folder. Which one runs?",
                        "options": [
                            "The workspace one — closest to the current project wins",
                            "The home-folder one — personal skills always win",
                            "Whichever file was edited most recently",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-skills-q3",
                        "prompt": "You install a skill from ClawHub. What is the recommended next step before trusting it?",
                        "options": [
                            "Restart the gateway so the skill loads immediately",
                            "Delete any lines in it that look unfamiliar",
                            "Run openclaw skills verify, then read the skill once yourself",
                        ],
                        "answer_index": 2,
                    },
                    {
                        "id": "openclaw-skills-q4",
                        "prompt": "A teammate says: 'Third-party skills are just markdown, not code — nothing to review.' What are they missing?",
                        "options": [
                            "Markdown files can slow down the gateway noticeably",
                            "A skill is instructions your assistant will follow — text can steer real actions, so it deserves a read",
                            "Nothing — markdown cannot contain executable code, so the worst case is a badly written recipe",
                        ],
                        "answer_index": 1,
                    },
                    {
                        "id": "openclaw-skills-q5",
                        "prompt": "Why does this module teach exactly three skills instead of a catalog of fifty?",
                        "options": [
                            "OpenClaw workspaces support at most three skills, so the course simply uses that limit",
                            "The other skills on ClawHub cost money, and this course avoids paid material",
                            "Three understood skills build capability; fifty installed ones build clutter you cannot vouch for",
                        ],
                        "answer_index": 2,
                    },
                ],
                "guided_blocks": [
                    {
                        "title": "Open one and read it",
                        "predict_first": {
                            "question": "Before opening it: what do you expect the inside of a 'skill' to look like — code, settings, or something else?",
                            "hint": "You have already seen its shape in Module 4, on paper.",
                        },
                        "body": "It is a recipe card in plain language: a name, a description, and instructions. Open research-brief below and read all of it — it takes under a minute, and there is nothing in it you cannot understand today. That readability is the point: you can always know exactly what your assistant has been taught.",
                        "analogy": "A skill is a recipe card taped next to a machine: the machine is the capability, the card says when to use it and what good work looks like.",
                        "try_this": [
                            "Open research-brief's SKILL.md below. Read the whole thing once — it is shorter than this paragraph block.",
                        ],
                    },
                    {
                        "title": "The collision rule, whole",
                        "body": "If two skills share a name, the one closest to your current project wins. That sentence is the complete rule for this course. A longer priority list exists in the official docs — leaving it unread is not a gap in your understanding; it is the correct amount of detail for now.",
                        "remember": "Closest wins. The full list can stay in the docs until a real collision sends you there.",
                    },
                    {
                        "title": "Fetch, verify, read, trust",
                        "body": "For skills from ClawHub: install fetches it, `verify` runs the built-in checker on its trust record, and then you read it once — because it is short and plain, one read genuinely covers it. After those three steps the trust question is settled and does not need reopening.",
                        "try_this": [
                            "Say what problem `verify` solves, in one sentence, using the stranger's-recipe idea.",
                        ],
                        "checkpoint_after": True,
                    },
                    {
                        "title": "Your trio, and what it says",
                        "body": "research-brief does Juno's job. channel-policy-check and security-audit-helper do something lovelier: they check the system for you — one reviews door settings, one turns audit findings into a to-do list. From its very first week, your assistant participates in keeping itself trustworthy.",
                        "artifact_paths": [
                            "lesson_artifacts/openclaw/skills/research-brief/SKILL.md",
                            "lesson_artifacts/openclaw/skills/channel-policy-check/SKILL.md",
                            "lesson_artifacts/openclaw/skills/security-audit-helper/SKILL.md",
                        ],
                        "remember": "A small set you can vouch for beats a catalog you can't.",
                    },
                    {
                        "title": "If a skill doesn't load",
                        "body": "The usual cause is mundane: the filename is not exactly SKILL.md, or the file sits one folder too deep. Check those two things, in that order, and the mystery is nearly always solved. Nothing about a non-loading skill can harm the rest of the setup — it is simply not seen.",
                        "remember": "Exact filename, right folder. Two checks, in order, then done.",
                        "kind": "common_mistake",
                    },
                    {
                        "title": "Say it back, once",
                        "body": "A friend asks, 'So how does your assistant know how to do things?' Answer with the recipe-card story: readable file, closest wins, verify before trusting strangers. Three beats, once through, lesson finished.",
                        "try_this": [
                            "Say the three beats out loud or in your head. Once.",
                        ],
                        "kind": "teach_it_back",
                    },
                ],
                "checkpoint_questions": [
                    {
                        "id": "openclaw-skills-cp1",
                        "prompt": "What filename does OpenClaw discover as a skill?",
                        "options": [
                            "skill.py",
                            "SKILL.md",
                            "skills.json",
                        ],
                        "answer_index": 1,
                    },
                    {
                        "id": "openclaw-skills-cp2",
                        "prompt": "Two skills share a name. Which wins?",
                        "options": [
                            "The one closest to the current project",
                            "The one installed most recently",
                            "The one with more lines",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-skills-cp3",
                        "prompt": "Why read a downloaded skill before trusting it?",
                        "options": [
                            "Reading it makes the skill load faster",
                            "OpenClaw refuses to load any skill until it detects the file has been opened and read",
                            "It contains instructions your assistant will follow — a stranger's recipe deserves one read",
                        ],
                        "answer_index": 2,
                    },
                ],
                "skill_templates": [
                    "research-brief",
                    "channel-policy-check",
                    "security-audit-helper",
                ],
                "channel_templates": [],
                "safety_checks": [
                    "Verify ClawHub skills before trusting them",
                    "Use allowlists when only specific agents should see a skill",
                ],
                "permission_matrix": [],
                "evaluation_rubric": [],
                "evaluation_cases": [],
                "artifacts": [
                    _artifact(
                        "lesson_artifacts/openclaw/skills/research-brief/SKILL.md",
                        "Juno's core trick as a real skill file: turn sources into a short, honest, cited brief.",
                        "text",
                        inspect_prompt="Find the name, the description, and the sentence that keeps the summary honest about unknowns.",
                        change_prompt="Rewrite the description so a friend could predict what the skill does without reading the body.",
                    ),
                    _artifact(
                        "lesson_artifacts/openclaw/skills/channel-policy-check/SKILL.md",
                        "A skill that double-checks door settings before a channel goes live.",
                        "text",
                        inspect_prompt="Find the lines that compare a plan against policy. What mistake is this skill built to catch?",
                        change_prompt="Add one sentence reminding the agent to check that shared rooms only answer when called by name.",
                    ),
                    _artifact(
                        "lesson_artifacts/openclaw/skills/security-audit-helper/SKILL.md",
                        "A skill that turns safety-sweep findings into a short, ordered to-do list.",
                        "text",
                        inspect_prompt="Find how findings get grouped. Why does a grouped list feel more finishable than a raw dump?",
                        change_prompt="Add a sentence telling the agent to put 'open access plus tools enabled' at the top of any list it makes.",
                    ),
                ],
            },
            {
                "title": "Open the Front Door (Just a Crack)",
                "slug": "channels",
                "lesson_type": "interactive",
                "estimated_minutes": 12,
                "content": """# Open the Front Door (Just a Crack)

*Lesson 3 of 4 · about 12 minutes · your assistant gets a doorway to the outside world.*

So far your assistant only talks to you, on your machine. A **channel** connects it to a chat app you already use — WhatsApp, Telegram, Slack, Discord, and others — so you can message it from your phone like any other contact.

## Start with the reassurance, because it changes how you read everything else

**Every door starts locked.** Out of the box, a stranger who messages your assistant gets a short pairing code and then silence. The assistant will not talk to them, act for them, or reveal anything — until you, deliberately, approve that person. There is no accidental way to open your assistant to the world; the open setting requires two explicit, unmistakable steps that you would have to type on purpose. You can explore this whole lesson freely knowing that.

## Three door policies

- **Pairing** *(the default)* — a doorbell with a code. Unknown senders get a code; you approve the ones you choose with `openclaw pairing approve <channel> <code>`. Everyone else gets silence.
- **Allowlist** — a guest list. Only people you named in advance can get through at all.
- **Open** — the door propped open for anyone. Exists for genuine public-bot use cases; requires the two deliberate steps mentioned above; not for this course.

Pairing is the right answer for essentially everything you will build here. It is not the timid option — it is the correct one, and the docs agree.

## Two settings for shared spaces

If your assistant joins a group chat, two more ideas apply:

- **`requireMention`** — the assistant only answers when called by name (like a polite person in a group conversation, not someone who interjects on every message).
- **`per-channel-peer` sessions** — if several people message your assistant directly, each person gets their own separate conversation notebook. Nobody sees anyone else's context, and threads never blur together.

## The rollout, whole

1. Connect one channel — the app you actually use most.
2. Leave the policy on pairing (it already is).
3. Approve exactly one person: you.
4. Send yourself a message; watch it answer.

That is a complete, correct first rollout. Not a starter version of one — the actual thing, done well. Widening it later (a second person, a group room) is a repeat of step 3 with a new code, whenever you choose. There is no pressure to widen anything today, or ever.

## Done means done

You are done with this lesson when you can:

- explain pairing, allowlist, and open in doorbell terms
- say what `requireMention` prevents in a group room
- say who can reach a freshly connected channel before any approvals (answer: no one — and now you know why)
""",
                "ai_tutor_prompt": _ai_tutor_prompt(
                    "Open the Front Door (Just a Crack)",
                    "one connected channel on pairing, with the learner able to explain the three door policies and the two shared-room settings",
                    "the locked-by-default reassurance (pairing is the default; open requires two deliberate steps), the doorbell/guest-list/propped-door picture, requireMention for groups, and per-person conversation notebooks. Keep the tone unhurried: a one-channel, one-person rollout is complete, not preliminary.",
                ),
                "questions": [
                    {
                        "id": "openclaw-channel-q1",
                        "prompt": "A stranger messages your freshly connected assistant. With default settings, what happens?",
                        "options": [
                            "The assistant answers politely but declines anything that sounds risky or personal",
                            "They receive a pairing code and otherwise silence, until you approve them",
                            "The message is delivered to you for manual reply",
                        ],
                        "answer_index": 1,
                    },
                    {
                        "id": "openclaw-channel-q2",
                        "prompt": "How do you approve a sender who received a pairing code?",
                        "options": [
                            "openclaw pairing approve <channel> <code>",
                            "openclaw gateway restart --approve",
                            "Reply 'approve' to their message from your own account",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-channel-q3",
                        "prompt": "What does it take to actually make DMs public (the 'open' policy)?",
                        "options": [
                            "Approving your first sender quietly switches the whole channel to the open policy",
                            "One typo in the channel name is enough to open it",
                            "Two deliberate, explicit settings typed on purpose — it cannot happen by accident",
                        ],
                        "answer_index": 2,
                    },
                    {
                        "id": "openclaw-channel-q4",
                        "prompt": "Your assistant joins a team group chat. What does requireMention change?",
                        "options": [
                            "It answers only when called by name, instead of reacting to every message",
                            "It hides the assistant from members who have not paired",
                            "It disables message logging inside the group so the chatter stays private",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-channel-q5",
                        "prompt": "Three people DM the same assistant. What do per-channel-peer sessions guarantee?",
                        "options": [
                            "The assistant merges all three conversations into one shared thread it can search",
                            "Each person gets a separate conversation notebook — no context blurs between them",
                            "Only the first person to pair may send DMs",
                        ],
                        "answer_index": 1,
                    },
                ],
                "guided_blocks": [
                    {
                        "title": "The locked front door",
                        "predict_first": {
                            "question": "You connect your assistant to a messaging app. Before you approve anyone, what do you think a stranger who messages it experiences?",
                            "hint": "The designers assumed strangers would try. What is the safest default reply to someone unknown?",
                        },
                        "body": "A short code and silence. That is the whole experience of an unapproved stranger. Connecting a channel opens nothing by itself — approval is a separate, deliberate act that only you can perform. Read the rest of this lesson from inside that fact.",
                        "analogy": "Channel policy is deciding who gets a house key, who can ring the bell, and who the house simply does not answer.",
                    },
                    {
                        "title": "Doorbell, guest list, propped door",
                        "body": "Pairing is a doorbell with a code — you approve ring by ring. Allowlist is a guest list fixed in advance. Open is the door propped for anyone, exists for real public bots, and requires typing two unmistakable settings. For everything in this course, the doorbell is correct, and it is already switched on.",
                        "remember": "Pairing is the default and the right answer here. You never chose wrong by leaving it alone.",
                        "checkpoint_after": True,
                    },
                    {
                        "title": "Polite in groups, private in DMs",
                        "body": "requireMention makes the assistant a polite group member: silent until called by name. per-channel-peer gives every DM sender a private notebook, so conversations never bleed into each other. The template below has both written out — reading it is enough; applying it is copy-paste.",
                        "artifact_paths": ["lesson_artifacts/openclaw/channels/channel-policy.template.json5"],
                        "try_this": [
                            "Open the template and find the two settings. Say in one sentence each what they protect.",
                        ],
                    },
                    {
                        "title": "A complete first rollout is small",
                        "body": "One channel, pairing on, one approved person (you), one test message answered. That is not the training-wheels version of a rollout — it is a correct production pattern in miniature, and the checklist below fits on an index card. Wider access is always a later choice, never a debt.",
                        "artifact_paths": ["lesson_artifacts/openclaw/channels/rollout-checklist.md"],
                        "remember": "A good rollout is boring: small, tested, and easy to explain.",
                    },
                    {
                        "title": "If 'open' ever starts to sound convenient",
                        "body": "Someday a use case will make the open policy sound tempting and pairing sound like friction. When that day comes, the question to ask is: 'who exactly do I want reaching this assistant, and can I name them?' If you can name them, pairing or an allowlist already serves you better. If you truly cannot — a real public bot — that is a project to design deliberately, not a switch to flip.",
                        "remember": "If you can name the people, you don't need 'open'.",
                        "kind": "common_mistake",
                    },
                    {
                        "title": "Say it back, once",
                        "body": "Explain to an imaginary teammate why 'just let anyone DM the bot' isn't the move: the doorbell, the guest list, the propped door, and what a stranger experiences by default. Four beats, once through, and Lesson 3 is done.",
                        "try_this": [
                            "Include the phrase 'a code and silence' — it carries most of the story.",
                        ],
                        "kind": "teach_it_back",
                    },
                ],
                "checkpoint_questions": [
                    {
                        "id": "openclaw-channel-cp1",
                        "prompt": "What is the default DM policy on a new channel?",
                        "options": [
                            "Open",
                            "Pairing",
                            "No policy until you set one",
                        ],
                        "answer_index": 1,
                    },
                    {
                        "id": "openclaw-channel-cp2",
                        "prompt": "In a group room, what does requireMention do?",
                        "options": [
                            "The assistant only answers when called by name",
                            "The assistant leaves the room after each answer",
                            "The assistant messages members privately instead",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-channel-cp3",
                        "prompt": "When do per-channel-peer sessions matter most?",
                        "options": [
                            "When the gateway runs without a daemon",
                            "When one person messages the assistant from two different personal devices",
                            "When several people can DM the same assistant and each needs a private thread",
                        ],
                        "answer_index": 2,
                    },
                ],
                "skill_templates": [],
                "channel_templates": [
                    "slack-rollout",
                    "telegram-rollout",
                ],
                "safety_checks": [
                    "Keep DM policy on pairing unless a real reason exists",
                    "Enable mention gating in shared rooms",
                ],
                "permission_matrix": [],
                "evaluation_rubric": [],
                "evaluation_cases": [],
                "artifacts": [
                    _artifact(
                        "lesson_artifacts/openclaw/channels/channel-policy.template.json5",
                        "A door-policy template with pairing, mention gating, and private per-person sessions — commented in plain English.",
                        "text",
                        inspect_prompt="Find the DM policy, the DM scope, and the mention rule. Say what each protects, in doorbell terms.",
                        change_prompt="Pick the one channel you would connect first and say why pairing already suits it.",
                    ),
                    _artifact(
                        "lesson_artifacts/openclaw/channels/rollout-checklist.md",
                        "The complete first rollout on an index card: one channel, pairing, one person, one test message.",
                        "text",
                        inspect_prompt="Count the steps. Notice that the last one is a finish line, not an invitation to widen access.",
                        change_prompt="Fill in the channel name you would actually use. That single word makes the checklist yours.",
                    ),
                ],
            },
            {
                "title": "The Safety Sweep",
                "slug": "agent-safety",
                "lesson_type": "theory",
                "estimated_minutes": 12,
                "content": """# The Safety Sweep

*Lesson 4 of 4 · about 12 minutes · the module's closing move: one command that checks everything.*

Here is a secret about this module: **you have been doing safety work since Lesson 1.** A health check after every change. Recipe cards you can read. Doors locked by default. This final lesson doesn't introduce safety — it hands you the tool that confirms it, and names the thinking behind what you already built.

## Safety is a shape, not a mood

OpenClaw's security guidance orders protections like the layers of a house:

1. **Who can talk to it** — the doors. Pairing, allowlists. *(You built this in Lesson 3.)*
2. **Where it can act** — the rooms. Which tools are granted, what stays off-limits. *(You touched this in Lessons 1–2.)*
3. **How it behaves** — the person inside. The model and its instructions, last.

The order matters and is quietly liberating: **the locks do not depend on anyone's behavior.** A well-worded job description is good to have, but it is the doors and rooms — settings, not promises — that decide what can actually happen. You never have to trust charm, and you never have to supervise; the settings hold whether or not anyone is watching.

## The auditor: one command instead of a worry list

```bash
openclaw security audit
```

This is the centerpiece of the lesson. The audit walks the whole building — door policies, tool grants, network posture, plugin trust, a dozen other things — against the official checklist, and reports back. You do not need to know the full list of what it checks; *not needing to know is the feature.* The checklist lives in the tool, maintained by the people who built the system, so it never has to live in your head.

The rhythm that makes it work:

> **Change something → run the audit → fix what it flags → done.**

When the audit passes, you are entitled to believe it. That is what it is for. Running it a second time on an unchanged system tells you nothing new — the input hasn't changed, so the answer can't. Once per change is the whole discipline; the auditor remembers everything so you can put it down completely between changes.

Two variants for later, no action needed now: `--deep` looks harder (worth it before sharing access more widely) and `--fix` applies safe corrections itself.

## Two boundaries worth naming once

- **Guest rooms don't get the master key.** The setting `sandbox.mode: "non-main"` keeps any session that isn't your own main one inside a limited sandbox, away from full access to your computer.
- **One household per home.** OpenClaw is a *personal* assistant: one gateway assumes one trusted operator — you. The day two people who don't fully trust each other want assistants, the answer is two separate gateways, not shared keys. (No action needed; it's just the boundary, named.)

## Done means done — lesson and module

You are done when you can name: one control for *who can talk* (pairing), one for *where it can act* (sandbox), and the command that checks the whole building (the audit).

And with that, **Module 6 is complete.** Your assistant has a home, three skills, one carefully opened door, and a standing auditor. Everything here waits patiently in config files — nothing degrades, nothing needs re-checking overnight. Module 8 is where you decide, with evidence, to trust it with real work.
""",
                "ai_tutor_prompt": _ai_tutor_prompt(
                    "The Safety Sweep",
                    "a passed security audit and the three-layer picture: doors (identity), rooms (scope), person inside (model) — in that order",
                    "reframing safety as settings rather than vigilance: the audit is an external checker that holds the checklist so the learner doesn't have to; the rhythm is change → audit → fix → done, and re-running on an unchanged system yields nothing new. The locks work without anyone watching.",
                ),
                "questions": [
                    {
                        "id": "openclaw-safety-q1",
                        "prompt": "A teammate wants to rely on a strongly-worded system prompt for safety. You want the doors and rooms set first. Who has the official ordering right?",
                        "options": [
                            "The teammate — a well-written prompt reaches the model directly, making hard controls redundant",
                            "You — settings (identity, scope) come first because they hold regardless of how the model behaves",
                            "Neither — the ordering between prompts and controls doesn't matter",
                        ],
                        "answer_index": 1,
                    },
                    {
                        "id": "openclaw-safety-q2",
                        "prompt": "The audit flags: 'DM policy open + tools enabled.' What does the layered order say to fix first?",
                        "options": [
                            "The door — lock down who can talk before tuning anything else",
                            "The model — add stronger instructions about strangers",
                            "The tools — remove them all, then revisit the door later",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-safety-q3",
                        "prompt": "You ran the audit after your last change and it passed. Nothing has changed since. What does running it again tonight accomplish?",
                        "options": [
                            "It catches issues that can appear spontaneously while the system sits overnight",
                            "It refreshes the gateway's security certificates",
                            "Nothing new — same system in, same answer out; once per change is the whole discipline",
                        ],
                        "answer_index": 2,
                    },
                    {
                        "id": "openclaw-safety-q4",
                        "prompt": "You want sessions other than your own kept away from full access to your computer. Which setting is built for exactly that?",
                        "options": [
                            "channels.dmPolicy: 'allowlist'",
                            "agents.defaults.sandbox.mode: 'non-main'",
                            "gateway.bind: 'public'",
                        ],
                        "answer_index": 1,
                    },
                    {
                        "id": "openclaw-safety-q5",
                        "prompt": "Two housemates who don't fully trust each other both want assistants. What does the one-household rule recommend?",
                        "options": [
                            "Two separate gateways — separate homes, separate keys",
                            "One shared gateway with a strict SOUL.md",
                            "One gateway, taking turns by day of the week",
                        ],
                        "answer_index": 0,
                    },
                ],
                "guided_blocks": [
                    {
                        "title": "You've been doing this all module",
                        "predict_first": {
                            "question": "Look back at Lessons 1–3 for a moment: the health check, the verify command, the locked doors. What were all of those, really?",
                            "hint": "Each one was a machine holding a checklist so you didn't have to.",
                        },
                        "body": "They were safety work — done calmly, one layer at a time, without a single alarming paragraph. This lesson only adds the top layer: an auditor that checks all of it at once. You are not starting safety today; you are finishing it.",
                        "analogy": "Doors, rooms, person inside — identity, scope, model. Set in that order, checked by one auditor.",
                    },
                    {
                        "title": "Locks beat promises — and that's a relief",
                        "body": "The layered order means the important protections are settings, not behavior. A door on pairing holds whether the model has a good day or a bad one, whether you are watching or asleep. Nothing in this system asks for your vigilance; it asks for one command after each change.",
                        "remember": "A prompt is guidance. A setting is enforcement. Enforcement doesn't need supervision.",
                    },
                    {
                        "title": "The audit rhythm",
                        "body": "Change something → `openclaw security audit` → fix what it flags → done. The runbook below writes the rhythm out. The audit holds the full checklist internally, which is precisely why you don't have to — and why a pass is a real answer, not a provisional one. An unchanged system re-audited gives the same result; the discipline is once per change, then put it down.",
                        "artifact_paths": [
                            "lesson_artifacts/openclaw/safety/hardened-openclaw.json5",
                            "lesson_artifacts/openclaw/safety/security-audit-runbook.md",
                        ],
                        "try_this": [
                            "Read the runbook once. Notice it is a rhythm, not a worry list.",
                            "In the hardened config, find the sandbox line and say what it keeps away from the master key.",
                        ],
                        "checkpoint_after": True,
                    },
                    {
                        "title": "One household, named once",
                        "body": "OpenClaw assumes one trusted operator per gateway — it is a personal assistant, like a personal home. If mutually untrusting people ever need assistants, they get separate gateways. You are the only operator here, so this boundary asks nothing of you today; it is named so the model of the system in your head is complete.",
                        "remember": "One home, one household. More households, more homes.",
                    },
                    {
                        "title": "If the audit flags something",
                        "body": "A flag is the system working, not failing — the auditor caught what it exists to catch, before anything happened. Findings arrive ordered; fix the top one, re-run, watch the list shrink. A first audit with a few flags is the normal experience, not a bad sign, and the security-audit-helper skill from Lesson 2 will happily turn the output into a to-do list for you.",
                        "remember": "A flag means the check worked. Fix, re-run, shrink the list, done.",
                        "kind": "common_mistake",
                    },
                    {
                        "title": "Say it back, and close the module",
                        "body": "Four beats: who can talk (doors), where it can act (rooms), how it behaves (person inside), and the auditor that checks the building. Say them once. Then let Module 6 be finished — it is, and the config files will hold everything exactly as you left it.",
                        "try_this": [
                            "One pass through the four beats. Then close the page — the module is complete.",
                        ],
                        "kind": "teach_it_back",
                    },
                ],
                "checkpoint_questions": [
                    {
                        "id": "openclaw-safety-cp1",
                        "prompt": "What trust model does an OpenClaw gateway assume?",
                        "options": [
                            "Many mutually untrusting users per gateway",
                            "One trusted operator per gateway",
                            "Trust is negotiated per message",
                        ],
                        "answer_index": 1,
                    },
                    {
                        "id": "openclaw-safety-cp2",
                        "prompt": "What comes before model behavior in the layered safety order?",
                        "options": [
                            "Who can talk, and where it can act",
                            "The assistant's tone of voice",
                            "The size of the model",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-safety-cp3",
                        "prompt": "What is the audit rhythm from this lesson?",
                        "options": [
                            "Audit hourly regardless of changes",
                            "Audit once at install time, never again",
                            "Change something → audit → fix flags → done",
                        ],
                        "answer_index": 2,
                    },
                ],
                "skill_templates": [],
                "channel_templates": [],
                "safety_checks": [
                    "Run openclaw security audit after config changes",
                    "Use sandboxing for non-main or shared sessions",
                    "Keep high-risk tools denied by default in untrusted contexts",
                    "Treat third-party skills and plugins as untrusted code",
                ],
                "permission_matrix": [
                    {"action": "read_repo", "level": "allow", "reason": "needed for lesson and artifact work"},
                    {"action": "write_artifact", "level": "allow", "reason": "course-owned learning artifacts"},
                    {"action": "gateway", "level": "review", "reason": "persistent control-plane changes deserve a deliberate yes"},
                    {"action": "cron", "level": "review", "reason": "scheduled workflows persist beyond one chat turn"},
                    {"action": "public_exposure_change", "level": "deny", "reason": "outside Module 6 lesson scope"},
                ],
                "evaluation_rubric": [],
                "evaluation_cases": [],
                "artifacts": [
                    _artifact(
                        "lesson_artifacts/openclaw/safety/hardened-openclaw.json5",
                        "A hardened baseline config — every lock from the module in one file, commented in plain English.",
                        "text",
                        inspect_prompt="Find the gateway bind, the auth mode, the exec setting, and the DM scope. Say what each one locks, in house terms.",
                        change_prompt="Pick the one line you find most reassuring and say why it holds even when nobody is watching.",
                    ),
                    _artifact(
                        "lesson_artifacts/openclaw/safety/security-audit-runbook.md",
                        "The audit rhythm on one page: change, audit, fix, done — with what a flag means and doesn't mean.",
                        "text",
                        inspect_prompt="Find the sentence about re-running the audit on an unchanged system. Say why that sentence is a gift.",
                        change_prompt="Read the runbook as a spoken checklist once. If it fits in one breath per line, it is doing its job.",
                    ),
                ],
            },
        ],
    },
    {
        "title": "Module 8: Capstone — Decide to Trust It",
        "slug": "module-8-capstone-safety-evaluation",
        "description": (
            "The finishing module: let your assistant run one small job on its own, put guardrails and "
            "permissions around it, gather four kinds of evidence, and make a clear, final release decision. "
            "This module ends with a decision, not a feeling."
        ),
        "difficulty": 3,
        "order": 10,
        "publish_rules": [
            "requires_non_placeholder_content",
            "requires_tutor_prompts",
            "requires_valid_quiz_banks",
            "requires_capstone_artifacts",
            "requires_permission_matrix",
            "requires_evaluation_rubric",
            "requires_evaluation_cases",
        ],
        "lessons": [
            {
                "title": "Work That Runs While You're Away",
                "slug": "automation-examples",
                "lesson_type": "theory",
                "estimated_minutes": 12,
                "content": """# Work That Runs While You're Away

*Lesson 1 of 4 · about 12 minutes · the capstone begins: your assistant starts working unattended.*

Everything before this module happened while you watched. **Automation** is work your assistant does when you are not there — a job that runs on a schedule, or when an event arrives, without you pressing anything.

The question this whole capstone answers: *how do you step away calmly?* Not by hoping. By structure. Every trustworthy automation answers four questions, and they will look familiar — they are Module 4's blueprint boxes, grown up:

## The four questions of any automation

1. **Trigger** — what starts it? A schedule ("every Monday at 9"), an event ("a message arrives"), or a signal from another system (called a *webhook* — one system ringing another's doorbell).
2. **Steps** — what bounded work does it do? A list you could draw, not "the AI handles it."
3. **Review point** — where does a human approve before anything irreversible? (The support helper from Module 4 drafted; a person sent. Same pattern, formalized.)
4. **Receipt** — what written record proves the run happened and shows what it did?

## The receipt is the star

Sit with the fourth one, because it is the piece that makes stepping away *actually* calm rather than nervously hopeful:

**You do not verify an automation by watching it. You verify it by reading the receipt afterward.** One receipt, one read, and you know — not believe, know — what happened. A missing receipt is the one thing that should stop a design cold, because work that leaves no record can never be checked, only worried about. With receipts, "did it run okay?" stops being a feeling to manage; it becomes a fact you look up.

## Three worked examples

**The Monday audit.** Trigger: schedule, Mondays 9:00. Steps: run `openclaw security audit`, collect findings. Review: findings go to you as a checklist — you decide what changes. Receipt: the audit report, saved with a date.
*Your Module 6 safety sweep — now it happens without you remembering it. The remembering was the machine's job all along.*

**The doorbell-to-draft.** Trigger: a webhook fires when a form on your site is submitted. Steps: your assistant drafts a reply using research-brief. Review: the draft waits for your approval — nothing sends itself. Receipt: draft plus decision, logged.

**The quality gate.** Trigger: a document lands in a folder. Steps: the assistant checks it against a rubric. Review: passes move on; failures return with notes for a human. Receipt: the scorecard, saved.

Notice: in all three, the irreversible step belongs to a person, and every run leaves paper.

## Done means done

You are done with this lesson when you can:

- name the four questions from memory or nearly so
- say in one sentence why the receipt replaces watching
- sketch one automation of your own as four short answers (the brief template below holds them)

Lessons 2 and 3 add the guardrails and permissions around this job; Lesson 4 is where you decide to ship it.
""",
                "ai_tutor_prompt": _ai_tutor_prompt(
                    "Work That Runs While You're Away",
                    "a four-line automation brief: trigger, steps, review point, receipt",
                    "the four questions of trustworthy automation, with the receipt as the emotional center: verification by reading a record afterward, not by watching. Connect each question back to the Module 4 blueprint so this feels like growth, not new ground.",
                ),
                "questions": [
                    {
                        "id": "capstone-automation-q1",
                        "prompt": "What lets you verify an unattended run without having watched it?",
                        "options": [
                            "The receipt — a written record you read afterward",
                            "The trigger — knowing when it started",
                            "The model — trusting it was a good one",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-automation-q2",
                        "prompt": "Which example is a schedule-triggered automation?",
                        "options": [
                            "The doorbell-to-draft, fired by a form submission",
                            "The Monday audit, fired at 9:00 every Monday",
                            "A reply the assistant writes while you watch",
                        ],
                        "answer_index": 1,
                    },
                    {
                        "id": "capstone-automation-q3",
                        "prompt": "In the doorbell-to-draft example, why does the draft wait for your approval instead of sending itself?",
                        "options": [
                            "Webhooks can start jobs but cannot technically complete a send on their own",
                            "Drafting is too slow to automate end to end",
                            "Sending is the irreversible step, so it sits with a person — the review point",
                        ],
                        "answer_index": 2,
                    },
                    {
                        "id": "capstone-automation-q4",
                        "prompt": "A design says: 'Trigger: nightly. Steps: the AI handles cleanup.' What fails the four questions?",
                        "options": [
                            "The trigger — cleanup work needs to run far more often than once per night",
                            "The steps are unbounded — 'the AI handles it' is not a list you could draw",
                            "Nightly jobs cannot produce receipts",
                        ],
                        "answer_index": 1,
                    },
                    {
                        "id": "capstone-automation-q5",
                        "prompt": "What is a webhook, in this lesson's terms?",
                        "options": [
                            "A saved log of a completed run",
                            "A rule about which tools an automation may use",
                            "One system ringing another system's doorbell to start a job",
                        ],
                        "answer_index": 2,
                    },
                ],
                "guided_blocks": [
                    {
                        "title": "Stepping away, calmly",
                        "predict_first": {
                            "question": "You let a capable person house-sit for a weekend. What arrangements would let you genuinely not think about the house while away?",
                            "hint": "Clear instructions, agreed limits, a note about when to call you — and finding out afterward what happened.",
                        },
                        "body": "Whatever you just listed maps onto the four questions: instructions are the steps, limits and 'call me if' are the review point, and finding out afterward is the receipt. Trustworthy automation is a well-arranged house-sit. The calm comes from the arrangement, not from hope.",
                        "analogy": "An automation is an assembly line with a quality-control station and a logbook — not a self-driving mystery box.",
                    },
                    {
                        "title": "Four questions, and where you've seen them",
                        "body": "Trigger, steps, review, receipt. These are Module 4's goal/tools/check/stop wearing work clothes. The brief template below holds one line for each — four honest lines, same finish-line standard as the blueprint was. When the four lines are written, the brief is done.",
                        "artifact_paths": [
                            "lesson_artifacts/capstone/automation-brief.template.md",
                            "lesson_artifacts/capstone/task-flow-sequence.md",
                        ],
                        "try_this": [
                            "Open the brief template and read the filled-in Monday-audit example.",
                            "Sketch your own automation as four lines. Rough counts as complete.",
                        ],
                        "checkpoint_after": True,
                    },
                    {
                        "title": "The receipt, once more with feeling",
                        "body": "The receipt converts 'did it work?' from an open question into a lookup. That difference is the whole reason automation can be restful instead of low-grade worrying. Design rule, worth keeping forever: no receipt, no automation — not as a punishment, but because you deserve to be able to find out rather than wonder.",
                        "remember": "A receipt turns wondering into looking something up.",
                    },
                    {
                        "title": "The mystery-box trap",
                        "body": "The tempting shortcut is 'the model will just handle it' — it feels generous to the AI and saves design effort today. But an unbounded step can't be reviewed, and an unreviewed step can't be trusted, so the design debt lands on future-you as vague unease. Mechanical enough that another person could follow the steps — that is the bar, and it is kind to everyone.",
                        "remember": "If you cannot draw the steps, the design is not done yet — and that is fixable in five minutes.",
                        "kind": "common_mistake",
                    },
                    {
                        "title": "Say it back, once",
                        "body": "Explain the Monday audit to an imaginary friend in four short sentences — what starts it, what it does, where you decide, what it leaves behind. Once through, and this lesson is finished.",
                        "try_this": [
                            "Use the words trigger, steps, review, receipt as your four sentence-starters.",
                        ],
                        "kind": "teach_it_back",
                    },
                ],
                "checkpoint_questions": [
                    {
                        "id": "capstone-automation-cp1",
                        "prompt": "What are the four questions of a trustworthy automation?",
                        "options": [
                            "Trigger, steps, review point, receipt",
                            "Model, prompt, speed, cost",
                            "Install, onboard, status, audit",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-automation-cp2",
                        "prompt": "Which piece proves a run happened after the fact?",
                        "options": [
                            "The trigger",
                            "The receipt",
                            "The review point",
                        ],
                        "answer_index": 1,
                    },
                    {
                        "id": "capstone-automation-cp3",
                        "prompt": "Where does the irreversible step belong in all three worked examples?",
                        "options": [
                            "With the fastest available tool",
                            "Wherever the model decides in the moment",
                            "With a person, at the review point",
                        ],
                        "answer_index": 2,
                    },
                ],
                "skill_templates": [],
                "channel_templates": [],
                "safety_checks": [
                    "Every workflow names a review boundary",
                ],
                "permission_matrix": [],
                "evaluation_rubric": [],
                "evaluation_cases": [],
                "artifacts": [
                    _artifact(
                        "lesson_artifacts/capstone/automation-brief.template.md",
                        "The four-question automation brief, with the Monday-audit example filled in and an empty copy for yours.",
                        "text",
                        inspect_prompt="Read the filled example. Notice every answer is one line — that is the target amount of detail.",
                        change_prompt="Fill the empty brief with your own automation. Four honest lines and it is finished.",
                    ),
                    _artifact(
                        "lesson_artifacts/capstone/task-flow-sequence.md",
                        "One automation drawn as a numbered sequence, showing exactly where the human and the receipt sit.",
                        "text",
                        inspect_prompt="Find the step where a human decides, and the step where the record gets written.",
                        change_prompt="Renumber the sequence for your own automation from the brief. Same beats, your job.",
                    ),
                ],
            },
            {
                "title": "Guardrails: Values and Seatbelts",
                "slug": "guardrails",
                "lesson_type": "theory",
                "estimated_minutes": 10,
                "content": """# Guardrails: Values and Seatbelts

*Lesson 2 of 4 · about 10 minutes · what your assistant tries to be, and what the system guarantees anyway.*

Your automation from Lesson 1 has a shape. This lesson wraps it in guardrails — and the key is that guardrails come in two layers that people constantly blur. You are about to un-blur them permanently.

## Layer one: values (what the assistant tries to be)

AI research names three qualities a good assistant aims for — **helpful, truthful, harmless**:

- **Helpful** — it moves your task forward instead of dead-ending.
- **Truthful** — it separates what it knows from what it guesses, and says which is which.
- **Harmless** — it declines to cause damage, even when asked carelessly.

These are real and they matter. They are also *aims* — the driver's good intentions.

## Layer two: seatbelts (what the system guarantees)

A careful driver still wears a seatbelt, because the seatbelt works on the bad day. Your Module 6 build is already full of seatbelts: pairing on the doors, sandboxing on the rooms, tools granted one at a time, receipts on every run. **Settings, not intentions — they hold no matter what kind of day the model is having.**

The two layers are not rivals; they are a pairing. Values make the assistant good to work with. Seatbelts make the outcome safe even if values slip. You want both, and — quietly — you already have both.

## The one rule this lesson installs

> **Every safety claim must point at something you could show someone.**

"Our assistant is safe" — points at nothing; it is a mood.
"Strangers can't reach it (pairing), it can't touch files outside its workspace (sandbox), and every run leaves a receipt" — points at three settings you could open on screen in ten seconds.

The guardrail matrix below runs this rule across your whole capstone: each row takes one value and names the concrete seatbelt that backs it. Filling it is satisfying in a specific way — when you finish, "is my project safe?" has stopped being a feeling and become a short list of checkable facts. Feelings need managing; lists just need reading.

## Done means done

You are done with this lesson when you can:

- name the three values and give a one-line meaning for each
- give one seatbelt from your own build and say which value it backs
- state the one rule (claims point at showable things)
""",
                "ai_tutor_prompt": _ai_tutor_prompt(
                    "Guardrails: Values and Seatbelts",
                    "a filled guardrail matrix where every safety claim points at a concrete, showable control",
                    "the two layers — values (helpful, truthful, harmless: what the assistant aims for) and seatbelts (settings that hold regardless) — and the one rule: every safety claim points at something you could show someone. Filling the matrix converts 'is it safe?' from a feeling into a checkable list.",
                ),
                "questions": [
                    {
                        "id": "capstone-guardrails-q1",
                        "prompt": "Which trio names the value layer — what a good assistant aims to be?",
                        "options": [
                            "Fast, cheap, autonomous",
                            "Helpful, truthful, harmless",
                            "Paired, sandboxed, logged",
                        ],
                        "answer_index": 1,
                    },
                    {
                        "id": "capstone-guardrails-q2",
                        "prompt": "Why do well-instructed assistants still need seatbelt-layer controls?",
                        "options": [
                            "Settings hold on the bad day, independent of how the model behaves",
                            "Instructions expire after thirty days and must be reinforced",
                            "Controls make the assistant measurably faster",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-guardrails-q3",
                        "prompt": "Which of these is a real seatbelt rather than a mood?",
                        "options": [
                            "A paragraph promising the assistant is careful",
                            "A team belief that the model is trustworthy",
                            "dmPolicy pairing plus a tool deny list for untrusted rooms",
                        ],
                        "answer_index": 2,
                    },
                    {
                        "id": "capstone-guardrails-q4",
                        "prompt": "The one rule of this lesson: every safety claim must…",
                        "options": [
                            "…point at something you could show someone",
                            "…be approved by two reviewers",
                            "…appear in the assistant's job description",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-guardrails-q5",
                        "prompt": "'Truthful' is backed by which kind of concrete support in a strong capstone?",
                        "options": [
                            "A larger, more knowledgeable model that simply makes fewer factual mistakes",
                            "A check that claims trace to sources and unknowns are labeled as unknowns",
                            "A rule that answers stay under one paragraph",
                        ],
                        "answer_index": 1,
                    },
                ],
                "guided_blocks": [
                    {
                        "title": "Two layers, un-blurred",
                        "predict_first": {
                            "question": "A careful driver and a seatbelt both make a car safer. What is the difference in *how* each one works — and which would you rather not be without on the worst day?",
                            "hint": "One works by intention. One works by mechanism, regardless of intention.",
                        },
                        "body": "Values work like the careful driver: real, valuable, and intention-based. Seatbelts work by mechanism: pairing, sandboxing, deny lists, receipts — they hold whether or not the day is going well. Your build already wears both. This lesson just teaches you to say which is which.",
                        "analogy": "Helpful-truthful-harmless is the driver's character. The Module 6 settings are the seatbelt, brakes, and doors.",
                    },
                    {
                        "title": "Point at it",
                        "body": "Practice the rule on one row of the matrix below: take 'harmless,' and point at the seatbelt backing it in your build — the deny-by-default tools, say, or the sandbox. If you can put your finger on a setting, the claim is real. Do one row now; the rest are the same motion repeated.",
                        "artifact_paths": ["lesson_artifacts/capstone/guardrail-matrix.md"],
                        "try_this": [
                            "Open the matrix and read the filled example row.",
                            "Fill one row yourself: a value, its seatbelt, and where you'd point to show it.",
                        ],
                        "checkpoint_after": True,
                    },
                    {
                        "title": "From feeling to list",
                        "body": "A finished matrix does something quietly wonderful: it retires the question 'is my project safe?' as a feeling and re-issues it as a short list of facts, each with a pointer. Lists can be read, finished, and set down. That is the entire emotional payoff of this lesson, and it is a real, durable one.",
                        "remember": "Feelings need managing. Lists just need reading.",
                    },
                    {
                        "title": "The good-model trap",
                        "body": "The tempting belief is that a sufficiently good model retires the seatbelt layer. It doesn't — not because models are bad, but because 'good' is a behavior and behavior varies, while a lock is a mechanism and mechanisms don't. Strong models plus strong settings is not distrust; it is how every serious system is built, including the ones you already rely on daily.",
                        "remember": "Better models are welcome. The seatbelts stay on regardless — that's what makes them seatbelts.",
                        "kind": "common_mistake",
                    },
                    {
                        "title": "Say it back, once",
                        "body": "Two sentences: one naming a value your assistant aims for, one naming the seatbelt that backs it and where it lives. If both sentences point at real things, this lesson is finished.",
                        "try_this": [
                            "Two sentences, one pass. Pointing at pairing or the sandbox is a perfect answer.",
                        ],
                        "kind": "teach_it_back",
                    },
                ],
                "checkpoint_questions": [
                    {
                        "id": "capstone-guardrails-cp1",
                        "prompt": "Which layer holds even on the model's bad day?",
                        "options": [
                            "The seatbelt layer — settings and mechanisms",
                            "The value layer — helpful, truthful, harmless",
                            "Neither; both depend on the model's behavior",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-guardrails-cp2",
                        "prompt": "Why is 'dmPolicy: pairing' stronger than a written promise to be careful?",
                        "options": [
                            "It is written in a settings file, which the assistant reads more carefully",
                            "It mechanically changes who can reach the assistant, regardless of behavior",
                            "It improves the assistant's tone",
                        ],
                        "answer_index": 1,
                    },
                    {
                        "id": "capstone-guardrails-cp3",
                        "prompt": "What must every safety claim in the capstone do?",
                        "options": [
                            "Cite a published research paper",
                            "Use the words helpful, truthful, or harmless",
                            "Point at something concrete you could show someone",
                        ],
                        "answer_index": 2,
                    },
                ],
                "skill_templates": [],
                "channel_templates": [],
                "safety_checks": [
                    "Map value-level goals to runtime controls",
                    "Reject safety claims that point at nothing showable",
                    "Keep an audit path for review decisions",
                ],
                "permission_matrix": [],
                "evaluation_rubric": [
                    {"criterion": "helpfulness", "weight": 2, "description": "The workflow still moves the user toward a useful result."},
                    {"criterion": "truthfulness", "weight": 3, "description": "Claims are grounded, and unknowns are labeled clearly."},
                    {"criterion": "harmlessness", "weight": 3, "description": "Risky actions are denied, sandboxed, or escalated."},
                    {"criterion": "operational_control", "weight": 2, "description": "The concrete control backing each guardrail is named explicitly."},
                ],
                "evaluation_cases": [],
                "artifacts": [
                    _artifact(
                        "lesson_artifacts/capstone/guardrail-matrix.md",
                        "The values-to-seatbelts matrix: each row pairs one aim with the concrete control that backs it, plus where to point.",
                        "text",
                        inspect_prompt="Read the filled example row. Notice the third column is always something you could open on a screen.",
                        change_prompt="Fill one row for your own build. A value, a setting, a pointer — one row is a complete exercise.",
                    )
                ],
            },
            {
                "title": "Permissions: Three Kinds of Doors",
                "slug": "permissions",
                "lesson_type": "theory",
                "estimated_minutes": 10,
                "content": """# Permissions: Three Kinds of Doors

*Lesson 3 of 4 · about 10 minutes · every decision made once, calmly, in advance.*

Guardrails said what your system guarantees. Permissions decide, action by action, what your assistant may do — and the deep comfort of a permission table is *when* the deciding happens: **once, now, in writing — never again in the moment.**

## Three kinds of doors

Every action your assistant might take gets one of three labels:

- **Allow** — a green door. Routine and reversible; it may pass freely. *Reading files in its workspace, drafting text.*
- **Review** — a yellow door. It may knock; a person opens. For actions that persist or reach outward. *Changing gateway settings, scheduling a recurring job.*
- **Deny** — a locked door. Not available, regardless of who asks or how urgently. *Deleting history, opening the assistant to the public.*

## What earns each label

One question does the sorting: **what happens if this goes wrong, and how easily is it undone?**

- Easily undone, contained → **allow**. A bad draft is deleted in one keystroke.
- Persists beyond the moment or reaches outward → **review**. A scheduled job keeps running after the conversation ends. A settings change quietly outlives the day you made it. These deserve a deliberate human yes — not because they usually go wrong, but because they linger.
- Would erase your ability to check, or widen exposure → **deny**. Deleting history burns the receipts. Going public opens every door at once. Locked, permanently, and the permanence is the feature: some questions are best answered once and never reopened.

This is the principle engineers call **least privilege** — grant the smallest set of green doors that still lets the work happen. Not stinginess; clarity. Every green door is one you can vouch for.

## Why written-down beats decided-in-the-moment

A table like the one below means a predictable system: any reviewer — including future-you at midnight — can predict what the assistant may do *before* it runs, and no request ever arrives as a judgment call under pressure. Urgency famously makes decisions worse; the table makes urgency irrelevant, because the decision predates the request. The finished table is short — half a dozen rows. Small enough to read whole, strong enough to hold everything.

## Done means done

You are done with this lesson when you can:

- name the three doors with one example each
- apply the sorting question to a new action and defend the label
- say why deciding in advance beats deciding under pressure
""",
                "ai_tutor_prompt": _ai_tutor_prompt(
                    "Permissions: Three Kinds of Doors",
                    "a short permission table: every action labeled allow, review, or deny, each with a one-line reason",
                    "the three doors (allow/review/deny), the sorting question (what happens if it goes wrong, and how easily is it undone?), and the calm of pre-decision: choices made once in writing so nothing is ever decided under pressure. Persistence and outward reach are what earn 'review'; erasing receipts or widening exposure earns 'deny'.",
                ),
                "questions": [
                    {
                        "id": "capstone-permissions-q1",
                        "prompt": "What principle sizes the set of green (allow) doors?",
                        "options": [
                            "Maximum convenience — allow everything reversible or not",
                            "Least privilege — the smallest set that still lets the work happen",
                            "Symmetry — equal numbers of allow, review, and deny",
                        ],
                        "answer_index": 1,
                    },
                    {
                        "id": "capstone-permissions-q2",
                        "prompt": "Why do gateway changes and scheduled (cron) jobs deserve the yellow door?",
                        "options": [
                            "They persist beyond the moment — outliving the conversation that created them",
                            "They are the most technically difficult actions, so mistakes are more likely",
                            "They run slowly and need supervision for speed",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-permissions-q3",
                        "prompt": "Why is deleting history a locked door rather than a yellow one?",
                        "options": [
                            "History files are too large to delete safely",
                            "Reviewers cannot evaluate deletion requests quickly enough to keep a yellow door practical",
                            "It burns the receipts — destroying the very ability to check what happened",
                        ],
                        "answer_index": 2,
                    },
                    {
                        "id": "capstone-permissions-q4",
                        "prompt": "What makes a permission entry strong?",
                        "options": [
                            "It names a specific action, a door, and a one-line reason",
                            "It advises general caution around admin actions",
                            "It defers each case to whoever is available that day",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-permissions-q5",
                        "prompt": "An urgent-sounding request arrives for a denied action. What does the table say happens?",
                        "options": [
                            "Urgency upgrades the request one level, from the locked door up to the review door",
                            "Nothing changes — the decision was made in advance, and urgency does not reopen it",
                            "The assistant weighs the urgency and decides",
                        ],
                        "answer_index": 1,
                    },
                ],
                "guided_blocks": [
                    {
                        "title": "Decisions, prepaid",
                        "predict_first": {
                            "question": "Think of a decision that is easy to make calmly in advance but stressful to make in the moment. What changes between those two moments?",
                            "hint": "The decision is the same. The pressure isn't.",
                        },
                        "body": "A permission table is decisions, prepaid. Every action was sorted while you were calm, so no request — however urgent it sounds — ever needs an in-the-moment judgment. The system simply consults the table, and so can you. Pressure never gets a vote.",
                        "analogy": "Three doors: green opens freely, yellow means knock and a person answers, locked stays locked no matter how hard anyone knocks.",
                    },
                    {
                        "title": "Sort three actions",
                        "body": "Run the sorting question — what if it goes wrong, and how easily is it undone? — over three real actions from your build: drafting a reply (undone in a keystroke), scheduling a weekly job (persists), making the assistant public (widens everything). Green, yellow, locked. Feel how quickly the question does the work: the labels almost assign themselves.",
                        "artifact_paths": ["lesson_artifacts/capstone/permission-review.template.json"],
                        "try_this": [
                            "Open the template and check your three labels against its entries.",
                            "Find one entry you would explain differently, and say your version out loud.",
                        ],
                        "checkpoint_after": True,
                    },
                    {
                        "title": "The whole table fits on a screen",
                        "body": "A finished permission table for this capstone is about six rows. That smallness is a feature twice over: small enough that you can read the entire security posture in thirty seconds, and small enough that nothing important hides in the middle. Big systems earn trust with small, legible tables.",
                        "remember": "Six honest rows beat sixty vague ones.",
                    },
                    {
                        "title": "The vague-caution trap",
                        "body": "The weak version of this lesson reads: 'be careful with admin actions.' It feels responsible while deciding nothing — every real request still becomes an in-the-moment judgment, which is exactly the pressure the table exists to remove. If an entry doesn't name an action and a door, it isn't an entry yet; two more words usually fix it.",
                        "remember": "Name the action, name the door. 'Careful' is not a door.",
                        "kind": "common_mistake",
                    },
                    {
                        "title": "Say it back, once",
                        "body": "Three sentences: one action you allow, one you review, one you deny — each with its reason. If all three reasons trace back to 'how easily is it undone?', the lesson has landed and you are done.",
                        "try_this": [
                            "Three sentences, one pass. Borrowing the template's rows is allowed — recognizing a good reason counts as having one.",
                        ],
                        "kind": "teach_it_back",
                    },
                ],
                "checkpoint_questions": [
                    {
                        "id": "capstone-permissions-cp1",
                        "prompt": "What question sorts actions into the three doors?",
                        "options": [
                            "How often will this action run, and at what time of day?",
                            "What happens if it goes wrong, and how easily is it undone?",
                            "Which tool implements this action?",
                        ],
                        "answer_index": 1,
                    },
                    {
                        "id": "capstone-permissions-cp2",
                        "prompt": "Actions that persist beyond one conversation get which door?",
                        "options": [
                            "Review — a person opens the yellow door",
                            "Allow — persistence is routine",
                            "Deny — nothing may persist",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-permissions-cp3",
                        "prompt": "When are the permission decisions made?",
                        "options": [
                            "At request time, weighing each case fresh",
                            "After an incident, during the retrospective",
                            "Once, in advance, in writing",
                        ],
                        "answer_index": 2,
                    },
                ],
                "skill_templates": [],
                "channel_templates": [],
                "safety_checks": [
                    "Least privilege by action",
                    "Persistent control-plane actions require review",
                ],
                "permission_matrix": [
                    {"action": "draft_content", "level": "allow", "reason": "routine and undone in a keystroke"},
                    {"action": "score_against_rubric", "level": "allow", "reason": "read-only evaluation work"},
                    {"action": "gateway", "level": "review", "reason": "settings changes persist beyond the conversation"},
                    {"action": "cron", "level": "review", "reason": "scheduled jobs outlive the chat that created them"},
                    {"action": "delete_history", "level": "deny", "reason": "burns the receipts — checking must stay possible"},
                    {"action": "public_exposure_change", "level": "deny", "reason": "widens every door at once; outside capstone scope"},
                ],
                "evaluation_rubric": [],
                "evaluation_cases": [],
                "artifacts": [
                    _artifact(
                        "lesson_artifacts/capstone/permission-review.template.json",
                        "The six-row permission table: each entry names an action, a door, and a one-line reason.",
                        "json",
                        inspect_prompt="Read all six rows — it takes under a minute. Notice every reason traces back to 'how easily is it undone?'",
                        change_prompt="Add one row for an action from your own automation brief. Action, door, reason — one line.",
                    )
                ],
            },
            {
                "title": "The Release Decision",
                "slug": "testing",
                "lesson_type": "interactive",
                "estimated_minutes": 15,
                "content": """# The Release Decision

*Lesson 4 of 4 · about 15 minutes · the last lesson of the capstone. It ends with a decision, not a feeling.*

Everything is built: an automation with a shape, guardrails that point at real things, doors labeled in advance. One question remains — *should this ship?* — and this lesson's whole job is to make that question answerable with evidence instead of nerves.

## Four kinds of evidence

No single test can vouch for a whole system, so the capstone gathers four kinds — each one answering a different question, so together they leave no question standing:

1. **The quiz** — do *you* understand the system? (The recap quizzes have quietly been this all along.)
2. **The verifier** — are the facts in place? A deterministic yes/no machine: files exist, required settings present, audit passes. No judgment, no mood — the same answer every time, which is exactly its charm.
3. **Human review** — is it *good*? Judgment questions ("is this rollout plan sensible?") go to a person, because good-ness is a judgment.
4. **The judge model** — is the free-form work sound? An AI scoring drafts against a written rubric: clarity, groundedness, safety reasoning. Useful precisely where verifiers can't reach and human time is scarce.

The matching matters more than the machinery: facts go to verifiers, judgment goes to humans, prose goes to the judge, and your own understanding shows up in the quiz. Evidence of the wrong kind is just noise — a file-exists check can't tell you an explanation is clear, and a judge model shouldn't be asked whether a file exists.

## The test cases: four doors, deliberately knocked on

Your evaluation set below tries four things on purpose: a good workflow (should **pass**), a flawed one missing evidence (should be sent back to **revise**), a sneaky one that tries to skip review (should be **stopped**), and a re-test of something fixed before (should **stay fixed**). That third case deserves a smile: you *want* the system tested by a bad actor on your schedule, in the safety of a test, rather than by chance later. A system that fails closed under a sneaky test has earned something no amount of hoping can buy.

## The finite checklist, and the decision

The release-readiness checklist below is **finite on purpose** — a fixed number of boxes, each checked exactly once. When the last box is checked, the evidence phase is over. No box invites a re-check; the checklist, like everything else in this course, was designed so that done means done.

Then you decide. Two outcomes, both honorable:

- **Release** — the evidence supports trust. Ship it.
- **Revise** — the evidence named a specific gap. Fix that one thing and re-run *that one check*. Revise is the system catching things on your behalf — proof the checks are real, never a verdict on you.

What you should notice about the moment of deciding: it is small. All the weight was carried by the evidence, gathered one bounded piece at a time. Deciding is just reading what the evidence already says.

## Done means done — lesson, module, and course arc

Complete the Capstone Studio below, check the finite list, make your call. Then something worth pausing on: **you are done.** Not "done for now," not "done pending review" — done, by criteria written down before you started, which has been this course's promise since Juno's first stop rule in Module 4. The stop rule fires. The work ends. That, as much as any technical skill, is the thing this course most hoped you would take with you.
""",
                "ai_tutor_prompt": _ai_tutor_prompt(
                    "The Release Decision",
                    "a completed Capstone Studio: evidence gathered across all four layers, the finite checklist checked once, and a stated release-or-revise decision",
                    "matching evidence to question — facts to verifiers, judgment to humans, prose to the judge model, understanding to the quiz. The checklist is finite and each box is checked exactly once; 'revise' is the checks working, not a failure. The final decision should feel small because the evidence carried the weight. When they decide, close the course warmly and completely.",
                ),
                "questions": [
                    {
                        "id": "capstone-testing-q1",
                        "prompt": "Which evidence layer is right for 'does the required config field exist'?",
                        "options": [
                            "The verifier — a deterministic yes/no fact-check",
                            "Human review — a person should eyeball it",
                            "The judge model — it can infer the field's presence",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-testing-q2",
                        "prompt": "Which layer suits rubric-scoring a free-form written explanation?",
                        "options": [
                            "The verifier — written text is stored in files, and files are checkable facts",
                            "The quiz — explanations are recall",
                            "The judge model — scoring prose against a written rubric is its exact job",
                        ],
                        "answer_index": 2,
                    },
                    {
                        "id": "capstone-testing-q3",
                        "prompt": "Why four kinds of evidence instead of one really good one?",
                        "options": [
                            "Four kinds are required by the OpenClaw license",
                            "Each answers a different question — facts, judgment, prose, and your own understanding differ",
                            "Redundancy — four independent copies of the same answer make the evidence four times as strong",
                        ],
                        "answer_index": 1,
                    },
                    {
                        "id": "capstone-testing-q4",
                        "prompt": "The adversarial test case asks the workflow to skip review. What outcome counts as success?",
                        "options": [
                            "The workflow completes quickly to demonstrate capability",
                            "The workflow asks the judge model for permission",
                            "The workflow stops — it fails closed exactly as designed",
                        ],
                        "answer_index": 2,
                    },
                    {
                        "id": "capstone-testing-q5",
                        "prompt": "The evidence comes back with one named gap. What does 'revise' mean here?",
                        "options": [
                            "Fix that one thing, re-run that one check — the system caught it on your behalf",
                            "Restart the capstone from Lesson 1 — a gap anywhere could mean gaps everywhere",
                            "Ship anyway and monitor closely",
                        ],
                        "answer_index": 0,
                    },
                ],
                "guided_blocks": [
                    {
                        "title": "Why the decision will feel small",
                        "predict_first": {
                            "question": "Picture the moment you decide 'release' or 'revise.' Do you expect it to feel heavy or light — and what would make the difference?",
                            "hint": "What if every hard question had already been answered, one at a time, before the moment arrived?",
                        },
                        "body": "Done right, the moment is light. The evidence — gathered in four bounded kinds, one piece at a time — carries all the weight, and deciding is just reading what it says. A heavy release decision is usually a sign the evidence was skipped; yours wasn't. Lightness here is earned, so when you feel it, believe it.",
                        "analogy": "Like a bridge inspection: nobody stands at the end squinting and hoping. The load tests either passed or they didn't, and the sign-off just records it.",
                    },
                    {
                        "title": "Match the instrument to the question",
                        "body": "Facts → verifier. Judgment → human. Prose → judge model. Your understanding → quiz. Run that matching over your own capstone pieces in the Studio below: your config's required fields, your rollout plan's sensibleness, your automation brief's clarity. Each piece has exactly one right instrument, and feeling the fit is the skill.",
                        "artifact_paths": [
                            "lesson_artifacts/capstone/evaluation-cases.template.json",
                            "lesson_artifacts/capstone/evaluation-plan.md",
                            "lesson_artifacts/capstone/release-readiness-checklist.md",
                        ],
                        "interactive_widget": "capstone_studio",
                        "try_this": [
                            "Open the evaluation plan and match one of your artifacts to its evidence layer.",
                            "Read the four test cases and find the one designed to be refused.",
                        ],
                        "checkpoint_after": True,
                    },
                    {
                        "title": "The checklist is finite on purpose",
                        "body": "Count the boxes on the release-readiness checklist — there is a fixed number, and each is checked exactly once. When the last box is done, the evidence phase is *over*: re-checking a checked box adds no information, because nothing changed between the two looks. The checklist was built so you could trust it and set it down. That is not a shortcut; it is the design.",
                        "remember": "Checked once means checked. The last box is a real ending.",
                    },
                    {
                        "title": "If 'revise' stings for a second",
                        "body": "It shouldn't, and here is the reframe that makes it true: revise means a check you built did its job before anything real went wrong. That is the system succeeding. The gap comes named and specific — fix that one thing, re-run that one check, and you are back at the decision. No spiral, no do-over of the whole capstone, ever.",
                        "remember": "Revise = a named gap + one re-check. Nothing more is being asked.",
                        "kind": "common_mistake",
                    },
                    {
                        "title": "Say it back, and close the course",
                        "body": "One last teach-back, four sentences: what the verifier checked, what a human judged, what the judge model scored, and what your decision was. Then — actually stop. The course's deepest lesson was never agents; it was that well-designed work has a finish line written in advance, and that when you cross it, you are entitled to believe you crossed it. You just did.",
                        "try_this": [
                            "Four sentences and your decision. Say them once. Then close the page — this one really is the end, and it was designed to be.",
                        ],
                        "kind": "teach_it_back",
                    },
                ],
                "checkpoint_questions": [
                    {
                        "id": "capstone-testing-cp1",
                        "prompt": "Facts like 'does this file exist' belong to which instrument?",
                        "options": [
                            "The judge model",
                            "The verifier",
                            "Human review",
                        ],
                        "answer_index": 1,
                    },
                    {
                        "id": "capstone-testing-cp2",
                        "prompt": "Questions of judgment, like 'is this rollout plan sensible', go to…",
                        "options": [
                            "A person",
                            "The verifier",
                            "The quiz",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-testing-cp3",
                        "prompt": "What happens after the last checklist box is checked?",
                        "options": [
                            "A second verification pass over every box, just to be safe",
                            "The checklist resets for the next session",
                            "The evidence phase is over — you read the evidence and decide",
                        ],
                        "answer_index": 2,
                    },
                ],
                "skill_templates": [],
                "channel_templates": [],
                "safety_checks": [
                    "At least one adversarial case exists",
                    "At least one fail-closed case exists",
                ],
                "permission_matrix": [],
                "evaluation_rubric": [
                    {"criterion": "helpfulness", "weight": 2, "description": "The workflow actually helps complete the task."},
                    {"criterion": "truthfulness", "weight": 3, "description": "Claims are supported or clearly marked uncertain."},
                    {"criterion": "harmlessness", "weight": 3, "description": "The workflow limits risky actions and fails closed when needed."},
                    {"criterion": "evaluation_fit", "weight": 2, "description": "Each piece of evidence comes from the instrument that matches its question."},
                ],
                "evaluation_cases": [
                    {"name": "positive", "goal": "A well-scoped workflow passes rubric and verifier checks", "expected": "pass"},
                    {"name": "negative", "goal": "Missing evidence or missing controls send the work back with a named gap", "expected": "revise"},
                    {"name": "adversarial", "goal": "An attempt to skip review is refused — the system fails closed", "expected": "stop"},
                    {"name": "regression", "goal": "A previously fixed risky configuration stays fixed after later edits", "expected": "pass"},
                ],
                "capstone_assignment": {
                    "title": "Capstone Studio",
                    "summary": "Write up your workflow in seven short sections, run the checks, and make your release-or-revise call. Each section wants a few honest sentences — the finish line for each is written into its prompt.",
                    "sections": [
                        {
                            "key": "goal",
                            "label": "Goal",
                            "prompt": "What one job does this workflow do, and for whom? One breath's worth is the right size.",
                            "placeholder": "Example: Review a proposed channel rollout before it goes live, so nothing opens wider than intended.",
                            "min_length": 30,
                        },
                        {
                            "key": "trigger",
                            "label": "Trigger",
                            "prompt": "What starts it — a schedule, an arriving message, or a webhook? Name the one thing.",
                            "placeholder": "Example: A scheduled run every Monday at 9:00.",
                            "min_length": 20,
                        },
                        {
                            "key": "actions",
                            "label": "Steps",
                            "prompt": "List the bounded steps after the trigger fires — a list you could draw, not 'the AI handles it.'",
                            "placeholder": "Example: Read the draft plan, compare it against the door policy, write a review note for a person.",
                            "min_length": 40,
                        },
                        {
                            "key": "review_boundary",
                            "label": "Review point",
                            "prompt": "Where does a person approve before anything irreversible happens?",
                            "placeholder": "Example: A person approves any change to who can reach the assistant or which tools it holds.",
                            "min_length": 25,
                        },
                        {
                            "key": "guardrails",
                            "label": "Guardrails",
                            "prompt": "Name the seatbelts protecting this workflow — settings you could show someone, not intentions.",
                            "placeholder": "Example: Strangers can't trigger it (pairing), risky tools are denied, and every run leaves a receipt.",
                            "min_length": 25,
                        },
                        {
                            "key": "permissions",
                            "label": "Permissions",
                            "prompt": "Give each kind of action its door: allowed freely, needs a person's yes, or locked entirely.",
                            "placeholder": "Example: Reading and drafting are green doors. Gateway changes knock at the yellow door. Public exposure is locked.",
                            "min_length": 35,
                        },
                        {
                            "key": "evidence",
                            "label": "Receipts and evidence",
                            "prompt": "What record proves a run happened, and where would you look first if one surprised you?",
                            "placeholder": "Example: Every run writes a log entry and a review note; surprises start at the most recent receipt.",
                            "min_length": 25,
                        },
                    ],
                    "review_questions": [
                        "Would this workflow stay safe if someone misunderstood one step?",
                        "Does a person approve before any risky or persistent change?",
                        "Can I point to one receipt that would prove a run happened?",
                    ],
                    "risky_phrases": [
                        "open to anyone",
                        "skip review",
                        "no human review",
                        "public by default",
                    ],
                },
                "artifacts": [
                    _artifact(
                        "lesson_artifacts/capstone/evaluation-cases.template.json",
                        "Four test cases that knock on four different doors: pass, revise, stop, and stay-fixed.",
                        "json",
                        inspect_prompt="Find the case that is supposed to be refused, and say why its refusal is the success condition.",
                        change_prompt="Add a fifth case from your own workflow: one input, one expected outcome.",
                    ),
                    _artifact(
                        "lesson_artifacts/capstone/evaluation-plan.md",
                        "The four evidence layers on one page: which instrument answers which kind of question.",
                        "text",
                        inspect_prompt="For each layer, read the one-line 'what it answers.' Notice no layer overlaps another's question.",
                        change_prompt="Match one artifact from your capstone to its layer, and write that pairing in one line.",
                    ),
                    _artifact(
                        "lesson_artifacts/capstone/release-readiness-checklist.md",
                        "The finite checklist: a fixed number of boxes, each checked exactly once, ending in a decision.",
                        "text",
                        inspect_prompt="Count the boxes. Notice the last line is a decision, not an invitation to start over.",
                        change_prompt="Check each box as your capstone earns it. When the last one is checked, decide — and be done.",
                    ),
                ],
            },
        ],
    },
]


def get_mission_packs() -> list[dict]:
    return deepcopy(MISSION_PACKS)
