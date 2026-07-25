# Tokens

LLMs do not read English the way you do. They break text into **tokens** — small chunks that get counted, priced, and fed into the model. Understanding tokens helps you estimate cost, respect context limits, and debug surprising outputs.

## What is a token?

A **token** is the basic unit of text an LLM processes. It might be:

- A whole common word (`" the"`)
- Part of a word (`"un"` + `"believ"` + `"able"`)
- Punctuation or whitespace
- A chunk of code or a symbol

Tokenization is done by a **tokenizer** — a ruleset or learned splitter tied to each model family. **You cannot assume 1 word = 1 token.**

## Quick intuition

| Text | Rough token count (English) |
|------|----------------------------|
| `"Hello, world!"` | ~4 tokens |
| A short email paragraph | ~50–150 tokens |
| 1 page of plain text | ~300–500 tokens |
| Rule of thumb | ~1 token ≈ 4 characters of English prose |

Code, JSON, and non-English text often use **more tokens per visible character** because rare symbols split into extra pieces.

## Why tokens matter

### 1. Context windows are measured in tokens

When a model advertises a "128K context window," that means **128,000 tokens total** across system prompt, history, attachments, and the reply — not 128,000 words.

### 2. APIs charge by tokens

Most providers bill separately for:

- **Input tokens** — everything you send in
- **Output tokens** — everything the model generates back

Long prompts and long answers cost more. Agents that loop (plan → act → observe → repeat) can burn tokens quickly.

### 3. Generation is token-by-token

Remember from Module 1: the model predicts **one token at a time**, then feeds that token back in to predict the next. That is why streaming responses appear word-by-word — each word may be several token steps.

## Input vs output tokens

| Type | When they count | Who controls them |
|------|-----------------|-------------------|
| **Input** | When your prompt + history is sent | You (via what you paste and keep in chat) |
| **Output** | As the model generates its reply | Partly you (`max_tokens` limits) and partly the model |

Hitting `max_tokens` mid-sentence produces a **cut-off answer** — a common bug when limits are set too low in apps.

## Surprises tokenization causes

- **Typos and rare words** can split into many tokens → slightly different behavior and cost.
- **Identical meaning, different formatting** — extra whitespace or verbose JSON uses more tokens for the same idea.
- **Repeating the same instruction** in every message wastes input tokens; system prompts exist partly to avoid that (Module 3).

## Mini exercise (mental)

Which uses more tokens?

**A:** `{"name":"Ada","role":"engineer"}`  
**B:** A three-sentence paragraph explaining Ada is an engineer.

Often **A** uses fewer tokens per fact because JSON is compact — but ugly for humans. **B** reads better but costs more. Builders trade readability, structure, and token budget constantly.

## Try it yourself (optional)

Many provider docs include a **tokenizer tool** (OpenAI, Hugging Face, etc.). Paste a paragraph from this lesson and compare token count to your guess. You will quickly calibrate how fast context fills up.

## Takeaway

**Tokens are how LLMs measure text.** Context limits, API bills, and truncation all speak in tokens. When something "doesn't fit" or costs too much, count tokens — not pages or words.
