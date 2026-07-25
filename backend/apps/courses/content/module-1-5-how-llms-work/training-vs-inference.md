# Training vs Inference

Module 1 introduced LLMs as models trained on huge amounts of text. This lesson separates **how a model is built** (training) from **how you use it every day** (inference). That distinction explains why chatbots can feel smart but cannot truly "learn" from a single conversation.

## Two phases, one model

| Phase | When it happens | Who does it | Cost & scale |
|-------|-----------------|-------------|--------------|
| **Training** | Weeks/months, once per model version | Labs (OpenAI, Anthropic, Meta, etc.) with massive GPU clusters | Very expensive |
| **Inference** | Every time you send a prompt | You, via API or local run | Pay per use (or your own hardware) |

You almost always work in **inference**. Training is the factory; inference is driving the car off the lot.

## What is AI training?

**Training** is the process of adjusting a model's internal **parameters** (billions of numeric weights) so it gets better at predicting text.

At a high level:

1. **Collect data** — books, web pages, code, conversations (with filtering and licensing).
2. **Pre-train** — show the model billions of examples of "predict the next token." It learns grammar, facts, coding patterns, and reasoning *styles* — not a perfect memory of every page.
3. **Fine-tune & align (optional)** — additional training on curated examples so the model follows instructions, refuses harmful requests, or speaks in a product's voice.

The output of training is a **checkpoint** — a frozen file of weights. That checkpoint **is** the "LLM model" from Module 1.

### What training is *not*

- It is **not** what happens when you paste notes into ChatGPT for one session.
- It is **not** the model permanently storing your company's secrets inside its weights after one chat.
- It is **not** something you rerun casually on a laptop for a full GPT-scale model.

## What is inference?

**Inference** (also called **decision-time** or **runtime**) is when the **already-trained** model reads your prompt and generates tokens.

Steps:

1. Your text is tokenized.
2. Tokens flow through the fixed network (the trained weights).
3. The model outputs a probability distribution over the next token.
4. One token is chosen (with some randomness unless temperature is 0).
5. Repeat until the reply is complete.

No weight updates happen during normal chat inference. The model does not "study" your message for next week — it **conditions** on it only for that request (within the context window).

## Training vs inference — mental models

| Question | Training | Inference |
|----------|----------|-----------|
| Are weights changing? | Yes, gradually | No (frozen) |
| Can it see your private doc? | Only if that doc was in training data (unlikely for your file) | Only if **you** put it in the prompt |
| Main bottleneck | Compute, data quality, time | Latency, token cost, context size |
| You in this course | Mostly learn concepts | Build agents that call models |

## Pre-training vs fine-tuning (short version)

- **Pre-training** — broad language ability from general text ("how language works").
- **Fine-tuning** — narrower behavior ("answer like a doctor," "output JSON tools," "refuse illegal advice").

Products you use are often **base model + fine-tuning + safety layers + UI**. When Module 2 compares Claude vs GPT vs open-source, you are comparing different training recipes and inference stacks.

## Why this matters for agents

1. **Do not expect live learning.** If an agent must remember facts long-term, you add **memory**, **databases**, or **RAG** — not "train the model on the fly."
2. **Behavior changes come from prompts and tools first.** Cheaper than retraining.
3. **Hallucinations make sense.** Inference predicts plausible text; it is not retrieving a verified fact table unless you give it one.

## Mini scenario

| Situation | Training or inference? |
|-----------|------------------------|
| OpenAI runs a multi-month job on 10,000 GPUs to release GPT-4.1 | Training |
| You send "Summarize this email" to the API | Inference |
| A company fine-tunes an open model on its support tickets | Training (specialized) |
| Your Hermes agent calls OpenRouter on each Telegram message | Inference |

## Common misconceptions

| Myth | Reality |
|------|---------|
| "The model learned my password from our chat." | Inference uses your prompt in memory for that session; it does not rewrite global weights. |
| "Smarter prompts train the model." | Prompts steer inference; they do not update parameters. |
| "Bigger context = the model knows more facts." | Context gives more **input** at inference time; it does not replace training. |

## Takeaway

**Training** builds the engine once. **Inference** runs the engine on your input every time. As an AgentCraft builder you live in inference — and you design prompts, context, tools, and memory around that fact.
