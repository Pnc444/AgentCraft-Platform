# Installing Docker Desktop

**Skeleton — swap in real screenshots at the image placeholders.**

Docker Desktop is the app that runs Docker on your computer and gives you a dashboard to see your containers.

## Download links

- **All platforms (start here):** https://docs.docker.com/desktop/
- **Windows:** https://docs.docker.com/desktop/setup/install/windows-install/
- **Mac:** https://docs.docker.com/desktop/setup/install/mac-install/
- **Linux:** https://docs.docker.com/desktop/setup/install/linux/

> **Windows users:** pick the right installer for your chip (most people want x86_64). Docker Desktop on Windows uses **WSL 2** — the installer sets it up, but if prompted, say yes.

## Install walkthrough

**Step 1 — Download the installer** for your OS from the links above.

![Step 1: download page](/images/lessons/docker-install/step-1-download.png)

**Step 2 — Run the installer.** Accept the defaults (on Windows, keep "Use WSL 2" checked).

![Step 2: installer options](/images/lessons/docker-install/step-2-installer.png)

**Step 3 — Launch Docker Desktop.** Accept the service agreement. You can skip creating an account — it's not required for this course.

![Step 3: first launch](/images/lessons/docker-install/step-3-launch.png)

**Step 4 — Wait for the whale.** Docker is ready when the whale icon in your menu bar / system tray stops animating and the dashboard says **"Engine running"** (green, bottom-left).

![Step 4: engine running](/images/lessons/docker-install/step-4-running.png)

**Step 5 — Verify from a terminal.** Open a terminal (PowerShell on Windows, Terminal on Mac/Linux) and run:

```bash
docker --version
```

You should see something like `Docker version 27.x.x`. If you do, you're installed.

<details>
<summary><strong>🛠️ Common issues — click to expand</strong></summary>

**"WSL 2 installation is incomplete" (Windows)**
Open PowerShell as Administrator and run `wsl --update`, then restart Docker Desktop.

**"Virtualization is not enabled" (Windows)**
Virtualization must be enabled in your BIOS/UEFI (usually called Intel VT-x, AMD-V, or SVM). Reboot into BIOS settings and enable it.

**"Docker Desktop requires a newer WSL kernel"**
Run `wsl --update` in PowerShell, then reboot.

**Whale icon never stops animating / "Engine starting" forever**
Quit Docker Desktop fully (right-click tray icon → Quit) and relaunch. On Windows, `wsl --shutdown` first, then relaunch.

**`docker: command not found` after install (Mac)**
Make sure Docker Desktop is actually running (whale in the menu bar), then open a **new** terminal window.

**Permission denied on Linux**
Add yourself to the docker group: `sudo usermod -aG docker $USER`, then log out and back in.

**Still stuck?**
Ask the AI tutor on this lesson — paste the exact error message.

</details>

## Takeaway
Docker Desktop installed, engine running, `docker --version` works. Next lesson: your first containers.
