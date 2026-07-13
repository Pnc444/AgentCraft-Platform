"""AgentCraft badge catalog + unlock evaluation."""

from __future__ import annotations

from apps.courses.models import Course, Lesson
from apps.learning.models import Badge, Progress, UserBadge

# Canonical definitions — seeded into the Badge table.
BADGE_CATALOG: list[dict] = [
    {
        "slug": "first-steps",
        "name": "First Steps",
        "description": "Complete your first lesson",
        "icon": "target",
        "criteria_type": Badge.Criteria.LESSONS_COMPLETED,
        "criteria_value": "1",
        "order": 1,
    },
    {
        "slug": "ai-initiate",
        "name": "AI Initiate",
        "description": "Finish Module 1: Introduction to AI",
        "icon": "lightbulb",
        "criteria_type": Badge.Criteria.COURSE_COMPLETED,
        "criteria_value": "module-1-introduction-to-ai",
        "order": 2,
    },
    {
        "slug": "token-tinkerer",
        "name": "Token Tinkerer",
        "description": "Finish Module 1.5: How LLMs Work",
        "icon": "hash",
        "criteria_type": Badge.Criteria.COURSE_COMPLETED,
        "criteria_value": "module-1-5-how-llms-work",
        "order": 3,
    },
    {
        "slug": "model-scout",
        "name": "Model Scout",
        "description": "Finish Module 2: Exploring LLM Models",
        "icon": "compass",
        "criteria_type": Badge.Criteria.COURSE_COMPLETED,
        "criteria_value": "module-2-exploring-llm-models",
        "order": 4,
    },
    {
        "slug": "prompt-crafter",
        "name": "Prompt Crafter",
        "description": "Finish Module 3: Prompting",
        "icon": "message-square",
        "criteria_type": Badge.Criteria.COURSE_COMPLETED,
        "criteria_value": "module-3-prompting",
        "order": 5,
    },
    {
        "slug": "agent-apprentice",
        "name": "Agent Apprentice",
        "description": "Finish Module 4: AI Agents",
        "icon": "bot",
        "criteria_type": Badge.Criteria.COURSE_COMPLETED,
        "criteria_value": "module-4-ai-agents",
        "order": 6,
    },
    {
        "slug": "docker-deckhand",
        "name": "Docker Deckhand",
        "description": "Finish Module 4.5: Docker and Environments",
        "icon": "container",
        "criteria_type": Badge.Criteria.COURSE_COMPLETED,
        "criteria_value": "module-4-5-docker-and-environments",
        "order": 7,
    },
    {
        "slug": "hermes-builder",
        "name": "Hermes Builder",
        "description": "Finish Module 5: Hermes (Build #1)",
        "icon": "rocket",
        "criteria_type": Badge.Criteria.COURSE_COMPLETED,
        "criteria_value": "module-5-hermes",
        "order": 8,
    },
    {
        "slug": "openclaw-operative",
        "name": "OpenClaw Operative",
        "description": "Finish Module 6: OpenClaw (Build #2)",
        "icon": "zap",
        "criteria_type": Badge.Criteria.COURSE_COMPLETED,
        "criteria_value": "module-6-openclaw",
        "order": 9,
    },
    {
        "slug": "claude-craftsman",
        "name": "Claude Craftsman",
        "description": "Finish Module 7: Claude (Build #3)",
        "icon": "sparkles",
        "criteria_type": Badge.Criteria.COURSE_COMPLETED,
        "criteria_value": "module-7-claude",
        "order": 10,
    },
    {
        "slug": "capstone-champion",
        "name": "Capstone Champion",
        "description": "Finish Module 8: Capstone — Safety & Evaluation",
        "icon": "trophy",
        "criteria_type": Badge.Criteria.COURSE_COMPLETED,
        "criteria_value": "module-8-capstone-safety-evaluation",
        "order": 11,
    },
    {
        "slug": "quiz-ace",
        "name": "Quiz Ace",
        "description": "Score 100% on any Recap Quiz",
        "icon": "star",
        "criteria_type": Badge.Criteria.PERFECT_QUIZ,
        "criteria_value": "",
        "order": 12,
    },
    {
        "slug": "path-graduate",
        "name": "Path Graduate",
        "description": "Complete every lesson on the Create an AI Agent path",
        "icon": "award",
        "criteria_type": Badge.Criteria.PATH_COMPLETE,
        "criteria_value": "",
        "order": 13,
    },
]


def seed_badges() -> int:
    """Upsert catalog badges into the database. Returns count of active badges."""
    for spec in BADGE_CATALOG:
        Badge.objects.update_or_create(
            slug=spec["slug"],
            defaults={
                "name": spec["name"],
                "description": spec["description"],
                "icon": spec["icon"],
                "criteria_type": spec["criteria_type"],
                "criteria_value": spec["criteria_value"],
                "order": spec["order"],
                "is_active": True,
            },
        )
    catalog_slugs = {spec["slug"] for spec in BADGE_CATALOG}
    Badge.objects.exclude(slug__in=catalog_slugs).update(is_active=False)
    return Badge.objects.filter(is_active=True).count()


def _course_fully_complete(user, course_slug: str) -> bool:
    try:
        course = Course.objects.get(slug=course_slug, is_published=True)
    except Course.DoesNotExist:
        return False
    total = course.lessons.count()
    if total == 0:
        return False
    done = Progress.objects.filter(
        user=user,
        lesson__course=course,
        status=Progress.Status.COMPLETED,
    ).count()
    return done >= total


def _user_meets_criteria(
    user,
    badge: Badge,
    *,
    lessons_completed: int,
    has_perfect_quiz: bool,
    path_complete: bool,
) -> bool:
    if badge.criteria_type == Badge.Criteria.LESSONS_COMPLETED:
        try:
            needed = int(badge.criteria_value or "0")
        except ValueError:
            needed = 0
        return lessons_completed >= needed
    if badge.criteria_type == Badge.Criteria.COURSE_COMPLETED:
        return bool(badge.criteria_value) and _course_fully_complete(user, badge.criteria_value)
    if badge.criteria_type == Badge.Criteria.PERFECT_QUIZ:
        return has_perfect_quiz
    if badge.criteria_type == Badge.Criteria.PATH_COMPLETE:
        return path_complete
    return False


def evaluate_badges_for_user(user) -> list[UserBadge]:
    """Unlock any badges the user newly qualifies for. Returns newly created awards."""
    completed = Progress.objects.filter(user=user, status=Progress.Status.COMPLETED)
    lessons_completed = completed.count()
    has_perfect_quiz = completed.filter(score__gte=100).exists()

    total_lessons = Lesson.objects.filter(course__is_published=True).count()
    path_complete = total_lessons > 0 and lessons_completed >= total_lessons

    newly_unlocked: list[UserBadge] = []
    has_equipped = UserBadge.objects.filter(user=user, equipped=True).exists()

    for badge in Badge.objects.filter(is_active=True).order_by("order"):
        if not _user_meets_criteria(
            user,
            badge,
            lessons_completed=lessons_completed,
            has_perfect_quiz=has_perfect_quiz,
            path_complete=path_complete,
        ):
            continue
        award, created = UserBadge.objects.get_or_create(user=user, badge=badge)
        if created:
            newly_unlocked.append(award)
            if not has_equipped:
                award.equipped = True
                award.save(update_fields=["equipped"])
                has_equipped = True

    return newly_unlocked


def badges_for_user(user) -> list[dict]:
    """Serialize all active badges with unlock/equip state for the API."""
    evaluate_badges_for_user(user)
    unlocked = {
        ub.badge_id: ub
        for ub in UserBadge.objects.filter(user=user).select_related("badge")
    }

    result = []
    for badge in Badge.objects.filter(is_active=True).order_by("order"):
        award = unlocked.get(badge.id)
        result.append(
            {
                "id": badge.slug,
                "name": badge.name,
                "description": badge.description,
                "icon": badge.icon,
                "unlocked": award is not None,
                "equipped": bool(award and award.equipped),
            }
        )
    return result
