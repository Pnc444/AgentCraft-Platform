# Hands-on Prompt Exercises

Time to **practice judging prompts**. You do not need a special sandbox — use any chat model (ChatGPT, Claude, Cursor, etc.) for the try-it-yourself parts. This lesson gives you a **rubric** and exercises you can repeat.

## How to judge good vs bad

Score each prompt (1–5) on:

| Criterion | Ask yourself |
|-----------|--------------|
| **Clarity** | Is the task obvious? |
| **Context** | Is needed background included or clearly referenced? |
| **Specificity** | Audience, scope, and success criteria defined? |
| **Format** | Does it say how the answer should look? |
| **Constraints** | Length, tone, “don’t invent facts,” language, etc.? |

**Good** prompts score high on most rows. **Bad** prompts force the model to guess.

## Exercise 1 — Pick the winner

**Scenario:** You need study notes from a textbook chapter.

- **Prompt A:** `Notes on chapter 4.`
- **Prompt B:** `I'm studying intro biology. Summarize chapter 4 on cell division in 8 bullet points for exam review. Define mitosis and meiosis in one line each.`

**Your task:** Score A and B with the rubric. Prompt B should win on Context, Specificity, and Format.

**Try it:** Paste a real paragraph from any article into your chatbot with Prompt A, then with Prompt B. Compare usefulness.

## Exercise 2 — Rewrite a bad prompt

**Bad starter:** `Make my resume good.`

**Rewrite checklist:**
1. Add **Role** — e.g. “You are a career coach for software interns.”
2. Add **Context** — paste resume text or key bullets.
3. Add **Action** — “Improve impact statements; do not invent jobs.”
4. Add **Format** — “Return revised bullet points only.”

**Your task:** Write your improved prompt, run it, and check whether the output respects your constraints.

## Exercise 3 — Context experiment

Use this **fixed question** twice:

`What should we do next?`

1. **Run 1 — no context:** Send only that sentence.
2. **Run 2 — rich context:** Prefix with: `We are a 3-person team; sprint ends Friday; blocker is failing CI on main; goal is ship login bugfix.`

**Your task:** Note how specific Run 2’s answer becomes. That gap is **context at work**.

## Exercise 4 — System vs user (optional)

If your tool exposes system instructions (or a “custom instructions” field):

- **System:** `Always answer in exactly 3 numbered steps.`
- **User:** `How do I reset a forgotten password in a typical web app?`

Verify each reply has **three numbered steps**. Move the rule into the user message only — behavior may become inconsistent. This reinforces the last lesson.

## Self-check: did your prompt work?

A prompt worked well if the response:

- Matches the **requested format**
- Stays within **stated constraints**
- Uses **provided context** without inventing missing facts
- Fits the **audience** you named

If not, **iterate the prompt** before blaming the model.

## Takeaway

Judging prompts is a skill: use the rubric, compare A/B versions on the **same model**, and improve **context and constraints** first. You will reuse this loop constantly when wiring agents in later modules.
