# Setup Checklist — one pass, in order

Each step is done once. When a box is checked, it stays checked — nothing here needs re-verifying later, because the status command re-verifies on demand.

- [ ] Install the program: `npm install -g openclaw@latest`
- [ ] Run the guided setup: `openclaw onboard --install-daemon`
      (it asks the questions in the right order so you don't have to know the order)
- [ ] Ask the one health question: `openclaw gateway status`
      → "healthy" means healthy. The command checked so you don't have to.
- [ ] Find the control panel: `~/.openclaw/openclaw.json` (just know where it lives)
- [ ] Find your workspace folder (where SOUL.md and skills will live)
- [ ] Leave channels for Lesson 3 — they come last on purpose

Why channels come last: every layer is added onto a base that is already proven healthy. Built this way, you always know which change caused anything, because you only ever changed one thing.
