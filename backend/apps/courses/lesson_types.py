"""What a lesson type actually promises, and whether a lesson delivers it.

`lesson_type` used to be decoration. `theory`, `interactive`, and `agent_lab`
rendered identically, so a learner reading the badge "interactive" got prose,
and "agent lab" — which sounds like the best part of the course — was the same
page again. Three labels, one experience.

Two changes fix that:

1. Each type owns a promise and states what a lesson must ship to keep it.
2. The label is computed from what the lesson *actually contains*, so a lesson
   that under-delivers is described honestly instead of advertising something
   it does not have.

Computed here rather than in the client because the course list only receives a
lesson summary, and a badge must not depend on which endpoint you came from.
The label upgrades on its own the moment the missing content is authored.
"""

from __future__ import annotations

# type -> (label, promise, requirement)
LESSON_TYPE_PROMISES: dict[str, tuple[str, str, str]] = {
    "theory": ("Read", "A short read, then a recap quiz.", "nothing"),
    "interactive": (
        "Interactive",
        "You'll answer or try something inside the lesson.",
        "interaction",
    ),
    "sandbox": (
        "Practice",
        "A practice terminal where you run the real commands.",
        "sandbox",
    ),
    "agent_lab": ("Build", "You'll build and submit something you can keep.", "assignment"),
    "quiz": ("Exam", "Covers the whole module.", "quiz"),
}

FALLBACK = LESSON_TYPE_PROMISES["theory"]


def _capabilities(lesson) -> dict[str, bool]:
    config = lesson.sandbox_config or {}
    sandbox = config.get("sandbox") or {}
    assignment = config.get("capstone_assignment") or None
    blocks = config.get("guided_blocks") or []
    return {
        "sandbox": bool(isinstance(sandbox, dict) and sandbox.get("tasks")),
        "assignment": bool(assignment),
        "interaction": bool(blocks) or bool(config.get("checkpoint_questions")),
    }


def delivers_promise(lesson) -> bool:
    """True when the lesson contains what its declared type advertises."""
    _, _, requirement = LESSON_TYPE_PROMISES.get(lesson.lesson_type, FALLBACK)
    caps = _capabilities(lesson)
    if requirement == "sandbox":
        return caps["sandbox"]
    if requirement == "assignment":
        return caps["assignment"]
    if requirement == "interaction":
        return caps["interaction"] or caps["sandbox"] or caps["assignment"]
    return True


def type_label(lesson) -> str:
    """Badge text that stays true even when the lesson under-delivers."""
    label, _, _ = LESSON_TYPE_PROMISES.get(lesson.lesson_type, FALLBACK)
    return label if delivers_promise(lesson) else FALLBACK[0]


def type_promise(lesson) -> str:
    _, promise, _ = LESSON_TYPE_PROMISES.get(lesson.lesson_type, FALLBACK)
    return promise if delivers_promise(lesson) else FALLBACK[1]
