# The Safety Sweep

*Lesson 4 of 4 · about 12 minutes · the module's closing move: one command that checks everything.*

Here is a secret about this module: **you have been doing safety work since Lesson 1.** A health check after every change. Recipe cards you can read. Doors locked by default. This final lesson hands you the tool that confirms it, and names the thinking behind what you already built.

## Safety is a shape, not a mood

OpenClaw orders protections like the layers of a house:

1. **Who can talk to it**: the doors. Pairing, allowlists. *(You built this in Lesson 3.)*
2. **Where it can act**: the rooms. Which tools are granted, what stays off-limits. *(Lessons 1 and 2.)*
3. **How it behaves**: the person inside. The model and its instructions, last.

The order is quietly liberating: **the locks do not depend on anyone's behavior.** A door on pairing holds whether the model has a good day or a bad one, whether you are watching or asleep. Settings, not promises, decide what can actually happen.

## The auditor: one command instead of a worry list

```bash
openclaw security audit
```

The audit walks the whole building (door policies, tool grants, network posture, plugin trust, and more) against the official checklist, and reports back. You do not need to know the full list of what it checks. The checklist lives in the tool, so it never has to live in your head.

The rhythm that makes it work:

> **Change something. Run the audit. Fix what it flags. Done.**

When the audit passes, you are entitled to believe it. Running it a second time on an unchanged system tells you nothing new: same system in, same answer out. Once per change is the whole discipline.

Two variants for later, no action needed now: `--deep` looks harder (worth it before sharing access more widely) and `--fix` applies safe corrections itself.

## Two boundaries worth naming once

- **Guest rooms don't get the master key.** The setting `sandbox.mode: "non-main"` keeps any session that is not your own main one inside a limited sandbox, away from full access to your computer.
- **One household per home.** OpenClaw is a personal assistant: one gateway assumes one trusted operator, you. If two people who do not fully trust each other want assistants, they get two separate gateways. No action needed; it is just the boundary, named.

## Done means done, lesson and module

You are done when you can name: one control for who can talk (pairing), one for where it can act (sandbox), and the command that checks the whole building (the audit).

And with that, **Module 6 is complete.** Your assistant has a home, three skills, one carefully opened door, and a standing auditor. Everything waits patiently in config files; nothing degrades overnight. Module 8 is where you decide, with evidence, to trust it with real work.