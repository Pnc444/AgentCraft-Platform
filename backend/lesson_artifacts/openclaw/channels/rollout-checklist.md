# OpenClaw Channel Rollout Checklist

- Choose one trusted channel first.
- Keep `dmPolicy` on `pairing` unless the use case truly requires `open`.
- Turn on `requireMention` for shared rooms.
- Test `openclaw pairing approve <channel> <code>` before inviting real users.
- Use `session.dmScope: "per-channel-peer"` when several people can DM the bot.
- Do not widen access until the policy reads clearly in plain English.
