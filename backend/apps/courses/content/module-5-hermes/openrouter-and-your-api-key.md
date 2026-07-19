# OpenRouter and Your API Key

## Why this comes before the install
Hermes v0.18.2's installer launches a **setup wizard** that asks for your model provider and API key *mid-install*. So we get our ducks in a row first: account, spending cap, key. When the wizard asks, you'll paste and keep moving instead of scrambling in a second browser tab.

## Why OpenRouter
One API key, many models. OpenRouter sits in the third box of our diagram: Hermes sends it requests, it routes them to whichever model we pick. Swapping models later is a config change, not a rebuild — and it has **free models**, which is what we'll use for this course.

## Get a key (the safe way)
1. **Sign up: [https://openrouter.ai](https://openrouter.ai)** — use a **dedicated email**, not your personal one. One identity for the agent means one kill switch if anything goes wrong.
2. Set a **hard spending cap of $5** in the dashboard *before anything else*. If the agent loops, the cap stops the bleeding. $5 is more than enough for this whole course — and since we use free models, you may spend nothing at all.
3. Create your API key at [https://openrouter.ai/settings/keys](https://openrouter.ai/settings/keys). Copy it somewhere you can paste from in the next lesson — you won't be able to view it again later.

![OpenRouter dashboard with the $5 spending cap set](/images/lessons/hermes-openrouter/spending-cap.png)

![Creating the API key at openrouter.ai/settings/keys](/images/lessons/hermes-openrouter/create-key.png)

## Pick your model (decide now, click later)
The wizard will also ask which model to use. Free models are tagged `:free`. Course recommendation: **`openai/gpt-oss-20b:free`** — the NVIDIA Nemotron free models also work fine and behave similarly. Anything with the `:free` tag is acceptable; if you already have a paid key for Claude or another provider you prefer, that works too (same $5-cap idea applies).

**Expectations check:** free models are slow and stubborn. A response can take **2–3 minutes** while the agent flails around trying commands — that's normal, not broken. You're trading patience for a $0 bill, which is the right trade while learning.

## Checkpoint
Key created, cap set, model chosen — and **nothing installed yet**. Don't run any installer until the next lesson; we walk the wizard together.

## Takeaway
The spending cap is your first guardrail and it exists before the agent does. Credentials ready, boundaries set — now we can let the installer ask its questions.
