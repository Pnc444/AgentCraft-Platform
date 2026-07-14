# Docker as Backend

**Skeleton — expand with final copy.**

## The box before the power switch
We set up the Docker backend **before the first real conversation** — not after. With the default `local` backend there is **no isolation at all**: the agent runs as your user, with full access to your filesystem, network, and environment variables. Twenty students running unsandboxed agents on lab machines is not a thought experiment we want to run. Frame: **we put the agent in the box before we turn it on.**

*(Three-box diagram callback: this lesson is about wrapping the middle box.)*

## What the Docker backend actually gives you
- **Read-only root filesystem** — the agent can't modify the container's system files or install anything outside its workspace.
- **Only mounted volumes are writable** — workspace and skills directories, nothing else. Your desktop, documents, and dotfiles don't exist as far as the agent is concerned.
- **Dropped Linux capabilities + namespace isolation** — no mounting filesystems, no touching network config, own PID/network/mount namespaces.
- **PID, memory, and CPU limits** — a runaway loop hits a ceiling instead of eating the machine.
- **Credentials mounted read-only** — the agent can use keys to call the model, but can't modify or move them.

## Set it up
*(TODO: exact steps — switch config `sandbox backend` from `local` to `docker`, plus the run flags we standardize on:)*

```
docker run -d --name hermes-agent \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid \
  --pids-limit 256 --memory 2g --cpus 1.5 \
  -v ./workspace:/app/workspace \
  -v ./skills:/app/skills \
  -v ./credentials:/app/credentials:ro \
  hermes-agent:latest
```

## Honest limits (say this out loud)
Docker is process isolation, not magic. It does **not** filter outbound network traffic — the agent can still make arbitrary HTTP requests. And nothing inspects what the agent writes into its own skill files (prompt injection via memory is the subtle attack surface). We revisit both in the safety lesson of Module 6.

## Takeaway
Local backend = agent runs as you. Docker backend = agent runs in a disposable box with only its workspace visible. Box first, power later — next lesson we finally turn it on.
