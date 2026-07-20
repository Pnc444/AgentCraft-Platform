"""Curriculum spec + lesson content loading, shared by seed_demo and sync_content.

Lesson markdown lives in apps/courses/content/<course-slug>/<lesson-slug>.md.
Drop a .md file there and run `python manage.py sync_content` (prod-safe) or
`python manage.py seed_demo` (dev full reset).
"""

from pathlib import Path

CONTENT_DIR = Path(__file__).resolve().parent / "content"

SKILL = {
    "slug": "create-an-ai-agent",
    "name": "Create an AI Agent",
    "description": "Build AI agents from foundations through capstone",
    "order": 1,
}


def placeholder(title: str) -> str:
    return f"# {title}\n\nLesson Content"


def load_content(course_slug: str, lesson_slug: str, title: str) -> str:
    """Prefer a non-empty content/*.md file; fall back to in-file dicts, then placeholder."""
    path = CONTENT_DIR / course_slug / f"{lesson_slug}.md"
    if path.is_file():
        text = path.read_text(encoding="utf-8")
        if text.strip():
            return text
    return MODULE_1_CONTENT.get(lesson_slug, placeholder(title))


def default_recap_questions(title: str, slug: str) -> list[dict]:
    """Filler recap bank so every lesson can be completed (≥80%) until real questions are written."""
    return [
        {
            "id": f"{slug}-rq1",
            "prompt": f"What is the main focus of the lesson “{title}”?",
            "options": [
                f"Concepts related to {title}",
                "How to reset a router password",
                "Formatting a spreadsheet only",
            ],
            "answer_index": 0,
        },
        {
            "id": f"{slug}-rq2",
            "prompt": "When you finish a lesson with a video, what should you do before the Recap Quiz?",
            "options": [
                "Watch the video through to the end",
                "Skip the video and guess on the quiz",
                "Close the browser and come back later without watching",
            ],
            "answer_index": 0,
        },
        {
            "id": f"{slug}-rq3",
            "prompt": "What score do you need on the Recap Quiz to complete a lesson?",
            "options": ["At least 80%", "Exactly 50%", "Any score is enough"],
            "answer_index": 0,
        },
        {
            "id": f"{slug}-rq4",
            "prompt": "Where should instructors add or edit lesson questions?",
            "options": [
                "Django admin (lesson quiz / sandbox config)",
                "Only in the browser URL bar",
                "Inside the Postgres password field",
            ],
            "answer_index": 0,
        },
        {
            "id": f"{slug}-rq5",
            "prompt": "If you miss a Recap Quiz question, what can you do?",
            "options": [
                "Retry the quiz until you reach 80% or higher",
                "Nothing — the lesson is permanently locked",
                "Delete the course from the database",
            ],
            "answer_index": 0,
        },
    ]


# Module 1 checkpoint — questions only (infinite retries in the UI). Terminology is
# introduced across earlier lessons, not as a standalone vocab page.
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
    ]
}

# Legacy in-file content for Module 1 — migrate these to content/*.md files over time.
MODULE_1_CONTENT = {
    "what-is-ai": """# What is AI?

**Filler lesson** — replace with final curriculum copy later.

## In plain terms
**Artificial intelligence (AI)** is a broad label for software that performs tasks that usually need human-like judgment: recognizing patterns, making predictions, or generating new content.

In this course we focus on **language-based AI** — systems that read and write text — because that’s the foundation for modern AI agents.

## What AI is (and isn’t)
- **Is:** pattern-matching at scale, trained on data, useful for drafting, summarizing, and deciding next steps with tools.
- **Isn’t:** a person, a perfect truth source, or a single “brain” that understands the world the way you do.

## Mini example
You ask: *“Summarize this email in three bullets.”*
An AI assistant drafts the bullets from the text you provided. That’s AI applied to language — not magic, just prediction + formatting.

## Takeaway
When we say “AI” here, we mean systems that help with intelligent-looking tasks — especially with language — so you can eventually wire them into **agents** that take actions.
""",
    "what-are-llms": """# What are LLMs?

**Filler lesson** — replace with final curriculum copy later.

## Definition
A **Large Language Model (LLM)** is a neural network trained on huge amounts of text to predict the next token (roughly: the next piece of a word). Stack those predictions and you get fluent paragraphs, code, and dialogue.

## Why “large”?
- Trained on massive datasets (web text, books, code, etc.)
- Billions of parameters (internal knobs learned during training)
- General-purpose: one model can chat, translate, outline, and brainstorm

## Everyday mental model
Think of an LLM as a **supercharged autocomplete** that has seen so much language it can continue almost any prompt in a useful way — if you give it clear instructions and context.

## Key terms (as you go)
| Term | Rough meaning |
|------|----------------|
| Prompt | What you send the model |
| Completion / response | What the model returns |
| Hallucination | Confident-sounding wrong output |

## Takeaway
LLMs are the engine behind most modern chatbots and agents you’ll meet in later modules.
""",
    "what-is-an-llm-model": """# What is an LLM model?

**Filler lesson** — replace with final curriculum copy later.

## “Model” vs “product”
- An **LLM model** is a specific trained artifact (e.g. a Claude, GPT, Gemini, or open-source checkpoint) you can call via API or run locally.
- A **product** (ChatGPT, Claude.ai, etc.) wraps a model with UI, memory, tools, and safety layers.

When builders say “pick a model,” they usually mean: which trained model should power this feature?

## What you get when you “call a model”
1. You send a prompt (plus optional system instructions).
2. The provider runs inference on that model.
3. You get text (or structured JSON) back.

## Why the name matters
Different models trade off **speed**, **cost**, **quality**, **context length**, and **tool-use** skill. Module 2 compares families; for now just remember: a model is a concrete thing you invoke, not a vague “AI cloud.”

## Takeaway
In AgentCraft, “model” = the specific LLM you point your agent or app at.
""",
    "brief-history": """# Brief History

**Filler lesson** — replace with final curriculum copy later.

## A tiny timeline (compressed)
1. **Early AI (1950s–80s)** — rules, search, expert systems. Brittle outside narrow domains.
2. **Machine learning boom (1990s–2010s)** — learn from data; deep learning wins at vision and speech.
3. **Transformers (2017+)** — architecture that unlocked scalable language models.
4. **LLM era (2020+)** — GPT-class models, chat UIs, then **tool-using agents**.

## Why this matters for agents
Agents aren’t new science-fiction — they’re the next product layer on top of LLMs: plan → call tools → observe → repeat. Understanding that LLMs came first helps you see why prompting, context, and model choice still matter.

## Placeholder note
Expand with named milestones, demos, and reading links when final content is ready.

## Takeaway
Today’s agent stack sits on decades of AI research, but you’ll mostly work in the **LLM + tools** era.
""",
    "checkpoint": """# Checkpoint

Quick check on Module 1 ideas: AI, LLMs, and what a “model” means in practice.

Answer the question below. You can retry as many times as you need.
""",
}


# Module 5 recap questions — real questions written from the lesson content.
MODULE_5_RECAP = {
    "what-hermes-is": [
        {
            "id": "m5-wh-1",
            "prompt": "What is Hermes?",
            "options": [
                "An AI model that runs on your machine",
                "An orchestrator that sits between you and a model provider, and executes actions",
                "A chat website like ChatGPT",
            ],
            "answer_index": 1,
        },
        {
            "id": "m5-wh-2",
            "prompt": "In the three-box diagram, which box runs on YOUR machine?",
            "options": [
                "The agent loop + tools (Hermes itself)",
                "The model provider",
                "None of them \u2014 everything runs in the cloud",
            ],
            "answer_index": 0,
        },
        {
            "id": "m5-wh-3",
            "prompt": "Where does the \u201cheavy thinking\u201d happen?",
            "options": [
                "On your machine, inside the container",
                "In the gateway (e.g. Telegram)",
                "On the model provider's servers",
            ],
            "answer_index": 2,
        },
        {
            "id": "m5-wh-4",
            "prompt": "What is a gateway in the Hermes architecture?",
            "options": [
                "How tasks get in \u2014 the CLI now, chat apps later",
                "The firewall between the agent and the internet",
                "The database where memories are stored",
            ],
            "answer_index": 0,
        },
        {
            "id": "m5-wh-5",
            "prompt": "Why does this module care so much about safety?",
            "options": [
                "Because the model might become self-aware",
                "Because the *doing* \u2014 shell commands, file access \u2014 happens on your machine",
                "Because OpenRouter requires it",
            ],
            "answer_index": 1,
        },
    ],
    "install-and-blank-slate": [
        {
            "id": "m5-ib-1",
            "prompt": "What does \u201cblank slate\u201d mean after installing Hermes?",
            "options": [
                "No API keys, no memory, no skills, nothing configured",
                "A fresh conversation window",
                "An empty Docker container",
            ],
            "answer_index": 0,
        },
        {
            "id": "m5-ib-2",
            "prompt": "Why do we deliberately stop BEFORE the first conversation?",
            "options": [
                "The API key takes 24 hours to activate",
                "The agent doesn't get turned on until it's sandboxed",
                "To let the installer finish downloading models",
            ],
            "answer_index": 1,
        },
        {
            "id": "m5-ib-3",
            "prompt": "What does the `sandbox backend` setting default to?",
            "options": [
                "docker",
                "ssh",
                "local \u2014 which we will never use for a running agent",
            ],
            "answer_index": 2,
        },
        {
            "id": "m5-ib-4",
            "prompt": "At the end of this lesson's checkpoint, the agent should be:",
            "options": [
                "Installed but NOT yet run \u2014 no keys entered",
                "Running with the default settings",
                "Connected to Telegram",
            ],
            "answer_index": 0,
        },
        {
            "id": "m5-ib-5",
            "prompt": "The course pins a specific Hermes version. What should you do if your install looks different?",
            "options": [
                "Uninstall Docker and try again",
                "Expect version drift \u2014 newer versions likely work, minor differences are normal",
                "Stop the course and wait for an update",
            ],
            "answer_index": 1,
        },
    ],
    "docker-as-backend": [
        {
            "id": "m5-db-1",
            "prompt": "Why do we set up the Docker backend BEFORE the first real conversation?",
            "options": [
                "Docker makes the model respond faster",
                "With the default `local` backend there is no isolation at all \u2014 box before power switch",
                "OpenRouter refuses connections from unsandboxed agents",
            ],
            "answer_index": 1,
        },
        {
            "id": "m5-db-2",
            "prompt": "Which command switches Hermes to the Docker backend?",
            "options": [
                "hermes config set terminal.backend docker",
                "docker run hermes --sandbox",
                "hermes --enable-docker",
            ],
            "answer_index": 0,
        },
        {
            "id": "m5-db-3",
            "prompt": "How many sandbox containers does Hermes use while it runs?",
            "options": [
                "A new container for every command",
                "Two \u2014 one for files, one for commands",
                "One long-lived container that every command runs inside",
            ],
            "answer_index": 2,
        },
        {
            "id": "m5-db-4",
            "prompt": "Where does your API key live once the sandbox is running?",
            "options": [
                "In ~/.hermes/.env on the host \u2014 commands inside the container never see it",
                "Copied into the container at /workspace/.env",
                "Uploaded to the model provider for safekeeping",
            ],
            "answer_index": 0,
        },
        {
            "id": "m5-db-5",
            "prompt": "How do you verify the sandbox container actually exists?",
            "options": [
                "Ask the agent \u2014 it always knows",
                "Run `docker ps` in your own terminal and look for the sandbox container",
                "Check Task Manager for a process called hermes-box",
            ],
            "answer_index": 1,
        },
    ],
    "openrouter-first-conversation": [
        {
            "id": "m5-of-1",
            "prompt": "Why does the course use OpenRouter?",
            "options": [
                "It's the only provider Hermes supports",
                "One API key, many models \u2014 swapping models is a config change, not a rebuild",
                "It's the fastest provider",
            ],
            "answer_index": 1,
        },
        {
            "id": "m5-of-2",
            "prompt": "Why create the OpenRouter account with a dedicated email?",
            "options": [
                "One identity for the agent means one kill switch if anything goes wrong",
                "OpenRouter bans personal email domains",
                "It gets you more free credits",
            ],
            "answer_index": 0,
        },
        {
            "id": "m5-of-3",
            "prompt": "What must you set in the OpenRouter dashboard BEFORE the first request?",
            "options": [
                "A profile picture for the agent",
                "Two-factor authentication",
                "A hard spending cap (the course uses $5)",
            ],
            "answer_index": 2,
        },
        {
            "id": "m5-of-4",
            "prompt": "Where does `hermes config set OPENROUTER_API_KEY ...` store the key?",
            "options": [
                "In ~/.hermes/.env",
                "Inside the sandbox container",
                "In config.yaml next to the model name",
            ],
            "answer_index": 0,
        },
        {
            "id": "m5-of-5",
            "prompt": "The parity checkpoint requires every student's agent to do what?",
            "options": [
                "Write a poem and send an email",
                "Respond to a CLI message AND successfully run a shell command",
                "Connect to Telegram and Discord",
            ],
            "answer_index": 1,
        },
    ],
    "sandbox-verification-lab": [
        {
            "id": "m5-sv-1",
            "prompt": "What's the point of the escape-attempt lab?",
            "options": [
                "You verify the containment yourself \u2014 failed escapes teach the isolation model",
                "To find bugs in Docker and report them",
                "To measure how fast the agent responds",
            ],
            "answer_index": 0,
        },
        {
            "id": "m5-sv-2",
            "prompt": "You ask the agent to read a file on your Desktop. What happens?",
            "options": [
                "It reads it \u2014 the sandbox only blocks writes",
                "The path doesn't exist \u2014 the container has its own filesystem",
                "Docker shows a permission popup",
            ],
            "answer_index": 1,
        },
        {
            "id": "m5-sv-3",
            "prompt": "The agent appends a line to /etc/hosts and it WORKS. Why is that still contained?",
            "options": [
                "It edited the container's copy \u2014 your machine's file is untouched and the change dies with the container",
                "It isn't \u2014 that's a security hole you should report",
                "Docker automatically reverts the change every minute",
            ],
            "answer_index": 0,
        },
        {
            "id": "m5-sv-4",
            "prompt": "Why is the fork bomb an instructor-only demo?",
            "options": [
                "It requires a paid Docker license",
                "It's boring to watch twice",
                "Run outside a sandbox it will freeze the machine \u2014 the demo shows the container's PID limit catching it",
            ],
            "answer_index": 2,
        },
        {
            "id": "m5-sv-5",
            "prompt": "\u201cFetch https://example.com and summarize it\u201d works from inside the sandbox. What's the lesson?",
            "options": [
                "The sandbox is broken and needs reconfiguring",
                "Docker limits what the agent can *touch*, not what it can *say to the internet* \u2014 that's Module 6's problem",
                "Websites can't tell the request came from a container",
            ],
            "answer_index": 1,
        },
    ],
}


# Module 4.5 recap questions — real questions written from the lesson content.
MODULE_4_5_RECAP = {
    "why-docker": [
        {
            "id": "m45-wd-1",
            "prompt": "What problem is Docker primarily built to solve?",
            "options": [
                "Computers not having enough storage for big apps",
                "\u201cIt works on my machine\u201d \u2014 code breaking on other computers due to environment differences",
                "Slow internet connections when downloading software",
            ],
            "answer_index": 1,
        },
        {
            "id": "m45-wd-2",
            "prompt": "What does a Docker container package together?",
            "options": [
                "The app plus everything it needs to run \u2014 code, runtime, libraries, settings",
                "Only the app's source code",
                "Just the operating system, with no application code",
            ],
            "answer_index": 0,
        },
        {
            "id": "m45-wd-3",
            "prompt": "Why does isolation matter when running AI agents?",
            "options": [
                "It makes the agent respond faster",
                "It hides the agent from other students",
                "An agent in a container can't wreck the rest of your computer",
            ],
            "answer_index": 2,
        },
        {
            "id": "m45-wd-4",
            "prompt": "Why does the course run every student's agent in the same container environment?",
            "options": [
                "Reproducibility \u2014 the builds behave the same for everyone",
                "Because Docker is the only way to run Python",
                "So students can't modify their own code",
            ],
            "answer_index": 0,
        },
        {
            "id": "m45-wd-5",
            "prompt": "In the shipping-container analogy, what is your computer?",
            "options": [
                "The crane",
                "The ship \u2014 it carries containers without caring what's inside",
                "The cargo inside the container",
            ],
            "answer_index": 1,
        },
    ],
    "docker-main-terms": [
        {
            "id": "m45-mt-1",
            "prompt": "What's the difference between an image and a container?",
            "options": [
                "An image is a read-only snapshot; a container is a running instance of it",
                "They're two names for the same thing",
                "A container is the recipe; an image is the dish",
            ],
            "answer_index": 0,
        },
        {
            "id": "m45-mt-2",
            "prompt": "Where does `docker run` download images from if they're not on your machine?",
            "options": [
                "Your operating system's app store",
                "GitHub",
                "Docker Hub (a registry)",
            ],
            "answer_index": 2,
        },
        {
            "id": "m45-mt-3",
            "prompt": "What is a volume for?",
            "options": [
                "Persistent storage that survives even when the container is deleted",
                "Making containers run louder",
                "Limiting how much CPU a container can use",
            ],
            "answer_index": 0,
        },
        {
            "id": "m45-mt-4",
            "prompt": "What does port mapping do?",
            "options": [
                "Deletes unused network ports",
                "Connects a port on your machine to a port inside a container",
                "Encrypts traffic between containers",
            ],
            "answer_index": 1,
        },
        {
            "id": "m45-mt-5",
            "prompt": "If you delete a container, what happens to the image it was made from?",
            "options": [
                "The image is deleted too",
                "The image becomes read-only",
                "Nothing \u2014 deleting a container never touches the image",
            ],
            "answer_index": 2,
        },
    ],
    "installing-docker-desktop": [
        {
            "id": "m45-id-1",
            "prompt": "On Windows, what should you do with the \u201cUse WSL 2\u201d option during install?",
            "options": [
                "Keep it checked \u2014 Docker Desktop on Windows runs on WSL 2",
                "Uncheck it to save disk space",
                "It doesn't matter either way",
            ],
            "answer_index": 0,
        },
        {
            "id": "m45-id-2",
            "prompt": "Do you need to create a Docker account for this course?",
            "options": [
                "Yes, containers won't run without one",
                "No \u2014 you can skip sign-in; it's not required",
                "Only on Mac",
            ],
            "answer_index": 1,
        },
        {
            "id": "m45-id-3",
            "prompt": "How do you know Docker is ready to use?",
            "options": [
                "The installer window closes",
                "Your computer restarts automatically",
                "The whale icon stops animating and the dashboard shows \u201cEngine running\u201d",
            ],
            "answer_index": 2,
        },
        {
            "id": "m45-id-4",
            "prompt": "Which command verifies Docker is installed from a terminal?",
            "options": [
                "docker --version",
                "docker install --check",
                "wsl --status",
            ],
            "answer_index": 0,
        },
        {
            "id": "m45-id-5",
            "prompt": "The installer says \u201cVirtualization is not enabled.\u201d Where do you fix that?",
            "options": [
                "In Docker Desktop's settings menu",
                "In your BIOS/UEFI settings (Intel VT-x / AMD-V)",
                "By reinstalling Windows",
            ],
            "answer_index": 1,
        },
    ],
    "first-containers": [
        {
            "id": "m45-fc-1",
            "prompt": "You run `docker run hello-world` and the image isn't on your machine. What happens?",
            "options": [
                "Docker pulls the image from Docker Hub, creates a container, and runs it",
                "You get an error and must download the image manually",
                "Docker builds the image from a Dockerfile on your desktop",
            ],
            "answer_index": 0,
        },
        {
            "id": "m45-fc-2",
            "prompt": "In `docker run -d -p 8080:80 nginx`, what does `-p 8080:80` mean?",
            "options": [
                "Run 8,080 copies on 80 CPUs",
                "Limit the container to 8080 MB of memory",
                "Map port 8080 on your machine to port 80 inside the container",
            ],
            "answer_index": 2,
        },
        {
            "id": "m45-fc-3",
            "prompt": "What does the `-d` flag do?",
            "options": [
                "Deletes the container when it stops",
                "Runs the container detached, in the background",
                "Downloads the image without running it",
            ],
            "answer_index": 1,
        },
        {
            "id": "m45-fc-4",
            "prompt": "After you stop and delete the nginx container, what's left on your machine?",
            "options": [
                "Leftover nginx config files you must clean up",
                "A background service that keeps running",
                "Just the cached image \u2014 your machine is otherwise unchanged",
            ],
            "answer_index": 2,
        },
        {
            "id": "m45-fc-5",
            "prompt": "You get \u201cport is already allocated\u201d on 8080. What's the fix?",
            "options": [
                "Use a different host port, e.g. `-p 8081:80`",
                "Restart your computer",
                "Delete the nginx image and re-pull it",
            ],
            "answer_index": 0,
        },
    ],
}


# Module 1.5 recap questions — context windows, tokens, training vs inference.
MODULE_1_5_RECAP = {
    "context-windows": [
        {
            "id": "m15-cw-rq1",
            "prompt": "A context window is best described as:",
            "options": [
                "The maximum amount of text (in tokens) a model can use when generating a reply",
                "The model's permanent memory of every conversation you ever had",
                "The number of users who can chat at the same time",
            ],
            "answer_index": 0,
        },
        {
            "id": "m15-cw-rq2",
            "prompt": "Which items typically compete for space inside the context window?",
            "options": [
                "System instructions, chat history, pasted documents, and your latest message",
                "Only the last word you typed",
                "Your computer's RAM and CPU usage meters",
            ],
            "answer_index": 0,
        },
        {
            "id": "m15-cw-rq3",
            "prompt": "In a very long chat thread, why might the model seem to 'forget' what you said at the start?",
            "options": [
                "Older messages may fall outside the context window or get truncated",
                "LLMs deliberately erase user messages after 10 minutes",
                "The model saves early messages to a private database instead of using them",
            ],
            "answer_index": 0,
        },
        {
            "id": "m15-cw-rq4",
            "prompt": "You need help with one bug in a huge codebase. What is usually the best context strategy?",
            "options": [
                "Paste the relevant file or function plus the error message, not the entire repo",
                "Paste every file so the model sees everything at once",
                "Send only the word 'bug' with no code",
            ],
            "answer_index": 0,
        },
        {
            "id": "m15-cw-rq5",
            "prompt": "Context window size is measured in:",
            "options": [
                "Tokens",
                "Pages of printed paper",
                "Megabytes of GPU video memory only",
            ],
            "answer_index": 0,
        },
    ],
    "tokens": [
        {
            "id": "m15-tk-rq1",
            "prompt": "In LLMs, a token is:",
            "options": [
                "A small chunk of text the model processes — not always a whole word",
                "Always exactly one English word",
                "A type of cryptocurrency used to pay for GPUs",
            ],
            "answer_index": 0,
        },
        {
            "id": "m15-tk-rq2",
            "prompt": "Why can you NOT assume 1 word equals 1 token?",
            "options": [
                "Tokenizers split text into pieces; words, subwords, and symbols vary in length",
                "Models ignore all words longer than four letters",
                "Only punctuation counts as tokens",
            ],
            "answer_index": 0,
        },
        {
            "id": "m15-tk-rq3",
            "prompt": "Most API pricing for LLMs is based on:",
            "options": [
                "Input tokens and output tokens",
                "The number of paragraphs you write",
                "Your monitor's screen resolution",
            ],
            "answer_index": 0,
        },
        {
            "id": "m15-tk-rq4",
            "prompt": "When a model generates a response one piece at a time, it is predicting:",
            "options": [
                "The next token, repeatedly, until the reply is complete",
                "The entire answer in one lookup from a fixed database",
                "Random words with no connection to the prompt",
            ],
            "answer_index": 0,
        },
        {
            "id": "m15-tk-rq5",
            "prompt": "A rough rule of thumb for English prose is:",
            "options": [
                "About 1 token per 4 characters",
                "Exactly 1 token per sentence",
                "Tokens only exist for numbers, not letters",
            ],
            "answer_index": 0,
        },
    ],
    "training-vs-inference": [
        {
            "id": "m15-tvi-rq1",
            "prompt": "Training an LLM primarily means:",
            "options": [
                "Adjusting the model's weights on large datasets so it learns language patterns",
                "Sending a long chat message so the model remembers you forever",
                "Installing Docker on your laptop",
            ],
            "answer_index": 0,
        },
        {
            "id": "m15-tvi-rq2",
            "prompt": "Inference is:",
            "options": [
                "Using an already-trained model to generate output from your prompt",
                "The same thing as pre-training on the entire internet",
                "Deleting old chat logs from a database",
            ],
            "answer_index": 0,
        },
        {
            "id": "m15-tvi-rq3",
            "prompt": "During normal chat inference, the model's weights:",
            "options": [
                "Stay frozen — they do not update from your conversation",
                "Rewrite themselves after every user message",
                "Are copied from your keyboard input",
            ],
            "answer_index": 0,
        },
        {
            "id": "m15-tvi-rq4",
            "prompt": "Which activity is inference, not training?",
            "options": [
                "Calling an API with 'Summarize this email' and reading the reply",
                "A lab running a month-long GPU job to release a new base model",
                "Fine-tuning an open model on a curated dataset of support tickets",
            ],
            "answer_index": 0,
        },
        {
            "id": "m15-tvi-rq5",
            "prompt": "If an agent must remember facts across weeks, the usual solution is:",
            "options": [
                "Add memory, databases, or retrieval — not rely on one chat to retrain the model",
                "Send the same paragraph 10,000 times to train weights at home",
                "Assume the model automatically stores all user data in its parameters",
            ],
            "answer_index": 0,
        },
    ],
}


# Module 3 recap questions — real questions (ported from feat/module3).
MODULE_3_RECAP = {
    "what-prompts-are": [
        {
            "id": "m3-wpa-rq1",
            "prompt": "In this course, a prompt is best described as:",
            "options": [
                "The text and instructions you send to an LLM to shape its response",
                "A password that unlocks the model's training data",
                "The model's reply after it finishes generating",
            ],
            "answer_index": 0,
        },
        {
            "id": "m3-wpa-rq2",
            "prompt": "Which is NOT typically part of a well-formed prompt?",
            "options": [
                "Your router's MAC address",
                "The task you want done",
                "Relevant background context",
            ],
            "answer_index": 0,
        },
        {
            "id": "m3-wpa-rq3",
            "prompt": "Why do prompts matter for agents you'll build later?",
            "options": [
                "They are the main way you tell the model what to do, how to behave, and what context to use",
                "They replace the need for any tools or code",
                "They only affect spelling and grammar, not behavior",
            ],
            "answer_index": 0,
        },
        {
            "id": "m3-wpa-rq4",
            "prompt": "An LLM generates a response by:",
            "options": [
                "Predicting likely next tokens based on everything in the prompt (and prior conversation)",
                "Looking up a single pre-written answer in a fixed database",
                "Running only on keywords you bold in the prompt",
            ],
            "answer_index": 0,
        },
        {
            "id": "m3-wpa-rq5",
            "prompt": "If you change your prompt but keep the same model, you should expect:",
            "options": [
                "Different outputs, because the model conditions on the new instructions and context",
                "Exactly the same output every time",
                "The model to refuse all requests",
            ],
            "answer_index": 0,
        },
    ],
    "how-context-affects-responses": [
        {
            "id": "m3-hcar-rq1",
            "prompt": "Context in prompting refers to:",
            "options": [
                "All the information the model can see when generating (history, docs, examples, etc.)",
                "Only the font size of your message",
                "The physical location of the data center",
            ],
            "answer_index": 0,
        },
        {
            "id": "m3-hcar-rq2",
            "prompt": "Two people send the identical question but with different prior messages in the chat. The answers may differ because:",
            "options": [
                "The model uses conversation history as part of its context",
                "Models randomly ignore earlier messages",
                "User prompts cannot include more than one sentence",
            ],
            "answer_index": 0,
        },
        {
            "id": "m3-hcar-rq3",
            "prompt": "You paste a 50-page document above your question. What is a realistic trade-off?",
            "options": [
                "Richer answers from that material, but you use more of the context window and may hit limits",
                "The model automatically summarizes all 50 pages with zero token cost",
                "Longer context always makes answers shorter",
            ],
            "answer_index": 0,
        },
        {
            "id": "m3-hcar-rq4",
            "prompt": "Which change is most likely to alter the model's answer?",
            "options": [
                "Adding a paragraph that defines key terms and constraints before your question",
                "Sending the same text with an extra space at the end",
                "Using a different browser tab color",
            ],
            "answer_index": 0,
        },
        {
            "id": "m3-hcar-rq5",
            "prompt": "If important facts are missing from the context, the model may:",
            "options": [
                "Guess or fill gaps plausibly (hallucinate) instead of admitting ignorance",
                "Always stop and ask a clarifying question",
                "Access private files on your computer without permission",
            ],
            "answer_index": 0,
        },
    ],
    "system-vs-user-prompts": [
        {
            "id": "m3-svup-rq1",
            "prompt": "A system prompt is usually:",
            "options": [
                "Hidden instructions that set behavior, role, and rules for the assistant",
                "The same thing as the user's latest chat message",
                "Only used when the model is offline",
            ],
            "answer_index": 0,
        },
        {
            "id": "m3-svup-rq2",
            "prompt": "A user prompt is:",
            "options": [
                "What the end user (or your app on their behalf) sends as the request",
                "A secret key stored in the GPU",
                "The model's internal weight file",
            ],
            "answer_index": 0,
        },
        {
            "id": "m3-svup-rq3",
            "prompt": "Why separate system and user prompts when building an agent?",
            "options": [
                "So stable rules and persona stay in system instructions while each request stays in user messages",
                "Because models cannot read user messages at all",
                "To make every response identical regardless of the question",
            ],
            "answer_index": 0,
        },
        {
            "id": "m3-svup-rq4",
            "prompt": "In a chat API, message roles often include:",
            "options": [
                "system, user, and assistant",
                "only user and printer",
                "admin, guest, and firewall",
            ],
            "answer_index": 0,
        },
        {
            "id": "m3-svup-rq5",
            "prompt": "Putting 'Always reply in JSON' in the system prompt is useful because:",
            "options": [
                "It applies consistently to every turn without repeating it in each user message",
                "It hides the rule from the model entirely",
                "It disables the model's ability to follow instructions",
            ],
            "answer_index": 0,
        },
    ],
    "good-and-bad-prompts": [
        {
            "id": "m3-gabp-rq1",
            "prompt": "Which prompt is stronger for getting useful output?",
            "options": [
                "'Summarize the text below in 3 bullet points for a busy manager; use plain language.'",
                "'Do something with this.'",
                "'Write stuff.'",
            ],
            "answer_index": 0,
        },
        {
            "id": "m3-gabp-rq2",
            "prompt": "A common problem with vague prompts is:",
            "options": [
                "The model has to guess your goal, audience, and format",
                "The model runs out of electricity",
                "The context window doubles in size",
            ],
            "answer_index": 0,
        },
        {
            "id": "m3-gabp-rq3",
            "prompt": "Which pair of instructions is worst for the model?",
            "options": [
                "'Be extremely brief' and 'Write at least 800 words' in the same prompt",
                "'Use bullet points' and 'Keep it under 5 bullets'",
                "'Explain for a beginner' and 'Avoid jargon'",
            ],
            "answer_index": 0,
        },
        {
            "id": "m3-gabp-rq4",
            "prompt": "The CRAFT-style checklist includes:",
            "options": [
                "Context, Role, Action, Format, and constraints/Tone",
                "CPU, RAM, ASCII, FTP, and TLS only",
                "Copy, Rename, Archive, File, and Trash",
            ],
            "answer_index": 0,
        },
        {
            "id": "m3-gabp-rq5",
            "prompt": "Good prompts often specify:",
            "options": [
                "Who the answer is for, what to do, and how the output should look",
                "Only a single emoji",
                "Nothing — shorter is always better",
            ],
            "answer_index": 0,
        },
    ],
    "hands-on-prompt-exercises": [
        {
            "id": "m3-hope-rq1",
            "prompt": "When judging two prompts, you should prioritize:",
            "options": [
                "Clarity, relevant context, and explicit output format",
                "Which one is shorter, even if vague",
                "Which one uses the most technical buzzwords",
            ],
            "answer_index": 0,
        },
        {
            "id": "m3-hope-rq2",
            "prompt": "Prompt A: 'Fix my code.' Prompt B: 'Find the bug in this Python function, explain it in 2 sentences, then show a corrected version.' Which is better for a coding assistant?",
            "options": [
                "Prompt B — it states the language, task, and output shape",
                "Prompt A — less text always wins",
                "They are equally good because both mention code",
            ],
            "answer_index": 0,
        },
        {
            "id": "m3-hope-rq3",
            "prompt": "After trying a weak prompt and a strong prompt on the same model, a good sign the strong prompt worked is:",
            "options": [
                "The answer matches your requested format, audience, and constraints more closely",
                "The model returns a random Wikipedia article",
                "Both outputs are identical every time",
            ],
            "answer_index": 0,
        },
        {
            "id": "m3-hope-rq4",
            "prompt": "If a prompt omits the audience ('for executives' vs 'for new hires'), you should expect:",
            "options": [
                "A generic answer that may not fit the reader",
                "The model to refuse to answer",
                "Automatic translation into another language",
            ],
            "answer_index": 0,
        },
        {
            "id": "m3-hope-rq5",
            "prompt": "The best next step when a prompt gives poor results is usually to:",
            "options": [
                "Add missing context, clarify the task, and specify format — then test again",
                "Assume the model is broken and never use AI again",
                "Remove all details until the prompt is one word",
            ],
            "answer_index": 0,
        },
    ],
}


CURRICULUM = [
    {
        "order": 1,
        "title": "Introduction to AI",
        "slug": "module-1-introduction-to-ai",
        "description": "What AI and LLMs are, a brief history, and a checkpoint. Terminology is introduced as you go.",
        "published": True,
        "difficulty": 1,
        "lessons": [
            ("What is AI?", "what-is-ai", "theory", 8),
            ("What are LLMs?", "what-are-llms", "theory", 8),
            ("What is an LLM model?", "what-is-an-llm-model", "theory", 8),
            ("Brief History", "brief-history", "theory", 8),
            ("Checkpoint", "checkpoint", "quiz", 10, MODULE_1_CHECKPOINT),
        ],
    },
    {
        "order": 2,
        "title": "How LLMs Work",
        "slug": "module-1-5-how-llms-work",
        "description": "Context windows, tokens, and training vs inference.",
        "published": True,
        "difficulty": 1,
        "lessons": [
            ("Context Windows", "context-windows", "theory", 8, {"questions": MODULE_1_5_RECAP["context-windows"]}),
            ("Tokens", "tokens", "theory", 8, {"questions": MODULE_1_5_RECAP["tokens"]}),
            ("Training vs Inference", "training-vs-inference", "theory", 10, {"questions": MODULE_1_5_RECAP["training-vs-inference"]}),
        ],
    },
    {
        "order": 3,
        "title": "Exploring LLM Models",
        "slug": "module-2-exploring-llm-models",
        "description": "Compare Hermes, Claude, Gemini, OpenAI, and open-source models — strengths, weaknesses, and when to choose each.",
        "published": True,
        "difficulty": 1,
        "lessons": [
            ("Introducing Different Models", "introducing-different-models", "theory", 12),
            ("What Each Model Is Good At", "what-each-model-is-good-at", "theory", 12),
            ("Strengths and Weaknesses", "strengths-and-weaknesses", "theory", 10),
            ("When to Choose One Over Another", "when-to-choose", "theory", 10),
            ("Video: Explaining Each Model", "video-explaining-each-model", "theory", 15),
            ("Comparison Activity", "comparison-activity", "interactive", 15),
        ],
    },
    {
        "order": 4,
        "title": "Prompting",
        "slug": "module-3-prompting",
        "description": "What prompts are, how context shapes responses, system vs user prompts, and hands-on practice.",
        "published": True,
        "difficulty": 1,
        "lessons": [
            ("What Prompts Are", "what-prompts-are", "theory", 8, {"questions": MODULE_3_RECAP["what-prompts-are"]}),
            ("How Context Affects Responses", "how-context-affects-responses", "theory", 10, {"questions": MODULE_3_RECAP["how-context-affects-responses"]}),
            ("System Prompts vs User Prompts", "system-vs-user-prompts", "theory", 10, {"questions": MODULE_3_RECAP["system-vs-user-prompts"]}),
            ("Good and Bad Prompts", "good-and-bad-prompts", "theory", 10, {"questions": MODULE_3_RECAP["good-and-bad-prompts"]}),
            ("Hands-on Prompt Exercises", "hands-on-prompt-exercises", "interactive", 15, {"questions": MODULE_3_RECAP["hands-on-prompt-exercises"]}),
        ],
    },
    {
        "order": 5,
        "title": "AI Agents",
        "slug": "module-4-ai-agents",
        "description": "What agents are, how they differ from chatbots, workflows, and an intro to Hermes, OpenClaw, Claude, and Gemini agents.",
        "published": True,
        "difficulty": 2,
        "lessons": [
            ("What an AI Agent Is", "what-an-ai-agent-is", "theory", 10),
            ("Agents vs Chatbots", "agents-vs-chatbots", "theory", 8),
            ("Basic Agent Workflow", "basic-agent-workflow", "theory", 10),
            ("Memory, Tools, and Reasoning", "memory-tools-reasoning", "theory", 12),
            ("Examples of Real AI Agents", "examples-of-real-ai-agents", "theory", 10),
            ("Introduction to Our Agents", "introduction-to-our-agents", "theory", 10),
            ("Video + Activity", "video-and-activity", "interactive", 15),
        ],
    },
    {
        "order": 6,
        "title": "Docker and Environments",
        "slug": "module-4-5-docker-and-environments",
        "description": "Why Docker exists, the core terms, installing Docker Desktop, and running your first containers.",
        "published": True,
        "difficulty": 2,
        "lessons": [
            ("Why Docker?", "why-docker", "theory", 8, {"questions": MODULE_4_5_RECAP["why-docker"]}),
            ("The Main Terms", "docker-main-terms", "theory", 8, {"questions": MODULE_4_5_RECAP["docker-main-terms"]}),
            ("Installing Docker Desktop", "installing-docker-desktop", "interactive", 15, {"questions": MODULE_4_5_RECAP["installing-docker-desktop"]}),
            ("Your First Containers", "first-containers", "sandbox", 12, {"questions": MODULE_4_5_RECAP["first-containers"]}),
        ],
    },
    {
        "order": 7,
        "title": "Hermes (Build #1)",
        "slug": "module-5-hermes",
        "description": "Understand what Hermes is, install it, put it in a Docker sandbox before first run, connect OpenRouter, and verify the isolation yourself.",
        "published": True,
        "difficulty": 2,
        "lessons": [
            ("What Hermes Is", "what-hermes-is", "theory", 8, {"questions": MODULE_5_RECAP["what-hermes-is"]}),
            ("Install and Blank Slate Setup", "install-and-blank-slate", "interactive", 15, {"questions": MODULE_5_RECAP["install-and-blank-slate"]}),
            ("Docker as Backend", "docker-as-backend", "sandbox", 15, {"questions": MODULE_5_RECAP["docker-as-backend"]}),
            ("OpenRouter and Your First Conversation", "openrouter-first-conversation", "interactive", 15, {"questions": MODULE_5_RECAP["openrouter-first-conversation"]}),
            ("Sandbox Verification Lab", "sandbox-verification-lab", "sandbox", 12, {"questions": MODULE_5_RECAP["sandbox-verification-lab"]}),
        ],
    },
    {
        "order": 8,
        "title": "OpenClaw (Build #2)",
        "slug": "module-6-openclaw",
        "description": "Configure OpenClaw, add skills and channels, with a focus on agent safety.",
        "published": False,
        "difficulty": 2,
        "lessons": [
            ("Configuration", "configuration", "agent_lab", 15),
            ("Adding Skills", "adding-skills", "agent_lab", 15),
            ("Channel", "channel", "interactive", 12),
            ("Agent Safety", "agent-safety", "theory", 15),
        ],
    },
    {
        "order": 9,
        "title": "Claude (Build #3)",
        "slug": "module-7-claude",
        "description": "Claude agent build — curriculum details forthcoming.",
        "published": False,
        "difficulty": 2,
        "lessons": [
            ("Claude Build Overview", "claude-build-overview", "theory", 10),
            ("Build with Claude", "build-with-claude", "agent_lab", 20),
        ],
    },
    {
        "order": 10,
        "title": "Capstone: Safety & Evaluation",
        "slug": "module-8-capstone-safety-evaluation",
        "description": "Automation examples, guardrails, permissions, and testing.",
        "published": False,
        "difficulty": 3,
        "lessons": [
            ("Automation Examples", "automation-examples", "theory", 12),
            ("Guardrails", "guardrails", "theory", 12),
            ("Permissions", "permissions", "theory", 10),
            ("Testing", "testing", "interactive", 15),
        ],
    },
]
