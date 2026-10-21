"""Generate adaptable, career-specific learning stages and project ideas."""

from __future__ import annotations

from typing import Any


def generate_roadmap(career: dict[str, Any], known_skills: list[str] | None = None) -> list[dict[str, Any]]:
    """Create learning stages without promising a fixed completion timeline."""
    known = {skill.lower() for skill in (known_skills or [])}
    required = career.get("required_skills", [])
    topics = career.get("learning_topics", [])
    projects = career.get("project_ideas", [])
    remaining_skills = [skill for skill in required if skill.lower() not in known]
    fundamentals = topics[:2] or required[:2]
    core = topics[2:] or remaining_skills or required
    return [
        {
            "stage": "1. Fundamentals",
            "focus": fundamentals,
            "milestone": "Explain the core concepts and complete small guided exercises.",
        },
        {
            "stage": "2. Core skills",
            "focus": core,
            "milestone": "Use the role's tools and concepts in independent practice tasks.",
        },
        {
            "stage": "3. Practical projects",
            "focus": projects[:2],
            "milestone": "Build, test, and document at least one project that solves a clear problem.",
        },
        {
            "stage": "4. Portfolio preparation",
            "focus": ["Refine project documentation", "Review fundamentals", "Seek feedback"],
            "milestone": "Present your decisions, trade-offs, and learning clearly; adapt the pace to your background.",
        },
    ]
