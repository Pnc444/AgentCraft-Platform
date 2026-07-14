from __future__ import annotations

from copy import deepcopy

from apps.courses.module4_missions import MODULE_4_MISSION_PACK


def _ai_tutor_prompt(lesson_title: str, deliverable: str, focus: str) -> str:
    return f"""You are ACADEMIC TUTOR AI HEADMASTER guiding a zero-knowledge student through {lesson_title}.

Operate in attempt-first mode.
- Start by asking what the learner already configured, drafted, or tested.
- Use the lesson content as the primary source of truth.
- Push for explicit tradeoffs, failure modes, and acceptance checks.
- Keep the learner moving toward the deliverable: {deliverable}.
- Focus especially on: {focus}.

If the learner asks for a shortcut, redirect them to the smallest safe next action. If they already have a draft, review it against the lesson checklist instead of replacing their work.
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
        "title": "Module 6: OpenClaw (Build #2)",
        "slug": "module-6-openclaw",
        "description": "Configure OpenClaw the official way: onboard, wire core files, add skills, connect channels, and harden the build before it is trusted.",
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
                "title": "Configuration",
                "slug": "configuration",
                "lesson_type": "agent_lab",
                "estimated_minutes": 15,
                "content": """# Configuration

OpenClaw is a **personal AI assistant you run on your own devices**. The Gateway is the control plane; the assistant is the product. For this module, configuration means learning the official OpenClaw setup path and the small set of files you actually need to understand.

## Fastest supported setup path
Use the OpenClaw path that the official README recommends:

1. `npm install -g openclaw@latest`
2. `openclaw onboard --install-daemon`
3. `openclaw gateway status`

`openclaw onboard` is the important part. It walks you through the gateway, workspace, channels, and skills instead of forcing you to hand-wire everything from scratch.

## Reference links
- [Official OpenClaw GitHub repository](https://github.com/openclaw/openclaw)
- [OpenClaw documentation home](https://docs.openclaw.ai/)
- [Getting started guide](https://docs.openclaw.ai/start/getting-started)
- [Onboarding guide](https://docs.openclaw.ai/start/wizard)

## The files that matter first

| Path | Why it matters |
| --- | --- |
| `~/.openclaw/openclaw.json` | Global runtime configuration: model, routing, tools, sandbox, and channels |
| `~/.openclaw/workspace` | Default agent workspace |
| `SOUL.md` | Agent identity, rules, operating style, and boundaries |
| `AGENTS.md` / `TOOLS.md` | Extra prompt files injected into the agent session |
| `<workspace>/skills/<skill>/SKILL.md` | The actual skill definition files |

## Minimal configuration idea
The official docs show a very small starting point for `openclaw.json`:

```json5
{
  agent: {
    model: "<provider>/<model-id>",
  },
}
```

That is enough to prove the gateway can talk to a model. After that, build outward in layers:

1. **Model**: choose a provider and confirm authentication works.
2. **Workspace**: know where OpenClaw will read agent files and skills.
3. **SOUL.md**: define the agent's role and rules.
4. **Channels**: connect only the messaging surfaces you actually plan to use.
5. **Safety**: tighten tools and sandboxing before you trust the agent outside your own main session.

## OpenClaw-specific configuration mindset
OpenClaw is config-first, not chain-first. The key decisions are:

- Which model the assistant uses.
- Which workspace and prompt files it should load.
- Which channels are enabled.
- Which tools stay on the host and which sessions should be sandboxed.
- How you will prove the gateway is healthy after each change.

## Configuration checklist
- Run `openclaw onboard --install-daemon` before hand-editing advanced settings.
- Check `openclaw gateway status` after onboarding or after config changes.
- Keep `openclaw.json` small until the base path works.
- Write `SOUL.md` so another operator can tell what the agent is for.
- Add tools and channels incrementally, not all at once.

## Definition of done
You are done when you can explain how `openclaw.json`, `SOUL.md`, the workspace, and the gateway fit together in one sentence each.
""",
                "ai_tutor_prompt": _ai_tutor_prompt(
                    "Configuration",
                    "a grounded OpenClaw starter configuration",
                    "the official onboarding path, the core files, and the difference between runtime config and agent identity",
                ),
                "questions": [
                    {
                        "id": "openclaw-config-q1",
                        "prompt": "Your colleague says: 'Start by opening openclaw.json and editing the model and channels directly.' What is the problem with this advice?",
                        "options": [
                            "You should run openclaw onboard first — it sets up the gateway and workspace in the correct order before you manually edit anything",
                            "No problem — editing the config directly is the fastest supported path",
                            "openclaw.json does not exist until the gateway creates it automatically",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-config-q2",
                        "prompt": "You change SOUL.md to give the agent a different personality, but it still uses the wrong AI model. Which file do you need to change, and why?",
                        "options": [
                            "~/.openclaw/openclaw.json — that is where the model setting lives; SOUL.md only controls identity and behavior, not which model is used",
                            "SOUL.md again — the model is defined in the persona section",
                            "SKILL.md — skills control which model is loaded",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-config-q3",
                        "prompt": "You run openclaw gateway status and it shows the gateway is healthy. What does this actually tell you?",
                        "options": [
                            "The gateway is running and can communicate with the configured model — safe to build on top of this foundation",
                            "All channels are connected and ready for messages",
                            "All skills have been verified and installed",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-config-q4",
                        "prompt": "You are reviewing someone's OpenClaw setup. The agent sounds wrong — it has an odd personality that does not match the intended role. Which file is most likely the problem?",
                        "options": [
                            "SOUL.md — that file defines the agent's identity, persona, and behavioral rules",
                            "openclaw.json — personality is stored in the model configuration",
                            "SKILL.md — skills define the agent's communication style",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-config-q5",
                        "prompt": "A student asks: 'Can I just add all the channels and skills on day one before testing anything?' What would you tell them?",
                        "options": [
                            "No — prove the gateway is healthy first, then add channels and skills incrementally so you can isolate what breaks if something goes wrong",
                            "Yes — adding everything at once is faster and shows the full system",
                            "Yes — channels must be configured before the gateway will start",
                        ],
                        "answer_index": 0,
                    },
                ],
                "guided_blocks": [
                    {
                        "title": "Why this exists",
                        "predict_first": {
                            "question": "Before reading: if you had to set up an AI assistant on your own computer, what would you configure first — who it is, or how it runs?",
                            "hint": "There is a meaningful difference between an assistant's personality and the system that keeps it alive. Which matters first?",
                        },
                        "body": "Before you connect tools or channels, imagine you just hired a digital intern. OpenClaw is the office, not the worker. The Gateway keeps the office running, while the agent files tell the assistant who it is and how it should behave.",
                        "analogy": "Think of `openclaw.json` as the control panel, `SOUL.md` as the job description, and `SKILL.md` as the procedure card the intern reaches for when it needs help.",
                        "try_this": [
                            "Say out loud what OpenClaw is in one sentence before reading further.",
                            "Open the artifact files below and find the three places where behavior is defined.",
                        ],
                    },
                    {
                        "title": "The fastest safe setup path",
                        "body": "Use the shortest official path first:\n\n1. `npm install -g openclaw@latest`\n2. `openclaw onboard --install-daemon`\n3. `openclaw gateway status`\n\nFor a beginner, this matters because `openclaw onboard` asks the questions in the right order instead of forcing you to memorize every config key on day one.",
                        "artifact_paths": ["lesson_artifacts/openclaw/config/onboard-checklist.md"],
                        "remember": "Do not start by hand-editing advanced settings if you have not proven the gateway is healthy yet.",
                    },
                    {
                        "title": "The three files to remember",
                        "body": "You only need three concepts right now:\n\n- `~/.openclaw/openclaw.json` chooses runtime behavior.\n- `SOUL.md` defines the agent's role and rules.\n- `SKILL.md` teaches the agent how to use a tool.\n\nIf you can explain the difference between those three, you are ready to build instead of just reading docs.",
                        "artifact_paths": [
                            "lesson_artifacts/openclaw/config/openclaw.json.template.json5",
                            "lesson_artifacts/openclaw/config/SOUL.md",
                        ],
                        "try_this": [
                            "Open `openclaw.json.template.json5` and find the model line.",
                            "Open `SOUL.md` and find the mission statement.",
                            "Predict which file you would change if the agent sounded wrong versus used the wrong model.",
                        ],
                        "checkpoint_after": True,
                    },
                    {
                        "title": "How to know you are ready",
                        "body": "You are ready to move on when you can answer four beginner questions without guessing:\n\n1. Where does runtime config live?\n2. What file gives the agent its identity?\n3. What file teaches a skill?\n4. What command tells you the gateway is healthy?",
                        "remember": "Configuration is not memorizing every option. It is knowing which file controls which layer.",
                    },
                    {
                        "title": "Common mistake",
                        "body": "Beginners often mix up `openclaw.json` and `SOUL.md`. The config file changes runtime behavior. `SOUL.md` changes who the agent is and how it should act. If you swap those roles in your head, every later lesson feels harder than it needs to.",
                        "remember": "Control panel versus job description: do not confuse them.",
                    },
                    {
                        "title": "Teach it back",
                        "body": "Pretend a classmate asks, 'Why are there so many files?' Your answer should be simple: one file runs the system, one file describes the worker, and one file teaches a reusable move. If you can explain that clearly, you truly understand the lesson.",
                        "try_this": [
                            "Explain the difference between `openclaw.json`, `SOUL.md`, and `SKILL.md` without looking back at the lesson.",
                            "Use the phrase 'control panel, job description, procedure card' in your explanation.",
                        ],
                    },
                ],
                "checkpoint_questions": [
                    {
                        "id": "openclaw-config-cp1",
                        "prompt": "If you want to change who the agent is, which file should you inspect first?",
                        "options": [
                            "SOUL.md",
                            "A random quiz answer",
                            "The progress bar UI",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-config-cp2",
                        "prompt": "Which file is the runtime control panel for OpenClaw?",
                        "options": [
                            "~/.openclaw/openclaw.json",
                            "SKILL.md only",
                            "The README badge section",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-config-cp3",
                        "prompt": "What command should you run to check whether the gateway is healthy after setup?",
                        "options": [
                            "openclaw gateway status",
                            "openclaw pairing approve test 0000",
                            "openclaw skills update --all",
                        ],
                        "answer_index": 0,
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
                        "Minimal OpenClaw runtime config template grounded in the official config-first setup path.",
                        "text",
                        inspect_prompt="Find the model line, the DM session setting, and the sandbox mode. Say what each one controls in plain English.",
                        change_prompt="Replace the model placeholder with the provider and model you would test first, then explain why you picked it.",
                    ),
                    _artifact(
                        "lesson_artifacts/openclaw/config/SOUL.md",
                        "Starter SOUL.md for a student-friendly OpenClaw builder agent.",
                        "text",
                        inspect_prompt="Look for the Mission and Rules sections. Ask yourself: would a new student know what this agent is supposed to do?",
                        change_prompt="Rewrite the Mission line in your own words so it sounds like a job description for a digital intern.",
                    ),
                    _artifact(
                        "lesson_artifacts/openclaw/config/onboard-checklist.md",
                        "Operator checklist for walking the official OpenClaw onboarding path.",
                        "text",
                        inspect_prompt="Notice the order: install, onboard, status, config, workspace, then channels. Explain why channels come late.",
                        change_prompt="Mark which checklist step you could do today and which step would still block you if you were starting from zero.",
                    ),
                ],
            },
            {
                "title": "Adding Skills",
                "slug": "adding-skills",
                "lesson_type": "agent_lab",
                "estimated_minutes": 15,
                "content": """# Adding Skills

In OpenClaw, a skill is not a Python class or a hidden plugin. A skill is a **markdown file named `SKILL.md`** with YAML frontmatter and instructions that teach the agent how and when to use a tool.

## Minimum skill shape
Every skill needs at least:

- `name`
- `description`
- a markdown body that tells the agent when to use it

Example:

```markdown
---
name: research-brief
description: Turn raw source material into a short, cited summary.
---

When the user asks for a short research brief, gather the source material,
summarize only supported claims, and label unknowns explicitly.
```

## Official loading order
OpenClaw loads skills by precedence. Highest wins if the same skill name appears in multiple places:

1. `<workspace>/skills`
2. `<workspace>/.agents/skills`
3. `~/.agents/skills`
4. `~/.openclaw/skills`
5. Bundled skills
6. Extra directories and plugin skills

That means **location** and **visibility** are separate ideas. You can also restrict which skills an agent sees with `agents.defaults.skills` and `agents.list[].skills` allowlists.

## Installing and trusting skills
OpenClaw's public registry is ClawHub.

- Install into the current workspace: `openclaw skills install @owner/<slug>`
- Install globally: `openclaw skills install @owner/<slug> --global`
- Verify trust envelope: `openclaw skills verify @owner/<slug>`

Useful references:
- [OpenClaw GitHub repository](https://github.com/openclaw/openclaw)
- [Official Skills documentation](https://docs.openclaw.ai/tools/skills)

The official docs are explicit: **treat third-party skills as untrusted code**. Review them before you trust them.

## What this module should teach
For Module 6, the useful skill set is:

- **research-brief**: summarize source material without losing the evidence trail.
- **channel-policy-check**: verify that a channel rollout matches the chosen DM and group policy.
- **security-audit-helper**: turn `openclaw security audit` findings into a triage checklist.

## Definition of done
You are done when you can explain where a skill lives, how OpenClaw decides whether to load it, and why verifying the source matters.
""",
                "ai_tutor_prompt": _ai_tutor_prompt(
                    "Adding Skills",
                    "three grounded OpenClaw skill definitions",
                    "the real SKILL.md format, precedence rules, install commands, and trust checks",
                ),
                "questions": [
                    {
                        "id": "openclaw-skills-q1",
                        "prompt": "You write a skill description in a file named skills-info.txt and place it in workspace/skills/. OpenClaw ignores it. Why?",
                        "options": [
                            "OpenClaw only loads SKILL.md files — the filename must be exactly SKILL.md for the skill to be discovered",
                            "The skills folder path is wrong for third-party skills",
                            "You need to restart the gateway twice after adding any text file",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-skills-q2",
                        "prompt": "You have a SKILL.md in your workspace/skills folder and another with the same name in ~/.openclaw/skills. Which one does OpenClaw use, and why?",
                        "options": [
                            "The workspace version — it has higher precedence because it is closest to the current project",
                            "The ~/.openclaw/skills version — global skills always win",
                            "Whichever file was created most recently",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-skills-q3",
                        "prompt": "You install a skill from ClawHub. Before enabling it for the agent, what is the recommended next step according to the official docs?",
                        "options": [
                            "Run openclaw skills verify to check the skill's trust envelope before trusting it",
                            "Restart the gateway immediately to load the new skill",
                            "Edit the skill's SKILL.md to remove any suspicious lines",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-skills-q4",
                        "prompt": "A teammate says: 'Third-party skills are fine — they are just markdown files, not code.' What's the risk they are ignoring?",
                        "options": [
                            "Skills inject instructions into the agent's behavior — a malicious skill can influence what actions the agent takes, even if it's just text",
                            "No risk — markdown cannot contain executable instructions",
                            "The only risk is a skill slowing down the gateway startup time",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-skills-q5",
                        "prompt": "You want a skill visible to one specific agent but hidden from all others in your setup. Which OpenClaw feature handles this?",
                        "options": [
                            "Agent allowlists — agents.list[].skills restricts which skills each agent can see, regardless of where they are loaded from",
                            "Place the skill in ~/.openclaw/skills to hide it from specific agents",
                            "Rename the SKILL.md file to make it invisible to other agents",
                        ],
                        "answer_index": 0,
                    },
                ],
                "guided_blocks": [
                    {
                        "title": "What a skill really is",
                        "body": "A skill is not a secret plugin or a hidden Python script. In OpenClaw, a skill is a markdown file named `SKILL.md` that teaches the agent when and how to use a tool.",
                        "analogy": "Think of a skill like a recipe card taped next to a machine. The machine already exists; the card tells the worker when to use it and what good work looks like.",
                        "try_this": [
                            "Open one of the skill files below and find the `name` and `description` frontmatter.",
                            "Say what the skill does in one sentence without using jargon.",
                        ],
                    },
                    {
                        "title": "Where OpenClaw looks first",
                        "body": "OpenClaw does not load every skill equally. The official load order starts with the current workspace, then project-agent skills, then personal skills, then shared managed skills, and finally bundled or extra sources. Highest precedence wins.",
                        "remember": "For beginners, the simplest safe mental model is: workspace skills are the closest to this project, so they win first.",
                    },
                    {
                        "title": "Install, verify, then allow",
                        "body": "The official flow is:\n\n- install with `openclaw skills install @owner/<slug>`\n- verify with `openclaw skills verify @owner/<slug>`\n- restrict visibility with agent allowlists when needed\n\nThat order matters because a skill can influence real tool behavior.",
                        "try_this": [
                            "Read the verify command and explain what problem it solves.",
                            "Explain why a third-party skill should be treated like untrusted code until reviewed.",
                        ],
                        "checkpoint_after": True,
                    },
                    {
                        "title": "Your first skill trio",
                        "body": "For this module, the important beginner outcome is not 'I installed 50 skills.' It is 'I understand three useful ones':\n\n- `research-brief` keeps summaries grounded\n- `channel-policy-check` keeps channel rollout disciplined\n- `security-audit-helper` turns audit findings into action\n\nThat is enough to make the platform feel real without overwhelming a new learner.",
                        "artifact_paths": [
                            "lesson_artifacts/openclaw/skills/research-brief/SKILL.md",
                            "lesson_artifacts/openclaw/skills/channel-policy-check/SKILL.md",
                            "lesson_artifacts/openclaw/skills/security-audit-helper/SKILL.md",
                        ],
                        "remember": "A beginner remembers a few trusted skills better than a giant catalog.",
                    },
                    {
                        "title": "Common mistake",
                        "body": "A common beginner error is treating a skill like the tool itself. In OpenClaw, the tool is the capability. The skill is the instruction sheet that teaches the agent when and how to use that capability responsibly.",
                        "remember": "Tool = can do. Skill = knows when and how to do it.",
                    },
                    {
                        "title": "Teach it back",
                        "body": "If a friend asked, 'Why can't I just install every skill I find?' your answer should mention trust, precedence, and visibility. A good answer explains that skills can shape real behavior, so install comes before verification only in the command list, not in your trust decision.",
                        "try_this": [
                            "Explain skill precedence in plain English: which location wins first and why?",
                            "Explain why a third-party skill should be reviewed before you trust it.",
                        ],
                    },
                ],
                "checkpoint_questions": [
                    {
                        "id": "openclaw-skills-cp1",
                        "prompt": "What file name does OpenClaw actually discover as a skill definition?",
                        "options": [
                            "SKILL.md",
                            "skill.py",
                            "tools.env",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-skills-cp2",
                        "prompt": "Which skill location wins first when two skills have the same name?",
                        "options": [
                            "The current workspace skill path",
                            "The lowest-precedence bundled path",
                            "Whichever one has more lines",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-skills-cp3",
                        "prompt": "Why should you verify a third-party OpenClaw skill before trusting it?",
                        "options": [
                            "Because skills can change agent behavior and should be treated like untrusted code until reviewed",
                            "Because verify makes the skill load faster",
                            "Because OpenClaw refuses to read markdown otherwise",
                        ],
                        "answer_index": 0,
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
                        "Workspace skill example for turning source material into a cited brief.",
                        "text",
                        inspect_prompt="Find the `name`, `description`, and the sentence that tells the agent how to behave.",
                        change_prompt="Rewrite the description so a first-year student could predict what the skill does without seeing the body.",
                    ),
                    _artifact(
                        "lesson_artifacts/openclaw/skills/channel-policy-check/SKILL.md",
                        "Workspace skill example for checking whether a channel setup matches policy.",
                        "text",
                        inspect_prompt="Look for the lines that compare a channel plan against policy. Explain what kind of mistake this skill is meant to catch.",
                        change_prompt="Add one more sentence that reminds the agent to look for mention gating in shared rooms.",
                    ),
                    _artifact(
                        "lesson_artifacts/openclaw/skills/security-audit-helper/SKILL.md",
                        "Workspace skill example for triaging openclaw security audit findings.",
                        "text",
                        inspect_prompt="Find the part that groups findings by category. Why is grouping helpful for a beginner reading audit output?",
                        change_prompt="Add a sentence that tells the agent to prioritize anything open plus tools enabled before all else.",
                    ),
                ],
            },
            {
                "title": "Channel",
                "slug": "channel",
                "lesson_type": "interactive",
                "estimated_minutes": 12,
                "content": """# Channel

OpenClaw is built to speak on the channels people already use: WhatsApp, Telegram, Slack, Discord, Google Chat, Signal, and more. For this lesson, the key question is not "which app is coolest?" It is **which channel policy keeps the agent useful without turning it into a public footgun**.

## Security defaults you should know
The OpenClaw docs treat inbound messages as untrusted input. The safe default for DM-capable channels is **pairing**:

- unknown senders receive a short pairing code
- the bot ignores them until approved
- you approve with `openclaw pairing approve <channel> <code>`

Useful references:
- [OpenClaw GitHub repository](https://github.com/openclaw/openclaw)
- [Channels documentation](https://docs.openclaw.ai/channels)
- [Security defaults and threat model](https://docs.openclaw.ai/gateway/security)

Public DMs are not the default. They require an explicit opt-in such as `dmPolicy=\"open\"` plus a wildcard allowlist entry.

## Group and room safety
For group rooms, the docs recommend mention gating and allowlists over always-on behavior. The big ideas are:

- prefer `requireMention` in shared rooms
- keep group allowlists tight
- separate trigger authorization from context visibility
- isolate multi-user DM sessions with `session.dmScope: \"per-channel-peer\"` when several people can DM the same bot

## A practical channel rollout order
1. Connect one trusted channel first.
2. Keep DMs on pairing unless you have a strong reason not to.
3. Turn on mention gating for shared rooms.
4. Decide which rooms are build rooms versus review rooms.
5. Test the policy before you widen access.

## What this module should teach
For this OpenClaw build, a good channel lesson is not about chat aesthetics. It is about proving that:

- the right people can reach the bot,
- the wrong people cannot trigger sensitive actions,
- and the session boundaries are clear.

## Definition of done
You are done when you can explain the difference between `pairing`, `allowlist`, and `open`, and say when `per-channel-peer` DM isolation matters.
""",
                "ai_tutor_prompt": _ai_tutor_prompt(
                    "Channel",
                    "an OpenClaw channel policy and rollout plan",
                    "pairing defaults, mention gating, DM isolation, and how to avoid opening the wrong room too early",
                ),
                "questions": [
                    {
                        "id": "openclaw-channel-q1",
                        "prompt": "What is the default DM policy OpenClaw recommends for most messaging channels?",
                        "options": [
                            "pairing",
                            "open",
                            "disabled forever",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-channel-q2",
                        "prompt": "How do you approve a new sender after they receive a pairing code?",
                        "options": [
                            "openclaw pairing approve <channel> <code>",
                            "openclaw gateway restart --approve",
                            "openclaw skills install pairing",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-channel-q3",
                        "prompt": "What extra step is required before public inbound DMs are truly open?",
                        "options": [
                            "Use dmPolicy open and explicitly include * in the allowlist",
                            "Add a brighter accent color",
                            "Turn off gateway auth",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-channel-q4",
                        "prompt": "Why is requireMention useful in shared rooms?",
                        "options": [
                            "It reduces accidental triggering in group conversations",
                            "It enables automatic publishing",
                            "It disables all channel logging",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-channel-q5",
                        "prompt": "When is session.dmScope per-channel-peer most useful?",
                        "options": [
                            "When multiple people can DM the same bot and you want isolated DM context",
                            "When you want one global session for every sender",
                            "When the gateway has no auth token",
                        ],
                        "answer_index": 0,
                    },
                ],
                "guided_blocks": [
                    {
                        "title": "Why channel policy matters",
                        "body": "A messaging channel is the front door to your agent. If the front door is too open, the wrong person can ask the right tools to do the wrong thing.",
                        "analogy": "Treat channel policy like deciding who gets a house key, who can ring the bell, and who can only speak when invited.",
                    },
                    {
                        "title": "The three DM policies",
                        "body": "OpenClaw documents three DM ideas beginners should know first:\n\n- `pairing`: unknown senders get a code and are ignored until approved\n- `allowlist`: only pre-approved senders can DM\n- `open`: public inbound DMs are allowed, but only with explicit opt-in\n\nThe safe default is `pairing`.",
                        "remember": "Open is never the beginner default. Pairing is.",
                    },
                    {
                        "title": "Shared rooms need mention rules",
                        "body": "In a group or team room, the bot should not wake up for every line of conversation. The docs recommend `requireMention` and tight room allowlists so the agent only acts when the room is intentionally addressing it.\n\nIf several people can DM the same bot, `session.dmScope: \"per-channel-peer\"` helps isolate DM context by sender.",
                        "artifact_paths": ["lesson_artifacts/openclaw/channels/channel-policy.template.json5"],
                        "try_this": [
                            "Explain in plain English what `pairing` protects.",
                            "Explain why `requireMention` is better than an always-on bot in a shared room.",
                        ],
                        "checkpoint_after": True,
                    },
                    {
                        "title": "Roll out one trusted room at a time",
                        "body": "For a first OpenClaw build, connect one trusted channel, test the policy, then widen access slowly. A good rollout is boring: predictable, reviewable, and hard to misuse by accident.",
                        "artifact_paths": ["lesson_artifacts/openclaw/channels/rollout-checklist.md"],
                        "remember": "A channel setup is good when the right people can reach the bot and the wrong people cannot trigger sensitive actions.",
                    },
                    {
                        "title": "Common mistake",
                        "body": "Beginners often think 'open' sounds convenient and therefore better. In practice, open channels widen the attack surface immediately. Pairing and mention gating feel slower at first, but they protect you from accidental or hostile triggers before the bot is trusted.",
                        "remember": "Convenient is not always safe. Safe defaults are there to buy you time to learn.",
                    },
                    {
                        "title": "Teach it back",
                        "body": "Imagine a teammate says, 'Why not just let anyone DM the bot?' A strong answer explains the pairing flow, the mention rule for shared rooms, and why session isolation matters once more than one person can talk to the assistant.",
                        "try_this": [
                            "Explain pairing, allowlist, and open as if you were teaching a student who has never deployed a bot before.",
                            "Give one reason `requireMention` protects a shared room.",
                        ],
                    },
                ],
                "checkpoint_questions": [
                    {
                        "id": "openclaw-channel-cp1",
                        "prompt": "What is the safest beginner default for inbound DMs in OpenClaw?",
                        "options": [
                            "pairing",
                            "open",
                            "no policy at all",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-channel-cp2",
                        "prompt": "Why is requireMention useful in a shared room?",
                        "options": [
                            "It reduces accidental triggering in group conversations",
                            "It publishes lessons automatically",
                            "It turns DMs into public chats",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-channel-cp3",
                        "prompt": "When is session.dmScope per-channel-peer most useful?",
                        "options": [
                            "When multiple people can DM the same bot and you want isolated DM context",
                            "When you want one shared conversation across everyone",
                            "When the gateway has no auth token",
                        ],
                        "answer_index": 0,
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
                        "Channel policy template for a student-facing OpenClaw build.",
                        "text",
                        inspect_prompt="Find the DM policy, the DM scope, and the mention rule. Say what each one protects.",
                        change_prompt="Choose one channel you would enable first and explain why you would keep it on pairing instead of open.",
                    ),
                    _artifact(
                        "lesson_artifacts/openclaw/channels/rollout-checklist.md",
                        "Operator checklist for rolling out a new OpenClaw messaging channel safely.",
                        "text",
                        inspect_prompt="Notice that trusted setup comes before wider access. Explain why that order matters.",
                        change_prompt="Turn the checklist into a one-channel rollout plan for the first platform you would test.",
                    ),
                ],
            },
            {
                "title": "Agent Safety",
                "slug": "agent-safety",
                "lesson_type": "theory",
                "estimated_minutes": 15,
                "content": """# Agent Safety

OpenClaw's security guide is unusually explicit about its trust model. It assumes a **personal assistant security model**: one trusted operator boundary per gateway. If people are mutually untrusted, the docs say to split them into separate gateways and ideally separate OS users or hosts.

## The official priority order
OpenClaw frames safety in this order:

1. **Identity first** - who can talk to the bot? (`dmPolicy`, allowlists, pairing)
2. **Scope next** - where can it act? (tools, sandboxing, device permissions)
3. **Model last** - assume prompt injection is possible and limit the blast radius

Useful references:
- [OpenClaw GitHub repository](https://github.com/openclaw/openclaw)
- [Gateway security guide](https://docs.openclaw.ai/gateway/security)
- [Sandboxing guide](https://docs.openclaw.ai/gateway/sandboxing)

That matters because prompt guardrails alone are not enough.

## Controls worth teaching in Module 6

### 1. Security audit
Run:

```bash
openclaw security audit
openclaw security audit --deep
openclaw security audit --fix
```

The audit checks DM and group policy, tool blast radius, plugin loading, network exposure, browser control, filesystem hygiene, and other common failure modes.

### 2. Sandbox non-main sessions
The official README calls out `agents.defaults.sandbox.mode: "non-main"` as the standard way to keep non-main sessions away from full host access.

### 3. Tight tool policy
For untrusted content or shared rooms, the docs recommend denying powerful control-plane tools such as `gateway`, `cron`, `sessions_spawn`, and `sessions_send` by default unless you truly need them.

### 4. Network posture
Keep the gateway on loopback or a tightly controlled remote path. Do not expose it broadly and unauthenticated.

### 5. Skills and plugins
Treat third-party skills and plugins as untrusted code until you review or verify them.

## The safety lesson in one sentence
OpenClaw safety is not "be careful". It is pairing, allowlists, sandboxing, tool scope, and auditability working together.

## Definition of done
You are done when you can explain which OpenClaw control handles identity, which handles tool blast radius, and which handles post-incident review.
""",
                "ai_tutor_prompt": _ai_tutor_prompt(
                    "Agent Safety",
                    "an OpenClaw hardening baseline and audit plan",
                    "the official trust model, security audit workflow, sandboxing, and tool-scope controls",
                ),
                "questions": [
                    {
                        "id": "openclaw-safety-q1",
                        "prompt": "You invite a second person to share your OpenClaw gateway. The docs warn this creates risk. What specifically could go wrong?",
                        "options": [
                            "They can trigger tools under your authority, see shared conversation context, and potentially cause your agent to act on your files without your knowledge",
                            "Nothing — OpenClaw automatically isolates all users on a shared gateway",
                            "Only if they know your API key — the gateway auth prevents any other access",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-safety-q2",
                        "prompt": "Your teammate wants to add a strong system prompt to prevent misuse. You want to add sandboxing and allowlists. Who is right?",
                        "options": [
                            "Both are useful, but OpenClaw docs put hard controls (identity, scope, sandboxing) before prompt tuning — a strong prompt alone is not enough",
                            "The teammate — a strong prompt is sufficient and sandboxing adds unnecessary complexity",
                            "You — prompts have no effect on agent safety at all",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-safety-q3",
                        "prompt": "You run openclaw security audit and it flags 'DM policy open + tools enabled.' What should you do first?",
                        "options": [
                            "Lock down the DM policy first — the audit priority order says open access plus tools enabled is the highest risk combination to address",
                            "Ignore it — open DMs are fine if the prompt tells the agent to be careful",
                            "Disable all tools immediately and add them back one at a time before changing the DM policy",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-safety-q4",
                        "prompt": "You want to share your agent with a small team but do not want their sessions to access your main workspace files. Which setting handles this?",
                        "options": [
                            "agents.defaults.sandbox.mode: 'non-main' — this sandboxes all non-main sessions away from full host access",
                            "gateway.bind: 'public' — opening the gateway publicly applies sandboxing automatically",
                            "channels.slack.dmPolicy: 'open' — open DMs separate session contexts",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-safety-q5",
                        "prompt": "A student says: 'If my prompt is strong enough, I do not need to worry about who can message the bot.' What would you tell them?",
                        "options": [
                            "Prompts can be bypassed — identity controls (who can talk to the bot) must be set independently of how the model is instructed to behave",
                            "Agree — a strong enough system prompt makes identity controls redundant",
                            "It depends on which AI model you are using",
                        ],
                        "answer_index": 0,
                    },
                ],
                "guided_blocks": [
                    {
                        "title": "What OpenClaw assumes",
                        "body": "OpenClaw's security guide assumes one trusted operator boundary per gateway. That means it is designed like a personal assistant first, not like a hostile multi-tenant system.",
                        "analogy": "Think of one gateway like one house with one trusted household. If two groups do not trust each other, they should not share the same keys, rooms, and rules.",
                    },
                    {
                        "title": "Identity first, scope next, model last",
                        "body": "The official order is simple:\n\n1. decide who can talk to the bot\n2. decide where it can act\n3. only then think about model behavior\n\nThat is why pairing, allowlists, sandboxing, and tool policy matter more than motivational safety text.",
                        "remember": "A strong prompt is helpful, but it is not a permission system.",
                    },
                    {
                        "title": "Audit and sandbox before trust",
                        "body": "OpenClaw gives you a real hardening tool: `openclaw security audit`. The docs also recommend sandboxing non-main sessions, limiting risky tools, and keeping the gateway private unless you intentionally widen exposure.",
                        "artifact_paths": [
                            "lesson_artifacts/openclaw/safety/hardened-openclaw.json5",
                            "lesson_artifacts/openclaw/safety/security-audit-runbook.md",
                        ],
                        "try_this": [
                            "Read the audit runbook and list the first two things you would check on a fresh setup.",
                            "Explain why non-main sandboxing matters before you invite other people into the workflow.",
                        ],
                        "checkpoint_after": True,
                    },
                    {
                        "title": "When to split the setup",
                        "body": "If people are mutually untrusted, the docs recommend separate gateways and ideally separate OS users or hosts. That is the cleanest way to avoid shared authority problems.",
                        "remember": "The moment trust boundaries change, the deployment shape may need to change too.",
                    },
                    {
                        "title": "Common mistake",
                        "body": "The most common mistake here is believing a strong system prompt is enough protection. The OpenClaw docs say otherwise: identity, scope, sandboxing, and auditability come before model trust. If those are weak, the prompt does not save you.",
                        "remember": "A prompt is guidance. A permission boundary is enforcement.",
                    },
                    {
                        "title": "Teach it back",
                        "body": "Teach this lesson back using the shortest possible format: who can talk, where it can act, how it is contained, and how you investigate after something goes wrong. If you can name those four categories, you are thinking like an operator instead of a spectator.",
                        "try_this": [
                            "Explain 'identity first, scope next, model last' without using security jargon.",
                            "Name one control for identity, one for scope, and one for post-incident review.",
                        ],
                    },
                ],
                "checkpoint_questions": [
                    {
                        "id": "openclaw-safety-cp1",
                        "prompt": "What trust model does the OpenClaw security guide assume by default?",
                        "options": [
                            "One trusted operator boundary per gateway",
                            "A public hostile multi-tenant gateway",
                            "Any channel is safe if the model is strong enough",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-safety-cp2",
                        "prompt": "What comes before model behavior in OpenClaw's security order?",
                        "options": [
                            "Identity and scope",
                            "Avatar design and themes",
                            "Longer recap quizzes",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "openclaw-safety-cp3",
                        "prompt": "What command family helps you inspect and harden an OpenClaw deployment?",
                        "options": [
                            "openclaw security audit",
                            "openclaw message send",
                            "openclaw skills publish",
                        ],
                        "answer_index": 0,
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
                    {"action": "gateway", "level": "review", "reason": "persistent control-plane mutations should not be casual"},
                    {"action": "cron", "level": "review", "reason": "scheduled workflows persist beyond one chat turn"},
                    {"action": "public_exposure_change", "level": "deny", "reason": "outside Module 6 lesson scope"},
                ],
                "evaluation_rubric": [],
                "evaluation_cases": [],
                "artifacts": [
                    _artifact(
                        "lesson_artifacts/openclaw/safety/hardened-openclaw.json5",
                        "Hardened baseline config adapted from the official OpenClaw security guidance.",
                        "text",
                        inspect_prompt="Find the gateway bind, auth mode, exec security, and DM scope. Explain what each one protects.",
                        change_prompt="Pick one line that makes the setup safer for a beginner and explain why you would keep it in place.",
                    ),
                    _artifact(
                        "lesson_artifacts/openclaw/safety/security-audit-runbook.md",
                        "Runbook for auditing an OpenClaw deployment before trusting it with real channel access.",
                        "text",
                        inspect_prompt="Look at the audit order and identify which checks happen before model selection is even discussed.",
                        change_prompt="Turn the runbook into a short spoken checklist you could use before inviting a real user into the system.",
                    ),
                ],
            },
        ],
    },
    {
        "title": "Module 8: Capstone — Safety & Evaluation",
        "slug": "module-8-capstone-safety-evaluation",
        "description": "Turn the OpenClaw build into a reviewable capstone with automation patterns, concrete guardrails, permission scope, and a multi-method evaluation stack.",
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
                "title": "Automation Examples",
                "slug": "automation-examples",
                "lesson_type": "theory",
                "estimated_minutes": 12,
                "content": """# Automation Examples

OpenClaw's 2026.6 documentation treats automation as more than a cron job. The current path includes **Task Flow**, **webhooks**, and the unified `openclaw infer` CLI for model, media, and web work. That means a good capstone automation should be framed as a workflow, not just a clever prompt.

## Three OpenClaw-shaped automation examples
1. **Webhook -> review flow**: an external event triggers the gateway, drafts an artifact, and routes it to review.
2. **Scheduled audit flow**: a timed run executes `openclaw security audit`, captures the result, and opens a remediation checklist.
3. **Content QA flow**: a lesson draft enters a rubric pass, then either escalates to review or returns with revision notes.

## What a capstone automation brief needs
- **Trigger**: what starts the workflow?
- **Inputs**: what data or message enters the system?
- **Tools or channels**: what OpenClaw surface is being used?
- **Review boundary**: where does a human need to approve or inspect?
- **Receipt**: what proves the run actually happened?

## Capstone rule
If the workflow cannot explain where review happens, it is not ready for release.

## Definition of done
You are done when your automation example reads like a small system design, not like a prompt trick.
""",
                "ai_tutor_prompt": _ai_tutor_prompt(
                    "Automation Examples",
                    "a capstone automation brief",
                    "Task Flow and webhook thinking, explicit triggers, and clear human review boundaries",
                ),
                "questions": [
                    {
                        "id": "capstone-automation-q1",
                        "prompt": "Which OpenClaw concepts make automation in this capstone more than just a one-off prompt?",
                        "options": [
                            "Task Flow, webhooks, and explicit review boundaries",
                            "Only a decorative dashboard",
                            "A larger font size in the UI",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-automation-q2",
                        "prompt": "Which automation example best matches a timed OpenClaw hardening workflow?",
                        "options": [
                            "A scheduled security-audit flow",
                            "A theme toggle",
                            "A manual screenshot rename",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-automation-q3",
                        "prompt": "What must every capstone automation brief name besides the trigger?",
                        "options": [
                            "Inputs, review boundary, and receipt",
                            "Only the preferred UI color",
                            "Nothing if the model is strong enough",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-automation-q4",
                        "prompt": "What makes an automation example release-ready in this lesson?",
                        "options": [
                            "It explains where automation stops and review begins",
                            "It hides the workflow behind one slash command",
                            "It removes all manual checkpoints",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-automation-q5",
                        "prompt": "How should this lesson describe a strong automation example overall?",
                        "options": [
                            "As a small system design, not a prompt trick",
                            "As a purely decorative demo",
                            "As a way to skip testing",
                        ],
                        "answer_index": 0,
                    },
                ],
                "guided_blocks": [
                    {
                        "title": "Why automation matters here",
                        "body": "For beginners, automation can sound magical. In this capstone, treat it as a repeatable workflow: something starts the work, the system does a bounded set of steps, and a human still knows where to review it.",
                        "analogy": "Think of automation like an assembly line with a quality-control checkpoint, not like a self-driving mystery box.",
                    },
                    {
                        "title": "The shape of a good workflow",
                        "body": "A strong OpenClaw automation says what triggers it, what inputs it reads, what surface it uses, where review happens, and what receipt proves the run occurred. If one of those is missing, the workflow is harder to trust.",
                        "artifact_paths": [
                            "lesson_artifacts/capstone/automation-brief.template.md",
                            "lesson_artifacts/capstone/task-flow-sequence.md",
                        ],
                        "try_this": [
                            "Read the automation brief template below and point to the trigger, review boundary, and receipt path sections.",
                            "Say which of those three is easiest for you to forget and why.",
                        ],
                        "checkpoint_after": True,
                    },
                    {
                        "title": "Common mistake",
                        "body": "A common beginner mistake is describing automation as 'the model will just handle it.' That hides the trigger, the tools, and the review step. Good automation descriptions are mechanical enough that another person could follow them.",
                        "remember": "If you cannot draw the workflow in steps, you probably do not understand it yet.",
                    },
                    {
                        "title": "Teach it back",
                        "body": "Explain the webhook-to-review example to a classmate in four parts: what starts it, what it does, where a person checks it, and what evidence the run leaves behind.",
                        "try_this": [
                            "Use the phrase 'trigger, action, review, receipt' in your explanation.",
                        ],
                    },
                ],
                "checkpoint_questions": [
                    {
                        "id": "capstone-automation-cp1",
                        "prompt": "What makes the capstone automation concrete instead of vague?",
                        "options": [
                            "It names the trigger, inputs, review boundary, and receipt",
                            "It uses more hype words",
                            "It hides the workflow behind one sentence",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-automation-cp2",
                        "prompt": "Which OpenClaw automation example best matches a timed hardening workflow?",
                        "options": [
                            "A scheduled security-audit flow",
                            "A theme switcher",
                            "A badge color update",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-automation-cp3",
                        "prompt": "Why is a review boundary important in an automation workflow?",
                        "options": [
                            "It shows where automation stops and a human judgment step begins",
                            "It removes the need for receipts",
                            "It guarantees no failure can happen",
                        ],
                        "answer_index": 0,
                    },
                ],
                "guided_blocks": [
                    {
                        "title": "Why automation matters here",
                        "body": "For beginners, automation can sound magical. In this capstone, treat it as a repeatable workflow: something starts the work, the system does a bounded set of steps, and a human still knows where to review it.",
                        "analogy": "Think of automation like an assembly line with a quality-control checkpoint, not like a self-driving mystery box.",
                    },
                    {
                        "title": "The shape of a good workflow",
                        "body": "A strong OpenClaw automation says what triggers it, what inputs it reads, what surface it uses, where review happens, and what receipt proves the run occurred. If one of those is missing, the workflow is harder to trust.",
                        "artifact_paths": [
                            "lesson_artifacts/capstone/automation-brief.template.md",
                            "lesson_artifacts/capstone/task-flow-sequence.md",
                        ],
                        "try_this": [
                            "Read the automation brief template below and point to the trigger, review boundary, and receipt path sections.",
                            "Say which of those three is easiest for you to forget and why.",
                        ],
                        "checkpoint_after": True,
                    },
                    {
                        "title": "Common mistake",
                        "body": "A common beginner mistake is describing automation as 'the model will just handle it.' That hides the trigger, the tools, and the review step. Good automation descriptions are mechanical enough that another person could follow them.",
                        "remember": "If you cannot draw the workflow in steps, you probably do not understand it yet.",
                    },
                    {
                        "title": "Teach it back",
                        "body": "Explain the webhook-to-review example to a classmate in four parts: what starts it, what it does, where a person checks it, and what evidence the run leaves behind.",
                        "try_this": [
                            "Use the phrase 'trigger, action, review, receipt' in your explanation.",
                        ],
                    },
                ],
                "checkpoint_questions": [
                    {
                        "id": "capstone-automation-cp1",
                        "prompt": "What makes the capstone automation concrete instead of vague?",
                        "options": [
                            "It names the trigger, inputs, review boundary, and receipt",
                            "It uses more hype words",
                            "It hides the workflow behind one sentence",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-automation-cp2",
                        "prompt": "Which OpenClaw automation example best matches a timed hardening workflow?",
                        "options": [
                            "A scheduled security-audit flow",
                            "A theme switcher",
                            "A badge color update",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-automation-cp3",
                        "prompt": "Why is a review boundary important in an automation workflow?",
                        "options": [
                            "It shows where automation stops and a human judgment step begins",
                            "It removes the need for receipts",
                            "It guarantees no failure can happen",
                        ],
                        "answer_index": 0,
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
                        "Template for writing a capstone automation brief using OpenClaw workflow concepts.",
                        "text",
                    ),
                    _artifact(
                        "lesson_artifacts/capstone/task-flow-sequence.md",
                        "Sequence sketch for an approval-driven OpenClaw automation flow.",
                        "text",
                    )
                ],
            },
            {
                "title": "Guardrails",
                "slug": "guardrails",
                "lesson_type": "theory",
                "estimated_minutes": 12,
                "content": """# Guardrails

This capstone needs two kinds of guardrails at the same time:

1. **Model-level alignment goals** such as being helpful, truthful, and harmless.
2. **OpenClaw runtime controls** such as pairing, allowlists, sandboxing, tool deny lists, and audit receipts.

The research sources matter here. Alignment work frames the model goal as **helpful, truthful, and harmless (HHH)**. The OpenClaw security guide makes a different but compatible point: prompt guardrails alone are not enough, so hard controls must limit blast radius.

## A practical capstone guardrail stack
- **Helpful**: the workflow should still move the task forward.
- **Truthful**: the workflow should separate supported claims from guesses.
- **Harmless**: the workflow should deny, sandbox, or escalate risky actions.
- **Operational**: the workflow should keep receipts, approvals, and review notes.

## Translate slogans into controls
If a capstone says "we are safe," it must point to something concrete such as:

- `dmPolicy: "pairing"`
- a sandbox setting
- a tool deny list
- a verifier check
- a reviewer step
- a logged audit receipt

## Capstone rule
Every guardrail claim must map to a runtime control, an evaluation rule, or a human review step.

## Definition of done
You are done when the capstone can explain both the value-level goal (HHH) and the runtime-level enforcement that backs it.
""",
                "ai_tutor_prompt": _ai_tutor_prompt(
                    "Guardrails",
                    "a concrete guardrail matrix for the capstone",
                    "how HHH goals map to OpenClaw runtime controls, review steps, and evaluation rules",
                ),
                "questions": [
                    {
                        "id": "capstone-guardrails-q1",
                        "prompt": "Which trio comes from the alignment literature used for this capstone's safety framing?",
                        "options": [
                            "Helpful, truthful, harmless",
                            "Fast, glossy, autonomous",
                            "Public, shared, unsandboxed",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-guardrails-q2",
                        "prompt": "What is the OpenClaw security guide's main objection to prompt-only guardrails?",
                        "options": [
                            "They do not replace hard controls like pairing, tool policy, and sandboxing",
                            "They are stronger than runtime controls",
                            "They remove the need for audit logs",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-guardrails-q3",
                        "prompt": "Which of these is the best example of a concrete capstone guardrail?",
                        "options": [
                            "dmPolicy pairing plus a tool deny list for untrusted rooms",
                            "A promise that the model is careful",
                            "A larger progress bar",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-guardrails-q4",
                        "prompt": "What must every guardrail claim map to in this lesson?",
                        "options": [
                            "A runtime control, evaluation rule, or human review step",
                            "Only a design preference",
                            "Only a course badge",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-guardrails-q5",
                        "prompt": "What marks the guardrails lesson as complete?",
                        "options": [
                            "The capstone can explain both the HHH goal and the concrete runtime enforcement behind it",
                            "The capstone says safety is important but shows no controls",
                            "The workflow has no human review point",
                        ],
                        "answer_index": 0,
                    },
                ],
                "guided_blocks": [
                    {
                        "title": "Two layers of safety",
                        "body": "This lesson combines two ideas students often confuse: the model should be helpful, truthful, and harmless, but the runtime also needs actual controls such as pairing, sandboxing, and deny lists. One is behavioral intent; the other is enforcement.",
                        "analogy": "Think of HHH as the driver's values and runtime controls as the brakes, doors, and seatbelts.",
                    },
                    {
                        "title": "From slogan to control",
                        "body": "A statement like 'our agent is safe' is weak unless you can point to a real mechanism such as `dmPolicy: pairing`, a sandbox rule, a verifier, or a reviewer step.",
                        "artifact_paths": ["lesson_artifacts/capstone/guardrail-matrix.md"],
                        "try_this": [
                            "Look at the guardrail matrix artifact and pick one row that turns a vague safety claim into a concrete control.",
                            "Explain why that row is stronger than just saying 'be careful'.",
                        ],
                        "checkpoint_after": True,
                    },
                    {
                        "title": "Common mistake",
                        "body": "The most common mistake is believing that a powerful model does not need a strict runtime. In practice, better models still need tight boundaries when tools, files, or public channels are involved.",
                        "remember": "Strong models reduce some problems. They do not erase the need for controls.",
                    },
                    {
                        "title": "Teach it back",
                        "body": "Teach the difference between HHH and runtime enforcement to someone else. Your explanation should name one value-level goal and one mechanism that actually enforces it in OpenClaw.",
                        "try_this": [
                            "Give one HHH example and one OpenClaw runtime control that supports it.",
                        ],
                    },
                ],
                "checkpoint_questions": [
                    {
                        "id": "capstone-guardrails-cp1",
                        "prompt": "Which trio comes from the alignment framing used in this lesson?",
                        "options": [
                            "Helpful, truthful, harmless",
                            "Fast, loud, autonomous",
                            "Public, shared, unsandboxed",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-guardrails-cp2",
                        "prompt": "Why is `dmPolicy: pairing` a stronger guardrail than a vague warning to the model?",
                        "options": [
                            "Because it actually changes who can reach the bot",
                            "Because it makes the prompt longer",
                            "Because it improves the font styling",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-guardrails-cp3",
                        "prompt": "What should every safety claim map to in this capstone?",
                        "options": [
                            "A runtime control, evaluation rule, or human review step",
                            "A badge only",
                            "A design preference only",
                        ],
                        "answer_index": 0,
                    },
                ],
                "guided_blocks": [
                    {
                        "title": "Two layers of safety",
                        "body": "This lesson combines two ideas students often confuse: the model should be helpful, truthful, and harmless, but the runtime also needs actual controls such as pairing, sandboxing, and deny lists. One is behavioral intent; the other is enforcement.",
                        "analogy": "Think of HHH as the driver's values and runtime controls as the brakes, doors, and seatbelts.",
                    },
                    {
                        "title": "From slogan to control",
                        "body": "A statement like 'our agent is safe' is weak unless you can point to a real mechanism such as `dmPolicy: pairing`, a sandbox rule, a verifier, or a reviewer step.",
                        "artifact_paths": ["lesson_artifacts/capstone/guardrail-matrix.md"],
                        "try_this": [
                            "Look at the guardrail matrix artifact and pick one row that turns a vague safety claim into a concrete control.",
                            "Explain why that row is stronger than just saying 'be careful'.",
                        ],
                        "checkpoint_after": True,
                    },
                    {
                        "title": "Common mistake",
                        "body": "The most common mistake is believing that a powerful model does not need a strict runtime. In practice, better models still need tight boundaries when tools, files, or public channels are involved.",
                        "remember": "Strong models reduce some problems. They do not erase the need for controls.",
                    },
                    {
                        "title": "Teach it back",
                        "body": "Teach the difference between HHH and runtime enforcement to someone else. Your explanation should name one value-level goal and one mechanism that actually enforces it in OpenClaw.",
                        "try_this": [
                            "Give one HHH example and one OpenClaw runtime control that supports it.",
                        ],
                    },
                ],
                "checkpoint_questions": [
                    {
                        "id": "capstone-guardrails-cp1",
                        "prompt": "Which trio comes from the alignment framing used in this lesson?",
                        "options": [
                            "Helpful, truthful, harmless",
                            "Fast, loud, autonomous",
                            "Public, shared, unsandboxed",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-guardrails-cp2",
                        "prompt": "Why is `dmPolicy: pairing` a stronger guardrail than a vague warning to the model?",
                        "options": [
                            "Because it actually changes who can reach the bot",
                            "Because it makes the prompt longer",
                            "Because it improves the font styling",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-guardrails-cp3",
                        "prompt": "What should every safety claim map to in this capstone?",
                        "options": [
                            "A runtime control, evaluation rule, or human review step",
                            "A badge only",
                            "A design preference only",
                        ],
                        "answer_index": 0,
                    },
                ],
                "skill_templates": [],
                "channel_templates": [],
                "safety_checks": [
                    "Map HHH goals to runtime controls",
                    "Reject prompt-only safety claims with no enforcement path",
                    "Keep an audit path for review decisions",
                ],
                "permission_matrix": [],
                "evaluation_rubric": [
                    {"criterion": "helpfulness", "weight": 2, "description": "The workflow still moves the user toward a useful result."},
                    {"criterion": "truthfulness", "weight": 3, "description": "Claims are grounded, and unknowns are labeled clearly."},
                    {"criterion": "harmlessness", "weight": 3, "description": "Risky actions are denied, sandboxed, or escalated."},
                    {"criterion": "operational_control", "weight": 2, "description": "The runtime control backing each guardrail is named explicitly."},
                ],
                "evaluation_cases": [],
                "artifacts": [
                    _artifact(
                        "lesson_artifacts/capstone/guardrail-matrix.md",
                        "Matrix that maps capstone guardrail claims to concrete OpenClaw enforcement points.",
                        "text",
                    )
                ],
            },
            {
                "title": "Permissions",
                "slug": "permissions",
                "lesson_type": "theory",
                "estimated_minutes": 10,
                "content": """# Permissions

Permissions are where a capstone stops being inspirational and starts being real. OpenClaw's README says the default `main` session can run tools on the host when it is just you. The same docs then recommend sandboxing non-main sessions and denying powerful control-plane tools for untrusted contexts.

## The permission question set
- Which actions are safe to allow automatically?
- Which actions need review every time?
- Which actions are out of scope for this workflow?
- Which actions change persistent state beyond one chat turn?

## OpenClaw-specific actions to classify
- `exec` / shell access
- `browser`
- `gateway` config mutation
- `cron` job creation
- `sessions_spawn` and `sessions_send`
- publishing or distribution actions in your own workflow

## Least privilege in this capstone
Use the smallest authority that still allows the workflow to do useful work. In practice that means:

- allow read-like or drafting steps when they are required
- review persistent control-plane changes
- deny actions that widen exposure or destroy audit history

## Definition of done
You are done when a reviewer can predict the decision for a risky action before the system runs it.
""",
                "ai_tutor_prompt": _ai_tutor_prompt(
                    "Permissions",
                    "a capstone OpenClaw permission matrix",
                    "classifying runtime, control-plane, and publish actions into allow, review, or deny with reasons",
                ),
                "questions": [
                    {
                        "id": "capstone-permissions-q1",
                        "prompt": "What principle should drive the capstone permission model?",
                        "options": [
                            "Least privilege",
                            "Maximum access by default",
                            "No written permissions",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-permissions-q2",
                        "prompt": "Which OpenClaw actions deserve special scrutiny because they can change state beyond one chat turn?",
                        "options": [
                            "gateway and cron",
                            "Markdown headings and badge icons",
                            "Only lesson titles",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-permissions-q3",
                        "prompt": "Why should a permission entry be action-based and explicit?",
                        "options": [
                            "Because reviewers need to know exactly what is being allowed, reviewed, or denied",
                            "Because explicit permissions make the UI prettier",
                            "Because permissions should never mention tools",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-permissions-q4",
                        "prompt": "Which choice best matches the capstone's deny category?",
                        "options": [
                            "Widening exposure or deleting audit history",
                            "Reading the current lesson markdown",
                            "Checking a rubric score",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-permissions-q5",
                        "prompt": "What marks the permissions lesson as complete?",
                        "options": [
                            "A reviewer can predict the decision for a risky action before the system runs it",
                            "Every action is automatically allowed",
                            "The matrix is replaced with a paragraph",
                        ],
                        "answer_index": 0,
                    },
                ],
                "guided_blocks": [
                    {
                        "title": "Why permissions matter",
                        "body": "Permissions are where the workflow becomes believable. If everything is allowed by default, the capstone cannot prove it understands risk. A permission model should tell you what is okay, what needs review, and what is out of scope.",
                        "analogy": "Think of permissions like color-coded doors: some open freely, some need a key from a supervisor, and some stay locked no matter how urgent the request sounds.",
                    },
                    {
                        "title": "The OpenClaw actions that matter",
                        "body": "In this lesson, the important actions are not abstract. They are real OpenClaw surfaces such as `gateway`, `cron`, `sessions_spawn`, and tool execution. These are the places where least privilege becomes visible.",
                        "artifact_paths": ["lesson_artifacts/capstone/permission-review.template.json"],
                        "try_this": [
                            "Look at the permission matrix artifact and find one action that should be reviewed and one that should be denied.",
                            "Explain why the two actions belong in different categories.",
                        ],
                        "checkpoint_after": True,
                    },
                    {
                        "title": "Common mistake",
                        "body": "A common mistake is writing permissions in vague sentences like 'be careful with admin actions.' That is too soft. Good permission entries are action-based, explicit, and easy for another reviewer to audit.",
                        "remember": "If the action is not named, the boundary is probably too fuzzy.",
                    },
                    {
                        "title": "Teach it back",
                        "body": "Teach the permission model back by giving one example of an allow action, one review action, and one deny action from this capstone.",
                        "try_this": [
                            "Use the words allow, review, and deny in your explanation.",
                        ],
                    },
                ],
                "checkpoint_questions": [
                    {
                        "id": "capstone-permissions-cp1",
                        "prompt": "What principle should drive this permission model?",
                        "options": [
                            "Least privilege",
                            "Maximum access",
                            "No written permissions",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-permissions-cp2",
                        "prompt": "Why do actions like gateway and cron deserve extra scrutiny?",
                        "options": [
                            "Because they can change state beyond one chat turn",
                            "Because they are decorative UI features",
                            "Because they only affect quiz scores",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-permissions-cp3",
                        "prompt": "What makes a permission entry strong?",
                        "options": [
                            "It names a specific action, a level, and a reason",
                            "It says trust the model",
                            "It avoids mentioning tools",
                        ],
                        "answer_index": 0,
                    },
                ],
                "guided_blocks": [
                    {
                        "title": "Why permissions matter",
                        "body": "Permissions are where the workflow becomes believable. If everything is allowed by default, the capstone cannot prove it understands risk. A permission model should tell you what is okay, what needs review, and what is out of scope.",
                        "analogy": "Think of permissions like color-coded doors: some open freely, some need a key from a supervisor, and some stay locked no matter how urgent the request sounds.",
                    },
                    {
                        "title": "The OpenClaw actions that matter",
                        "body": "In this lesson, the important actions are not abstract. They are real OpenClaw surfaces such as `gateway`, `cron`, `sessions_spawn`, and tool execution. These are the places where least privilege becomes visible.",
                        "artifact_paths": ["lesson_artifacts/capstone/permission-review.template.json"],
                        "try_this": [
                            "Look at the permission matrix artifact and find one action that should be reviewed and one that should be denied.",
                            "Explain why the two actions belong in different categories.",
                        ],
                        "checkpoint_after": True,
                    },
                    {
                        "title": "Common mistake",
                        "body": "A common mistake is writing permissions in vague sentences like 'be careful with admin actions.' That is too soft. Good permission entries are action-based, explicit, and easy for another reviewer to audit.",
                        "remember": "If the action is not named, the boundary is probably too fuzzy.",
                    },
                    {
                        "title": "Teach it back",
                        "body": "Teach the permission model back by giving one example of an allow action, one review action, and one deny action from this capstone.",
                        "try_this": [
                            "Use the words allow, review, and deny in your explanation.",
                        ],
                    },
                ],
                "checkpoint_questions": [
                    {
                        "id": "capstone-permissions-cp1",
                        "prompt": "What principle should drive this permission model?",
                        "options": [
                            "Least privilege",
                            "Maximum access",
                            "No written permissions",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-permissions-cp2",
                        "prompt": "Why do actions like gateway and cron deserve extra scrutiny?",
                        "options": [
                            "Because they can change state beyond one chat turn",
                            "Because they are decorative UI features",
                            "Because they only affect quiz scores",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-permissions-cp3",
                        "prompt": "What makes a permission entry strong?",
                        "options": [
                            "It names a specific action, a level, and a reason",
                            "It says trust the model",
                            "It avoids mentioning tools",
                        ],
                        "answer_index": 0,
                    },
                ],
                "skill_templates": [],
                "channel_templates": [],
                "safety_checks": [
                    "Least privilege by action",
                    "Persistent control-plane actions require review",
                ],
                "permission_matrix": [
                    {"action": "draft_content", "level": "allow", "reason": "core lesson authoring work"},
                    {"action": "score_against_rubric", "level": "allow", "reason": "evaluation pre-check for release"},
                    {"action": "gateway", "level": "review", "reason": "persistent gateway changes alter the control plane"},
                    {"action": "cron", "level": "review", "reason": "scheduled jobs survive the original chat turn"},
                    {"action": "delete_history", "level": "deny", "reason": "audit history must stay intact"},
                    {"action": "public_exposure_change", "level": "deny", "reason": "capstone should not widen exposure to untrusted users"},
                ],
                "evaluation_rubric": [],
                "evaluation_cases": [],
                "artifacts": [
                    _artifact(
                        "lesson_artifacts/capstone/permission-review.template.json",
                        "Permission matrix template for the capstone release path using OpenClaw-specific action categories.",
                        "json",
                    )
                ],
            },
            {
                "title": "Testing",
                "slug": "testing",
                "lesson_type": "interactive",
                "estimated_minutes": 15,
                "content": """# Testing

This capstone should not use one evaluation method and pretend that is enough. The research material for this module points to a **stack** of evaluation approaches:

1. **Multiple-choice checks** - quick, standardized knowledge checks.
2. **Verifiers** - deterministic checks for things that can be objectively verified.
3. **Human or preference review** - useful when comparing free-form outputs or release candidates.
4. **LLM-as-a-judge** - rubric-based scoring for free-form explanations and artifacts.

## How that maps onto this capstone

### 1. Recap quiz
Use the lesson quiz to verify the student actually knows the terms and control surfaces.

### 2. Deterministic verifiers
Use hard checks for things like:

- artifact files exist
- expected config fields are present
- `openclaw security audit` passes the intended threshold
- required permission entries exist

### 3. Human review
Have a human reviewer compare release candidates when the question is "which explanation, workflow, or rollout plan is better?" rather than "is this JSON valid?"

### 4. LLM-as-a-judge
Use a scoring rubric when the output is free-form but still evaluable: clarity, correctness, safety reasoning, and release readiness.

## Best-practice takeaway
The evaluation source material is clear: **there is no single best evaluation method**. Strong evaluation combines methods that match the real task.

## Definition of done
You are done when the capstone can name which part is tested by quiz, which by verifier, which by human review, and which by an LLM judge.
""",
                "ai_tutor_prompt": _ai_tutor_prompt(
                    "Testing",
                    "a capstone evaluation stack and release test plan",
                    "how to combine quizzes, verifiers, human review, and LLM-as-a-judge into one credible release gate",
                ),
                "questions": [
                    {
                        "id": "capstone-testing-q1",
                        "prompt": "Which evaluation method is best for deterministic checks like 'does this artifact file exist'?",
                        "options": [
                            "Verifier-based evaluation",
                            "Preference leaderboard only",
                            "UI theme review",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-testing-q2",
                        "prompt": "Which method is useful when you want rubric-based scoring of a free-form explanation?",
                        "options": [
                            "LLM-as-a-judge",
                            "Only a file existence check",
                            "Only a CSS snapshot",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-testing-q3",
                        "prompt": "Why should this capstone combine multiple evaluation approaches instead of picking one?",
                        "options": [
                            "Because different parts of the workflow need different kinds of evidence",
                            "Because quizzes can replace all runtime checks",
                            "Because one model score is always enough",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-testing-q4",
                        "prompt": "Which evaluation layer is most appropriate for comparing two release candidates on overall quality and style?",
                        "options": [
                            "Human or preference-based review",
                            "Only a JSON schema validator",
                            "Only a port health check",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-testing-q5",
                        "prompt": "What marks this lesson as complete?",
                        "options": [
                            "The capstone can name which part is tested by quiz, verifier, human review, and LLM judge",
                            "Only the recap quiz exists",
                            "The workflow has no negative or adversarial cases",
                        ],
                        "answer_index": 0,
                    },
                ],
                "guided_blocks": [
                    {
                        "title": "Why one test is not enough",
                        "body": "Beginners often want a single score that proves the workflow is good. This lesson teaches the opposite: different parts of the workflow need different kinds of evidence.",
                        "analogy": "Testing a capstone is like checking a bridge. You do not only ask if it looks good. You check the design, the materials, the load, and the failure cases.",
                    },
                    {
                        "title": "The four-layer evaluation stack",
                        "body": "This capstone uses four layers: quiz for concept recall, verifiers for objective checks, human review for comparative judgment, and LLM-as-a-judge for free-form rubric scoring.",
                        "artifact_paths": [
                            "lesson_artifacts/capstone/evaluation-cases.template.json",
                            "lesson_artifacts/capstone/evaluation-plan.md",
                            "lesson_artifacts/capstone/release-readiness-checklist.md",
                        ],
                        "interactive_widget": "capstone_studio",
                        "try_this": [
                            "Match one real capstone artifact to the evaluation layer that should judge it first.",
                            "Explain why a human review and a verifier solve different problems.",
                        ],
                        "checkpoint_after": True,
                    },
                    {
                        "title": "Common mistake",
                        "body": "A common mistake is using only the easiest evaluation method. For example, a file existence check cannot tell you whether an explanation is clear, and a model judge cannot replace every deterministic verifier.",
                        "remember": "Use the method that matches the evidence you need.",
                    },
                    {
                        "title": "Teach it back",
                        "body": "Teach this lesson back by giving one example of what should be checked by quiz, one by verifier, one by human review, and one by an LLM judge.",
                        "try_this": [
                            "Use one sentence for each of the four evaluation layers.",
                        ],
                    },
                ],
                "checkpoint_questions": [
                    {
                        "id": "capstone-testing-cp1",
                        "prompt": "Which method is best for deterministic checks like 'does this file exist'?",
                        "options": [
                            "Verifier-based evaluation",
                            "Preference leaderboard only",
                            "Theme review",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-testing-cp2",
                        "prompt": "Which layer is most appropriate for rubric-based scoring of a free-form explanation?",
                        "options": [
                            "LLM-as-a-judge",
                            "Only a file check",
                            "Only a color audit",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-testing-cp3",
                        "prompt": "Why combine multiple evaluation methods in the capstone?",
                        "options": [
                            "Because different outputs need different kinds of evidence",
                            "Because one method should always be ignored",
                            "Because quizzes can replace all other checks",
                        ],
                        "answer_index": 0,
                    },
                ],
                "guided_blocks": [
                    {
                        "title": "Why one test is not enough",
                        "body": "Beginners often want a single score that proves the workflow is good. This lesson teaches the opposite: different parts of the workflow need different kinds of evidence.",
                        "analogy": "Testing a capstone is like checking a bridge. You do not only ask if it looks good. You check the design, the materials, the load, and the failure cases.",
                    },
                    {
                        "title": "The four-layer evaluation stack",
                        "body": "This capstone uses four layers: quiz for concept recall, verifiers for objective checks, human review for comparative judgment, and LLM-as-a-judge for free-form rubric scoring.",
                        "artifact_paths": [
                            "lesson_artifacts/capstone/evaluation-cases.template.json",
                            "lesson_artifacts/capstone/evaluation-plan.md",
                            "lesson_artifacts/capstone/release-readiness-checklist.md",
                        ],
                        "interactive_widget": "capstone_studio",
                        "try_this": [
                            "Match one real capstone artifact to the evaluation layer that should judge it first.",
                            "Explain why a human review and a verifier solve different problems.",
                        ],
                        "checkpoint_after": True,
                    },
                    {
                        "title": "Common mistake",
                        "body": "A common mistake is using only the easiest evaluation method. For example, a file existence check cannot tell you whether an explanation is clear, and a model judge cannot replace every deterministic verifier.",
                        "remember": "Use the method that matches the evidence you need.",
                    },
                    {
                        "title": "Teach it back",
                        "body": "Teach this lesson back by giving one example of what should be checked by quiz, one by verifier, one by human review, and one by an LLM judge.",
                        "try_this": [
                            "Use one sentence for each of the four evaluation layers.",
                        ],
                    },
                ],
                "checkpoint_questions": [
                    {
                        "id": "capstone-testing-cp1",
                        "prompt": "Which method is best for deterministic checks like 'does this file exist'?",
                        "options": [
                            "Verifier-based evaluation",
                            "Preference leaderboard only",
                            "Theme review",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-testing-cp2",
                        "prompt": "Which layer is most appropriate for rubric-based scoring of a free-form explanation?",
                        "options": [
                            "LLM-as-a-judge",
                            "Only a file check",
                            "Only a color audit",
                        ],
                        "answer_index": 0,
                    },
                    {
                        "id": "capstone-testing-cp3",
                        "prompt": "Why combine multiple evaluation methods in the capstone?",
                        "options": [
                            "Because different outputs need different kinds of evidence",
                            "Because one method should always be ignored",
                            "Because quizzes can replace all other checks",
                        ],
                        "answer_index": 0,
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
                    {"criterion": "evaluation_fit", "weight": 2, "description": "The chosen evaluation method matches the kind of output being judged."},
                ],
                "evaluation_cases": [
                    {"name": "positive", "goal": "Well-scoped OpenClaw workflow passes rubric and verifier checks", "expected": "pass"},
                    {"name": "negative", "goal": "Missing evidence or missing controls block release", "expected": "revise"},
                    {"name": "adversarial", "goal": "Review bypass or prompt-injection-style escalation attempt is rejected", "expected": "stop"},
                    {"name": "regression", "goal": "A previously fixed risky configuration stays fixed after later edits", "expected": "pass"},
                ],
                "capstone_assignment": {
                    "title": "Capstone Studio",
                    "summary": "Build a beginner-safe OpenClaw workflow plan, run the verifier, check the rubric, and leave with a pass or revise result.",
                    "sections": [
                        {
                            "key": "goal",
                            "label": "Goal",
                            "prompt": "What job is this workflow supposed to do for a student or operator?",
                            "placeholder": "Example: Review a proposed OpenClaw channel rollout before it is published.",
                            "min_length": 30,
                        },
                        {
                            "key": "trigger",
                            "label": "Trigger",
                            "prompt": "What starts the workflow? Describe the event, message, schedule, or button that kicks it off.",
                            "placeholder": "Example: A scheduled task runs every Monday, or a message arrives in a trusted room.",
                            "min_length": 20,
                        },
                        {
                            "key": "actions",
                            "label": "Action flow",
                            "prompt": "What are the main steps after the trigger fires?",
                            "placeholder": "Example: Read the draft, compare against policy, prepare a review note for a human to check.",
                            "min_length": 40,
                        },
                        {
                            "key": "review_boundary",
                            "label": "Review boundary",
                            "prompt": "Where does a person need to check or approve something before the workflow continues?",
                            "placeholder": "Example: A person approves any change that affects who can reach the bot or which tools are enabled.",
                            "min_length": 25,
                        },
                        {
                            "key": "guardrails",
                            "label": "Guardrails",
                            "prompt": "What safety controls protect this workflow from being misused or going wrong?",
                            "placeholder": "Example: Unknown senders cannot trigger it, risky tool access is blocked, and every run leaves a log.",
                            "min_length": 25,
                        },
                        {
                            "key": "permissions",
                            "label": "Permissions",
                            "prompt": "For each type of action, is it allowed automatically, does it need approval, or is it blocked entirely?",
                            "placeholder": "Example: Reading and drafting happen automatically. Changing gateway settings needs a person to approve. Exposing the bot publicly is blocked.",
                            "min_length": 35,
                        },
                        {
                            "key": "evidence",
                            "label": "Receipts and evidence",
                            "prompt": "How do you prove the workflow ran correctly and how would you investigate if something went wrong?",
                            "placeholder": "Example: The run produces a log entry and a review note that a person can inspect afterward.",
                            "min_length": 25,
                        },
                    ],
                    "review_questions": [
                        "Would I trust this workflow to run if a new student misunderstood one step?",
                        "Did I name a human review point before any risky or persistent change?",
                        "Can I point to at least one receipt or verifier result that proves success?",
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
                        "Evaluation case library for capstone validation.",
                        "json",
                    ),
                    _artifact(
                        "lesson_artifacts/capstone/evaluation-plan.md",
                        "Evaluation plan that ties capstone checks to quiz, verifier, human review, and LLM-judge layers.",
                        "text",
                    ),
                    _artifact(
                        "lesson_artifacts/capstone/release-readiness-checklist.md",
                        "Final release checklist for the capstone review.",
                        "text",
                    ),
                ],
            },
        ],
    },
]


def get_mission_packs() -> list[dict]:
    return deepcopy(MISSION_PACKS)