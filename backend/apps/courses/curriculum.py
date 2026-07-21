"""Curriculum spec + lesson content loading, shared by seed_demo and sync_content.

Lesson markdown lives in apps/courses/content/<course-slug>/<lesson-slug>.md.
Drop a .md file there and run `python manage.py sync_content` (prod-safe) or
`python manage.py seed_demo` (dev full reset).
"""

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, cast

from apps.courses.structured_course_packs import STRUCTURED_COURSE_PACKS_BY_SLUG

CONTENT_DIR = Path(__file__).resolve().parent / "content"

SKILL = {
    "slug": "create-an-ai-agent",
    "name": "Create an AI Agent",
    "description": "Build AI agents from foundations through capstone",
    "order": 1,
}

STRUCTURED_KEYS = (
    "artifact_bundle",
    "skill_templates",
    "channel_templates",
    "safety_checks",
    "permission_matrix",
    "evaluation_rubric",
    "evaluation_cases",
    "guided_blocks",
    "checkpoint_questions",
    "capstone_assignment",
    "publish_rules",
)

def placeholder(title: str) -> str:
    return f"# {title}\n\nLesson Content"


def default_output_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _artifact_source_path(artifact: dict, source_root: Path | None = None) -> Path:
    root = default_output_root() if source_root is None else source_root
    return (root / artifact["path"]).resolve()


def _read_authored_artifact_text(artifact: dict, source_root: Path | None = None) -> str:
    return _artifact_source_path(artifact, source_root).read_text(encoding="utf-8")


def _load_authored_artifact_body(artifact: dict, source_root: Path | None = None):
    artifact_text = _read_authored_artifact_text(artifact, source_root)
    if artifact.get("format") == "json":
        return json.loads(artifact_text)
    return artifact_text


def _hydrate_artifact(artifact: dict, source_root: Path | None = None) -> dict:
    hydrated = deepcopy(artifact)
    hydrated["body"] = _load_authored_artifact_body(artifact, source_root)
    return hydrated


def _hydrate_artifacts(artifacts: list[dict], source_root: Path | None = None) -> list[dict]:
    return [_hydrate_artifact(artifact, source_root) for artifact in artifacts]


def build_structured_sandbox_config(lesson_pack: dict, source_root: Path | None = None) -> dict:
    sandbox_config = {key: deepcopy(lesson_pack.get(key, [])) for key in STRUCTURED_KEYS}
    sandbox_config["questions"] = deepcopy(lesson_pack.get("questions", []))
    sandbox_config["artifact_bundle"] = _hydrate_artifacts(lesson_pack.get("artifacts", []), source_root)
    return sandbox_config


def _structured_lesson_spec(lesson_pack: dict) -> tuple:
    config = build_structured_sandbox_config(lesson_pack)
    if lesson_pack.get("ai_tutor_prompt"):
        config["ai_tutor_prompt"] = lesson_pack["ai_tutor_prompt"]
    return (
        lesson_pack["title"],
        lesson_pack["slug"],
        lesson_pack["lesson_type"],
        lesson_pack["estimated_minutes"],
        config,
    )


def _structured_course_entry(course_slug: str) -> dict:
    course_pack = cast(dict[str, Any], STRUCTURED_COURSE_PACKS_BY_SLUG[course_slug])
    return {
        "order": course_pack["order"],
        "title": course_pack["title"],
        "slug": course_pack["slug"],
        "description": course_pack["description"],
        "difficulty": course_pack["difficulty"],
        "published": course_pack.get("published", True),
        "lessons": [_structured_lesson_spec(lesson_pack) for lesson_pack in course_pack["lessons"]],
    }


def load_content(course_slug: str, lesson_slug: str, title: str) -> str:
    """Prefer a non-empty content/*.md file; fall back to in-file dicts, then placeholder."""
    path = CONTENT_DIR / course_slug / f"{lesson_slug}.md"
    if path.is_file():
        text = path.read_text(encoding="utf-8")
        if text.strip():
            return text
    return MODULE_1_CONTENT.get(lesson_slug, placeholder(title))


def default_recap_questions(title: str, slug: str) -> list[dict]:
    """Filler recap bank so every lesson can be completed (>=80%) until real questions are written."""
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


MODULE_1_WHAT_IS_AI_VIDEO_URL = "https://www.youtube-nocookie.com/embed/c0m6yaGlZh4"
MODULE_1_WHAT_ARE_LLMS_VIDEO_URL = "https://www.youtube-nocookie.com/embed/qMxuthTIQq4"
MODULE_1_OTHER_TYPES_OF_AI_VIDEO_URL = "https://www.youtube-nocookie.com/embed/XFZ-rQ8eeR8"
MODULE_1_BRIEF_HISTORY_VIDEO_URL = "https://www.youtube-nocookie.com/embed/FO8Qq025uc8"

MODULE_1_WHAT_IS_AI_RECAP_QUESTIONS = [
    {
        "id": "m1-ai-video-q1",
        "prompt": "How does the video define artificial intelligence at a high level?",
        "options": [
            "Using computers to do things that usually require human intelligence",
            "Building only humanoid robots for factories",
            "Storing as much digital data as possible",
        ],
        "answer_index": 0,
    },
    {
        "id": "m1-ai-video-q2",
        "prompt": "Why does the video say AI systems need large datasets?",
        "options": [
            "To make computer screens brighter and faster",
            "To identify patterns, make predictions, and recommend actions",
            "To replace every kind of human decision-making immediately",
        ],
        "answer_index": 1,
    },
    {
        "id": "m1-ai-video-q3",
        "prompt": "Which example does the video use to show a narrow AI success?",
        "options": [
            "A household robot that can cook dinner and clean the house",
            "A chatbot that can walk, drive, and play sports",
            "AlphaGo defeating a legendary professional Go player",
        ],
        "answer_index": 2,
    },
    {
        "id": "m1-ai-video-q4",
        "prompt": "After the AlphaGo example, what limitation does the video highlight?",
        "options": [
            "That same system still could not drive a car, walk, or play Monopoly on its own",
            "The system could only answer math questions and nothing else",
            "The system needed to be retrained every single minute",
        ],
        "answer_index": 0,
    },
    {
        "id": "m1-ai-video-q5",
        "prompt": "How does the video compare AI with the human brain?",
        "options": [
            "AI and the human brain are already equal across every task",
            "AI has massive computing power, but human brains can handle a wider range of data and methods",
            "Human brains work like small versions of the exact same algorithm",
        ],
        "answer_index": 1,
    },
]

MODULE_1_WHAT_ARE_LLMS_RECAP_QUESTIONS = [
    {
        "id": "m1-llm-video-q1",
        "prompt": "According to the video, what is a large language model?",
        "options": [
            "A type of AI trained to generate and understand humanlike text",
            "A physical robot designed to replace teachers",
            "A database that stores every answer exactly as written",
        ],
        "answer_index": 0,
    },
    {
        "id": "m1-llm-video-q2",
        "prompt": "Why does the video say an LLM is called both a language model and a large model?",
        "options": [
            "Because it only works in large office buildings",
            "Because it understands how language is used and is trained on large amounts of text",
            "Because it can only answer very long questions",
        ],
        "answer_index": 1,
    },
    {
        "id": "m1-llm-video-q3",
        "prompt": "What are parameters in the video's explanation?",
        "options": [
            "The names of different chatbot apps",
            "Hidden feelings the model develops during training",
            "Internal settings or dials the AI adjusts to make better predictions",
        ],
        "answer_index": 2,
    },
    {
        "id": "m1-llm-video-q4",
        "prompt": "What example does the video use to explain next-word prediction?",
        "options": [
            "The cat sat on the blank",
            "How do airplanes stay in the air?",
            "Write a full essay about history",
        ],
        "answer_index": 0,
    },
    {
        "id": "m1-llm-video-q5",
        "prompt": "What does the video say is really happening when an LLM seems humanlike?",
        "options": [
            "It is expressing real feelings and desires",
            "It is using powerful pattern recognition based on lots of training data",
            "It is manually controlled by a hidden human operator",
        ],
        "answer_index": 1,
    },
]

MODULE_1_OTHER_TYPES_OF_AI_RECAP_QUESTIONS = [
    {
        "id": "m1-other-ai-q1",
        "prompt": "How does the video organize its seven types of AI?",
        "options": [
            "Into AI capabilities and AI functionalities",
            "Into hardware types and software colors",
            "Into business tools and school tools only",
        ],
        "answer_index": 0,
    },
    {
        "id": "m1-other-ai-q2",
        "prompt": "According to the video, which AI capability is the only one that exists today?",
        "options": [
            "Artificial super AI",
            "Artificial general intelligence",
            "Artificial narrow AI",
        ],
        "answer_index": 2,
    },
    {
        "id": "m1-other-ai-q3",
        "prompt": "What does the video say would make AGI different from narrow AI?",
        "options": [
            "AGI could apply previous learning to new tasks without humans retraining it for each one",
            "AGI can only do one small task at a time",
            "AGI is just another name for a chatbot interface",
        ],
        "answer_index": 0,
    },
    {
        "id": "m1-other-ai-q4",
        "prompt": "Which example does the video use to explain reactive machine AI?",
        "options": [
            "A music recommender improving over months of listening",
            "IBM Deep Blue defeating Garry Kasparov at chess",
            "A self-aware assistant inventing its own goals",
        ],
        "answer_index": 1,
    },
    {
        "id": "m1-other-ai-q5",
        "prompt": "In the video's framework, what is limited memory AI able to do?",
        "options": [
            "Use past and present data to decide on actions and improve over time",
            "Feel emotions and form personal beliefs",
            "Work without any data or training at all",
        ],
        "answer_index": 0,
    },
]

MODULE_1_BRIEF_HISTORY_RECAP_QUESTIONS = [
    {
        "id": "m1-history-q1",
        "prompt": "What question did Alan Turing famously ask in 1950, according to the video?",
        "options": [
            "Can machines think?",
            "Can robots replace all jobs tomorrow?",
            "Can data exist without computers?",
        ],
        "answer_index": 0,
    },
    {
        "id": "m1-history-q2",
        "prompt": "When does the video say the term artificial intelligence was introduced?",
        "options": [
            "1956 at a Dartmouth summer research project",
            "1940 during World War II",
            "1980 in Japan's computing boom",
        ],
        "answer_index": 0,
    },
    {
        "id": "m1-history-q3",
        "prompt": "Why did the video say the first AI winter happened?",
        "options": [
            "AI had already solved every major problem and no funding was needed",
            "The field failed to deliver on big promises and funding dried up after critical reports",
            "Researchers stopped using computers entirely",
        ],
        "answer_index": 1,
    },
    {
        "id": "m1-history-q4",
        "prompt": "What helped set up AI's dramatic turn in the late 1990s?",
        "options": [
            "Less data and weaker computers",
            "A complete rejection of machine learning",
            "Much stronger computers and much more digital training data",
        ],
        "answer_index": 2,
    },
    {
        "id": "m1-history-q5",
        "prompt": "What event does the video point to as making AI an overnight sensation again?",
        "options": [
            "The release of ChatGPT",
            "Deep Blue beating Garry Kasparov",
            "The creation of DARPA",
        ],
        "answer_index": 0,
    },
]

MODULE_1_EXAM_QUESTIONS = [
    *MODULE_1_WHAT_IS_AI_RECAP_QUESTIONS,
    *MODULE_1_WHAT_ARE_LLMS_RECAP_QUESTIONS,
    *MODULE_1_OTHER_TYPES_OF_AI_RECAP_QUESTIONS,
    *MODULE_1_BRIEF_HISTORY_RECAP_QUESTIONS,
]

MODULE_1_CHECKPOINT = {
    "questions": MODULE_1_EXAM_QUESTIONS,
}


MODULE_1_CONTENT = {
    "what-is-ai": """# What is AI?

This lesson is delivered as a video.

Open the Video tab to watch the introduction, then continue to the Recap Quiz when you finish.
""",
    "what-are-llms": """# What are LLMs?

This lesson is delivered as a video.

Open the Video tab to watch how LLMs learn from huge text datasets and predict language patterns, then continue to the Recap Quiz when you finish.
""",
    "what-is-an-llm-model": """# Other Types of AI

This lesson is delivered as a video.

Open the Video tab to watch how AI can be grouped by capabilities and functionalities, then continue to the Recap Quiz when you finish.
""",
    "brief-history": """# Brief History

This lesson is delivered as a video.

Open the Video tab to watch how AI rose, crashed into two winters, and returned through better compute and more data, then continue to the Recap Quiz when you finish.
""",
    "checkpoint": """# Module 1 Exam

This exam covers the full Module 1 lesson set: What is AI, What are LLMs, Other Types of AI, and Brief History.

Answer every question. You can retry as many times as you need.
""",
}


CURRICULUM = [
    {
        "order": 1,
        "title": "Module 1: Introduction to AI",
        "slug": "module-1-introduction-to-ai",
        "description": "What AI and LLMs are, other major AI categories, a brief history, and a checkpoint.",
        "difficulty": 1,
        "lessons": [
            (
                "What is AI?",
                "what-is-ai",
                "theory",
                8,
                {
                    "video_url": MODULE_1_WHAT_IS_AI_VIDEO_URL,
                    "questions": MODULE_1_WHAT_IS_AI_RECAP_QUESTIONS,
                },
            ),
            (
                "What are LLMs?",
                "what-are-llms",
                "theory",
                8,
                {
                    "video_url": MODULE_1_WHAT_ARE_LLMS_VIDEO_URL,
                    "questions": MODULE_1_WHAT_ARE_LLMS_RECAP_QUESTIONS,
                },
            ),
            (
                "Other Types of AI",
                "what-is-an-llm-model",
                "theory",
                8,
                {
                    "video_url": MODULE_1_OTHER_TYPES_OF_AI_VIDEO_URL,
                    "questions": MODULE_1_OTHER_TYPES_OF_AI_RECAP_QUESTIONS,
                },
            ),
            (
                "Brief History",
                "brief-history",
                "theory",
                8,
                {
                    "video_url": MODULE_1_BRIEF_HISTORY_VIDEO_URL,
                    "questions": MODULE_1_BRIEF_HISTORY_RECAP_QUESTIONS,
                },
            ),
            ("Module 1 Exam", "checkpoint", "quiz", 10, MODULE_1_CHECKPOINT),
        ],
    },
    {
        "order": 2,
        "title": "Module 1.5: How LLMs Work",
        "slug": "module-1-5-how-llms-work",
        "description": "Context windows, tokens, and training vs inference.",
        "difficulty": 1,
        "lessons": [
            ("Context Windows", "context-windows", "theory", 8),
            ("Tokens", "tokens", "theory", 8),
            ("Training vs Inference", "training-vs-inference", "theory", 10),
        ],
    },
    {
        "order": 3,
        "title": "Module 2: Exploring LLM Models",
        "slug": "module-2-exploring-llm-models",
        "description": "Compare Hermes, Claude, Gemini, OpenAI, and open-source models — strengths, weaknesses, and when to choose each.",
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
        "title": "Module 3: Prompting",
        "slug": "module-3-prompting",
        "description": "What prompts are, how context shapes responses, system vs user prompts, and hands-on practice.",
        "difficulty": 1,
        "lessons": [
            ("What Prompts Are", "what-prompts-are", "theory", 8),
            ("How Context Affects Responses", "how-context-affects-responses", "theory", 10),
            ("System Prompts vs User Prompts", "system-vs-user-prompts", "theory", 10),
            ("Good and Bad Prompts", "good-and-bad-prompts", "theory", 10),
            ("Hands-on Prompt Exercises", "hands-on-prompt-exercises", "interactive", 15),
        ],
    },
    _structured_course_entry("module-4-ai-agents"),
    {
        "order": 6,
        "title": "Module 4.5: Docker and Environments",
        "slug": "module-4-5-docker-and-environments",
        "description": "A brief primer on containers, images, and volumes — enough to get Docker running for agent builds.",
        "difficulty": 2,
        "lessons": [
            ("Containers, Images, Volumes", "containers-images-volumes", "theory", 8),
            ("Why Agents Need Isolation", "why-agents-need-isolation", "theory", 6),
            ("Getting Docker Running", "getting-docker-running", "sandbox", 10),
        ],
    },
    {
        "order": 7,
        "title": "Module 5: Hermes (Build #1)",
        "slug": "module-5-hermes",
        "description": "Create a Hermes agent with Telegram (or similar), Docker backend, blank-slate setup, and OpenRouter or local Ollama.",
        "difficulty": 2,
        "lessons": [
            ("Creating the Hermes Agent", "creating-the-hermes-agent", "agent_lab", 20),
            ("Setting Up Telegram", "setting-up-telegram", "interactive", 15),
            ("Docker as Backend", "docker-as-backend", "sandbox", 15),
            ("Blank Slate Setup", "blank-slate-setup", "agent_lab", 15),
            ("OpenRouter or Local Ollama", "openrouter-or-local-ollama", "interactive", 15),
        ],
    },
    _structured_course_entry("module-6-openclaw"),
    {
        "order": 9,
        "title": "Module 7: Claude (Build #3)",
        "slug": "module-7-claude",
        "description": "Claude agent build — curriculum details forthcoming.",
        "difficulty": 2,
        "lessons": [
            ("Claude Build Overview", "claude-build-overview", "theory", 10),
            ("Build with Claude", "build-with-claude", "agent_lab", 20),
        ],
    },
    _structured_course_entry("module-8-capstone-safety-evaluation"),
]