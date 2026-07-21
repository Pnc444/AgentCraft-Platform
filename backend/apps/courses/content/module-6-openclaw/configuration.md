# Set Up the Home Base

*Lesson 1 of 4 · about 15 minutes · your Module 4 blueprint gets a real home today.*

In Module 4 you designed an agent on paper. This module gives it an actual home on your own computer, using a tool called **OpenClaw**: a program that runs a personal AI assistant on your own devices. Your machine, your rules, your files.

## First, the question worth answering before any command

*"What can go wrong here?"* Honestly: very little, and nothing permanent. Every step below is undone by editing a text file or re-running a command. OpenClaw's defaults are private. Nothing you do in this lesson is visible to anyone else, and nobody can talk to your assistant until you explicitly allow them (that is Lesson 3, and it is opt-in).

## Three commands, in order

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
openclaw gateway status
```

One line each:

1. **Install** puts the OpenClaw program on your computer. (npm is a standard installer for software like this.)
2. **Onboard** is a guided setup that asks you questions in the right order, so you never have to know the right order yourself. The `--install-daemon` part sets up a *daemon*: a small background program that keeps your assistant awake even when you close the window.
3. **Status** asks the *Gateway* one question: "are you healthy?" The Gateway is the front desk of the whole building, the part that stays running.

## The one health question

`openclaw gateway status` deserves a moment of appreciation. After **any** change you make in this module, this single command answers "is everything okay?" If it says healthy, it is healthy. One run, one answer, move on.

## The home, mapped

Only three files matter this week:

| File | Job | Plain name |
| --- | --- | --- |
| `~/.openclaw/openclaw.json` | How the system runs: model, tools, doors | The control panel |
| `SOUL.md` | Who your assistant is: role, rules, boundaries | The job description |
| `<workspace>/skills/<name>/SKILL.md` | How to do one specific task well | A recipe card |

The map below shows where each one lives. It is a picture, not your real computer, so click anything.

One routing rule makes every later lesson easier: **the control panel changes how the system runs; the job description changes who the assistant is.** Wrong model? Control panel. Wrong personality? Job description.

## Done means done

You are done when you can:

- say what the Gateway is in one sentence
- route two problems: "wrong model" goes to which file? "wrong personality" goes to which file?
- name the command that answers "is everything okay?"

That is the whole foundation. Lesson 2 adds recipe cards.