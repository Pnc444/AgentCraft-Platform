# Put It to Work

## Chatbot or agent? Now you'll feel the difference
You might be thinking: *I installed all this and it just answers questions — isn't that a chatbot with extra steps?* Fair thought. Here's the answer, and you're about to watch it happen.

A **chatbot** goes text in → text out. It can *tell* you the first 20 Fibonacci numbers.

An **agent** goes goal in → *acts* → reads the result → acts again → until the goal is done, with no human in the middle of that chain. It can **write a program, run it on a real computer, check the output, and report back** — a loop, not a reply. You already glimpsed this in the lab: one sentence ("read the TARGET file") made the agent run `find`, then `grep`, then `ls`, then search the whole filesystem — decisions *it* made. That was the loop turning. `whoami` only felt chatbot-ish because it was a one-step job, so the loop turned once.

Let's give it a job where the loop has to turn several times.

## Task 1 — Make it write and run code
At the Hermes prompt, type this as a single message:

> write a Python script that prints the first 20 Fibonacci numbers, run it, save the output to fib.txt, then tell me the largest number

Watch the tool line. In one go, with no further input from you, the agent will:

1. **write_file** — create the script
2. **terminal** — run it with `python` *inside the container*
3. **read** — open `fib.txt` to see what came out
4. **answer** — report the largest number

![The agent writing a script, running it, and reporting the result](/images/lessons/hermes-lab/put-it-to-work.png)

That's the whole point in four steps: it didn't *tell* you the numbers, it **wrote a program and ran it on a real machine** — one that happens to be a locked-down container, exactly as you designed. A chatbot cannot do step 2. Your agent just did it unsupervised.

Confirm it for yourself: ask *"show me fib.txt"* and check the file actually exists inside the box.

## Task 2 — Now you drive
Time to experiment. Everything runs in the disposable sandbox, so **be bold** — the worst case is you delete the container and a fresh one appears. Try one of these, or invent your own:

- *"Create a folder called `planets` with one text file per inner planet, each holding a fun fact, then list them back to me."*
- *"Write a number-guessing game in Python and play one round against yourself to prove it works."*
- *"Make a CSV of 10 made-up employees, then write a script that prints the average age."*

Notice what you're doing: you state a **goal**, not a list of commands. The agent figures out the steps. The more open-ended the goal, the more of the loop you'll see — and the more it stops feeling like a chatbot.

## The autonomy dial
This is still the *minimal* agent — Blank Slate left almost everything off. The capabilities you turned down are the ones that make an agent more autonomous, and each is a later lesson:

- **Skills + memory** — it remembers and follows learned procedures across sessions
- **Gateways** (Telegram/Discord) — it acts on messages when you're nowhere near the terminal
- **Cron** — it acts on a schedule, with no human present at all
- **Delegation** — it spawns sub-agents to chase pieces of a bigger goal

You built the engine and kept it in the garage on purpose. Turning that dial up — safely — is the rest of this course.

## Don't want an agent anymore? Full removal
An agent you can't cleanly remove is an agent you don't control. Hermes ships its own uninstaller that does most of the work — but two things live *outside* your machine and it can't reach them, so teardown is three steps.

**Step 1 — Preview, then run the uninstaller.** Good habit first: see what it'll remove without changing anything.

```bash
hermes uninstall --dry-run
```

Then run it for real:

```bash
hermes uninstall
```

You get a menu: **(1) Keep data** removes the code but leaves your config, sessions, and logs so you can reinstall later with settings intact; **(2) Full uninstall** deletes everything including config and the `.env` holding your API key; **(3) Cancel**. For a clean break choose **2** — or skip the menu entirely with `hermes uninstall --full --yes`. This clears the whole `AppData\Local\hermes` folder (Windows) / `~/.hermes` (macOS/Linux): runtime, agent, config, skills, memory, and key file.

**Step 2 — Delete the Docker containers and image.** The uninstaller handles Hermes, not Docker. In Docker Desktop remove every `hermes-...` container, then the `nikolaik/python-nodejs` image under Images. (Or: `docker ps -a`, `docker rm -f <ids>`, `docker rmi nikolaik/python-nodejs`.) These are what actually took up disk space, so don't skip them.

**Step 3 — Revoke the API key.** This is the one thing no local uninstaller can do, because the key lives on OpenRouter's servers, not your machine. Go to [openrouter.ai/settings/keys](https://openrouter.ai/settings/keys) and delete it. *This* is the real kill switch — even a leaked copy is now worthless. (Using a dedicated email back in lesson 2 pays off here: you can delete the whole account.)

Do all three and nothing of the agent survives, on your machine or off it.

## Takeaway
You gave an agent a goal, and it wrote code, ran it, and checked its own work — the loop, not a reply. That's the line between a chatbot and an agent, and you can now point to the exact moment it crossed. You also know how to make the whole thing vanish. Control at both ends of the lifecycle: that's what "building agents safely" actually means, and it's the foundation for every build that follows.
