"""Module 1 interactive curriculum extras: expanded checkpoint + per-lesson recap banks."""

MODULE_1_CHECKPOINT = {
    "questions": [
        {
            "id": "m1-q1",
            "prompt": "Which best describes an LLM?",
            "options": [
                "A fixed database of every possible answer",
                "A model trained to predict and generate language from patterns in data",
                "A rule-based chatbot with hand-written scripts only",
            ],
            "answer_index": 1,
        },
        {
            "id": "m1-q2",
            "prompt": "What does AI typically mean in this course?",
            "options": [
                "Only physical robots that move around",
                "Systems that perform tasks that usually need human-like intelligence",
                "Any website with a search box",
            ],
            "answer_index": 1,
        },
        {
            "id": "m1-q3",
            "prompt": "An “LLM model” in practice usually refers to:",
            "options": [
                "A specific trained model you can call (e.g. via an API or locally)",
                "A single PowerPoint slide about AI",
                "A password for ChatGPT",
            ],
            "answer_index": 0,
        },
        {
            "id": "m1-q4",
            "prompt": "Why do builders care which model they pick?",
            "options": [
                "Models only differ by logo color",
                "Models trade off speed, cost, quality, context length, and tool skill",
                "Every model is identical once you open a browser",
            ],
            "answer_index": 1,
        },
        {
            "id": "m1-q5",
            "prompt": "Modern AI agents are best described as:",
            "options": [
                "A product layer on LLMs that can plan, use tools, and loop",
                "A replacement for electricity",
                "Only 1950s expert systems with no learning",
            ],
            "answer_index": 0,
        },
    ]
}

MODULE_1_RECAP = {
    "what-is-ai": [
        {
            "id": "m1-ai-rq1",
            "prompt": "In Knight's Academy, AI mainly means…",
            "options": [
                "Software that performs tasks needing human-like judgment (especially with language)",
                "Any website with a login button",
                "Only humanoid robots on campus",
            ],
            "answer_index": 0,
        },
        {
            "id": "m1-ai-rq2",
            "prompt": "Which statement is true?",
            "options": [
                "AI is always a perfect source of truth",
                "AI can draft and summarize but can still be wrong or overconfident",
                "AI never uses patterns from training data",
            ],
            "answer_index": 1,
        },
        {
            "id": "m1-ai-rq3",
            "prompt": "Why does this course focus on language-based AI?",
            "options": [
                "Because language models are the foundation for modern AI agents",
                "Because images are illegal in browsers",
                "Because keyboards cannot type numbers",
            ],
            "answer_index": 0,
        },
        {
            "id": "m1-ai-rq4",
            "prompt": "Asking an assistant to turn a long email into three bullets is an example of…",
            "options": [
                "AI applied to language (prediction + formatting)",
                "Replacing your Wi‑Fi router firmware",
                "A mechanical timer popping toast",
            ],
            "answer_index": 0,
        },
        {
            "id": "m1-ai-rq5",
            "prompt": "A helpful mindset for beginners is:",
            "options": [
                "Treat AI like a person who never errs",
                "Give clear instructions and verify important outputs",
                "Never read what the model returns",
            ],
            "answer_index": 1,
        },
    ],
    "what-are-llms": [
        {
            "id": "m1-llm-rq1",
            "prompt": "An LLM primarily learns to…",
            "options": [
                "Predict the next token from patterns in text",
                "Guaranteed-correct answers to every exam",
                "Control physical robot joints only",
            ],
            "answer_index": 0,
        },
        {
            "id": "m1-llm-rq2",
            "prompt": "“Large” in Large Language Model usually refers to…",
            "options": [
                "Huge training data and many parameters",
                "The physical size of the laptop screen",
                "How loud the fans get",
            ],
            "answer_index": 0,
        },
        {
            "id": "m1-llm-rq3",
            "prompt": "A useful mental model for an LLM is:",
            "options": [
                "Supercharged autocomplete for language",
                "A paper dictionary that cannot generate new sentences",
                "A light switch with two states only",
            ],
            "answer_index": 0,
        },
        {
            "id": "m1-llm-rq4",
            "prompt": "A hallucination is…",
            "options": [
                "Confident-sounding wrong output",
                "When the GPU is cold",
                "A perfect citation of every source",
            ],
            "answer_index": 0,
        },
        {
            "id": "m1-llm-rq5",
            "prompt": "Tokens are best described as…",
            "options": [
                "Bite-sized pieces of text the model predicts",
                "USB cables",
                "User passwords",
            ],
            "answer_index": 0,
        },
    ],
    "what-is-an-llm-model": [
        {
            "id": "m1-model-rq1",
            "prompt": "An LLM model is…",
            "options": [
                "A specific trained artifact you can call via API or run locally",
                "Any website’s CSS theme",
                "The chat product’s marketing slogan",
            ],
            "answer_index": 0,
        },
        {
            "id": "m1-model-rq2",
            "prompt": "A chat product like Claude.ai or ChatGPT typically…",
            "options": [
                "Wraps one or more models with UI, memory, tools, and safety",
                "Is identical to raw model weights with no extra layers",
                "Cannot use a model at all",
            ],
            "answer_index": 0,
        },
        {
            "id": "m1-model-rq3",
            "prompt": "When you “call a model,” the basic loop is:",
            "options": [
                "Send prompt → run inference → get text (or structured) output",
                "Flip a breaker → reboot the building → print a PDF",
                "Delete the database → hope for the best",
            ],
            "answer_index": 0,
        },
        {
            "id": "m1-model-rq4",
            "prompt": "Builders compare models because they differ in…",
            "options": [
                "Speed, cost, quality, context length, and tool-use skill",
                "Only the font on the login page",
                "Whether water is wet",
            ],
            "answer_index": 0,
        },
        {
            "id": "m1-model-rq5",
            "prompt": "In Knight's Academy, “pick a model” means…",
            "options": [
                "Choose which trained LLM will power a feature or agent",
                "Choose a desktop wallpaper",
                "Choose a cafeteria table",
            ],
            "answer_index": 0,
        },
    ],
    "brief-history": [
        {
            "id": "m1-hist-rq1",
            "prompt": "Early rule-based AI systems were often…",
            "options": [
                "Brittle outside narrow domains",
                "Perfect at every open-world task",
                "Identical to today’s LLM agents",
            ],
            "answer_index": 0,
        },
        {
            "id": "m1-hist-rq2",
            "prompt": "Transformers (2017+) mattered because they…",
            "options": [
                "Unlocked scalable language models",
                "Banned electricity",
                "Removed the need for any data",
            ],
            "answer_index": 0,
        },
        {
            "id": "m1-hist-rq3",
            "prompt": "The LLM era is associated with…",
            "options": [
                "Chat UIs and then tool-using agents",
                "Only mechanical clocks",
                "Abandoning neural networks forever",
            ],
            "answer_index": 0,
        },
        {
            "id": "m1-hist-rq4",
            "prompt": "Modern agents are best seen as…",
            "options": [
                "A product layer on LLMs: plan, use tools, observe, repeat",
                "A total replacement for keyboards",
                "Unrelated to language models",
            ],
            "answer_index": 0,
        },
        {
            "id": "m1-hist-rq5",
            "prompt": "For Knight's Academy day-to-day work, you mostly live in…",
            "options": [
                "The LLM + prompts + tools era",
                "1950s vacuum-tube assembly only",
                "Hand-written HTML with no models ever",
            ],
            "answer_index": 0,
        },
    ],
}
