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
    # "publish_rules" is gone: it shipped to the client as inert JSON that no
    # code ever evaluated. Its job is now done for real by the content
    # validator in sync_content (warn by default, hard-fail under --strict).
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


def _structured_course_entry(course_slug: str, extra_lessons: tuple = ()) -> dict:
    course_pack = cast(dict[str, Any], STRUCTURED_COURSE_PACKS_BY_SLUG[course_slug])
    return {
        "order": course_pack["order"],
        "title": course_pack["title"],
        "slug": course_pack["slug"],
        "description": course_pack["description"],
        "difficulty": course_pack["difficulty"],
        "published": course_pack.get("published", True),
        "lessons": [_structured_lesson_spec(lesson_pack) for lesson_pack in course_pack["lessons"]]
        + list(extra_lessons),
    }


def load_content(course_slug: str, lesson_slug: str, title: str) -> str:
    """Prefer a non-empty content/*.md file; otherwise a visible placeholder."""
    path = CONTENT_DIR / course_slug / f"{lesson_slug}.md"
    if path.is_file():
        text = path.read_text(encoding="utf-8")
        if text.strip():
            return text
    return placeholder(title)


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


# Module 4 exam — the authoring standard-setter (plan §6). Every item combines
# at least two lessons or applies one to a novel scenario; none appears in any
# recap bank (machine-checked by sync_content); wrong answers explain why and
# name the lesson that teaches the idea.
MODULE_4_EXAM_QUESTIONS = [
    {
        "id": "m4-exam-1",
        "prompt": "Mid-errand, one of Juno's searches hits a paywalled article it cannot read. According to the loop, what happens next?",
        "options": [
            "Juno stops and reports that the errand failed",
            "The failed step becomes information for the next decision, and the plan adjusts",
            "Juno asks the human to pay for the article before continuing",
        ],
        "answer_index": 1,
        "explanation": "In the loop (The Loop: Watch Juno Work), a failed step is just information for the next step — the paywall was not a crisis.",
    },
    {
        "id": "m4-exam-2",
        "prompt": "A support tool answers every customer question with a single reply and never takes steps on its own. What is it?",
        "options": [
            "An agent, because it uses AI to answer",
            "A workflow, because customers follow steps to reach it",
            "A chatbot — it answers, but it does not plan, act, and check",
        ],
        "answer_index": 2,
        "explanation": "Answering well is not agency (Agents vs Chatbots): an agent plans steps, acts, and checks its own work.",
    },
    {
        "id": "m4-exam-3",
        "prompt": "Your research agent keeps re-reading the same article it already summarized. Which of the six questions did you skip when designing it?",
        "options": [
            "Memory — it is not tracking what it has already done",
            "Goal — it does not know what the human wants",
            "Tools — it is not allowed to read articles",
        ],
        "answer_index": 0,
        "explanation": "Memory is the notebook (Notebook, Hands, Judgment): what the agent keeps track of so it never redoes finished work.",
    },
    {
        "id": "m4-exam-4",
        "prompt": "The support helper drafts replies, but a person clicks send. Why is the boundary drawn there?",
        "options": [
            "Because agents cannot write complete replies on their own",
            "That is its stop rule: the agent's job ends at a draft, and a human decides what reaches the customer",
            "Because email tools cannot be given to agents",
        ],
        "answer_index": 1,
        "explanation": "Stop rules draw the finish line before the race (Checks and Stop Rules); the support helper from Four Agents stops at a draft on purpose.",
    },
    {
        "id": "m4-exam-5",
        "prompt": "The coding helper's check is the project's test suite. What makes that a strong check?",
        "options": [
            "It is an automatic judge that does not rely on the agent's own opinion of its work",
            "Running tests makes the agent finish faster",
            "A test suite means the agent no longer needs a stop rule",
        ],
        "answer_index": 0,
        "explanation": "A check is how the agent doubts itself (Checks and Stop Rules); the test suite is an automatic judge built into the job (Four Agents).",
    },
    {
        "id": "m4-exam-6",
        "prompt": "You design a grocery-planning agent and answer five of the six questions — but skip Stop. What is the likely failure?",
        "options": [
            "It never starts, because it has no first step",
            "It forgets which items it already added to the list",
            "It keeps working past done — revising a finished list because nothing tells it it is finished",
        ],
        "answer_index": 2,
        "explanation": "Without a stop rule the finish line does not exist (Checks and Stop Rules) — done never means done.",
    },
    {
        "id": "m4-exam-7",
        "prompt": "Match the everyday objects to the agent parts: the notebook, the hands, the judgment.",
        "options": [
            "Notebook = tools, hands = memory, judgment = reasoning",
            "Notebook = memory, hands = tools, judgment = reasoning",
            "Notebook = reasoning, hands = tools, judgment = memory",
        ],
        "answer_index": 1,
        "explanation": "Memory keeps, tools do, reasoning decides what is next (Notebook, Hands, Judgment).",
    },
    {
        "id": "m4-exam-8",
        "prompt": "A task runs the exact same three steps every time, with nothing to decide. What should you build?",
        "options": [
            "An agent, because agents are always the smarter choice",
            "A chatbot, so a human can ask it to do the steps",
            "A checklist workflow — when nothing needs deciding, the boring choice is the right one",
        ],
        "answer_index": 2,
        "explanation": "Agents earn their keep only when steps must be chosen (Agents vs Chatbots — permission to choose the boring one).",
    },
    {
        "id": "m4-exam-9",
        "prompt": "Juno's check rejects a summary. What decides what happens next?",
        "options": [
            "Judgment — reasoning picks the next step using what memory holds",
            "The human, who must approve every retry",
            "The search tool, which automatically reruns itself",
        ],
        "answer_index": 0,
        "explanation": "After a check, reasoning decides the next move (Notebook, Hands, Judgment meets The Loop).",
    },
    {
        "id": "m4-exam-10",
        "prompt": "The support helper's tool is the company knowledge base. Which of the six questions do tools answer?",
        "options": [
            "What is the agent allowed to do and use to act?",
            "How does the agent know its work is good?",
            "What does the human actually want?",
        ],
        "answer_index": 0,
        "explanation": "Tools are the hands — what the agent may use to act (What an Agent Actually Is; Four Agents).",
    },
    {
        "id": "m4-exam-11",
        "prompt": "Grown-up Juno delivers summaries where claims cite no sources, yet declares the errand complete. Which question was designed too weakly?",
        "options": [
            "Plan — it should have searched differently",
            "Check — 'every claim traces back to a source' would have caught it before 'done'",
            "Goal — summarizing was the wrong job",
        ],
        "answer_index": 1,
        "explanation": "The research helper's check is that every claim traces to a source (Four Agents); a weak check lets bad work pass as done.",
    },
    {
        "id": "m4-exam-12",
        "prompt": "Your new agent's first search returns junk. As its designer, what should you conclude?",
        "options": [
            "Nothing is wrong — the first plan is a starting point, and the loop revises it",
            "The goal was wrong and the errand should be restarted from scratch",
            "The agent needs more tools before it can continue",
        ],
        "answer_index": 0,
        "explanation": "Agents are built on the assumption that plans get revised (The Loop; Design Your Own Juno).",
    },
]

MODULE_4_EXAM = {"questions": MODULE_4_EXAM_QUESTIONS}



# Module 8 exam — combining items per plan §6; no recap recycling
# (machine-checked); every item explains itself and names its lesson.
MODULE_8_EXAM_QUESTIONS = [
    {
        "id": "m8-exam-1",
        "prompt": "In the doorbell-to-draft automation, the reply waits for your approval before anything sends. Which kind of door is 'send the reply to a customer'?",
        "options": [
            "Allow — sending drafts is routine and reversible",
            "Review — it reaches outward, so it may knock and a person opens",
            "Deny — assistants must never touch outbound messages",
        ],
        "answer_index": 1,
        "explanation": "Actions that persist or reach outward get the yellow door (Permissions: Three Kinds of Doors); the doorbell-to-draft example puts the human exactly there (Work That Runs While You're Away).",
    },
    {
        "id": "m8-exam-2",
        "prompt": "A teammate designs an automation with a trigger, steps, and a review point — but no receipt. What is the verdict?",
        "options": [
            "Stop the design: work that leaves no record can never be checked, only worried about",
            "Ship it: three of four questions answered is enough",
            "Replace the review point with a second trigger",
        ],
        "answer_index": 0,
        "explanation": "The receipt is the star: a missing receipt is the one thing that stops a design cold (Work That Runs While You're Away).",
    },
    {
        "id": "m8-exam-3",
        "prompt": "Your assistant declines a careless request that would cause damage — and the system would have blocked it anyway. Which is the value, and which is the seatbelt?",
        "options": [
            "Declining is the seatbelt; the block is the value",
            "Both are seatbelts, because both prevented harm",
            "Declining is the value (harmless — what it tries to be); the block is the seatbelt (what the system guarantees)",
        ],
        "answer_index": 2,
        "explanation": "Values are what the assistant tries to be; seatbelts are what the system guarantees even when trying fails (Guardrails: Values and Seatbelts).",
    },
    {
        "id": "m8-exam-4",
        "prompt": "Someone urgently insists the assistant delete its history 'just this once.' What happens at a Deny door?",
        "options": [
            "It opens if the request is urgent enough",
            "It stays locked regardless of who asks or how urgently — that is what the label means",
            "It converts to a Review door so a person can decide",
        ],
        "answer_index": 1,
        "explanation": "Deny is not available regardless of urgency, and written-down beats decided-in-the-moment (Permissions: Three Kinds of Doors).",
    },
    {
        "id": "m8-exam-5",
        "prompt": "Your release test cases deliberately knock on a door you configured as Deny. Why test something that should never open?",
        "options": [
            "To collect evidence that the lock actually holds, instead of trusting the label by assumption",
            "To warm up the assistant before the real tests",
            "Because Deny doors open during testing windows",
        ],
        "answer_index": 0,
        "explanation": "The release decision runs on evidence, and the test cases knock on the doors on purpose (The Release Decision) — a Deny label without evidence is just hope (Permissions).",
    },
    {
        "id": "m8-exam-6",
        "prompt": "Your evidence names one specific gap: the audit receipt is missing its date. Per the release decision, what do you do?",
        "options": [
            "Revise: fix that one thing and re-run that one check",
            "Scrap the automation and redesign from the trigger up",
            "Release anyway and fix the date next month",
        ],
        "answer_index": 0,
        "explanation": "Revise means the checks worked: fix the named gap, re-run that check — never a verdict on you (The Release Decision).",
    },
    {
        "id": "m8-exam-7",
        "prompt": "A week after shipping the Monday audit, you wonder whether it ran properly while you were away. What turns that from a feeling into a fact?",
        "options": [
            "Watching next Monday's run live from start to finish",
            "Asking the assistant whether everything went okay",
            "Reading the dated audit report it saved — the receipt",
        ],
        "answer_index": 2,
        "explanation": "You verify an automation by reading the receipt afterward, not by watching it (Work That Runs While You're Away).",
    },
    {
        "id": "m8-exam-8",
        "prompt": "Your assistant answers with 'I know X; I am guessing Y.' Which guardrail layer produced that behavior?",
        "options": [
            "A seatbelt — the system physically blocks guesses",
            "The truthful value: separating what it knows from what it guesses is what it tries to be",
            "A Review door — a person approved the phrasing",
        ],
        "answer_index": 1,
        "explanation": "Truthful is one of the three values — helpful, truthful, harmless (Guardrails: Values and Seatbelts); no system guarantee forces phrasing.",
    },
]

MODULE_8_EXAM = {"questions": MODULE_8_EXAM_QUESTIONS}


# Exam banks for the inline modules (plan §6): combining items, no recap
# recycling (machine-checked), every item explained.
MODULE_1_5_EXAM_QUESTIONS = [
    {"id": "m15-exam-1", "prompt": "A long chat suddenly 'forgets' rules you set an hour ago. Connect the mechanism: what happened?", "options": ["The model retrained itself mid-chat and overwrote the rules", "The conversation outgrew the context window, and the earliest turns fell out of the model's working memory", "Your API key expired, which clears memory"], "answer_index": 1, "explanation": "The window is working memory; exceed it and the oldest content drops (Context Windows)."},
    {"id": "m15-exam-2", "prompt": "Why does an API bill and a context window use the same unit?", "options": ["Both are measured in tokens — the pieces the model actually reads and writes", "Both are measured in characters for historical reasons", "Coincidence: providers picked similar names"], "answer_index": 0, "explanation": "Tokens are the model's native unit — windows are sized in them and usage is billed in them (Tokens)."},
    {"id": "m15-exam-3", "prompt": "You correct a chatbot's mistake today. Tomorrow, a fresh chat makes the same mistake. Why?", "options": ["The correction only lived in that conversation's context; inference never changes the weights", "The model chose to ignore you", "Corrections require at least a week to take effect"], "answer_index": 0, "explanation": "Learning happens in training; inference runs frozen weights, so chats teach it nothing permanent (Training vs Inference)."},
    {"id": "m15-exam-4", "prompt": "Roughly how does 'a token' relate to text?", "options": ["Exactly one word, always", "One sentence", "A chunk of characters — common words are often one token, longer words split into several"], "answer_index": 2, "explanation": "Tokens are subword pieces, roughly a few characters each (Tokens)."},
    {"id": "m15-exam-5", "prompt": "What actually fills a context window during a chat with an agent?", "options": ["Only your latest message", "The system prompt, the conversation so far, and whatever files or tool results were pulled in", "The model's training data"], "answer_index": 1, "explanation": "Everything the model must currently see competes for the same window (Context Windows)."},
    {"id": "m15-exam-6", "prompt": "Training vs inference: which is the expensive, rare phase, and which happens every time you chat?", "options": ["Training is rare and expensive; inference runs on every request", "Inference is rare; training happens per message", "They are the same process at different speeds"], "answer_index": 0, "explanation": "Weights change once during training; every chat afterward is inference (Training vs Inference)."},
    {"id": "m15-exam-7", "prompt": "A teammate pastes an entire book into the prompt 'so the model knows everything.' What's the flaw?", "options": ["Books are copyrighted, so the model refuses", "The book joins the context window and crowds out the conversation — long inputs have real costs", "Nothing — bigger input always improves answers"], "answer_index": 1, "explanation": "Window space is finite and shared; strategy beats volume (Context Windows; Tokens)."},
    {"id": "m15-exam-8", "prompt": "Why can a model discuss yesterday's news only if you paste the article?", "options": ["Its knowledge froze at training time; new facts must arrive through the context window", "News sites block AI companies", "It can, using its live internet connection"], "answer_index": 0, "explanation": "Frozen weights hold old knowledge; the window is the only door for new facts (Training vs Inference; Context Windows)."},
]

MODULE_3_EXAM_QUESTIONS = [
    {"id": "m3-exam-1", "prompt": "Two colleagues send the identical prompt but get very different answers. One had pasted the project brief earlier in the chat. What explains the difference?", "options": ["Random luck — identical prompts always give identical answers otherwise", "Context: the same prompt reads differently against different conversation history", "One colleague's account has a better model"], "answer_index": 1, "explanation": "The same prompt against different context produces different responses (How Context Affects Responses)."},
    {"id": "m3-exam-2", "prompt": "Which request is the better prompt, per the good/bad patterns?", "options": ["'Write an email to my landlord asking to fix the heater by Friday; polite but firm; 3 sentences'", "'Write something about my apartment'", "'You know what I need — do it'"], "answer_index": 0, "explanation": "Task + context + constraints + format is the good pattern; vagueness is the bad one (Good and Bad Prompts)."},
    {"id": "m3-exam-3", "prompt": "In an agent like your Module 6 assistant, what plays the role of the system prompt?", "options": ["Its persona/rules file (like SOUL.md) — standing instructions loaded before any user message", "The last thing the user typed", "The model's training data"], "answer_index": 0, "explanation": "System prompts are standing rules, exactly what an agent's persona file provides (System vs User Prompts)."},
    {"id": "m3-exam-4", "prompt": "Why do system and user prompts exist as separate roles at all?", "options": ["To bill the two kinds of text differently", "So durable rules (how to behave) survive independently of each changing request", "The split is decorative; models merge them anyway"], "answer_index": 1, "explanation": "The split keeps standing behavior stable across every user turn (System vs User Prompts)."},
    {"id": "m3-exam-5", "prompt": "A one-line prompt with no context gets a perfect answer. When is that expected rather than lucky?", "options": ["When the task is unambiguous and self-contained — short is fine when nothing is missing", "Never; long prompts are always better", "Only on paid models"], "answer_index": 0, "explanation": "Short is fine when the task carries all its own context (Good and Bad Prompts)."},
    {"id": "m3-exam-6", "prompt": "You want a JSON list, but got prose. Which prompt part was missing?", "options": ["The format constraint — say what shape the answer must take", "The greeting", "A larger context window"], "answer_index": 0, "explanation": "Format instructions are one of the parts of a prompt (What Prompts Are; Good and Bad Prompts)."},
    {"id": "m3-exam-7", "prompt": "Halfway through a long chat, answers drift off-topic. Which habit helps most?", "options": ["Restate the key context — recent, explicit context outweighs stale history", "Type in all caps", "Start insulting the model"], "answer_index": 0, "explanation": "Order and recency matter; refreshing context re-anchors the response (How Context Affects Responses)."},
    {"id": "m3-exam-8", "prompt": "'Summarize this contract for a first-time renter, plain language, 5 bullets.' Which parts of a prompt are present?", "options": ["Task, audience context, style constraint, and format — the full kit", "Only a task", "Only constraints"], "answer_index": 0, "explanation": "That one line carries task + context + constraints + format (What Prompts Are)."},
    {"id": "m3-exam-9", "prompt": "Your agent behaves rudely in one channel. Fixing it belongs where?", "options": ["In the system-level rules, so the fix holds for every future message", "In each user message, forever", "Nowhere; tone is untrainable"], "answer_index": 0, "explanation": "Durable behavior lives in the system prompt, not per-message patching (System vs User Prompts)."},
    {"id": "m3-exam-10", "prompt": "Rewrite culture: what turns 'fix my code' into a good prompt?", "options": ["Adding the code, the error, what you expected, and what you tried", "Adding 'please' twice", "Sending it five times"], "answer_index": 0, "explanation": "Bad prompts starve the model of context; good ones feed the specifics (Good and Bad Prompts)."},
]

MODULE_4_5_EXAM_QUESTIONS = [
    {"id": "m45-exam-1", "prompt": "Your teammate says 'it works on my machine' and the demo dies on yours. What is Docker's answer?", "options": ["Buy identical laptops", "Ship the environment with the app: the image bundles what it needs, so the container runs the same everywhere", "Email the app as a zip"], "answer_index": 1, "explanation": "Docker packages the environment itself — the exact problem it exists to solve (Why Docker?)."},
    {"id": "m45-exam-2", "prompt": "Image vs container — which pair is right?", "options": ["Image = a running box; container = its recipe", "Image = the recipe; container = a running instance made from it", "They are synonyms"], "answer_index": 1, "explanation": "The two terms you use constantly: recipe and running instance (The Main Terms)."},
    {"id": "m45-exam-3", "prompt": "You delete the nginx container from the lesson. What did you lose?", "options": ["Nothing that matters — containers are disposable; a fresh one starts from the image on demand", "The nginx image, which must be re-downloaded from a backup", "Your Docker license"], "answer_index": 0, "explanation": "Disposability is the point: delete with no consequences (Your First Containers)."},
    {"id": "m45-exam-4", "prompt": "Why does an AI agent belong inside a container specifically?", "options": ["Containers make agents smarter", "An agent that runs commands gets a sealed, disposable room — mistakes stay inside the box", "Docker is required by AI law"], "answer_index": 1, "explanation": "Isolation turns 'agent ran a command' from scary to shrug (Why Docker?; and Module 5 uses exactly this)."},
    {"id": "m45-exam-5", "prompt": "The first time you ran hello-world, Docker paused before printing. What was it doing?", "options": ["Pulling the image from the registry because it wasn't on your machine yet", "Compiling hello-world from source", "Waiting for admin approval"], "answer_index": 0, "explanation": "Run looks locally, pulls if missing, then starts the container (Your First Containers)."},
    {"id": "m45-exam-6", "prompt": "You ran nginx with '-p 8080:80'. What did that flag do?", "options": ["Limited nginx to 8080 kilobytes", "Mapped your machine's port 8080 onto the container's port 80 so the browser could reach it", "Made the container 80x faster"], "answer_index": 1, "explanation": "Port mapping is the doorway between your machine and the sealed box (Your First Containers)."},
    {"id": "m45-exam-7", "prompt": "In Module 5, every Hermes session spawns another container and they pile up. Why is deleting old ones safe?", "options": ["Containers are furniture made from the image — throw them out and a fresh one appears on demand", "Hermes containers are decorative", "It is not safe; never delete containers"], "answer_index": 0, "explanation": "Module 4.5's disposability lesson applied for real in Module 5 (Your First Containers; First Conversation and the Container)."},
    {"id": "m45-exam-8", "prompt": "Docker Desktop shows a green 'Engine running' bar. What does that tell you before a lesson?", "options": ["Your images are all up to date", "The engine that runs containers is up — the prerequisite every agent build in this course leans on", "Green means a container is currently billing you"], "answer_index": 1, "explanation": "The running engine is the handoff the docker lessons end on (Installing Docker Desktop; Your First Containers)."},
]

MODULE_5_EXAM_QUESTIONS = [
    {"id": "m5-exam-1", "prompt": "Hermes is called an orchestrator, not a model. In practice that means:", "options": ["It coordinates the pieces — your machine, a gateway, and a model reached over an API — rather than doing the thinking itself", "It is a small model that runs offline", "It replaces Docker"], "answer_index": 0, "explanation": "Not a model — an orchestrator across the three boxes (What Hermes Is)."},
    {"id": "m5-exam-2", "prompt": "Why does the course get your OpenRouter key BEFORE running the installer?", "options": ["Keys expire in an hour, so timing is tight", "The wizard asks for it mid-flow — arriving with key in hand means no dead end halfway through setup", "OpenRouter requires install proof first"], "answer_index": 1, "explanation": "The key comes first so the wizard never strands you (OpenRouter and Your API Key; Install and the Setup Wizard)."},
    {"id": "m5-exam-3", "prompt": "What does the spending cap on your OpenRouter account actually protect you from?", "options": ["Slow models", "A runaway or mistaken agent burning real money past the limit you chose", "Losing your chat history"], "answer_index": 1, "explanation": "The cap bounds the blast radius in dollars — set before the agent exists (OpenRouter and Your API Key)."},
    {"id": "m5-exam-4", "prompt": "Free models in the lab sometimes grind for minutes on a hard request. The lesson calls this:", "options": ["A bug to report to OpenRouter", "The expected trade: patience for a $0 bill while learning", "Proof the sandbox is broken"], "answer_index": 1, "explanation": "Free models trade speed for cost — stated up front (OpenRouter and Your API Key; Sandbox Verification Lab)."},
    {"id": "m5-exam-5", "prompt": "In the verification lab you ask the agent to read a file outside its box, and it spends three minutes searching before failing. The lesson's verdict?", "options": ["Best possible result: an exhaustive attempt that still failed is the strongest evidence the box holds", "A failure of the lab — it should have succeeded instantly", "The agent is broken and should be reinstalled"], "answer_index": 0, "explanation": "A long, thorough failure is the point of the lab (Sandbox Verification Lab)."},
    {"id": "m5-exam-6", "prompt": "Why does each Hermes session getting its own container matter to you as the operator?", "options": ["It doesn't; containers are shared", "Sessions stay isolated and old boxes are safe to throw away — disposability from Module 4.5, applied", "More containers mean more speed"], "answer_index": 1, "explanation": "The box is furniture: accumulate, then delete safely (First Conversation and the Container)."},
    {"id": "m5-exam-7", "prompt": "During setup you chose 'Blank Slate.' What did that choice mean?", "options": ["Starting with no pre-loaded persona or config — you build the agent's setup yourself", "Erasing your hard drive", "Choosing the cheapest model"], "answer_index": 0, "explanation": "Blank slate = a clean starting configuration (Install and the Setup Wizard)."},
    {"id": "m5-exam-8", "prompt": "'Make it write and run code' felt different from any chatbot you used in Module 2. What changed?", "options": ["The model got bigger", "The agent acts: it writes the file, runs it in the box, reads the result, and adjusts — the loop from Module 4, live", "Nothing; it is the same experience"], "answer_index": 1, "explanation": "Put It to Work is Module 4's loop felt firsthand (Put It to Work; The Loop)."},
    {"id": "m5-exam-9", "prompt": "The 'autonomy dial' in the last lesson controls what?", "options": ["Model temperature", "How much the agent does before checking back with you", "Docker memory limits"], "answer_index": 1, "explanation": "The dial trades oversight for independence (Put It to Work)."},
    {"id": "m5-exam-10", "prompt": "Even inside the sandbox, the lab reminds you the agent can still do real things. Which is one of them?", "options": ["Rewrite files inside its own workspace and hit the internet through its tools", "Modify your host system settings", "Spend money with no cap"], "answer_index": 0, "explanation": "The box bounds it, but inside the box it is a real agent — that is why caps and review exist (Sandbox Verification Lab; Discuss section)."},
    {"id": "m5-exam-11", "prompt": "The uninstall lesson has you preview the uninstaller before running it. Which course habit is that?", "options": ["Check before act: see what will change before letting anything change it", "Speed above all", "Uninstalls are irreversible, so preview is pointless"], "answer_index": 0, "explanation": "Preview-then-run is the check discipline applied to your own machine (Put It to Work — Full Removal)."},
    {"id": "m5-exam-12", "prompt": "Your friend wants to upgrade to a stronger model. Which box changes, and which stay put?", "options": ["Only the model behind the API changes; Hermes and the gateway on your side stay the same", "All three boxes must be reinstalled", "The Docker container must be rebuilt from scratch"], "answer_index": 0, "explanation": "The three-box split exists exactly so pieces swap independently (What Hermes Is)."},
]

MODULE_7_EXAM_QUESTIONS = [
    {"id": "m7-exam-1", "prompt": "Claude Code is 'the same picture, third time.' What is the picture?", "options": ["A program on your machine orchestrating a model reached over an API", "A model that runs fully offline", "A web dashboard"], "answer_index": 0, "explanation": "Same three-box shape as Hermes and OpenClaw, new coat (What Claude Code Is)."},
    {"id": "m7-exam-2", "prompt": "Compared to your Hermes and OpenClaw builds, what is Claude Code's home turf?", "options": ["Group chats and channels", "Your terminal and your files — it works where your projects live", "Social media automation"], "answer_index": 1, "explanation": "It lives in the terminal and works on files, unlike the channel-facing builds (What Claude Code Is)."},
    {"id": "m7-exam-3", "prompt": "Why does the install lesson set a spending cap before your first session, echoing Module 5?", "options": ["Caps unlock extra features", "Bounding cost is a before-the-agent-exists decision, every time, whatever the vendor", "Anthropic requires it for downloads"], "answer_index": 1, "explanation": "The cap habit transfers across builds — set it before the agent can spend (Install and First Session; OpenRouter lesson)."},
    {"id": "m7-exam-4", "prompt": "CLAUDE.md vs a skill — which belongs where?", "options": ["Standing rules that always apply go in CLAUDE.md; a triggered procedure goes in a skill", "Everything goes in CLAUDE.md", "Skills are for rules; CLAUDE.md is for procedures"], "answer_index": 0, "explanation": "Always-on rules vs on-trigger procedures — the two ways to teach it (CLAUDE.md and Skills)."},
    {"id": "m7-exam-5", "prompt": "Your research-note skill ends by invoking the daily-log skill. What design idea is that?", "options": ["Skills can chain: small procedures composing into a pipeline", "A bug — skills must never call skills", "Decoration; the second skill does nothing"], "answer_index": 0, "explanation": "The build wires research-note to invoke daily-log — composition (Build Your Agent; CLAUDE.md and Skills)."},
    {"id": "m7-exam-6", "prompt": "Why give the reviewer subagent fewer tools than the main agent?", "options": ["To save money on tokens only", "Least privilege: a helper that only needs to read should not be able to write or run anything", "Subagents cannot technically hold tools"], "answer_index": 1, "explanation": "Subagents get their own context and a trimmed toolset on purpose (Custom Subagents) — the permissions idea from Module 8, early."},
    {"id": "m7-exam-7", "prompt": "Your notebook agent's CLAUDE.md says 'never delete notes; stay inside this folder.' Which layer is that, in Module 8's language?", "options": ["A value it tries to hold", "Written-down rules functioning like doors: what is allowed, and where the walls are", "A receipt"], "answer_index": 1, "explanation": "Standing rules in CLAUDE.md are the write-it-down discipline permissions run on (Build Your Agent; Permissions)."},
    {"id": "m7-exam-8", "prompt": "Every note must carry a '## Sources' section. Which agent question is that enforcing?", "options": ["Check — work is verifiable when claims trace to sources", "Stop — sources end the session", "Plan — sources are the first step"], "answer_index": 0, "explanation": "Sources make the check possible, the same rule grown-up Juno ran on (Build Your Agent; Module 4's check)."},
    {"id": "m7-exam-9", "prompt": "First session opens in an empty folder on purpose. Why?", "options": ["Claude Code crashes in full folders", "An empty room makes the agent's file activity legible: everything there, it made — easy to inspect, easy to trust", "Empty folders are faster to index"], "answer_index": 1, "explanation": "A clean workspace keeps cause and effect visible for your first session (Install and First Session)."},
    {"id": "m7-exam-10", "prompt": "You ask for research on a new topic and a properly built notebook agent finishes. What exists afterward?", "options": ["Only chat history", "notes/<topic>.md with Summary, Key points, and Sources — plus a daily-log entry: files as receipts", "A tweet"], "answer_index": 1, "explanation": "The four-file build turns each run into inspectable artifacts (Build Your Agent) — receipts, as Module 8 will name them."},
]


# Module 6 exam — combining items on the four-object home (plan §6).
MODULE_6_EXAM_QUESTIONS = [
    {"id": "m6-exam-1", "prompt": "Your assistant suddenly sounds rude in every channel. Which file do you open first, and why?", "options": ["SOUL.md — the job description owns who the assistant is", "openclaw.json — tone lives in the control panel", "logs/ — receipts change behavior"], "answer_index": 0, "explanation": "Who the assistant is lives in the job description; the control panel runs the system (Set Up the Home Base)."},
    {"id": "m6-exam-2", "prompt": "The office/worker analogy: what keeps the office open even when nobody is talking to the assistant?", "options": ["The gateway — the front desk", "SOUL.md", "The recipe box"], "answer_index": 0, "explanation": "The gateway is the front desk that keeps the office running (Set Up the Home Base)."},
    {"id": "m6-exam-3", "prompt": "You teach the assistant a new repeatable job. Where does the procedure go?", "options": ["A SKILL.md recipe card in the skills folder", "Pasted into every chat", "openclaw.json"], "answer_index": 0, "explanation": "Each skill is a recipe card — one procedure, one file (Teach It Skills)."},
    {"id": "m6-exam-4", "prompt": "The channel policy says polite in groups, private in DMs. What is that file actually doing?", "options": ["Setting the model's temperature", "Giving the same worker different rules per front door — behavior scoped by channel", "Blocking all group messages"], "answer_index": 1, "explanation": "Channel policy scopes conduct to where the conversation happens (Open the Front Door)."},
    {"id": "m6-exam-5", "prompt": "Why does the rollout checklist insist the first opening be small?", "options": ["Small rollouts are cheaper to bill", "One door, a few people, reversible — you learn safely before opening wider", "OpenClaw only supports one channel"], "answer_index": 1, "explanation": "A complete first rollout is small on purpose (Open the Front Door)."},
    {"id": "m6-exam-6", "prompt": "The safety sweep found nothing wrong. What did you actually gain?", "options": ["Nothing — sweeps only matter when they fail", "Evidence: the audit checked the doors on purpose, so trust now rests on a check, not a feeling", "A faster assistant"], "answer_index": 1, "explanation": "The sweep is the audit rhythm producing evidence (The Safety Sweep) — the same idea Module 8 grades."},
    {"id": "m6-exam-7", "prompt": "One command tells you the system is healthy after any change. Why does the module lean on it?", "options": ["Because re-verifying on demand beats trusting that yesterday's setup still holds", "It restarts the model", "It deletes old logs"], "answer_index": 0, "explanation": "The status check re-verifies instead of assuming (Set Up the Home Base; The Safety Sweep)."},
    {"id": "m6-exam-8", "prompt": "A friend edits openclaw.json to make the assistant friendlier and is confused when nothing changes. Diagnose it.", "options": ["They edited the control panel; personality lives in SOUL.md — the whole trick is never confusing the two files", "The file needs to be renamed first", "Friendliness requires a paid plan"], "answer_index": 0, "explanation": "Control panel vs job description — the distinction the module opens with (Set Up the Home Base)."},
]


# Module 1.5: a Claude Code walkthrough of context management. Supplementary —
# the lesson prose teaches the concept; the video shows one real tool doing it.
# Stored without the ?si= share parameter, matching every other video here.
MODULE_1_5_CONTEXT_VIDEO_URL = "https://www.youtube-nocookie.com/embed/eW3oTyfeWZ0"
MODULE_1_5_TOKENS_VIDEO_URL = "https://www.youtube-nocookie.com/embed/OjrGu0L5K7M"
MODULE_1_5_TRAINING_VIDEO_URL = "https://www.youtube-nocookie.com/embed/gZYrSZHHZns"

# All three Module 1.5 videos sit at the same place in their lesson: beat 3, after the
# opening explanation and its check, before the second teaching beat. Position is
# 1-based and counts the beats the learner sees, matching the player's "3 / 8".
MODULE_1_5_VIDEO_POSITION = 3

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

# Module 1 exam — fresh combining items (plan §6). The old exam was the four
# recap banks concatenated: a student re-answered the identical 20 questions
# and got a completion. Every item below spans at least two lessons or applies
# one to a novel scenario, and none appears in any recap bank (machine-checked).
MODULE_1_EXAM_QUESTIONS = [
    {
        "id": "m1-exam-1",
        "prompt": "AlphaGo beat a world champion at Go, yet it cannot drive a car or plan a holiday. In the seven-types framework, what is it?",
        "options": [
            "Narrow AI — superhuman at one task, and the only capability that exists today",
            "AGI, because beating a champion requires general intelligence",
            "A reactive machine that remembers every game it ever played",
        ],
        "answer_index": 0,
        "explanation": "Superhuman at one task is not general intelligence (What is AI?); narrow AI is the only capability that exists today (Other Types of AI).",
    },
    {
        "id": "m1-exam-2",
        "prompt": "A friend insists the chatbot 'really understands' them because its replies feel human. What is actually happening under the hood?",
        "options": [
            "It looked up their messages in a database of every possible reply",
            "It is predicting the next words from statistical patterns learned in training",
            "It passed the Turing test, which proves understanding",
        ],
        "answer_index": 1,
        "explanation": "Humanlike output is next-word prediction over learned patterns (What are LLMs?), not thinking — the gap Turing's 1950 question opened (Brief History).",
    },
    {
        "id": "m1-exam-3",
        "prompt": "Why does training a capable LLM require enormous amounts of text?",
        "options": [
            "The model memorizes the text so it can quote it back on demand",
            "Regulations require a minimum dataset size",
            "The patterns it predicts from are learned from data — more varied text, better predictions",
        ],
        "answer_index": 2,
        "explanation": "AI systems find patterns in large datasets (What is AI?), and an LLM's language ability is those patterns at scale (What are LLMs?).",
    },
    {
        "id": "m1-exam-4",
        "prompt": "The term 'artificial intelligence' was coined in the 1950s, yet the first AI winter followed. What ended the drought decades later?",
        "options": [
            "Cheaper, faster compute and far more data than early researchers ever had",
            "A new definition of intelligence that was easier to meet",
            "Governments banning AI research until it improved",
        ],
        "answer_index": 0,
        "explanation": "Early promises outran the era's compute and data; the return ran on both arriving at scale (Brief History).",
    },
    {
        "id": "m1-exam-5",
        "prompt": "A model card advertises '70 billion parameters.' What are parameters?",
        "options": [
            "The rules programmers hand-wrote for every situation",
            "The learned values inside the model, tuned during training, that shape its predictions",
            "The number of documents the model can search per second",
        ],
        "answer_index": 1,
        "explanation": "Parameters are what training adjusts — the 'large' in large language model (What are LLMs?).",
    },
    {
        "id": "m1-exam-6",
        "prompt": "One system evaluates only the current chessboard with no memory of past games; another uses recent traffic to steer a car. Which types are these?",
        "options": [
            "Both are AGI, because both make decisions",
            "Reactive machine and limited memory AI, respectively",
            "Limited memory and reactive machine, respectively",
        ],
        "answer_index": 1,
        "explanation": "Reactive machines respond to the present only; limited memory AI uses recent data (Other Types of AI).",
    },
    {
        "id": "m1-exam-7",
        "prompt": "Turing asked in 1950 whether machines can think. Which answer best matches where AI actually stands today?",
        "options": [
            "Yes — modern chatbots think and understand like people",
            "No progress at all — the question remains purely theoretical",
            "We have narrow systems that perform impressively without thinking; AGI remains hypothetical",
        ],
        "answer_index": 2,
        "explanation": "Today's AI is narrow (Other Types of AI); humanlike output is pattern prediction, not thought (What are LLMs?; Brief History).",
    },
    {
        "id": "m1-exam-8",
        "prompt": "An LLM writes a brilliant essay about swimming technique. What follows from Module 1 about its other abilities?",
        "options": [
            "Nothing — excellence at language implies nothing about tasks outside its training",
            "It could also coach swimming in a pool, since it clearly understands the sport",
            "It must be AGI, because essays require general knowledge",
        ],
        "answer_index": 0,
        "explanation": "Superhuman at one task is not general intelligence (What is AI?) — the AlphaGo lesson applied to language.",
    },
    {
        "id": "m1-exam-9",
        "prompt": "Which sequence puts Module 1's history in the right order?",
        "options": [
            "AI term coined → first AI winter → compute and data return → modern breakthrough moment",
            "First AI winter → AI term coined → modern breakthrough → compute arrives",
            "Modern breakthrough → AI term coined → first AI winter → compute arrives",
        ],
        "answer_index": 0,
        "explanation": "Coined in the 1950s, frozen by unmet promises, revived by compute and data, then the overnight-sensation moment (Brief History).",
    },
    {
        "id": "m1-exam-10",
        "prompt": "What would a system need to demonstrate before Module 1 would call it AGI rather than narrow AI?",
        "options": [
            "Beating humans at one more benchmark than last year",
            "Handling unfamiliar intellectual tasks across domains the way a person can",
            "Generating text fast enough to feel conversational",
        ],
        "answer_index": 1,
        "explanation": "AGI differs from narrow AI by generality across tasks, not by higher scores on one (Other Types of AI).",
    },
]

MODULE_1_CHECKPOINT = {
    "questions": MODULE_1_EXAM_QUESTIONS,
}


# Module 1's lesson bodies finished migrating to content/module-1-introduction-to-ai/*.md.
# The old in-file copies told learners to "open the Video tab", which no longer
# exists — the player renders inside the lesson step — so they are gone rather
# than kept as a fallback that would serve wrong instructions.


# Module 5 recap questions — real questions written from the lesson content.
# Module 5 seam checks (plan §0.2), grounded in each lesson's own text.
MODULE_5_SEAM_CHECKS = {
    "what-hermes-is": [
        {
            "id": "m5-what-seam1",
            "prompt": "Hermes sends API calls to a model and then executes actions. Which half happens on your machine?",
            "options": [
                "The heavy thinking — the model runs locally",
                "The doing — commands, files, and services run on yours; thinking happens on the provider's servers",
                "Neither; Hermes is entirely cloud-hosted",
            ],
            "answer_index": 1,
            "explanation": "Thinking happens on the provider's servers, doing happens on yours — and that last part is exactly why this module cares so much about safety.",
        },
        {
            "id": "m5-what-seam2",
            "prompt": "In the three-box diagram, which box runs on your machine?",
            "options": [
                "The middle one — the agent loop and its tools",
                "The right one — the model provider",
                "The left one — the gateways only",
            ],
            "answer_index": 0,
            "explanation": "Tasks flow left to right and results flow back, but the middle box — agent loop plus tools — is the one running on your machine.",
        },
    ],
    "openrouter-and-your-api-key": [
        {
            "id": "m5-or-seam1",
            "prompt": "Why does this lesson come *before* the install?",
            "options": [
                "Because the installer launches a setup wizard that asks for provider and key mid-install",
                "Because OpenRouter must approve your account for 24 hours first",
                "Because Hermes cannot be installed without a paid plan",
            ],
            "answer_index": 0,
            "explanation": "v0.18.2's installer launches the wizard mid-install and asks for provider and key, so you get the account, cap, and key ready first.",
        },
        {
            "id": "m5-or-seam2",
            "prompt": "The lesson says to use a dedicated email rather than your personal one. What is the reason given?",
            "options": [
                "OpenRouter blocks personal email domains",
                "One identity for the agent means one kill switch if anything goes wrong",
                "Dedicated emails get higher free-model rate limits",
            ],
            "answer_index": 1,
            "explanation": "One identity for the agent means one kill switch — and it pays off in the final lesson, where you can delete the whole account.",
        },
    ],
    "install-and-setup-wizard": [
        {
            "id": "m5-inst-seam1",
            "prompt": "Windows 10 users are told to install Windows Terminal first. What breaks without it?",
            "options": [
                "The installer refuses to run at all",
                "The wizard's ANSI colours render as garbage, so you cannot read the menus",
                "Docker cannot be detected as a backend",
            ],
            "answer_index": 1,
            "explanation": "Everything still works, but the legacy console renders the wizard's ANSI colours as garbage — you cannot read the menus or match the screenshots.",
        },
        {
            "id": "m5-inst-seam2",
            "prompt": "Blank Slate force-enables only three things. Which three?",
            "options": [
                "Provider & Model, File Operations, and Terminal",
                "Web, Browser, and Code Execution",
                "Memory, Skills, and Delegation",
            ],
            "answer_index": 0,
            "explanation": "Only the minimum to run an agent at all is force-enabled. Everything else — web, browser, code exec, vision, memory, delegation, cron, skills, plugins, MCP — starts disabled.",
        },
        {
            "id": "m5-inst-seam3",
            "prompt": "At the provider step, what happens right after you paste your key?",
            "options": [
                "The wizard prints `API key saved.`",
                "The wizard immediately starts a chat to test it",
                "The wizard restarts so the key can load",
            ],
            "answer_index": 0,
            "explanation": "You paste at the `OPENROUTER_API_KEY` prompt and see `API key saved.`, then move on to picking a default model from the list.",
        },
        {
            "id": "m5-inst-seam4",
            "prompt": "The wizard offers Local as the default terminal backend. Why does the lesson say never to choose it for a running agent?",
            "options": [
                "Local is slower than Docker",
                "With Local there is no isolation — the agent runs as you, with your files and network",
                "Local does not support Python",
            ],
            "answer_index": 1,
            "explanation": "No isolation at all: the agent runs as you, with your files, your network, your environment. Box before power switch.",
        },
        {
            "id": "m5-inst-seam5",
            "prompt": "Which four lines should `/config` show before you exit?",
            "options": [
                "Model, API Key (masked), Environment: docker, Toolsets: file, terminal",
                "Model, Password, Environment: local, Toolsets: all",
                "Provider, Region, Container ID, Skills: 73",
            ],
            "answer_index": 0,
            "explanation": "Those four lines prove the configuration: your free model via openrouter.ai, a masked key, the docker environment, and the minimal toolsets.",
        },
        {
            "id": "m5-inst-seam6",
            "prompt": "After the wizard, Docker Desktop shows no Hermes container. What does the lesson say about that?",
            "options": [
                "The Docker backend failed and must be reconfigured",
                "It is expected — and it is the first question of the next lesson",
                "The container is hidden and can only be seen with `docker ps -a`",
            ],
            "answer_index": 1,
            "explanation": "Expected: the sandbox does not exist yet. The checkpoint calls it out deliberately as the opening question of the next lesson.",
        },
    ],
    "first-conversation-and-container": [
        {
            "id": "m5-first-seam1",
            "prompt": "Why was there no container after you chose the Docker backend?",
            "options": [
                "The backend is lazy — choosing it wrote one line of config; the container appears on the first command",
                "Docker Desktop had to be restarted first",
                "Containers are only created when you exit Hermes",
            ],
            "answer_index": 0,
            "explanation": "Choosing the backend only wrote config. The container is created the first time the agent actually runs a command.",
        },
        {
            "id": "m5-first-seam2",
            "prompt": "Commands run inside the container, but where does your API key live?",
            "options": [
                "Inside the container, so commands can reach the provider",
                "In the `.env` file on the host — commands inside the box never see the credential",
                "In the container's environment variables, masked",
            ],
            "answer_index": 1,
            "explanation": "Keys stay outside the box: the `.env` lives on the host and the Hermes process makes the model calls, so commands inside the container never see it.",
        },
        {
            "id": "m5-first-seam3",
            "prompt": "You ask the agent to run `whoami`. The answer is `root`. What does that tell you?",
            "options": [
                "Your own account has been elevated to administrator",
                "Inside the container the agent runs as the container's root user, not as you",
                "The sandbox failed and the command ran on the host",
            ],
            "answer_index": 1,
            "explanation": "The answer is the tell: inside the container the agent is the container's root user — not you on your machine.",
        },
        {
            "id": "m5-first-seam4",
            "prompt": "You start several Hermes sessions across the course. What accumulates, and what should you do?",
            "options": [
                "Nothing accumulates; sessions reuse one container",
                "Each session gets its own container; old ones are safe to delete — the box is furniture",
                "Sessions share a container but each adds a new image",
            ],
            "answer_index": 1,
            "explanation": "Each session gets its own container, so they pile up. Deleting old ones is Module 4.5's disposability lesson in practice — throw it out and a fresh one appears on demand.",
        },
    ],
    "sandbox-verification-lab": [
        {
            "id": "m5-lab-seam1",
            "prompt": "The lab warns each attempt may take 2–3+ minutes while the agent hunts. What does a long, exhaustive failure mean?",
            "options": [
                "The agent is broken and should be interrupted",
                "It is the best result — the agent tried everything and the box still held",
                "The model is too small and should be swapped",
            ],
            "answer_index": 1,
            "explanation": "Don't interrupt it. A long exhaustive failure is the best result this lab produces: the agent tried everything with its full toolset and the box held.",
        },
        {
            "id": "m5-lab-seam2",
            "prompt": "On Windows, why is `/mnt/c/Users/` the realistic escape route to test?",
            "options": [
                "Because Docker runs via WSL, and `/mnt/c` is how WSL normally reaches your C: drive",
                "Because Windows stores all Docker images there",
                "Because Hermes mounts it by default for file operations",
            ],
            "answer_index": 0,
            "explanation": "It is the realistic back door on lab machines — and the hardened container does not get that mount. If you ever DO see your files there, the setup is misconfigured; stop and flag it.",
        },
    ],
    "put-it-to-work": [
        {
            "id": "m5-work-seam1",
            "prompt": "What is the line between a chatbot and an agent, as this lesson draws it?",
            "options": [
                "A chatbot can *tell* you the Fibonacci numbers; an agent writes a program, runs it, checks the output, and reports back",
                "An agent uses a bigger model than a chatbot",
                "A chatbot works offline; an agent needs the internet",
            ],
            "answer_index": 0,
            "explanation": "Text in → text out versus goal in → acts → reads the result → acts again. A chatbot cannot run the program; your agent did it unsupervised.",
        },
        {
            "id": "m5-work-seam2",
            "prompt": "In Task 1 the agent performs four steps with no further input. Which is the one a chatbot could not do?",
            "options": [
                "write_file — creating the script",
                "terminal — running the script with python inside the container",
                "answer — reporting the largest number",
            ],
            "answer_index": 1,
            "explanation": "Step 2 is the dividing line: a chatbot cannot run the program on a real machine. Your agent ran it inside the locked-down container you designed.",
        },
        {
            "id": "m5-work-seam3",
            "prompt": "In Task 2 you are told to be bold. What makes that safe?",
            "options": [
                "The agent asks permission before every command",
                "Everything runs in the disposable sandbox — worst case you delete the container and a fresh one appears",
                "Free models cannot cause damage",
            ],
            "answer_index": 1,
            "explanation": "Everything runs in the disposable sandbox. Being bold is safe precisely because the box is furniture.",
        },
        {
            "id": "m5-work-seam4",
            "prompt": "The autonomy dial lists capabilities Blank Slate left off. Which one makes the agent act with no human present at all?",
            "options": [
                "Skills + memory",
                "Gateways such as Telegram or Discord",
                "Cron — it acts on a schedule",
            ],
            "answer_index": 2,
            "explanation": "Gateways let it act when you are nowhere near the terminal; cron goes further — it acts on a schedule with no human present at all.",
        },
        {
            "id": "m5-work-seam5",
            "prompt": "Teardown is three steps because two things live outside your machine. Which step is the real kill switch?",
            "options": [
                "Running `hermes uninstall --full`",
                "Deleting the hermes containers and the nikolaik/python-nodejs image",
                "Revoking the API key on OpenRouter — no local uninstaller can reach it",
            ],
            "answer_index": 2,
            "explanation": "The key lives on OpenRouter's servers. Revoking it is the real kill switch: even a leaked copy becomes worthless.",
        },
    ],
}


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
    "openrouter-and-your-api-key": [
        {
            "id": "m5-or-1",
            "prompt": "Why does OpenRouter setup happen BEFORE installing Hermes?",
            "options": [
                "OpenRouter must approve your machine first",
                "The v0.18.2 installer launches a setup wizard that asks for your provider and API key mid-install",
                "Hermes refuses to install without a key on disk",
            ],
            "answer_index": 1,
        },
        {
            "id": "m5-or-2",
            "prompt": "Why create the OpenRouter account with a dedicated email?",
            "options": [
                "One identity for the agent means one kill switch if anything goes wrong",
                "OpenRouter bans personal email domains",
                "It gets you more free credits",
            ],
            "answer_index": 0,
        },
        {
            "id": "m5-or-3",
            "prompt": "What must you set in the OpenRouter dashboard before anything else?",
            "options": [
                "A profile picture for the agent",
                "Two-factor authentication",
                "A hard spending cap (the course uses $5)",
            ],
            "answer_index": 2,
        },
        {
            "id": "m5-or-4",
            "prompt": "What should you expect from a :free model?",
            "options": [
                "Identical performance to paid models",
                "Simple requests are quick, but hard tasks can mean minutes of visible trial-and-error \u2014 normal, not broken",
                "It only answers 10 questions per day",
            ],
            "answer_index": 1,
        },
        {
            "id": "m5-or-5",
            "prompt": "Why does the course use OpenRouter?",
            "options": [
                "It's the only provider Hermes supports",
                "One API key, many models \u2014 swapping models is a config change, not a rebuild",
                "It's the fastest provider",
            ],
            "answer_index": 1,
        },
    ],
    "install-and-setup-wizard": [
        {
            "id": "m5-iw-1",
            "prompt": "What does choosing Blank Slate in the wizard mean?",
            "options": [
                "Everything off except Provider & Model, File Operations, and Terminal \u2014 you opt in to each capability deliberately",
                "The agent starts with no model configured",
                "All 73 bundled skills are enabled",
            ],
            "answer_index": 0,
        },
        {
            "id": "m5-iw-2",
            "prompt": "Which terminal backend must you NEVER use for a running agent?",
            "options": [
                "Docker",
                "Local \u2014 no isolation at all: the agent runs as you, with your files and network",
                "SSH",
            ],
            "answer_index": 1,
        },
        {
            "id": "m5-iw-3",
            "prompt": "You chose Docker in the wizard, but Docker Desktop shows no Hermes container. Why?",
            "options": [
                "The wizard only wrote config \u2014 the container is created the first time the agent runs a command",
                "The install failed silently",
                "Containers are invisible until you sign in to Docker Hub",
            ],
            "answer_index": 0,
        },
        {
            "id": "m5-iw-4",
            "prompt": "What state should everyone be in at this lesson's checkpoint?",
            "options": [
                "First conversation completed",
                "Wizard done, /config verified (docker backend, :free model, file+terminal toolsets), no conversation yet",
                "Agent connected to Telegram",
            ],
            "answer_index": 1,
        },
        {
            "id": "m5-iw-5",
            "prompt": "The course pins Hermes v0.18.2. What should you do if your wizard looks slightly different?",
            "options": [
                "Uninstall Docker and try again",
                "Expect version drift \u2014 newer versions likely work, minor differences are normal",
                "Stop the course and wait for an update",
            ],
            "answer_index": 1,
        },
    ],
    "first-conversation-and-container": [
        {
            "id": "m5-fc-1",
            "prompt": "You ask the agent to run `whoami` and it answers `root`. What does that tell you?",
            "options": [
                "The agent has hacked your machine's admin account",
                "The command ran as the container's root user \u2014 inside the box, not as you",
                "Hermes always lies about usernames",
            ],
            "answer_index": 1,
        },
        {
            "id": "m5-fc-2",
            "prompt": "Where does your API key live once the agent is running?",
            "options": [
                "In the .env file on the host \u2014 commands inside the container never see it",
                "Copied into the container at /workspace/.env",
                "Uploaded to the model provider for safekeeping",
            ],
            "answer_index": 0,
        },
        {
            "id": "m5-fc-3",
            "prompt": "You give the agent a hard request and it works for minutes, visibly trying and retrying commands. What are you watching?",
            "options": [
                "The container throttling it \u2014 raise the CPU limit",
                "The agent loop running live: model picks a tool call, it runs in the container, the result feeds back, repeat",
                "Your spending cap being hit",
            ],
            "answer_index": 1,
        },
        {
            "id": "m5-fc-4",
            "prompt": "How do you verify the sandbox container actually exists?",
            "options": [
                "Ask the agent \u2014 it always knows",
                "Run `docker ps` in your own terminal and look for the hermes container",
                "Check Task Manager for a process called hermes-box",
            ],
            "answer_index": 1,
        },
        {
            "id": "m5-fc-5",
            "prompt": "After a week of sessions you have several stopped hermes containers. What do you do?",
            "options": [
                "Never touch them \u2014 the agent needs its history",
                "Delete the old ones \u2014 each session gets its own container, and they're disposable by design",
                "Merge them into one container",
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
            "prompt": "The container caps processes at 256. What does that protect against?",
            "options": [
                "The model sending too many API requests",
                "A runaway loop (like a fork bomb) taking down the machine \u2014 it hits the ceiling instead",
                "Other students connecting to your container",
            ],
            "answer_index": 1,
        },
        {
            "id": "m5-sv-6",
            "prompt": "You ask the agent to list /mnt/c/Users/ and it's empty. What does that mean?",
            "options": [
                "The sandbox is holding \u2014 the container doesn't get WSL's mount of your C: drive. If your files DID show up, the setup is misconfigured",
                "Windows is broken",
                "The agent refused the command",
            ],
            "answer_index": 0,
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
    "put-it-to-work": [
        {
            "id": "m5-pw-1",
            "prompt": "What's the core difference between a chatbot and an agent?",
            "options": [
                "An agent uses a bigger model",
                "A chatbot goes text-in/text-out; an agent pursues a goal by acting, reading the result, and acting again in a loop",
                "An agent always runs in the cloud",
            ],
            "answer_index": 1,
        },
        {
            "id": "m5-pw-2",
            "prompt": "In Task 1, why can a chatbot NOT do what your agent did?",
            "options": [
                "A chatbot can't count that high",
                "A chatbot can only produce text \u2014 it can't write a program and actually run it on a real machine",
                "A chatbot isn't allowed to use Python",
            ],
            "answer_index": 1,
        },
        {
            "id": "m5-pw-3",
            "prompt": "Where does the code the agent writes actually run?",
            "options": [
                "Directly on your Windows machine",
                "On OpenRouter's servers",
                "Inside the locked-down Docker container you built",
            ],
            "answer_index": 2,
        },
        {
            "id": "m5-pw-4",
            "prompt": "You state a GOAL instead of a list of commands. What does the agent do with it?",
            "options": [
                "Asks you for the exact commands to run",
                "Figures out the steps itself and executes them \u2014 that's the loop, and the autonomy",
                "Refuses unless you enable admin mode",
            ],
            "answer_index": 1,
        },
        {
            "id": "m5-pw-5",
            "prompt": "This is still the 'minimal' agent. What makes an agent MORE autonomous?",
            "options": [
                "Capabilities Blank Slate left off \u2014 skills, memory, gateways, cron, delegation",
                "A faster internet connection",
                "Turning off the Docker sandbox",
            ],
            "answer_index": 0,
        },
    ],
}


# Module 7 recap questions — real questions written from the lesson content.
# Module 7 seam checks (plan §0.2), grounded in each lesson's own text.
MODULE_7_SEAM_CHECKS = {
    "what-claude-code-is": [
        {
            "id": "m7-what-seam1",
            "prompt": "In the three-box diagram, what is different about Claude Code compared with the Hermes build?",
            "options": [
                "The middle and right boxes come from the same company — no OpenRouter-style model swapping",
                "There is no model provider box at all",
                "The gateway box disappears because Claude Code has no interface",
            ],
            "answer_index": 0,
            "explanation": "Claude Code talks to Claude models only: the agent loop and the model provider are both Anthropic, so there is no model swapping.",
        },
        {
            "id": "m7-what-seam2",
            "prompt": "Hermes needed you to bring a Docker sandbox before first run. What does Claude Code ship with instead?",
            "options": [
                "Nothing — you still build the sandbox yourself",
                "A permission system that asks before editing files or running commands",
                "A separate antivirus layer",
            ],
            "answer_index": 1,
            "explanation": "Safety is built in, not bolted on: Claude Code ships a permission system and a sandboxable shell tool, so this module configures guardrails rather than building them.",
        },
    ],
    "install-and-first-session": [
        {
            "id": "m7-inst-seam1",
            "prompt": "Why does the lesson tell you to buy prepaid credits and leave auto-reload off?",
            "options": [
                "Because prepaid credits are the spending cap — when they are gone, the agent stops",
                "Because auto-reload is not available on Console accounts",
                "Because credits expire if reloading is enabled",
            ],
            "answer_index": 0,
            "explanation": "Same pattern as the OpenRouter step: set the money limit before the agent does anything. Prepaid credits with no auto-reload *are* the cap.",
        },
        {
            "id": "m7-inst-seam2",
            "prompt": "You ask Claude Code to \"delete every file in this folder\". What does the lesson have you do?",
            "options": [
                "Approve it, to see whether the sandbox holds",
                "Deny it — the deny button is the explicit boundary the agent acts inside",
                "Nothing; the agent refuses without asking",
            ],
            "answer_index": 1,
            "explanation": "It asks first, and you deny. The lesson frames that deny as Module 4.5's principle as a feature: the agent acts on your machine, so the boundary has to be explicit.",
        },
        {
            "id": "m7-inst-seam3",
            "prompt": "Why does the first session happen in a fresh empty folder like `~/agent-practice`?",
            "options": [
                "Because Claude Code cannot start in a folder that already has files",
                "Same discipline as Hermes' blank slate — the working directory is the agent's default territory",
                "Because permission prompts only appear in empty folders",
            ],
            "answer_index": 1,
            "explanation": "The prompt shows the working directory, and that directory is the agent's default territory — so the first run happens in an empty practice folder, not your real files.",
        },
    ],
    "claudemd-and-skills": [
        {
            "id": "m7-cmd-seam1",
            "prompt": "Which file is loaded automatically at the start of every session?",
            "options": [
                "CLAUDE.md — standing instructions, always loaded",
                "SKILL.md — loaded every session so triggers stay fresh",
                "log.md — the agent reads its own history first",
            ],
            "answer_index": 0,
            "explanation": "CLAUDE.md is always loaded; skills are loaded when relevant. That is exactly why CLAUDE.md should stay short.",
        },
        {
            "id": "m7-cmd-seam2",
            "prompt": "In a skill's frontmatter, what decides *when* the agent uses it?",
            "options": [
                "The `name` field",
                "The `description` field — the agent reads it to decide the skill applies",
                "Alphabetical order of the skill folders",
            ],
            "answer_index": 1,
            "explanation": "The description is the trigger, exactly like OpenClaw's frontmatter — which is why a natural phrase can invoke the skill without typing `/daily-log`.",
        },
        {
            "id": "m7-cmd-seam3",
            "prompt": "You run the daily-log skill twice and the second run overwrites the file instead of appending. What does the lesson tell you to do?",
            "options": [
                "File a bug — the skill system is unreliable",
                "Sharpen the prose in the skill's steps and try again — debugging a skill is editing prose",
                "Switch to writing the log with code instead",
            ],
            "answer_index": 1,
            "explanation": "If the second run rewrites the file, step 4 was not clear enough. Editing the prose *is* the debugging — that is what programming an agent looks like here.",
        },
    ],
    "custom-subagents": [
        {
            "id": "m7-sub-seam1",
            "prompt": "The reviewer subagent's frontmatter reads `tools: Read, Glob, Grep`. What does that guarantee?",
            "options": [
                "It is physically unable to modify files or run commands, no matter what it is asked",
                "It will ask permission before editing, like the main agent",
                "It can edit files but not delete them",
            ],
            "answer_index": 0,
            "explanation": "No Write, no Edit, no Bash. Restriction lives in the file — you audit it by reading one line.",
        },
        {
            "id": "m7-sub-seam2",
            "prompt": "Which Module 4.5 idea do restricted subagents apply, and at what scale?",
            "options": [
                "Reproducibility, applied per-project",
                "Least privilege, applied per-agent instead of per-container",
                "Disposability, applied per-session",
            ],
            "answer_index": 1,
            "explanation": "Choosing each subagent's tools is least privilege — the container principle from 4.5, now applied one agent at a time.",
        },
        {
            "id": "m7-sub-seam3",
            "prompt": "You ask the reviewer to fix the problems it found. What happens?",
            "options": [
                "It fixes them, since it already read the files",
                "It cannot — the main agent has to apply fixes, with your permission prompt still in the loop",
                "It asks you to grant it the Write tool for this one request",
            ],
            "answer_index": 1,
            "explanation": "The reviewer has no Write tool, so it cannot act. The main agent applies fixes and your permission prompt stays in the loop.",
        },
    ],
    "build-your-agent": [
        {
            "id": "m7-lab-seam1",
            "prompt": "The lab's `CLAUDE.md` must state that notes go in `notes/`, every note gets a Sources section, and notes are never deleted. Why do those belong there rather than in a skill?",
            "options": [
                "They are standing rules that apply always, not a triggered procedure",
                "Because skills cannot mention folders",
                "Because CLAUDE.md is the only file the agent can read",
            ],
            "answer_index": 0,
            "explanation": "Standing rule that applies always → CLAUDE.md; procedure that applies when triggered → skill. The lab splits the four files on exactly that line.",
        },
        {
            "id": "m7-lab-seam2",
            "prompt": "You give one instruction and expect four hand-offs. Which component fires *first*?",
            "options": [
                "The reviewer subagent, so the plan gets checked before work starts",
                "The research-note skill — triggered without you naming it",
                "The daily-log skill, to record that work began",
            ],
            "answer_index": 1,
            "explanation": "The expected flow is research-note skill → note written → daily-log fires → reviewer reports. The first hand-off is the skill triggering on its description alone.",
        },
        {
            "id": "m7-lab-seam3",
            "prompt": "During the pipeline run, a step never fires. Where does the lesson send you to debug?",
            "options": [
                "The model settings, to raise the temperature",
                "The `description:` line that carries the trigger — sharpen it and rerun",
                "The permission mode, which must be switched off",
            ],
            "answer_index": 1,
            "explanation": "Same debugging move as lesson 3: the trigger lives in a description line. Sharpen the prose and run it again.",
        },
    ],
}


MODULE_7_RECAP = {
    "what-claude-code-is": [
        {
            "id": "m7-wc-1",
            "prompt": "In the three-box diagram, what is Claude Code?",
            "options": [
                "The model provider",
                "The agent loop + tools box — an orchestrator, not a model",
                "A gateway like Telegram",
            ],
            "answer_index": 1,
        },
        {
            "id": "m7-wc-2",
            "prompt": "What's different about Claude Code's boxes compared to Hermes?",
            "options": [
                "The agent loop runs in the cloud instead of your machine",
                "There is no model provider box",
                "The agent and the model come from the same company — no OpenRouter-style model swapping",
            ],
            "answer_index": 2,
        },
        {
            "id": "m7-wc-3",
            "prompt": "How does Claude Code's safety approach differ from the Hermes build?",
            "options": [
                "It ships with a built-in permission system, instead of us adding a Docker sandbox before first run",
                "It has no safety features, so Docker is mandatory",
                "It refuses to run shell commands entirely",
            ],
            "answer_index": 0,
        },
        {
            "id": "m7-wc-4",
            "prompt": "Which concept is genuinely NEW in build #3 (not in Hermes or OpenClaw)?",
            "options": [
                "Skills",
                "Subagents — specialist agents the main agent delegates to",
                "Persistent memory files",
            ],
            "answer_index": 1,
        },
        {
            "id": "m7-wc-5",
            "prompt": "How do we customize Claude Code in this module?",
            "options": [
                "By writing Python with the Agent SDK",
                "By editing markdown and config files — no code",
                "Through a web dashboard",
            ],
            "answer_index": 1,
        },
    ],
    "install-and-first-session": [
        {
            "id": "m7-if-1",
            "prompt": "Why do we use prepaid Console credits with auto-reload OFF?",
            "options": [
                "Because subscriptions don't work with Claude Code",
                "Prepaid credits ARE the spending cap — when they're gone, the agent stops",
                "Auto-reload is a security vulnerability",
            ],
            "answer_index": 1,
        },
        {
            "id": "m7-if-2",
            "prompt": "Where does the first session happen, and why?",
            "options": [
                "In an empty practice folder — same blank-slate discipline as the Hermes install",
                "In your most important project, to test it properly",
                "In the cloud, so nothing local is at risk",
            ],
            "answer_index": 0,
        },
        {
            "id": "m7-if-3",
            "prompt": "What happens in default permission mode when the agent wants to write a file?",
            "options": [
                "It writes the file and reports afterwards",
                "It asks for your approval first",
                "It refuses to write files at all",
            ],
            "answer_index": 1,
        },
        {
            "id": "m7-if-4",
            "prompt": "Why does the lesson have you DENY a request on purpose?",
            "options": [
                "To exercise the boundary: the agent acts on your machine, so you should see refusal work",
                "Because the delete command would have escaped the folder",
                "To trigger a refund of unused tokens",
            ],
            "answer_index": 0,
        },
        {
            "id": "m7-if-5",
            "prompt": "What does the working directory shown at the prompt represent?",
            "options": [
                "Where Claude Code was installed",
                "The agent's default territory for the session",
                "A temporary cache that is deleted on exit",
            ],
            "answer_index": 1,
        },
    ],
    "claudemd-and-skills": [
        {
            "id": "m7-cs-1",
            "prompt": "What is CLAUDE.md?",
            "options": [
                "Standing instructions loaded automatically every session — prompt-writing you do once",
                "A log of everything the agent has done",
                "The agent's source code",
            ],
            "answer_index": 0,
        },
        {
            "id": "m7-cs-2",
            "prompt": "What decides WHEN a skill gets used?",
            "options": [
                "The order skills appear in the folder",
                "The description in its YAML frontmatter — the trigger",
                "Skills only run when typed as /commands",
            ],
            "answer_index": 1,
        },
        {
            "id": "m7-cs-3",
            "prompt": "Standing rule vs procedure — which file does each go in?",
            "options": [
                "Rules in a skill; procedures in CLAUDE.md",
                "Both go in CLAUDE.md",
                "Always-on rules in CLAUDE.md; triggered procedures in a skill",
            ],
            "answer_index": 2,
        },
        {
            "id": "m7-cs-4",
            "prompt": "Your skill overwrites the log instead of appending. What's the fix?",
            "options": [
                "Edit the skill's prose to make the append step unambiguous, and rerun",
                "Reinstall Claude Code",
                "Switch the skill from markdown to Python",
            ],
            "answer_index": 0,
        },
        {
            "id": "m7-cs-5",
            "prompt": "Where do the OpenClaw skills you wrote in Module 6 fit in?",
            "options": [
                "They're incompatible — Claude Code uses JSON skills",
                "Same SKILL.md idea — the format transfers almost line for line",
                "OpenClaw skills must be compiled first",
            ],
            "answer_index": 1,
        },
    ],
    "custom-subagents": [
        {
            "id": "m7-su-1",
            "prompt": "What is a subagent?",
            "options": [
                "A smaller, cheaper model",
                "A specialist agent with its own instructions, tools, and context that the main agent delegates to",
                "A backup copy of the main agent",
            ],
            "answer_index": 1,
        },
        {
            "id": "m7-su-2",
            "prompt": "The reviewer has `tools: Read, Glob, Grep`. Why can't it damage your files?",
            "options": [
                "Its system prompt politely asks it not to",
                "Subagents can never touch files",
                "No Write, Edit, or Bash — it is physically unable to modify anything",
            ],
            "answer_index": 2,
        },
        {
            "id": "m7-su-3",
            "prompt": "Which Module 4.5 principle do restricted subagent toolsets implement?",
            "options": [
                "Least privilege — minimum access needed for the job, now per-agent",
                "Disposability — delete and rebuild",
                "Port isolation",
            ],
            "answer_index": 0,
        },
        {
            "id": "m7-su-4",
            "prompt": "What comes back to the main conversation after a delegation?",
            "options": [
                "The subagent's full reading and exploration history",
                "Only the subagent's final report — its working context stays separate",
                "Nothing; you must open the subagent's log file",
            ],
            "answer_index": 1,
        },
        {
            "id": "m7-su-5",
            "prompt": "Where is a subagent defined?",
            "options": [
                "One markdown file in .claude/agents/ — YAML badge on top, job description below",
                "In CLAUDE.md under a ## Subagents heading",
                "In a Python class registered with the CLI",
            ],
            "answer_index": 0,
        },
    ],
    "build-your-agent": [
        {
            "id": "m7-ba-1",
            "prompt": "The research notebook agent is built from what?",
            "options": [
                "Four markdown/config files — CLAUDE.md, two skills, one subagent",
                "A Python script using the Agent SDK",
                "A Docker compose file",
            ],
            "answer_index": 0,
        },
        {
            "id": "m7-ba-2",
            "prompt": "You ask for research and the research-note skill doesn't fire. First debugging move?",
            "options": [
                "Sharpen the skill's description: line — that's where the trigger lives",
                "Reinstall the skill folder",
                "Grant the skill more tools",
            ],
            "answer_index": 0,
        },
        {
            "id": "m7-ba-3",
            "prompt": "Why must 'have the reviewer delete log.md' fail?",
            "options": [
                "log.md is write-protected by the OS",
                "The reviewer's tools: line grants no Write/Edit/Bash — deletion is impossible for it",
                "CLAUDE.md forbids the reviewer from reading logs",
            ],
            "answer_index": 1,
        },
        {
            "id": "m7-ba-4",
            "prompt": "The agent happily saves a note to your Desktop. What does that tell you?",
            "options": [
                "Your CLAUDE.md boundary rule is too vague — fix the wording and retest",
                "Claude Code ignores CLAUDE.md",
                "The Desktop is inside the workspace",
            ],
            "answer_index": 0,
        },
        {
            "id": "m7-ba-5",
            "prompt": "Across the three builds, what did the red-team checks have in common?",
            "options": [
                "They prove the model can't lie",
                "You verify the safety boundary yourself instead of trusting that it works",
                "They measure token spend",
            ],
            "answer_index": 1,
        },
    ],
}


# Module 4.5 recap questions — real questions written from the lesson content.
# Module 4.5 seam checks (plan §0.2). One per gap between reading beats,
# answerable from the beat before it; distinct from MODULE_4_5_RECAP.
MODULE_4_5_SEAM_CHECKS = {
    "why-docker": [
        {
            "id": "m45-why-seam1",
            "prompt": "In the shipping-container analogy, what plays the part of the crane?",
            "options": [
                "Docker itself — the ship does not care what is inside, it just carries containers",
                "Your operating system, which unpacks each container",
                "Docker Hub, which lifts images off the internet",
            ],
            "answer_index": 0,
            "explanation": "The ship is your computer, the container is the packaged app, and Docker is the crane that moves it.",
        },
    ],
    "docker-main-terms": [
        {
            "id": "m45-terms-seam1",
            "prompt": "Which term does the lesson compare to \"Tupperware for leftovers\"?",
            "options": [
                "Port mapping",
                "Volume — persistent storage that survives deletion",
                "Dockerfile",
            ],
            "answer_index": 1,
            "explanation": "A volume is persistent storage a container can use and it survives deletion — leftovers you keep. Port mapping is forwarding your mail; a Dockerfile is writing your own recipe.",
        },
    ],
    "installing-docker-desktop": [
        {
            "id": "m45-install-seam1",
            "prompt": "On Windows, Docker Desktop runs on top of which system that the installer sets up for you?",
            "options": [
                "WSL 2 — say yes if the installer prompts you",
                "A virtual machine you must build yourself first",
                "Docker Hub, installed locally",
            ],
            "answer_index": 0,
            "explanation": "Docker Desktop on Windows uses WSL 2. The installer sets it up; if prompted, accept.",
        },
        {
            "id": "m45-install-seam2",
            "prompt": "You finished the installer. What tells you Docker is actually ready to use?",
            "options": [
                "The download finished, so it is ready",
                "The whale icon stops animating and the dashboard shows \"Engine running\" in green",
                "You created a Docker account",
            ],
            "answer_index": 1,
            "explanation": "Wait for the whale: Docker is ready when the icon stops animating and the dashboard says Engine running. An account is not required for this course.",
        },
    ],
    "first-containers": [
        {
            "id": "m45-first-seam1",
            "prompt": "You ran `docker run hello-world` and the image was not on your machine. What did Docker do first?",
            "options": [
                "Refused, and told you to download the image manually",
                "Pulled the image from Docker Hub, then created a container from it",
                "Built the image from a Dockerfile in your current folder",
            ],
            "answer_index": 1,
            "explanation": "Docker looked locally, did not find it, pulled it from Docker Hub, created a container, ran it, and the container exited — the whole loop in one command.",
        },
        {
            "id": "m45-first-seam2",
            "prompt": "You stopped and deleted the nginx container. What is left on your machine?",
            "options": [
                "Nothing at all — the image is deleted with the container",
                "The cached image, so re-running the command brings it back in seconds",
                "A running web server on port 8080",
            ],
            "answer_index": 1,
            "explanation": "Deleting a container leaves your machine exactly as it was, but the image stays cached locally — that is why re-running `docker run` is instant.",
        },
    ],
}


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
# Module 1.5 seam checks (plan §0.2). One question per gap between reading
# beats, each answerable from the beat immediately before it, in the lesson's
# own vocabulary. Distinct from MODULE_1_5_RECAP by construction — the recap
# bank belongs to the recap quiz.
MODULE_1_5_SEAM_CHECKS = {
    "context-windows": [
        {
            "id": "m15-cw-seam1",
            "prompt": "You attach a 50-page document to an already-long chat thread. What does the lesson say can happen to the earliest messages?",
            "options": [
                "They get pushed out — everything competes for the same limited space",
                "They are saved permanently, because the model remembers all past chats",
                "They move to a second context window reserved for older turns",
            ],
            "answer_index": 0,
            "explanation": "System instructions, history, your message, and pasted material all compete for one window, so a big attachment plus a long thread can push out the earliest messages.",
        },
        {
            "id": "m15-cw-seam2",
            "prompt": "An app silently keeps the system prompt and your most recent turns, but drops the older middle of the conversation. Which overflow behaviour is that?",
            "options": [
                "Truncate from the start",
                "Truncate from the middle",
                "Summarize",
            ],
            "answer_index": 1,
            "explanation": "Truncating from the middle keeps the system prompt plus recent turns. The lesson lists it alongside truncate-from-start, error, and summarize.",
        },
        {
            "id": "m15-cw-seam3",
            "prompt": "Halfway through a long chat the topic changes completely. Which strategy from this lesson fits best?",
            "options": [
                "Paste the whole project so nothing is missing",
                "Reset the thread, so old noise stops eating tokens",
                "Ask the model to remember the new topic permanently",
            ],
            "answer_index": 1,
            "explanation": "Resetting the thread is one of the four strategies — a fresh chat when the topic changes keeps old noise from eating tokens.",
        },
    ],
    "tokens": [
        {
            "id": "m15-tok-seam1",
            "prompt": "Why do code and JSON often use more tokens than the same number of characters of ordinary English?",
            "options": [
                "Rare symbols split into extra pieces, so more tokens per visible character",
                "Tokenizers refuse to process punctuation and skip it",
                "Code is always sent twice, once as text and once as data",
            ],
            "answer_index": 0,
            "explanation": "Code, JSON, and non-English text use more tokens per visible character because rare symbols split into extra pieces.",
        },
        {
            "id": "m15-tok-seam2",
            "prompt": "Why can an agent that loops — plan, act, observe, repeat — run up a bill quickly?",
            "options": [
                "Each pass through the loop sends and generates more tokens, and APIs bill per token",
                "Looping switches the model to a more expensive premium tier",
                "Loops are charged per minute of wall-clock time",
            ],
            "answer_index": 0,
            "explanation": "Providers bill separately for input and output tokens, so an agent that loops burns tokens on every pass.",
        },
        {
            "id": "m15-tok-seam3",
            "prompt": "An app's answers keep stopping mid-sentence. Based on this lesson, what is the likely cause?",
            "options": [
                "The context window has been permanently used up",
                "`max_tokens` is set too low, cutting the reply off as it generates",
                "The tokenizer failed and dropped the rest of the text",
            ],
            "answer_index": 1,
            "explanation": "Hitting `max_tokens` mid-sentence produces a cut-off answer — a common bug when app limits are set too low.",
        },
    ],
    "training-vs-inference": [
        {
            "id": "m15-ti-seam1",
            "prompt": "According to the two-phase table, who performs training and how often?",
            "options": [
                "You, every time you send a prompt",
                "Labs with massive GPU clusters, once per model version",
                "The app you are using, once per conversation",
            ],
            "answer_index": 1,
            "explanation": "Training happens over weeks or months, once per model version, at labs with massive GPU clusters. You almost always work in inference.",
        },
        {
            "id": "m15-ti-seam2",
            "prompt": "You paste confidential notes into a chat for one session. Does that put them into the model's weights?",
            "options": [
                "No — pasting notes for one session is explicitly not training",
                "Yes, anything you send is absorbed into the weights permanently",
                "Only if the conversation lasts longer than the context window",
            ],
            "answer_index": 0,
            "explanation": "The lesson is explicit: training is not what happens when you paste notes for one session, and one chat does not store your secrets inside the weights.",
        },
        {
            "id": "m15-ti-seam3",
            "prompt": "During inference the model outputs a probability distribution over the next token. What happens immediately after that?",
            "options": [
                "The weights are nudged so the model improves for next time",
                "One token is chosen — with some randomness unless temperature is 0",
                "The whole reply is written at once from the distribution",
            ],
            "answer_index": 1,
            "explanation": "One token is chosen (with randomness unless temperature is 0), then the loop repeats until the reply is complete. No weights change.",
        },
        {
            "id": "m15-ti-seam4",
            "prompt": "Why does this lesson say hallucinations 'make sense'?",
            "options": [
                "Because inference predicts plausible text rather than retrieving verified facts",
                "Because the model deliberately invents answers to seem confident",
                "Because the context window is always too small to hold the truth",
            ],
            "answer_index": 0,
            "explanation": "Inference predicts plausible text; it is not reading a verified fact table unless you give it one — which is why agents add memory, databases, or RAG.",
        },
    ],
}


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
# Module 3 seam checks (plan §0.2). One per gap between reading beats, each
# answerable from the beat immediately before it. Scenario-shaped where the
# MODULE_3_RECAP bank is definitional.
MODULE_3_SEAM_CHECKS = {
    "what-prompts-are": [
        {
            "id": "m3-wpa-seam1",
            "prompt": "Your prompt says \"summarize this\" and nothing else. Which of the four parts of a prompt is most clearly missing?",
            "options": [
                "Output format — nothing says bullets, JSON, length, or tone",
                "Instruction — there is no verb telling the model what to do",
                "The model name, which every prompt must include",
            ],
            "answer_index": 0,
            "explanation": "The instruction is present (summarize). Context, examples, and especially output format are what is missing — the lesson's rule is more signal, less guesswork.",
        },
    ],
    "how-context-affects-responses": [
        {
            "id": "m3-ctx-seam1",
            "prompt": "You ask \"Should we ship this feature?\" twice — once with just the feature name, once with the full PRD, deadline, and team size. What changes?",
            "options": [
                "Nothing, because the question string is identical both times",
                "The answer shifts from generic pros and cons to trade-offs tied to your project",
                "The model retrains itself on the PRD before answering",
            ],
            "answer_index": 1,
            "explanation": "The question string did not change — the surrounding information did. Context steers the angle of the answer.",
        },
    ],
    "system-vs-user-prompts": [
        {
            "id": "m3-sys-seam1",
            "prompt": "Which instruction belongs in the system prompt rather than the user prompt?",
            "options": [
                "\"Draft a reply to the email below.\"",
                "\"Reply only in valid JSON matching this schema.\"",
                "\"Explain recursion like I'm 12.\"",
            ],
            "answer_index": 1,
            "explanation": "System prompts carry behaviour that should stay stable across the whole session. The other two are this-turn requests, so they are user prompts.",
        },
        {
            "id": "m3-sys-seam2",
            "prompt": "The lesson lists three common mistakes with roles. Which one is a mistake?",
            "options": [
                "Putting a long one-off document in the system prompt instead of user context",
                "Keeping persona and formatting rules in the system prompt",
                "Sending a different user prompt on every turn",
            ],
            "answer_index": 0,
            "explanation": "Long one-off documents belong in user context. The other two are exactly how the split is supposed to work.",
        },
    ],
    "good-and-bad-prompts": [
        {
            "id": "m3-gbp-seam1",
            "prompt": "\"Be brief\" and \"Write 1000 words\" in the same prompt. Which bad pattern is that, and what does the model do?",
            "options": [
                "Assumed context — the model cannot see your files",
                "Contradictory instructions — the model picks one arbitrarily",
                "Overloaded ask — the tasks should be split up",
            ],
            "answer_index": 1,
            "explanation": "Contradictory instructions leave the model to pick one arbitrarily. Assumed context and overloaded asks are separate bad patterns in the same table.",
        },
        {
            "id": "m3-gbp-seam2",
            "prompt": "In CRAFT, which letter covers \"return bullets, max 5 items\"?",
            "options": [
                "A for Action — it is part of the task",
                "F for Format — how the answer should look",
                "T for Tone — it constrains the writing",
            ],
            "answer_index": 1,
            "explanation": "Format is bullets, JSON, table, or max length. Action is the verb; Tone is formality and constraints like \"no invented citations\".",
        },
    ],
    "hands-on-prompt-exercises": [
        {
            "id": "m3-hop-seam1",
            "prompt": "On the five-row rubric, which rows does Prompt B (\"...8 bullet points for exam review, define mitosis and meiosis in one line each\") clearly beat \"Notes on chapter 4\"?",
            "options": [
                "Context, Specificity, and Format",
                "Only Clarity, since both name a chapter",
                "None — rubric scores apply to models, not prompts",
            ],
            "answer_index": 0,
            "explanation": "Prompt B should win on Context, Specificity, and Format — it names the subject, the audience, the count, and the shape of the answer.",
        },
        {
            "id": "m3-hop-seam2",
            "prompt": "In the context experiment you send \"What should we do next?\" twice — once bare, once prefixed with team size, sprint deadline, and the CI blocker. What does the gap between the two answers demonstrate?",
            "options": [
                "That the second run used a smarter model",
                "Context at work — the same question gets a far more specific answer",
                "That short prompts are always wrong",
            ],
            "answer_index": 1,
            "explanation": "Same fixed question, same model — only the context changed. The lesson calls that gap \"context at work\".",
        },
        {
            "id": "m3-hop-seam3",
            "prompt": "Your reply ignores the format you asked for. According to the self-check, what do you do first?",
            "options": [
                "Switch to a different model",
                "Iterate the prompt before blaming the model",
                "Send the same prompt again unchanged",
            ],
            "answer_index": 1,
            "explanation": "If the response misses the format, constraints, context, or audience you named, iterate the prompt first — improving context and constraints beats changing models.",
        },
    ],
}


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
        "title": "Module 1: Introduction to AI",
        "slug": "module-1-introduction-to-ai",
        "description": "What AI and LLMs are, other major AI categories, a brief history, and an exam.",
        "published": True,
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
        "published": True,
        "difficulty": 1,
        "lessons": [
            (
                "Context Windows",
                "context-windows",
                "theory",
                8,
                {
                    "questions": MODULE_1_5_RECAP["context-windows"],
                    "checkpoint_questions": MODULE_1_5_SEAM_CHECKS["context-windows"],
                    "video_url": MODULE_1_5_CONTEXT_VIDEO_URL,
                    "video_title": "Context management in Claude Code",
                    "video_position": MODULE_1_5_VIDEO_POSITION,
                    # Supplementary, so it does NOT gate the recap quiz. Module 1's
                    # videos ARE the lesson and require full playback; here the
                    # prose carries the teaching and the video shows an example,
                    # so locking the assessment behind it would gate the lesson on
                    # material that is not the lesson.
                    "require_full_watch": False,
                },
            ),
            (
                "Tokens",
                "tokens",
                "theory",
                8,
                {
                    "questions": MODULE_1_5_RECAP["tokens"],
                    "checkpoint_questions": MODULE_1_5_SEAM_CHECKS["tokens"],
                    "video_url": MODULE_1_5_TOKENS_VIDEO_URL,
                    "video_position": MODULE_1_5_VIDEO_POSITION,
                    # Supplementary, like the context-windows video: the prose
                    # teaches tokens, so the recap quiz is not gated on playback.
                    "require_full_watch": False,
                    "video_title": "What is an AI Token?",
                },
            ),
            (
                "Training vs Inference",
                "training-vs-inference",
                "theory",
                10,
                {
                    "questions": MODULE_1_5_RECAP["training-vs-inference"],
                    "checkpoint_questions": MODULE_1_5_SEAM_CHECKS["training-vs-inference"],
                    "video_url": MODULE_1_5_TRAINING_VIDEO_URL,
                    "video_title": "AI Training vs Inference Explained",
                    "video_position": MODULE_1_5_VIDEO_POSITION,
                    # Supplementary, like the module's other two: the prose
                    # teaches the distinction, so the quiz is not gated on it.
                    "require_full_watch": False,
                },
            ),
            ("Module 1.5 Exam", "module-1-5-exam", "quiz", 10, {"questions": MODULE_1_5_EXAM_QUESTIONS}),
        ],
    },
    {
        "order": 3,
        "title": "Module 2: Exploring LLM Models",
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
        "title": "Module 3: Prompting",
        "slug": "module-3-prompting",
        "description": "What prompts are, how context shapes responses, system vs user prompts, and hands-on practice.",
        "published": True,
        "difficulty": 1,
        "lessons": [
            ("What Prompts Are", "what-prompts-are", "theory", 8, {
                    "questions": MODULE_3_RECAP["what-prompts-are"],
                    "checkpoint_questions": MODULE_3_SEAM_CHECKS["what-prompts-are"],
                }),
            ("How Context Affects Responses", "how-context-affects-responses", "theory", 10, {
                    "questions": MODULE_3_RECAP["how-context-affects-responses"],
                    "checkpoint_questions": MODULE_3_SEAM_CHECKS["how-context-affects-responses"],
                }),
            ("System Prompts vs User Prompts", "system-vs-user-prompts", "theory", 10, {
                    "questions": MODULE_3_RECAP["system-vs-user-prompts"],
                    "checkpoint_questions": MODULE_3_SEAM_CHECKS["system-vs-user-prompts"],
                }),
            ("Good and Bad Prompts", "good-and-bad-prompts", "theory", 10, {
                    "questions": MODULE_3_RECAP["good-and-bad-prompts"],
                    "checkpoint_questions": MODULE_3_SEAM_CHECKS["good-and-bad-prompts"],
                }),
            ("Hands-on Prompt Exercises", "hands-on-prompt-exercises", "interactive", 15, {
                    "questions": MODULE_3_RECAP["hands-on-prompt-exercises"],
                    "checkpoint_questions": MODULE_3_SEAM_CHECKS["hands-on-prompt-exercises"],
                }),
            ("Module 3 Exam", "module-3-exam", "quiz", 10, {"questions": MODULE_3_EXAM_QUESTIONS}),
        ],
    },
    _structured_course_entry(
        "module-4-ai-agents",
        extra_lessons=(("Module 4 Exam", "module-4-exam", "quiz", 12, MODULE_4_EXAM),),
    ),
    {
        "order": 6,
        "title": "Module 4.5: Docker and Environments",
        "slug": "module-4-5-docker-and-environments",
        "description": "Why Docker exists, the core terms, installing Docker Desktop, and running your first containers.",
        "published": True,
        "difficulty": 2,
        "lessons": [
            ("Why Docker?", "why-docker", "theory", 8, {
                    "questions": MODULE_4_5_RECAP["why-docker"],
                    "checkpoint_questions": MODULE_4_5_SEAM_CHECKS["why-docker"],
                }),
            ("The Main Terms", "docker-main-terms", "theory", 8, {
                    "questions": MODULE_4_5_RECAP["docker-main-terms"],
                    "checkpoint_questions": MODULE_4_5_SEAM_CHECKS["docker-main-terms"],
                }),
            ("Installing Docker Desktop", "installing-docker-desktop", "interactive", 15, {
                    "questions": MODULE_4_5_RECAP["installing-docker-desktop"],
                    "checkpoint_questions": MODULE_4_5_SEAM_CHECKS["installing-docker-desktop"],
                }),
            ("Your First Containers", "first-containers", "sandbox", 12, {
                    "questions": MODULE_4_5_RECAP["first-containers"],
                    "checkpoint_questions": MODULE_4_5_SEAM_CHECKS["first-containers"],
                }),
            ("Module 4.5 Exam", "module-4-5-exam", "quiz", 10, {"questions": MODULE_4_5_EXAM_QUESTIONS}),
        ],
    },
    {
        "order": 7,
        "title": "Module 5: Hermes (Build #1)",
        "slug": "module-5-hermes",
        "description": "Understand what Hermes is, set up OpenRouter with a spending cap, walk the install wizard into a Docker sandbox, hold your first conversation, and verify the isolation yourself.",
        "published": True,
        "difficulty": 2,
        "lessons": [
            ("What Hermes Is", "what-hermes-is", "theory", 8, {
                    "questions": MODULE_5_RECAP["what-hermes-is"],
                    "checkpoint_questions": MODULE_5_SEAM_CHECKS["what-hermes-is"],
                }),
            ("OpenRouter and Your API Key", "openrouter-and-your-api-key", "interactive", 10, {
                    "questions": MODULE_5_RECAP["openrouter-and-your-api-key"],
                    "checkpoint_questions": MODULE_5_SEAM_CHECKS["openrouter-and-your-api-key"],
                }),
            ("Install and the Setup Wizard", "install-and-setup-wizard", "interactive", 15, {
                    "questions": MODULE_5_RECAP["install-and-setup-wizard"],
                    "checkpoint_questions": MODULE_5_SEAM_CHECKS["install-and-setup-wizard"],
                }),
            ("First Conversation and the Container", "first-conversation-and-container", "sandbox", 15, {
                    "questions": MODULE_5_RECAP["first-conversation-and-container"],
                    "checkpoint_questions": MODULE_5_SEAM_CHECKS["first-conversation-and-container"],
                }),
            ("Sandbox Verification Lab", "sandbox-verification-lab", "sandbox", 12, {
                    "questions": MODULE_5_RECAP["sandbox-verification-lab"],
                    "checkpoint_questions": MODULE_5_SEAM_CHECKS["sandbox-verification-lab"],
                }),
            ("Put It to Work", "put-it-to-work", "agent_lab", 15, {
                    "questions": MODULE_5_RECAP["put-it-to-work"],
                    "checkpoint_questions": MODULE_5_SEAM_CHECKS["put-it-to-work"],
                }),
            ("Module 5 Exam", "module-5-exam", "quiz", 12, {"questions": MODULE_5_EXAM_QUESTIONS}),
        ],
    },
    _structured_course_entry(
        "module-6-openclaw",
        extra_lessons=(("Module 6 Exam", "module-6-exam", "quiz", 10, {"questions": MODULE_6_EXAM_QUESTIONS}),),
    ),
    {
        "order": 9,
        "title": "Module 7: Claude (Build #3)",
        "slug": "module-7-claude",
        "description": "Build an agent with Claude Code — no code required: install it with a spending cap, teach it with CLAUDE.md and skills, create a least-privilege subagent, and assemble a working research notebook agent.",
        "published": True,
        "difficulty": 2,
        "lessons": [
            ("What Claude Code Is", "what-claude-code-is", "theory", 8, {
                    "questions": MODULE_7_RECAP["what-claude-code-is"],
                    "checkpoint_questions": MODULE_7_SEAM_CHECKS["what-claude-code-is"],
                }),
            ("Install and First Session", "install-and-first-session", "interactive", 12, {
                    "questions": MODULE_7_RECAP["install-and-first-session"],
                    "checkpoint_questions": MODULE_7_SEAM_CHECKS["install-and-first-session"],
                }),
            ("CLAUDE.md and Skills", "claudemd-and-skills", "sandbox", 15, {
                    "questions": MODULE_7_RECAP["claudemd-and-skills"],
                    "checkpoint_questions": MODULE_7_SEAM_CHECKS["claudemd-and-skills"],
                }),
            ("Custom Subagents", "custom-subagents", "sandbox", 15, {
                    "questions": MODULE_7_RECAP["custom-subagents"],
                    "checkpoint_questions": MODULE_7_SEAM_CHECKS["custom-subagents"],
                }),
            ("Build Your Agent Lab", "build-your-agent", "agent_lab", 15, {
                    "questions": MODULE_7_RECAP["build-your-agent"],
                    "checkpoint_questions": MODULE_7_SEAM_CHECKS["build-your-agent"],
                }),
            ("Module 7 Exam", "module-7-exam", "quiz", 12, {"questions": MODULE_7_EXAM_QUESTIONS}),
        ],
    },
    _structured_course_entry(
        "module-8-capstone-safety-evaluation",
        extra_lessons=(("Module 8 Exam", "module-8-exam", "quiz", 10, MODULE_8_EXAM),),
    ),
]
