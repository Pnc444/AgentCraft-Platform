# Install and First Session

## Goal
Install Claude Code, sign in with a **spending-capped** account, and run one careful first session. Like the Hermes install, we set the money limit *before* the agent does anything.

## Step 1 — Install
One-liner, like Hermes. Pick your platform:

**macOS / Linux / WSL:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell:**
```powershell
irm https://claude.ai/install.ps1 | iex
```

Verify:
```bash
claude --version
```
You should see a version number followed by `(Claude Code)`. Version drift note: this module was written against the mid-2026 release — if a menu looks different from the screenshots, check the changelog first.

![claude --version output in the terminal](/images/lessons/claude-install/version-check.png)

## Step 2 — Account with a cap
Claude Code needs either a Claude subscription (Pro/Max) or a **Claude Console** account with pre-paid API credits. For this course, use the Console route — it's the OpenRouter pattern again:

1. Create an account at console.anthropic.com.
2. Buy the minimum credits (**$5 is plenty** for this module).
3. Do **not** enable auto-reload. Prepaid credits *are* the spending cap — when they're gone, the agent stops.

If you already pay for Claude Pro, you can use that instead; your subscription's usage limits act as the cap.

![Console account with $5 prepaid credits, auto-reload off](/images/lessons/claude-install/console-credits.png)

## Step 3 — First session, empty room
Same discipline as Hermes' blank slate: first run happens in an **empty practice folder**, not in your real files.

```bash
mkdir ~/agent-practice && cd ~/agent-practice
claude
```

Follow the login prompt in your browser, then you're at the Claude Code prompt. Note what it shows: model, working directory. That working directory matters — it's the agent's default territory.

## Step 4 — Watch the permission system work
Type:

```text
create a file called hello.txt containing one haiku about containers
```

Claude Code will propose the file and **ask for approval** before writing it. This is the built-in guardrail we talked about in the overview. Approve it, confirm `hello.txt` exists, then try:

```text
delete every file in this folder
```

It asks first. Deny it. That deny button is Module 4.5's lesson as a feature: *the agent acts on your machine, so the boundary has to be explicit.*

![Claude Code asking permission before writing hello.txt](/images/lessons/claude-install/permission-prompt.png)

Press `Shift+Tab` and watch the permission mode cycle (default → auto-accept edits → plan mode). Put it back to default for now. We stay in default mode all module.

## Useful commands before you leave
`/help` (list commands), `/clear` (wipe conversation), `claude -c` (continue last session), `/exit`.

## Self-check
1. Does `claude --version` print a version?
2. Is your spend capped (prepaid credits, no auto-reload)?
3. Did you see the agent ask permission before touching a file — and did you deny one request successfully?

## Takeaway
Installed, capped, and you've already exercised the permission boundary. Next lesson we start teaching the agent things — with files, not code.
