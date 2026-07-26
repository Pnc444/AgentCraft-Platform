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


def test_fallback_merges_short_sections_and_never_recycles_the_recap_bank():
    """Three short sections are one screen, not three; and the recap bank stays
    with the recap quiz — appending it here made learners answer the identical
    questions twice in a row."""
    questions = [{"prompt": "Q1?", "options": ["a", "b"], "answer_index": 0}]
    beats = beats_from_markdown(MD, title="Your First Containers", questions=questions)
    assert [b["type"] for b in beats] == ["explain"]
    # nothing is discarded: absorbed headings survive inside the body
    body = beats[0]["body"]
    assert "Time to actually run something." in body
    assert "## 1. Hello, world" in body
    assert "## 2. A real web server" in body
    assert "Run nginx." in body
    # the recap question is NOT duplicated into the lesson
    assert not any(b["type"] == "check" for b in beats)


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
    beats = beats_from_markdown(MD, title="T", sandbox={"title": "Practice It", "tasks": []})
    types = [(b["type"], b.get("action")) for b in beats]
    assert ("do", "terminal") in types
    # the practice terminal is the lesson's last beat, after the reading
    assert types[-1] == ("do", "terminal")


def test_two_long_sections_never_merge_into_one_wall():
    """Merging is for short sections. Two substantial ones stay two screens —
    otherwise the fix would just rebuild the wall inside a single beat."""
    long_md = "Intro.\n\n## A\n\n" + ("x" * 700) + "\n\n## B\n\n" + ("y" * 700)
    beats = beats_from_markdown(long_md, title="T")
    # the 6-char intro folds into A (706 <= limit); A and B do not (1406 > limit)
    assert [b["type"] for b in beats] == ["explain", "explain"]
    assert "Intro." in beats[0]["body"] and "## A" in beats[0]["body"]
    assert beats[1]["title"] == "B"
    assert "x" * 700 not in beats[1]["body"]


def test_distribute_checks_never_reuses_a_question_already_asked():
    from apps.courses.beats import distribute_checks

    q = {"prompt": "Already asked?", "options": ["a", "b"], "answer_index": 0}
    beats = [
        {"type": "check", "question": q},
        {"type": "explain", "body": "one"},
        {"type": "explain", "body": "two"},
    ]
    out = distribute_checks(beats, [q])
    assert [b["type"] for b in out] == ["check", "explain", "explain"]


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


import pytest


@pytest.mark.parametrize(
    ("course_slug", "recap_name", "seam_name"),
    [
        ("module-1-5-how-llms-work", "MODULE_1_5_RECAP", "MODULE_1_5_SEAM_CHECKS"),
        ("module-3-prompting", "MODULE_3_RECAP", "MODULE_3_SEAM_CHECKS"),
        ("module-4-5-docker-and-environments", "MODULE_4_5_RECAP", "MODULE_4_5_SEAM_CHECKS"),
        ("module-7-claude", "MODULE_7_RECAP", "MODULE_7_SEAM_CHECKS"),
        ("module-5-hermes", "MODULE_5_RECAP", "MODULE_5_SEAM_CHECKS"),
    ],
)
def test_seam_checks_close_every_reading_run_without_recycling(course_slug, recap_name, seam_name):
    """Plan §0.2: authored seam checks break every reading run, and none of them
    repeats a question the recap quiz already asks."""
    from apps.courses import curriculum
    from apps.courses.beats import derive_beats

    recap = getattr(curriculum, recap_name)
    seams = getattr(curriculum, seam_name)
    recap_prompts = {q["prompt"] for bank in recap.values() for q in bank}

    for slug, questions in seams.items():
        for q in questions:
            assert q["prompt"] not in recap_prompts, f"{slug}: recycles a recap question"
            assert q.get("explanation"), f"{slug}: seam check needs an explanation"
            assert q.get("id"), f"{slug}: seam check needs an id"
            assert 0 <= q["answer_index"] < len(q["options"])

        beats = derive_beats(
            content=curriculum.load_content(course_slug, slug, slug),
            sandbox_config={"questions": recap[slug], "checkpoint_questions": questions},
            title=slug,
        )
        run = worst = 0
        for beat in beats:
            run = run + 1 if beat["type"] == "explain" else 0
            worst = max(worst, run)
        assert worst == 1, f"{course_slug}/{slug}: still has a reading run of {worst}"

        asked = [
            (b.get("question") or {}).get("prompt")
            for b in beats
            if b["type"] == "check"
        ]
        assert len(asked) == len(set(asked)), f"{slug}: asks the same question twice"


def test_seam_check_ids_are_unique_across_the_course():
    from apps.courses import curriculum

    ids = [
        q["id"]
        for name in ("MODULE_1_5_SEAM_CHECKS", "MODULE_3_SEAM_CHECKS", "MODULE_4_5_SEAM_CHECKS", "MODULE_5_SEAM_CHECKS", "MODULE_7_SEAM_CHECKS")
        for bank in getattr(curriculum, name).values()
        for q in bank
    ]
    assert len(ids) == len(set(ids))


def test_required_video_leads_and_supplementary_video_trails():
    """Module 1's videos ARE the lesson, so they lead. Module 1.5's Claude Code
    walkthrough is an example of a concept the prose already taught, so it
    follows the reading instead of pre-empting it."""
    required = beats_from_markdown(MD, title="T", video_url="https://v/x", video_required=True)
    assert required[1]["action"] == "video", "a required video leads the lesson"

    supplementary = beats_from_markdown(
        MD, title="T", video_url="https://v/x", video_required=False, video_title="See it in practice"
    )
    assert supplementary[-1]["action"] == "video", "a supplementary video trails the reading"
    assert supplementary[-1]["title"] == "See it in practice"
    # and the generic label is only a fallback
    assert beats_from_markdown(MD, title="T", video_url="https://v/x")[1]["title"] == "Watch the video"


def test_module_1_5_context_lesson_ships_the_video_ungated():
    from apps.courses.curriculum import CURRICULUM, MODULE_1_5_CONTEXT_VIDEO_URL

    module = next(m for m in CURRICULUM if m["slug"] == "module-1-5-how-llms-work")
    spec = next(l for l in module["lessons"] if l[1] == "context-windows")
    config = spec[4]
    assert config["video_url"] == MODULE_1_5_CONTEXT_VIDEO_URL
    assert "?si=" not in config["video_url"], "share tracking param must not be stored"
    # Supplementary: the prose teaches the concept, so the recap quiz is not
    # gated behind watching a demo of one specific tool.
    assert config["require_full_watch"] is False
    assert config["video_title"]
