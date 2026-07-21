# Docker as Backend

## The box before the power switch
We set up the Docker backend **before the first real conversation** — not after. With the default `local` backend there is **no isolation at all**: the agent runs as your user, with full access to your filesystem, network, and environment variables. Twenty students running unsandboxed agents on lab machines is not a thought experiment we want to run. Frame: **we put the agent in the box before we turn it on.**

Here's the three-box diagram again — this lesson is about wrapping the middle box:

<div class="lesson-diagram">
  <div class="ld-box">
    <div class="ld-title">Gateways</div>
    <div class="ld-sub">CLI, Telegram, web UI</div>
  </div>
  <div class="ld-arrow">→</div>
  <div class="ld-box ld-warning">
    <div class="ld-title">Agent loop + tools</div>
    <div class="ld-sub">Hermes: shell, files, memory, skills<br /><strong>← wrapped in the Docker sandbox</strong></div>
  </div>
  <div class="ld-arrow">→</div>
  <div class="ld-box">
    <div class="ld-title">Model provider</div>
    <div class="ld-sub">OpenRouter → any model</div>
  </div>
  <div class="ld-caption">Same three boxes as before — but now the middle one runs inside a locked-down container instead of directly as you.</div>
</div>

## What the Docker backend actually gives you
- **A separate filesystem** — the container has its own files. Your desktop, documents, and dotfiles don't exist as far as the agent is concerned. Anything the agent writes stays in the container and disappears when the container is deleted.
- **Dropped Linux capabilities + namespace isolation** — `--cap-drop ALL` and `no-new-privileges`: no mounting filesystems, no touching the host's network config, its own process/network/mount namespaces.
- **PID, memory, and CPU limits** — a process limit of 256 plus the memory/CPU caps we set below, so a runaway loop hits a ceiling instead of eating the machine.
- **Keys stay outside the box** — your API key lives in `~/.hermes/.env` on the *host*, and the model calls happen from the host process. The sandboxed commands never see the key at all (unless you explicitly forward it).

## Set it up
Hermes builds the hardened `docker run` command for you — you just switch the terminal backend. One command:

```bash
hermes config set terminal.backend docker
```

Then add our course-standard resource limits. Open `~/.hermes/config.yaml` and make the `terminal` section look like this:

```yaml
terminal:
  backend: docker
  container_cpu: 1          # CPU cores the agent can use
  container_memory: 2048    # MB — a runaway process hits this ceiling
  container_persistent: true
```

![config.yaml terminal section set to the docker backend](/images/lessons/hermes-docker/config-terminal-docker.png)

That's the whole setup. Hermes will pull a default sandbox image (`nikolaik/python-nodejs`) the first time it needs it.

## How it behaves
Hermes starts **one long-lived container** the first time the agent runs a command, and routes every terminal and file call through it. Installed packages and files in `/workspace` persist from one command to the next — it feels like a normal shell, it's just a shell *in the box*. The container is stopped and removed when Hermes shuts down.

## Verify the box exists
Start Hermes, ask the agent to run any command (e.g. *"run `whoami`"*), then in **your own** terminal:

```bash
docker ps
```

You should see a new container running (image `nikolaik/python-nodejs:...`). That container is where the agent now lives.

![docker ps showing the Hermes sandbox container running](/images/lessons/hermes-docker/docker-ps-sandbox.png)

In the next lesson we give it a brain; in the lesson after that, you'll try to break out of the box yourself.

## Takeaway
One config change, and every command the agent runs is inside a locked-down, resource-capped container instead of directly on your machine. Box first, power switch later.