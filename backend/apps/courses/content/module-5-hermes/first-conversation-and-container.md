# First Conversation and the Container

## Where's the box?
You chose the Docker backend, but Docker Desktop shows no Hermes container. That's because the backend is **lazy**: choosing it only wrote one line of config. The container is created the first time the agent actually runs a command. Today you turn the key and watch it happen.

Here's the three-box diagram one more time — this lesson is about the wrapper around the middle box:

<div class="lesson-diagram">
  <div class="ld-box">
    <div class="ld-title">Gateways</div>
    <div class="ld-sub">CLI, Telegram, web UI</div>
  </div>
  <div class="ld-arrow">→</div>
  <div class="ld-box ld-warning">
    <div class="ld-title">Agent loop + tools</div>
    <div class="ld-sub">Hermes: shell, files, memory, skills<br /><strong>← commands run in the Docker sandbox</strong></div>
  </div>
  <div class="ld-arrow">→</div>
  <div class="ld-box">
    <div class="ld-title">Model provider</div>
    <div class="ld-sub">OpenRouter → any model</div>
  </div>
  <div class="ld-caption">Same three boxes — but every command the middle box runs now happens inside a locked-down container.</div>
</div>

## What the Docker backend gives you
- **A separate filesystem** — the container has its own files. Your desktop, documents, and dotfiles don't exist as far as the agent's commands are concerned. Anything the agent writes stays in the container and dies with it.
- **Dropped Linux capabilities + namespace isolation** — no mounting filesystems, no touching the host's network config, its own process/network/mount namespaces.
- **A process limit (256 PIDs)** — a runaway loop hits a ceiling instead of eating the machine.
- **Keys stay outside the box** — your API key lives in the `.env` file on the *host* (AppData\Local\hermes on Windows, ~/.hermes on macOS/Linux), and model calls are made by the Hermes process — also on the host. Commands running inside the box never see the credential.

Optional hardening for lab machines — open `config.yaml` in a text editor and add resource caps to the `terminal` section. Where it lives (same place the install lesson showed):

- **Windows:** `C:\Users\<you>\AppData\Local\hermes\config.yaml` — quickest open: `notepad $env:LOCALAPPDATA\hermes\config.yaml` in PowerShell
- **macOS/Linux:** `~/.hermes/config.yaml`

```yaml
terminal:
  backend: docker
  container_cpu: 1          # CPU cores the agent can use
  container_memory: 2048    # MB — a runaway process hits this ceiling
```

**Or skip the editor entirely** — Hermes can change its own config from your terminal:

```bash
hermes config set terminal.container_cpu 1
hermes config set terminal.container_memory 2048
```

`hermes config set <key> <value>` routes each value to the right file automatically: settings go to config.yaml (dotted keys reach nested sections), secrets like `OPENROUTER_API_KEY` go to `.env`. Two more to know: `hermes config` (no arguments) prints your whole configuration — paths, keys, model, backend — in one screen, and `hermes config edit` opens config.yaml in your editor without you hunting for the path. All routes end up in the same file; the full view is worth seeing at least once so you know everything your agent is configured to do.

![config.yaml terminal section with docker backend and resource caps](/images/lessons/hermes-docker/config-terminal-docker.png)

## First conversation
Start `hermes` and say hello. Then the real test — ask it to run a shell command:

> run `whoami` and tell me what it says

A simple command like this usually comes back in seconds — but give a free model a minute without worrying. Watch the progress line while it works: that's the agent loop from the theory lesson happening live — your message → model decides on a tool call → command runs **inside the container** → result feeds back → repeat until it answers. (Tip: `/verbose` cycles how much of this you see.)

The answer itself is a tell: `root` — inside the container the agent runs as the container's root user, not as you.

![First conversation — the agent runs a shell command inside the container](/images/lessons/hermes-openrouter/first-conversation.png)

## Watch the box get born
While the agent works, check Docker Desktop (or run `docker ps` in your own terminal). There it is: a new container named `hermes-...`, image `nikolaik/python-nodejs`. It was created the moment the agent first needed a shell — lazy, remember. That container is where the agent now lives; files and installed packages persist inside it from command to command.

![docker ps showing the hermes sandbox container running](/images/lessons/hermes-docker/docker-ps-sandbox.png)

**Housekeeping:** each Hermes session gets its own container, so they accumulate as you start new sessions across the course. Old ones are safe to delete in Docker Desktop — which is Module 4.5's disposability lesson in practice: the box is furniture, throw it out and a fresh one appears on demand.

## Milestone — parity checkpoint
Before anyone moves on, every student must have:

1. Agent responds to a CLI message.
2. Agent successfully runs a shell command and reports the result (even if it took three minutes).
3. The hermes container is visible in `docker ps` and you can point at it.

This is the "everyone at the same base camp" moment. Instructors: don't advance the class until all machines pass.

## Takeaway
One config choice made earlier, and now every command the agent runs happens inside a locked-down, disposable container you can see with your own eyes. Next lesson you attack it.
