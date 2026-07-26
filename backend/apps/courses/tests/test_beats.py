"""Beat schema, validator, and generic fallback (plan §2, §3, §7)."""

from apps.courses.beats import beats_from_markdown, derive_beats, validate_beats

GOOD_BEATS = [
    {"type": "explain", "title": "One idea", "body": "Short."},
    {"type": "predict", "title": "Think first", "question": {"prompt": "What would you do?"}},
    {"type": "check", "question": {"prompt": "Which?", "options": ["a", "b"], "answer_index": 0}},
    {"type": "do", "action": "terminal", "title": "Run it"},
    {"type": "recap", "bullets": ["You learned a thing."]},
]


def test_valid_authored_beats_pass():
    assert validate_beats(GOOD_BEATS) == []


def test_beat_count_bounds():
    assert any("4 beats" in p for p in validate_beats(GOOD_BEATS[:4]))
    ten = GOOD_BEATS + [{"type": "check", "question": {"prompt": "x", "options": ["a"]}}] * 5
    assert any("10 beats" in p for p in validate_beats(ten))


def test_unknown_beat_type_and_unknown_do_action_are_named():
    beats = [dict(b) for b in GOOD_BEATS]
    beats[3] = {"type": "do", "action": "hologram"}
    problems = validate_beats(beats)
    assert any("'hologram' does not exist" in p for p in problems)

    beats[3] = {"type": "quiz"}
    assert any("unknown type 'quiz'" in p for p in validate_beats(beats))


def test_beat_two_must_be_predict():
    beats = [GOOD_BEATS[0], GOOD_BEATS[2], GOOD_BEATS[1], GOOD_BEATS[3], GOOD_BEATS[4]]
    assert any("beat 2 must be a predict" in p for p in validate_beats(beats))


def test_consecutive_explains_flagged():
    beats = [
        GOOD_BEATS[0],
        GOOD_BEATS[1],
        {"type": "explain", "body": "more"},
        {"type": "explain", "body": "and more"},
        GOOD_BEATS[4],
    ]
    assert any("two explain beats in a row" in p for p in validate_beats(beats))


def test_workbench_task_must_reference_bundled_artifact():
    beats = [dict(b) for b in GOOD_BEATS]
    beats[3] = {"type": "do", "action": "workbench", "task": {"artifact_path": "nope.md"}}
    problems = validate_beats(beats, artifact_paths=("lesson_artifacts/openclaw/SOUL.md",))
    assert any("'nope.md'" in p for p in problems)
    beats[3]["task"]["artifact_path"] = "lesson_artifacts/openclaw/SOUL.md"
    assert validate_beats(beats, artifact_paths=("lesson_artifacts/openclaw/SOUL.md",)) == []


MD = """# Your First Containers

Time to actually run something.

## 1. Hello, world

Run the thing.

## 2. A real web server

Run nginx.
"""


def test_fallback_splits_sections_and_appends_checks():
    questions = [{"prompt": "Q1?", "options": ["a", "b"], "answer_index": 0}]
    beats = beats_from_markdown(MD, title="Your First Containers", questions=questions)
    types = [b["type"] for b in beats]
    assert types == ["explain", "explain", "explain", "check"]
    # the duplicate leading h1 is stripped, intro becomes the first explain
    assert "Time to actually run something." in beats[0]["body"]
    assert beats[1]["title"] == "1. Hello, world"
    assert all(b["source"] == "fallback" for b in beats)


def test_fallback_places_video_after_first_explain():
    beats = beats_from_markdown(MD, title="Your First Containers", video_url="https://v.example/x")
    assert beats[1] == {
        "type": "do",
        "action": "video",
        "title": "Watch the video",
        "video_url": "https://v.example/x",
        "source": "fallback",
    }


def test_fallback_video_leads_when_there_is_no_prose():
    beats = beats_from_markdown("", title="Stub", video_url="https://v.example/x")
    assert beats[0]["action"] == "video"


def test_derive_prefers_authored_beats():
    config = {"beats": GOOD_BEATS, "questions": [{"prompt": "ignored", "options": ["a"]}]}
    assert derive_beats(content=MD, sandbox_config=config, title="t") == GOOD_BEATS


def test_derive_falls_back_for_plain_lessons():
    beats = derive_beats(content=MD, sandbox_config={}, title="Your First Containers")
    assert beats and beats[0]["type"] == "explain"


BLOCKS = [
    {"title": "One helper", "body": "Meet Juno.", "predict_first": {"question": "What would a friend do?", "hint": "Think steps."}, "remember": "Agents act."},
    {"title": "The map", "body": "Six questions.", "analogy": "A checklist.", "checkpoint_after": True},
    {"title": "Tools", "body": "Search and read.", "try_this": ["Open the map."]},
]
CHECKPOINTS = [{"prompt": "Which question?", "options": ["goal", "vibes"], "answer_index": 0}]


def test_blocks_map_to_beats_mechanically():
    from apps.courses.beats import beats_from_guided_blocks

    beats = beats_from_guided_blocks(BLOCKS, checkpoint_questions=CHECKPOINTS, title="T")
    types = [b["type"] for b in beats]
    assert types == ["predict", "explain", "check", "explain", "recap"]
    assert beats[0]["question"] == "What would a friend do?"
    assert beats[2]["question"]["prompt"] == "Which question?"
    assert beats[4]["bullets"] == ["Agents act."]


def test_derive_prefers_blocks_over_markdown():
    config = {"guided_blocks": BLOCKS, "checkpoint_questions": CHECKPOINTS, "questions": [{"prompt": "recap q", "options": ["a"]}]}
    beats = derive_beats(content=MD, sandbox_config=config, title="T")
    assert beats[0]["source"] == "blocks"
    assert all(b["type"] != "explain" or "Hello, world" not in b.get("title", "") for b in beats)


def test_module_4_exam_meets_the_authoring_standard():
    """Plan §6: 12 items, none recycled from any Module 4 recap bank, every
    item explains itself. This is the standard the other eight banks follow."""
    from apps.courses.curriculum import CURRICULUM, MODULE_4_EXAM_QUESTIONS
    from apps.courses.management.commands.sync_content import _module_assessment_problems

    assert len(MODULE_4_EXAM_QUESTIONS) == 12
    assert all(q.get("explanation") for q in MODULE_4_EXAM_QUESTIONS)
    ids = [q["id"] for q in MODULE_4_EXAM_QUESTIONS]
    assert len(set(ids)) == 12

    module = next(m for m in CURRICULUM if m["slug"] == "module-4-ai-agents")
    assert module["lessons"][-1][2] == "quiz", "the exam must be the module's last lesson"
    problems = _module_assessment_problems(module)
    assert problems == [], f"validator flags module 4: {problems}"


def test_blocks_with_artifacts_emit_workbench_beats():
    from apps.courses.beats import beats_from_guided_blocks

    blocks = [
        {"title": "Idea", "body": "Read.", "predict_first": {"question": "Q?"}},
        {
            "title": "The routing rule",
            "body": "Two files.",
            "try_this": ["Open SOUL.md", "Find the name line"],
            "artifact_paths": ["a/SOUL.md", "a/openclaw.json"],
        },
        {"title": "Map", "body": "The home.", "interactive_widget": "openclaw_file_explorer"},
    ]
    beats = beats_from_guided_blocks(blocks, title="T")
    types = [(b["type"], b.get("action")) for b in beats]
    assert types == [
        ("predict", None),
        ("explain", None),
        ("do", "workbench"),
        ("explain", None),
        ("do", "workbench"),
    ]
    wb = beats[2]
    assert wb["artifact_paths"] == ["a/SOUL.md", "a/openclaw.json"]
    assert wb["instructions"] == ["Open SOUL.md", "Find the name line"]
    # try_this moved onto the workbench beat, not duplicated on the explain
    assert beats[1]["try_this"] == []
    # the explorer-widget block gets the whole bundle (empty = all)
    assert beats[4]["artifact_paths"] == []


def test_capstone_studio_block_emits_studio_beat():
    from apps.courses.beats import beats_from_guided_blocks

    blocks = [{"title": "Run it", "body": "Apply.", "interactive_widget": "capstone_studio", "try_this": ["Verify one case"]}]
    beats = beats_from_guided_blocks(blocks, title="T")
    assert [(b["type"], b.get("action")) for b in beats] == [("explain", None), ("do", "studio")]
    assert beats[1]["instructions"] == ["Verify one case"]


def test_module_8_exam_meets_the_authoring_standard():
    from apps.courses.curriculum import CURRICULUM, MODULE_8_EXAM_QUESTIONS
    from apps.courses.management.commands.sync_content import _module_assessment_problems

    assert len(MODULE_8_EXAM_QUESTIONS) == 8
    assert all(q.get("explanation") for q in MODULE_8_EXAM_QUESTIONS)
    module = next(m for m in CURRICULUM if m["slug"] == "module-8-capstone-safety-evaluation")
    assert module["lessons"][-1][2] == "quiz"
    assert _module_assessment_problems(module) == []


def test_fallback_emits_terminal_beat_for_sandbox_lessons():
    beats = beats_from_markdown(MD, title="T", questions=[{"prompt": "q", "options": ["a"]}], sandbox={"title": "Practice It", "tasks": []})
    types = [(b["type"], b.get("action")) for b in beats]
    assert ("do", "terminal") in types
    # terminal sits after the prose, before the checks
    assert types.index(("do", "terminal")) < types.index(("check", None))


def test_every_published_module_passes_assessment_validation():
    """Plan §6 complete: every published module has an exam and no exam
    recycles its recap bank. Module 2 is exempt by directive."""
    from apps.courses.curriculum import CURRICULUM
    from apps.courses.management.commands.sync_content import (
        VALIDATION_EXEMPT_SLUGS,
        _module_assessment_problems,
    )

    for module in CURRICULUM:
        if module["slug"] in VALIDATION_EXEMPT_SLUGS:
            continue
        assert _module_assessment_problems(module) == [], module["slug"]


def test_orphaned_artifacts_become_reachable_and_carry_their_instruction():
    """A block saying 'open the card below' with no artifact_paths used to
    resolve by accident on the stacked page. One-beat-per-screen orphaned the
    file and turned the instruction into a lie (FAKE)."""
    from apps.courses.beats import beats_from_guided_blocks

    blocks = [
        {"title": "Who carries the doubt?", "body": "Ask.", "predict_first": {"question": "Q?"}},
        {"title": "Three ways to stop", "body": "Goal met.", "try_this": ["Open the card below and read the three stop rules once."]},
        {"title": "Trap", "body": "One more search.", "remember": "Stop rules exist."},
    ]
    beats = beats_from_guided_blocks(
        blocks, title="T", lesson_artifact_paths=("lesson_artifacts/agents/stop-rules-and-checks.md",)
    )
    types = [(b["type"], b.get("action")) for b in beats]
    assert ("do", "workbench") in types, "the lesson's artifact must be reachable"

    wb = next(b for b in beats if b.get("action") == "workbench")
    # The instruction rides WITH the file it names, so "the card below" is true.
    assert wb["instructions"] == ["Open the card below and read the three stop rules once."]
    # And it is not also left on the explain beat.
    assert beats[types.index(("do", "workbench")) - 1]["try_this"] == []


def test_artifacts_reachable_even_when_no_block_has_try_this():
    from apps.courses.beats import beats_from_guided_blocks

    blocks = [{"title": "A", "body": "x", "predict_first": {"question": "Q?"}}, {"title": "B", "body": "y"}]
    beats = beats_from_guided_blocks(blocks, title="T", lesson_artifact_paths=("a/f.md",))
    assert any(b.get("action") == "workbench" for b in beats)


def test_no_workbench_invented_when_lesson_has_no_artifacts():
    from apps.courses.beats import beats_from_guided_blocks

    blocks = [{"title": "A", "body": "x", "try_this": ["Say it out loud."]}]
    beats = beats_from_guided_blocks(blocks, title="T", lesson_artifact_paths=())
    assert not any(b.get("action") == "workbench" for b in beats)
    # try_this stays where it was — there is no file to move it to.
    assert beats[0]["try_this"] == ["Say it out loud."]
