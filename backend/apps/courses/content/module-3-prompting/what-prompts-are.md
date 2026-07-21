# What Prompts Are

Prompting is how you **steer** a language model. Everything you type — instructions, examples, pasted documents — becomes input the model uses to predict its reply.

## Definition

A **prompt** is the text (and structured messages) you send to an LLM before it generates a response. Think of it as the **user interface** to the model: no prompt, no useful output.

From Module 1 you know LLMs predict the next token from patterns. The prompt is the pattern you supply *right now*.

## Parts of a prompt

Most useful prompts combine some of these:

| Piece | What it does |
|-------|----------------|
| **Instruction** | The job: summarize, debug, brainstorm, compare |
| **Context** | Background: docs, data, prior chat, constraints |
| **Examples** | Show the shape of a good answer (optional but powerful) |
| **Output format** | Bullets, JSON, table, word limit, tone |

You do not need a novel every time — but **more signal, less guesswork** for the model.

## Mini example

**Weak:** `Tell me about dogs.`

**Stronger:** `List 5 dog breeds good for apartments. One sentence each, friendly tone, no medical advice.`

Same model, same day — the second prompt narrows *what* to produce and *how*.

## Prompt vs response

- **Prompt** → what you send in
- **Completion / response** → what the model sends back

When you build agents later, prompts often live in code or config while users only see their side of the chat.

## Takeaway

A prompt is not magic words — it is **clear instructions plus context**. Better prompts are the cheapest upgrade you can make before changing models or adding tools.
