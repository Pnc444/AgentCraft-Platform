# Module 7 (Claude) — Screenshot Checklist

7 images, in lesson order. All go under `frontend/public/images/lessons/`.
Filenames must match exactly — the markdown already references them.

---

## Lesson 1 — What Claude Code Is
No images referenced. Nothing to shoot.

---

## Lesson 2 — Install and First Session
Folder: `claude-install/`

- [ ] **1. `version-check.png`**
  Terminal showing `claude --version` output — version number followed by `(Claude Code)`.

- [ ] **2. `console-credits.png`**
  console.anthropic.com billing page: $5 prepaid credits, auto-reload visibly **off**.

- [ ] **3. `permission-prompt.png`**
  Claude Code asking for approval before writing `hello.txt` — the approve/deny prompt.

---

## Lesson 3 — CLAUDE.md and Skills
Folder: `claude-claudemd/`

- [ ] **4. `note-in-notes.png`**
  Agent obeying CLAUDE.md: the note saved into `notes/` as markdown, unprompted.

- [ ] **5. `daily-log.png`**
  `log.md` after **two** skill invocations — dated heading with bullets appended (not overwritten).

---

## Lesson 4 — Custom Subagents
Folder: `claude-subagents/`

- [ ] **6. `delegation.png`**
  Main agent handing off to the reviewer subagent, with the report coming back.

---

## Lesson 5 — Build Your Agent Lab
Folder: `claude-lab/`

- [ ] **7. `pipeline-run.png`**
  Full pipeline in one shot: research-note skill fires → note written → daily-log appends → reviewer subagent reports.

---

## Notes

- All four folders already exist (with `.gitkeep`) — just drop the PNGs in.
- Format is `.png` for every one; the markdown paths are hardcoded.
- Images are served by Next.js from `public/`, so **no `sync_content` needed** — hard-refresh the browser.
- Full paths for reference:

```
frontend/public/images/lessons/claude-install/version-check.png
frontend/public/images/lessons/claude-install/console-credits.png
frontend/public/images/lessons/claude-install/permission-prompt.png
frontend/public/images/lessons/claude-claudemd/note-in-notes.png
frontend/public/images/lessons/claude-claudemd/daily-log.png
frontend/public/images/lessons/claude-subagents/delegation.png
frontend/public/images/lessons/claude-lab/pipeline-run.png
```
