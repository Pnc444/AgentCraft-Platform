---
name: channel-policy-check
description: Double-check a channel's door settings against the intended policy before it goes live.
---

When the user shares a channel plan:
- name the channel type and restate the intended DM policy in plain words
- compare the plan's dmPolicy, group settings, and mention rule against that intention
- flag any mismatch before rollout — catching it now is the point of this skill
- check that shared rooms only answer when called by name (requireMention)
- if the plan opens access wider than the stated intention, stop and say so plainly
