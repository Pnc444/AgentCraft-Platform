# The Audit Rhythm — one page

**The whole discipline:**

> Change something → `openclaw security audit` → fix what it flags → done.

The audit walks the entire building — door policies, tool grants, network posture, plugin trust, and more — against the official checklist. The checklist lives in the tool, so it never has to live in your head. When the audit passes, you are entitled to believe it.

**Re-running the audit on an unchanged system tells you nothing new.** Same system in, same answer out. Once per change is the complete discipline — the auditor remembers everything so you can put it down entirely between changes.

## If it flags something

A flag is the system working: the auditor caught what it exists to catch, before anything happened.

1. Findings arrive ordered. Fix the top one first (anything "open access + tools enabled" always sorts to the top).
2. Re-run once. Watch the list shrink.
3. When it passes, stop. Passing means passing.

A first audit with a few flags is the normal experience, not a bad sign. The `security-audit-helper` skill will turn any audit output into a tidy to-do list for you.

## Two variants for later (no action needed now)

- `openclaw security audit --deep` — looks harder; worth it before sharing access more widely.
- `openclaw security audit --fix` — applies safe corrections itself.
