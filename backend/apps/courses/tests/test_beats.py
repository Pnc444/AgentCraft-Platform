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
