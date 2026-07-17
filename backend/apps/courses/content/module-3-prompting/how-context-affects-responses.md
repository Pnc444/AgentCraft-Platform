# How Context Affects Responses

The **same question** can get **different answers** depending on what else the model can see. Context is everything in the window that influences the next reply.

## What counts as context?

- **This conversation** — earlier user and assistant messages
- **Pasted material** — emails, code files, specs, notes
- **System instructions** — rules set by the app (covered in the next lesson)
- **Implicit cues** — tone, language, what you did *not* say

LLMs do not “remember” your life — they only use what is **in the current context window** (see Module 1.5 on context limits).

## Same prompt, different context

Imagine you ask: *“Should we ship this feature?”*

| Context provided | Likely angle of the answer |
|------------------|----------------------------|
| A one-line feature name only | Generic pros/cons |
| Full PRD + deadline + team size | Trade-offs tied to *your* project |
| Prior message: “We are a solo founder” | Advice scaled to small teams |

The **question string** did not change — the **surrounding information** did.

## Order and length matter

- **Recency:** Models often weigh recent text heavily. Put must-follow rules near the end if they get ignored.
- **Noise:** Irrelevant paragraphs dilute focus and burn tokens.
- **Missing facts:** If context omits something critical, the model may **hallucinate** plausible fill-ins.

## Practical habits

1. **Paste the source** — don’t assume the model saw your file.
2. **State assumptions** — audience, stack, deadline, “do not invent URLs.”
3. **Trim** — include what helps; delete what confuses.

## Mini exercise (mental)

Prompt: `Summarize the meeting.`

Add context: `Here are notes from a 30-min sprint planning call. Focus on action items and owners.`

Which version would you trust for a stand-up email?

## Takeaway

Context is not optional decoration — it **steers** answers. Control context and you control quality more than chasing a “smarter” model.
