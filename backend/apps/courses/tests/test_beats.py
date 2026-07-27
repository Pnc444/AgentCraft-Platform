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


def test_a_beats_body_never_leads_with_its_own_title():
    """The player renders beat.title as a header inside the content column, so
    a body that opens with the same heading shows the same words twice, ~40px
    apart. The fallback briefly echoed the heading (for the pre-redesign
    chrome, where the title read as navigation); the echo must stay gone."""
    md = "Intro.\n\n## Why the split matters\n\n" + ("x" * 600) + "\n\n## Another idea\n\n" + ("y" * 600)
    beats = beats_from_markdown(md, title="T")
    for beat in beats:
        title = (beat.get("title") or "").strip()
        body = (beat.get("body") or "").lstrip()
        assert not (title and body.startswith(f"## {title}")), (
            f"beat {beat['title']!r} opens by repeating its own title"
        )


def test_a_merged_section_heading_appears_exactly_once():
    """Absorbed sections keep their heading inside the merged body — that is
    mid-body structure, not a duplicate of the card title — and only once."""
    beats = beats_from_markdown(MD, title="Your First Containers")
    assert len(beats) == 1
    assert beats[0]["body"].count("## 1. Hello, world") == 1
    assert beats[0]["body"].count("## 2. A real web server") == 1
    # the merged card is titled after the first section, not the absorbed ones
    assert beats[0]["title"] == "Your First Containers"


TAKEAWAY_MD = """# Why Docker?

## The problem Docker solves

""" + ("x" * 600) + """

## Takeaway

Docker gives every agent a clean, disposable, identical environment. Modules 5 and 6 run their agents inside Docker, so we set it up now.
"""


def test_trailing_takeaway_becomes_a_recap_beat():
    """23 lessons close with '## Takeaway'. It was rendering as a two-sentence
    explain card — or being merged into the wall of prose it summarises."""
    beats = beats_from_markdown(TAKEAWAY_MD, title="Why Docker?")
    assert [b["type"] for b in beats] == ["explain", "recap"]
    assert beats[-1]["bullets"] == [
        "Docker gives every agent a clean, disposable, identical environment.",
        "Modules 5 and 6 run their agents inside Docker, so we set it up now.",
    ]
    # the inline heading the fallback keeps is chrome, not a bullet
    assert not any(b.startswith("#") or b == "Takeaway" for b in beats[-1]["bullets"])
    # the summary is not also left sitting in the prose beat
    assert "disposable" not in beats[0]["body"]


def test_recap_bullets_drop_markdown_emphasis_but_keep_the_words():
    """Recap bullets render as plain text, so '**System**' would show its own
    asterisks."""
    md = "Intro.\n\n## A\n\n" + ("x" * 600) + "\n\n## Takeaway\n\n**System** = behaviour. Use `docker --version` to check."
    beats = beats_from_markdown(md, title="T")
    bullets = beats[-1]["bullets"]
    assert bullets == ["System = behaviour.", "Use docker --version to check."]
    assert not any("*" in b or "`" in b for b in bullets)


def test_recap_uses_existing_list_items_when_the_section_has_them():
    md = "Intro.\n\n## A\n\n" + ("x" * 600) + "\n\n## Takeaway\n\n- First thing.\n- Second thing.\n"
    beats = beats_from_markdown(md, title="T")
    assert beats[-1]["bullets"] == ["First thing.", "Second thing."]


def test_a_long_takeaway_folds_its_tail_rather_than_dropping_it():
    """Capping at three bullets must not silently lose the fourth sentence."""
    md = "Intro.\n\n## A\n\n" + ("x" * 600) + "\n\n## Takeaway\n\nOne. Two. Three. Four. Five."
    beats = beats_from_markdown(md, title="T")
    bullets = beats[-1]["bullets"]
    assert len(bullets) == 3
    assert bullets[-1] == "Three. Four. Five."


def test_a_lesson_that_is_only_a_takeaway_keeps_its_content():
    """Retyping the sole section would leave a lesson with no reading at all."""
    beats = beats_from_markdown("## Takeaway\n\nThat's all.", title="T")
    assert [b["type"] for b in beats] == ["explain"]


def test_a_seam_check_still_lands_in_front_of_the_recap():
    """The authored question that used to sit before the Takeaway must not be
    retired just because the Takeaway changed type."""
    seam = [{"prompt": "Which?", "options": ["a", "b"], "answer_index": 0}]
    beats = beats_from_markdown(TAKEAWAY_MD, title="Why Docker?", seam_checks=seam)
    assert [b["type"] for b in beats] == ["explain", "check", "recap"]


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


def test_explicit_video_position_counts_learner_visible_beats():
    """video_position is 1-based over the FINAL sequence, so it matches the
    numbers the player shows. Insertion happens after merging and check
    distribution for exactly that reason."""
    md = "Intro.\n\n## A\n\n" + ("x" * 700) + "\n\n## B\n\n" + ("y" * 700)
    seams = [{"prompt": "q?", "options": ["a", "b"], "answer_index": 0}]
    beats = beats_from_markdown(
        md, title="T", video_url="https://v/x", seam_checks=seams, video_position=3
    )
    kinds = [b.get("action") or b["type"] for b in beats]
    assert kinds == ["explain", "check", "video", "explain"]
    assert beats[2]["action"] == "video"


def test_every_module_1_5_lesson_has_a_video():
    """The module is now uniformly video-supported; a lesson quietly losing its
    video should fail here rather than being noticed in a screenshot."""
    from apps.courses.curriculum import CURRICULUM

    module = next(m for m in CURRICULUM if m["slug"] == "module-1-5-how-llms-work")
    teaching = [l for l in module["lessons"] if l[2] != "quiz"]
    assert len(teaching) == 3
    for lesson in teaching:
        assert lesson[4].get("video_url"), f"{lesson[1]} lost its video"


def test_module_1_5_videos_share_one_position_and_stay_ungated():
    from apps.courses.curriculum import (
        CURRICULUM,
        MODULE_1_5_CONTEXT_VIDEO_URL,
        MODULE_1_5_TOKENS_VIDEO_URL,
        MODULE_1_5_TRAINING_VIDEO_URL,
        MODULE_1_5_VIDEO_POSITION,
    )

    module = next(m for m in CURRICULUM if m["slug"] == "module-1-5-how-llms-work")
    expected = {
        "context-windows": (MODULE_1_5_CONTEXT_VIDEO_URL, "Context management in Claude Code"),
        "tokens": (MODULE_1_5_TOKENS_VIDEO_URL, "What is an AI Token?"),
        "training-vs-inference": (
            MODULE_1_5_TRAINING_VIDEO_URL,
            "AI Training vs Inference Explained",
        ),
    }
    for slug, (url, video_title) in expected.items():
        config = next(l for l in module["lessons"] if l[1] == slug)[4]
        assert config["video_url"] == url
        # Every video names what it shows — "Watch the video" is only a fallback.
        assert config["video_title"] == video_title
        assert "?si=" not in config["video_url"], f"{slug}: share param must not be stored"
        # Both videos illustrate prose that already teaches the concept, so
        # neither gates the recap quiz.
        assert config["require_full_watch"] is False
        # Same place in both lessons, so the module reads consistently.
        assert config["video_position"] == MODULE_1_5_VIDEO_POSITION


def test_module_3_opening_lesson_video_sits_before_its_quick_check():
    """The request was "before the quick check", which in this lesson is beat 2 —
    a different index from Module 1.5's beat 3 because the seam check falls
    earlier here. video_position counts learner-visible beats, so the number
    means the same thing in both places."""
    from apps.courses.beats import derive_beats
    from apps.courses.curriculum import (
        MODULE_3_PROMPTS_VIDEO_URL,
        MODULE_3_RECAP,
        MODULE_3_SEAM_CHECKS,
        CURRICULUM,
        load_content,
    )

    module = next(m for m in CURRICULUM if m["slug"] == "module-3-prompting")
    config = next(l for l in module["lessons"] if l[1] == "what-prompts-are")[4]
    assert config["video_url"] == MODULE_3_PROMPTS_VIDEO_URL
    assert "?si=" not in config["video_url"]
    assert config["require_full_watch"] is False

    beats = derive_beats(
        content=load_content("module-3-prompting", "what-prompts-are", "What Prompts Are"),
        sandbox_config={
            "questions": MODULE_3_RECAP["what-prompts-are"],
            "checkpoint_questions": MODULE_3_SEAM_CHECKS["what-prompts-are"],
            "video_position": config["video_position"],
        },
        # video_url is its own parameter: sync_content pops it out of the spec
        # config and the serializer reads it off the model column.
        video_url=config["video_url"],
        title="What Prompts Are",
        require_full_watch=False,
    )
    kinds = [b.get("action") or b["type"] for b in beats]
    assert kinds[1] == "video", f"video must be beat 2, got {kinds}"
    assert kinds[2] == "check", "the quick check must follow the video"
