# OpenClaw Security Audit Runbook

1. Run `openclaw security audit`.
2. If the setup will be exposed or shared, run `openclaw security audit --deep`.
3. Lock down anything that is open plus tools enabled before tuning model behavior.
4. Review DM policy, allowlists, gateway bind/auth, plugins, and sandbox state.
5. Re-run the audit after every meaningful config change.
