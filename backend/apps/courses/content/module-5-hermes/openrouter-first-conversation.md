# OpenRouter and Your First Conversation

## Why OpenRouter
One API key, many models. OpenRouter sits in the third box of our diagram: Hermes sends it requests, it routes them to whichever model we pick. Swapping models later is a config change, not a rebuild.

## Get a key (the safe way)
- **Sign up here: [https://openrouter.ai](https://openrouter.ai)** — then create your API key at [https://openrouter.ai/settings/keys](https://openrouter.ai/settings/keys).
- Create the OpenRouter account with a **dedicated email**, not your personal one — one identity for the agent means one kill switch if anything goes wrong.
- Set a **hard spending cap of $5** in the dashboard before the first request. If the agent loops, the cap stops the bleeding. $5 is more than enough for this whole course.
- **Model choice:** any of OpenRouter's **free models** (filter by the `:free` tag) works for this course. If you already have an API key for Claude or another provider you prefer, you can use that instead — same $5-cap idea applies.

![OpenRouter dashboard with the $5 spending cap set](/images/lessons/hermes-openrouter/spending-cap.png)

## Wire it up
Two commands. Hermes routes each value to the right file automatically (keys go to `~/.hermes/.env`, settings to `config.yaml`):

```bash
hermes config set OPENROUTER_API_KEY sk-or-your-key-here
hermes config set model your-chosen-model
```

One detail worth appreciating: the key lives in `~/.hermes/.env` on your **host**, and model calls are made by the Hermes process — also on your host. The sandboxed container from the previous lesson never sees the key. The agent can *use* the model, but a command running inside the box can't read or leak the credential.

## First conversation
Start the CLI gateway and say hello. Then the real test — ask the agent to run a shell command, e.g. *"What files are in your workspace?"* Watch the loop happen live: your message → model decides to call the shell tool → command runs **inside the container** → result comes back → model answers.

![First conversation — the agent runs a shell command inside the container](/images/lessons/hermes-openrouter/first-conversation.png)

## Milestone — parity checkpoint
Before anyone moves on, every student must have:

1. Agent responds to a CLI message.
2. Agent successfully runs a shell command and reports the result.

This is the "everyone at the same base camp" moment. Instructors: don't advance the class until all machin