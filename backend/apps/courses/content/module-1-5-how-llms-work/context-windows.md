# Context Windows

In Module 1 you learned that LLMs predict the next token from patterns in text. But there is a hard limit on **how much text** the model can consider at once. That limit is the **context window**.

## Definition

The **context window** is the maximum amount of text (measured in **tokens** — covered in the next lesson) that a model can read and use when generating a reply. Everything in that window influences the answer; anything outside it might as well not exist.

Think of it as the model's **short-term memory for this request** — not a permanent database of everything it ever learned.

## What fills the window?

When you chat with an LLM, the context window typically includes:

| Source | Example |
|--------|---------|
| **System instructions** | "You are a helpful coding tutor." |
| **Conversation history** | Your earlier questions and the model's replies |
| **Current user message** | What you just typed |
| **Pasted material** | Code files, emails, specs, notes you attach |

All of these compete for the same limited space. A 50-page document plus a long chat thread can **push out** the earliest messages.

## Why context windows matter

1. **The model cannot see your whole project.** A large codebase may exceed the window. You must choose what to paste, summarize, or retrieve.
2. **Long chats forget the beginning.** If you talked for an hour, the model may no longer "see" what you said at the start unless the product summarizes or truncates smartly.
3. **Quality vs quantity.** More relevant context usually helps — until you hit the limit and lose important details at the edges.

Different models offer different window sizes (e.g. 8K, 128K, 1M tokens). Module 2 compares models partly on this trade-off.

## What happens when you exceed the limit?

Behavior depends on the product or API:

- **Truncate from the start** — oldest messages drop off first
- **Truncate from the middle** — keep system prompt + recent turns
- **Error** — API rejects the request until you shorten input
- **Summarize** — some apps compress older history automatically

As a builder, assume you are responsible for **what fits** — do not rely on the model magically remembering files it never received.

## Practical strategies

When context is tight, builders use patterns you will see again in agent modules:

1. **Be selective** — paste only the function or section you need, not the whole repo.
2. **Summarize first** — ask the model to condense a long doc, then work from the summary.
3. **Retrieve on demand (RAG)** — search a knowledge base and inject only the top matching chunks (advanced; introduced later).
4. **Reset the thread** — start a fresh chat when the topic changes so old noise does not eat tokens.

## Mini scenario

You are debugging one Python file in a 200-file project.

| Approach | Likely outcome |
|----------|----------------|
| Paste the entire repo | Context overflow; model sees a random slice; wrong advice |
| Paste the one file + error message | Model focuses on the actual bug |
| Paste file + "here is what I already tried" | Faster, more targeted help |

Same model, same question — **context management** changed the result.

## Connection to later modules

- **Module 3 (Prompting):** Context is why pasted docs and chat history shape answers.
- **Module 4 (Agents):** Agents often fetch only the snippets they need so they stay within the window.
- **Module 2 (Models):** "Context length" is a key spec when choosing which model to use.

## Takeaway

The context window is the model's **working desk**, not its **library**. Everything on the desk must fit at once. Managing what you put on that desk is one of the most important skills in working with LLMs.
