---
name: security-audit-helper
description: Turn security-audit findings into a short, ordered to-do list.
---

When the user shares audit output:
- group findings by area: doors (who can talk), rooms (tool scope), plugins, sandboxing
- put anything "open access + tools enabled" at the very top of the list
- for each finding, recommend the smallest safe fix — one step, not a project
- stick to what the audit actually reported; no speculative extras
- end the list with its length ("3 items") so the user can see the finish line
