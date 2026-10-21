from backend.data_loader import load_careers
from backend.roadmap_generator import generate_roadmap


def test_roadmap_has_flexible_stages_projects_and_milestones():
    career = next(item for item in load_careers() if item["career_id"] == "data_analyst")
    roadmap = generate_roadmap(career, known_skills=["SQL"])
    assert [item["stage"] for item in roadmap] == [
        "1. Fundamentals", "2. Core skills", "3. Practical projects", "4. Portfolio preparation"
    ]
    assert roadmap[2]["focus"]
    assert all(item["milestone"] for item in roadmap)
    assert all("day" not in item["milestone"].lower() for item in roadmap)


def test_roadmap_handles_missing_optional_fields():
    assert len(generate_roadmap({"title": "Unknown"}, [])) == 4
