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
    """Prefer a content/*.md file; fall back to in-file dicts, then placeholder."""
    path = CONTENT_DIR / course_slug / f"{lesson_slug}.md"
    if path.is_file():
        return path.read_text(encoding="utf-8")
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


CURRICULUM = [
    {
        "order": 1,
        "title": "Introduction to AI",
        "slug": "module-1-introduction-to-ai",
        "description": "What AI and LLMs are, a brief history, and a checkpoint. Terminology is introduced as you go.",
        "published": False,
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
        "published": False,
        "difficulty": 1,
        "lessons": [
            ("Context Windows", "context-windows", "theory", 8),
            ("Tokens", "tokens", "theory", 8),
            ("Training vs Inference", "training-vs-inference", "theory", 10),
        ],
    },
    {
        "order": 3,
        "title": "Exploring LLM Models",
        "slug": "module-2-exploring-llm-models",
        "description": "Compare Hermes, Claude, Gemini, OpenAI, and open-source models — strengths, weaknesses, and when to choose each.",
        "published": False,
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
        "published": False,
        "difficulty": 1,
        "lessons": [
            ("What Prompts Are", "what-prompts-are", "theory", 8),
            ("How Context Affects Responses", "how-context-affects-responses", "theory", 10),
            ("System Prompts vs User Prompts", "system-vs-user-prompts", "theory", 10),
            ("Good and Bad Prompts", "good-and-bad-prompts", "theory", 10),
            ("Hands-on Prompt Exercises", "hands-on-prompt-exercises", "interactive", 15),
        ],
    },
    {
        "order": 5,
        "title": "AI Agents",
        "slug": "module-4-ai-agents",
        "description": "What agents are, how they differ from chatbots, workflows, and an intro to Hermes, OpenClaw, Claude, and Gemini agents.",
        "published": False,
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
            ("Why Docker?", "why-docker", "theory", 8),
            ("The Main Terms", "docker-main-terms", "theory", 8),
            ("Installing Docker Desktop", "installing-docker-desktop", "interactive", 15),
            ("Your First Containers", "first-containers", "sandbox", 12),
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
            ("What Hermes Is", "what-hermes-is", "theory", 8),
            ("Install and Blank Slate Setup", "install-and-blank-slate", "interactive", 15),
            ("Docker as Backend", "docker-as-backend", "sandbox", 15),
            ("OpenRouter and Your First Conversation", "openrouter-first-conversation", "interactive", 15),
            ("Sandbox Verification Lab", "sandbox-verification-lab", "sandbox", 12),
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
