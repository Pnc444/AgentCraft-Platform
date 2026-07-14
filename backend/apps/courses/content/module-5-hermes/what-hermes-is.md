# What Hermes Is

**Skeleton — expand with final copy.**

## Not a model — an orchestrator
Hermes doesn't run AI on your machine. It's a program that sits between you and a model provider: it takes your task, sends API calls to an LLM, and **executes actions** based on the responses — running shell commands, reading and writing files, calling other services. The heavy thinking happens on the provider's servers; the *doing* happens on yours. That last part is why this module cares so much about safety.

## The three-box diagram
*(Draw this once — we reuse it in every lesson this module.)*

```
[ Gateways ]  →  [ Agent loop + tools ]  →  [ Model provider ]
 CLI, Telegram,     Hermes: shell, files,      OpenRouter →
 web UI              memory, skills             (any model)
```

- **Gateways** — how tasks get in: the CLI for now, chat apps later.
- **Agent loop + tools** — Hermes itself: receives a task, asks the model what to do, runs the tool call, feeds the result back, repeats until done.
- **Model provider** — where the intelligence lives. We use OpenRouter so we can swap models without changing anything else.

## Why the tools are the point (and the risk)
A chatbot that can only *talk* can't hurt anything. Hermes has **shell and file tools** — it can do real work, which means it can also do real damage if it runs unsandboxed. Keep the three-box picture in mind: the box we need to control is the middle one.

## Takeaway
Hermes = gateways in front, agent loop with real tools in the middle, a model provider behind. Next lesson we install it — but we don't turn it on until it's in a box.
