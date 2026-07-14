# Approval-Driven Task Flow

1. Trigger arrives through a webhook or channel.
2. OpenClaw drafts the first artifact.
3. A verifier or rubric probe runs.
4. If the result is incomplete or risky, the workflow routes to review.
5. Only a passing artifact reaches the publish step.
