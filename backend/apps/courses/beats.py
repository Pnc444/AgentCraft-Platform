"""Beat model: the lesson player's unit of content.

A lesson is a sequence of beats — one screen, one idea, one action each
(docs/UI-OVERHAUL-PLAN.md §2). Five types, closed set:

    explain  one idea, one analogy or visual
    predict  ask before telling
    check    one question, instant feedback
    do       one real action (closed family: DO_ACTIONS)
    recap    what you now know

Two sources, in priority order:

1. **Authored** — a ``beats`` list in the lesson's sandbox_config. Authored
   beats are held to the §2 rules by :func:`validate_beats`; sync_content
   reports violations (and fails under ``--strict``).
2. **Fallback** — :func:`beats_from_markdown` converts any plain lesson
   (markdown + optional video + recap bank) into beats mechanically. This is
   the migration safety net: every lesson renders in the player from day one.
   Fallback output is deliberately exempt from the authoring rules — it is
   honest-but-ugly, not authored.
"""

from __future__ import annotations

import re
from typing import Any

BEAT_TYPES = ("explain", "predict", "check", "do", "recap")

# The do-beat family is closed (§2.1). A sixth action means deleting one.
DO_ACTIONS = ("video", "terminal", "workbench", "studio", "tutor_try")

MIN_BEATS = 5
MAX_BEATS = 9

_H2_SPLIT = re.compile(r"\n(?=##\s+)")
_H_LINE = re.compile(r"^#{1,6}\s+(.*?)\s*$", re.MULTILINE)


def validate_beats(
    beats: list[dict],
    *,
    artifact_paths: tuple[str, ...] = (),
    lesson_label: str = "lesson",
) -> list[str]:
    """Check authored beats against the §2 rules. Returns problem strings."""
    problems: list[str] = []

    def bad(index: int, message: str) -> None:
        problems.append(f"{lesson_label}: beat {index + 1}: {message}")

    if not isinstance(beats, list) or not all(isinstance(b, dict) for b in beats):
        return [f"{lesson_label}: beats must be a list of objects"]

    if not MIN_BEATS <= len(beats) <= MAX_BEATS:
        problems.append(
            f"{lesson_label}: {len(beats)} beats — a lesson is {MIN_BEATS}-{MAX_BEATS}; "
            "under merges, over splits"
        )

    previous_type = None
    for i, beat in enumerate(beats):
        beat_type = beat.get("type")
        if beat_type not in BEAT_TYPES:
            bad(i, f"unknown type {beat_type!r} (allowed: {', '.join(BEAT_TYPES)})")
            previous_type = None
            continue

        if beat_type == "explain" and previous_type == "explain":
            bad(i, "two explain beats in a row — passive streaks are where attention dies")

        if beat_type == "do":
            action = beat.get("action")
            if action not in DO_ACTIONS:
                bad(i, f"do-beat action {action!r} does not exist (allowed: {', '.join(DO_ACTIONS)})")
            if action == "workbench":
                task_path = (beat.get("task") or {}).get("artifact_path")
                if task_path and task_path not in artifact_paths:
                    bad(i, f"workbench task references {task_path!r}, not in this lesson's artifact bundle")

        if beat_type == "check":
            question = beat.get("question") or {}
            if not question.get("prompt") or not question.get("options"):
                bad(i, "check beat needs a question with prompt and options")

        previous_type = beat_type

    if len(beats) >= 2 and beats[1].get("type") != "predict":
        problems.append(
            f"{lesson_label}: beat 2 must be a predict — learners act before they read"
        )

    return problems


def explain_streak_problems(beats: list[dict], *, lesson_label: str = "lesson") -> list[str]:
    """Report runs of 2+ consecutive `explain` beats.

    Split out from :func:`validate_beats` so derived lessons can be held to the
    passive-streak rule without also being held to the beat-count budget —
    trimming a shipped lesson to 5-9 beats is content work, but a 10-beat wall
    of reading is a defect either way.
    """
    problems: list[str] = []
    run_start = -1
    run = 0
    for i, beat in enumerate(beats + [{"type": "_end"}]):
        if beat.get("type") == "explain":
            if run == 0:
                run_start = i
            run += 1
            continue
        if run >= 2:
            problems.append(
                f"{lesson_label}: beats {run_start + 1}-{run_start + run}: "
                f"{run} explain beats in a row — passive streaks are where attention dies"
            )
        run = 0
    return problems


def _strip_leading_title(content: str, title: str) -> str:
    """Drop a leading h1 that repeats the lesson title (mirrors the frontend)."""
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            norm = lambda s: re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()  # noqa: E731
            if norm(match.group(1)) == norm(title):
                return "\n".join(lines[i + 1 :]).lstrip("\n")
        break
    return content


def _section_title(section: str, fallback: str) -> tuple[str, str]:
    """Pull the leading heading off a section; return (title, body)."""
    match = _H_LINE.match(section.strip())
    if match:
        body = section.strip()[match.end() :].lstrip("\n")
        return match.group(1), body
    return fallback, section.strip()


def beats_from_markdown(
    content: str,
    *,
    title: str = "",
    video_url: str = "",
    questions: list[dict] | None = None,
    sandbox: dict | None = None,
) -> list[dict]:
    """Mechanical markdown → beats conversion (the generic fallback, §3).

    ``##`` sections become explain beats; a video becomes a `do` beat right
    after the first explain; the recap bank trails as check beats. No count
    clamping — fallback is exempt from authoring rules by design.
    """
    body = _strip_leading_title(content or "", title or "")
    beats: list[dict] = []

    sections = [s for s in _H2_SPLIT.split(body) if s.strip()]
    for index, section in enumerate(sections):
        section_title, section_body = _section_title(section, "Read" if index else (title or "Read"))
        if not section_body and not section_title:
            continue
        beats.append(
            {
                "type": "explain",
                "title": section_title,
                "body": section_body,
                "source": "fallback",
            }
        )

    if video_url:
        video_beat = {
            "type": "do",
            "action": "video",
            "title": "Watch the video",
            "video_url": video_url,
            "source": "fallback",
        }
        # After the first explain when there is one; otherwise the video leads.
        beats.insert(1 if beats else 0, video_beat)

    if sandbox:
        # The practice terminal is a real action, not an appendix below the
        # prose — it becomes a do-beat before the checks (plan step 5).
        beats.append(
            {
                "type": "do",
                "action": "terminal",
                "title": str(sandbox.get("title") or "Practice it"),
                "source": "fallback",
            }
        )

    for question in questions or []:
        if not isinstance(question, dict) or not question.get("prompt"):
            continue
        beats.append(
            {
                "type": "check",
                "title": "Check yourself",
                "question": question,
                "source": "fallback",
            }
        )

    return beats


def beats_from_guided_blocks(
    blocks: list[dict],
    *,
    checkpoint_questions: list[dict] | None = None,
    title: str = "",
    lesson_artifact_paths: tuple[str, ...] = (),
) -> list[dict]:
    """Mechanical guided-blocks → beats mapping (plan step 1).

    The structured modules were authored as beats before the player existed:
    ``predict_first`` is a predict beat, a block body is an explain beat, a
    ``checkpoint_after`` flag pulls one question from the checkpoint bank as a
    check beat, and the blocks' ``remember`` lines fold into one closing recap.
    """
    beats: list[dict] = []
    bank = [
        q for q in (checkpoint_questions or [])
        if isinstance(q, dict) and q.get("prompt") and q.get("options")
    ]
    bank_cursor = 0
    remember_lines: list[str] = []
    produced_workbench = False

    # Blocks whose try_this points at a practice file ("open the card below")
    # while declaring no artifact_paths. The stacked page rendered the lesson's
    # artifacts alongside everything else, so the reference resolved by accident;
    # one-beat-per-screen breaks that, and the instruction becomes a lie. The
    # first such block adopts the lesson's bundle so the file it names is on the
    # very same screen.
    adopting_index = -1
    if lesson_artifact_paths and not any(
        isinstance(b, dict) and (b.get("artifact_paths") or b.get("interactive_widget"))
        for b in blocks
    ):
        for i, b in enumerate(blocks):
            if isinstance(b, dict) and b.get("try_this"):
                adopting_index = i
                break

    for block_index, block in enumerate(blocks):
        if not isinstance(block, dict):
            continue
        # A block that points at real files becomes two beats: its idea, then a
        # workbench do-beat where the learner opens (and safely edits) those
        # files for real (plan §4). The block's try_this lines are the task
        # instructions there, not reading-side decoration.
        artifact_paths = block.get("artifact_paths") or []
        adopts_bundle = block_index == adopting_index
        opens_files = (
            bool(artifact_paths)
            or block.get("interactive_widget") == "openclaw_file_explorer"
            or adopts_bundle
        )
        common = {
            "title": block.get("title") or title,
            "body": block.get("body") or "",
            "analogy": block.get("analogy") or "",
            "try_this": [] if opens_files else (block.get("try_this") or []),
            "kind": block.get("kind") or "",
            "source": "blocks",
        }
        predict = block.get("predict_first") or {}
        if predict.get("question"):
            beats.append(
                {
                    "type": "predict",
                    "question": predict["question"],
                    "hint": predict.get("hint") or "",
                    **common,
                }
            )
        else:
            beats.append({"type": "explain", **common})

        if opens_files:
            produced_workbench = True
            beats.append(
                {
                    "type": "do",
                    "action": "workbench",
                    "title": block.get("title") or "Open the files",
                    # Empty means "the whole bundle" — the widget block maps the home.
                    "artifact_paths": artifact_paths,
                    "instructions": block.get("try_this") or [],
                    "source": "blocks",
                }
            )

        if block.get("interactive_widget") == "capstone_studio":
            beats.append(
                {
                    "type": "do",
                    "action": "studio",
                    "title": block.get("title") or "Capstone studio",
                    "instructions": block.get("try_this") or [],
                    "source": "blocks",
                }
            )

        if block.get("checkpoint_after") and bank:
            question = bank[bank_cursor % len(bank)]
            bank_cursor += 1
            beats.append(
                {"type": "check", "title": "Checkpoint", "question": question, "source": "blocks"}
            )

        if block.get("remember"):
            remember_lines.append(block["remember"])

    if lesson_artifact_paths and not produced_workbench:
        beats.append(
            {
                "type": "do",
                "action": "workbench",
                "title": "The practice file",
                "artifact_paths": [],
                "instructions": [],
                "source": "blocks",
            }
        )

    if remember_lines:
        beats.append(
            {
                "type": "recap",
                "title": "Remember this",
                "bullets": remember_lines[:3],
                "source": "blocks",
            }
        )
    return beats


def derive_beats(
    *,
    content: str,
    sandbox_config: dict[str, Any] | None,
    video_url: str = "",
    title: str = "",
) -> list[dict]:
    """The player's single entry point: authored beats, else fallback."""
    config = sandbox_config or {}
    authored = config.get("beats")
    if isinstance(authored, list) and authored:
        return authored
    blocks = config.get("guided_blocks")
    if isinstance(blocks, list) and blocks:
        bundle = config.get("artifact_bundle") or []
        mapped = beats_from_guided_blocks(
            blocks,
            checkpoint_questions=config.get("checkpoint_questions"),
            title=title,
            lesson_artifact_paths=tuple(
                a["path"] for a in bundle if isinstance(a, dict) and a.get("path")
            ),
        )
        if mapped:
            return mapped
    questions = config.get("questions")
    sandbox = config.get("sandbox")
    return beats_from_markdown(
        content,
        title=title,
        video_url=(video_url or "").strip(),
        questions=questions if isinstance(questions, list) else None,
        sandbox=sandbox if isinstance(sandbox, dict) else None,
    )
