# Good and Bad Prompts

Prompt quality is the difference between *“sort of helpful”* and *“exactly what I needed.”* Use side-by-side comparisons and a simple checklist.

## Bad patterns (and why they fail)

| Bad habit | Example | Problem |
|-----------|---------|---------|
| Too vague | `Help with marketing` | No audience, channel, or goal |
| Missing format | `Analyze this data` | Table? essay? one number? |
| Contradictory | `Be brief` + `Write 1000 words` | Model picks one arbitrarily |
| Assumed context | `Fix the bug in the usual file` | Model cannot see your repo |
| Overloaded ask | `Plan my trip, write code, and roast my essay` | Split tasks get better results |

## Good patterns

Strong prompts often answer:

1. **Who** is the output for?
2. **What** should the model do?
3. **What** material should it use?
4. **How** should the answer look?

We call this **CRAFT** in AgentCraft:

- **C**ontext — background, source text, constraints
- **R**ole — “act as a senior reviewer,” “explain like a teacher”
- **A**ction — the verb: summarize, compare, refactor, list
- **F**ormat — bullets, JSON, table, max length
- **T**one / constraints — formal, no jargon, no invented citations

## Side-by-side: email task

**Bad**
```
Write an email.
```

**Good**
```
Draft a polite email to my manager requesting Friday off for a family event.
3 short paragraphs, professional tone, offer to finish X report before EOD Thursday.
```

## Side-by-side: code task

**Bad**
```
Make this better.
```
*(paste 200 lines with no language specified)*

**Good**
```
You are a Python reviewer. Refactor the function below for readability only — no new features.
Return: (1) revised code (2) bullet list of changes ≤ 5 items.

[paste function]
```

## When “short” is fine

Quick chat, brainstorming, or follow-ups in an ongoing thread can stay short **because context already exists**. The bad examples above are **cold starts** — first message, no history.

## Takeaway

Good prompts **reduce ambiguity**. Before you send, scan for CRAFT: if Action and Format are missing, expect generic output.
