# Install and the Setup Wizard

## What we're doing
Install Hermes and walk its setup wizard end to end: blank slate, OpenRouter key, free model, Docker backend. By the end the agent is fully configured but **we haven't chatted with it yet** — that's next lesson.

This course was built and tested on **Hermes Agent v0.18.2** — newer versions will most likely work fine, but if a menu looks different from the screenshots, version drift is why.

## Step 0 — Install
**Windows 10 users, one prerequisite:** install Windows Terminal first (`winget install Microsoft.WindowsTerminal`, then run PowerShell inside it). The Hermes wizard uses ANSI colors, and the legacy console renders them as garbage like `[32m(•)[0m` — everything still *works*, but you can't read the menus and your screen won't match our screenshots. Windows 11 has it by default.

**Windows (PowerShell):**
```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

**macOS / Linux:**
```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

To pin everyone to the same version, download the script first and run it with `-Tag <release>` (Windows) or `--tag <release>` (macOS/Linux) instead of piping. The installer clones the Hermes source from GitHub — read-only download, no GitHub account involved.

The installer syncs its bundled skills (you'll see a list of ~73 scroll past), writes a bootstrap marker, and then **launches the setup wizard automatically**. Don't panic-close it — everything it asks, you already have answers for.

![Installer finishing and launching the setup wizard](/images/lessons/hermes-install/installer-done.png)

## Step 1 — Choose Blank Slate
The wizard offers three setup styles. Choose **option 3, Blank Slate**: everything off except the bare minimum, and you opt in to each capability deliberately.

Read what the wizard says here, because it's this module's philosophy in one screen: only **Provider & Model, File Operations, and Terminal** are force-enabled — the minimum to run an agent at all. Everything else (web, browser, code exec, vision, memory, delegation, cron, skills, plugins, MCP…) starts **disabled**. Every capability an agent has is one you chose to give it.

![Wizard setup-style menu — Blank Slate selected](/images/lessons/hermes-install/wizard-blank-slate.png)

## Step 2 — Provider, key, model
The wizard now walks Provider & Model:

1. **Select provider:** choose **OpenRouter** from the provider list (pay-per-use model API aggregator).
2. **API key:** paste the key from last lesson at the `OPENROUTER_API_KEY` prompt. You'll see `API key saved.`
3. **Default model:** the wizard shows a model list with prices. Free models show as `free` — pick the one you chose last lesson (course recommendation `openai/gpt-oss-20b:free`; a Nemotron `:free` model is fine too). You can also type option numbers for custom model names — but stay with the list for now.

![Wizard provider list with OpenRouter selected](/images/lessons/hermes-install/wizard-provider.png)

![Wizard model list — picking a :free model](/images/lessons/hermes-install/wizard-model.png)

## Step 3 — Terminal backend: Docker
Next the wizard asks where Hermes should run shell commands and code — this is the sandbox decision, and it's why Module 4.5 happened. The options include Local (run directly on this machine — the default), **Docker**, and some cloud/remote options.

Choose **Docker**. The wizard detects your Docker Desktop install (`Docker found: ...docker.EXE`) and sets `Terminal backend: docker`.

**Never choose Local for a running agent.** With Local there is no isolation at all: the agent runs as you, with your files, your network, your environment. Box before power switch.

![Wizard terminal backend menu — Docker selected and detected](/images/lessons/hermes-install/wizard-docker-backend.png)

The wizard finishes with a **minimal baseline** confirmation: toolsets `file, terminal` — everything else off. That's the blank slate holding.

## Step 4 — Verify with /config
Start Hermes (`hermes`) and immediately run `/config`. Check four lines: **Model** (your `:free` model via openrouter.ai), **API Key** (masked), **Environment: docker**, and **Toolsets: file, terminal**. Then exit (`Ctrl+C`). Yes — exit. We're proving configuration, not chatting yet.

Where things landed on disk: Windows keeps config in `%LOCALAPPDATA%\hermes\config.yaml` (i.e. `C:\Users\<you>\AppData\Local\hermes\`), macOS/Linux in `~/.hermes/`. Your API key is in the `.env` file next to it — on the **host**, a fact that matters next lesson.

![The /config output showing docker backend and free model](/images/lessons/hermes-install/config-check.png)

## Checkpoint
Everyone should have: wizard completed with Blank Slate → OpenRouter → free model → Docker backend, `/config` showing all four lines correct, and **no conversation held yet**. One thing you may notice: Docker Desktop shows **no Hermes container**. That's expected — and it's the first question of the next lesson.

## Takeaway
The wizard front-loads every decision that matters: what the agent can use (almost nothing), who it talks to (OpenRouter, capped), and where it acts (a Docker sandbox that doesn't exist yet). Configured but silent — next we turn it on and watch the box appear.
