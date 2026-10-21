from pathlib import Path

import pytest

from backend.career_matcher import CareerMatcher, build_profile_text
from backend.data_loader import load_careers


def test_dataset_has_valid_unique_records_and_parsed_lists():
    careers = load_careers()
    assert len(careers) >= 18
    assert len({career["career_id"] for career in careers}) == len(careers)
    assert isinstance(careers[0]["required_skills"], list)


def test_dataset_rejects_missing_columns(tmp_path: Path):
    source = tmp_path / "bad.csv"
    source.write_text("career_id,title\n1,Only two fields\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing required columns"):
        load_careers(source)


def test_dataset_deduplicates_and_handles_blank_list_fields(tmp_path: Path):
    from backend.data_loader import REQUIRED_COLUMNS

    columns = sorted(REQUIRED_COLUMNS)
    row = {column: "" for column in columns}
    row.update(career_id="same", title="Example", required_skills="Python; SQL")
    lines = [",".join(columns), ",".join(f'"{row[column]}"' for column in columns)]
    lines.append(",".join(f'"{row[column]}"' for column in columns))
    source = tmp_path / "duplicates.csv"
    source.write_text("\n".join(lines), encoding="utf-8")
    records = load_careers(source)
    assert len(records) == 1
    assert records[0]["required_skills"] == ["Python", "SQL"]
    assert records[0]["interests"] == []


def test_java_backend_profile_ranks_java_backend_and_detects_skills():
    matcher = CareerMatcher()
    matches = matcher.recommend(
        "I am a CSE student. I know Java, SQL, HTML, CSS and enjoy problem solving and backend development."
    )
    assert matches
    assert matches[0]["career_id"] == "java_backend_developer"
    assert "Java" in matches[0]["relevant_skills"]
    assert matches[0]["unconfirmed_skills"]
    assert "not a probability" in matches[0]["explanation"]


def test_empty_unknown_and_whitespace_inputs_do_not_recommend():
    matcher = CareerMatcher()
    assert matcher.recommend("") == []
    assert matcher.recommend("   ") == []
    assert matcher.recommend("florbish zentangle") == []


def test_zero_threshold_does_not_return_zero_similarity_profiles():
    matcher = CareerMatcher(relevance_threshold=0)
    matches = matcher.recommend("Java", relevance_threshold=0)
    assert matches
    assert all(match["similarity_score"] > 0 for match in matches)


def test_profile_fields_emphasize_explicit_skills_and_goals():
    combined = build_profile_text({"skills": ["Java"], "goals": "backend APIs"})
    assert combined.count("java") == 2
    assert "backend" in combined


def test_compare_returns_shared_and_distinct_skills():
    comparison = CareerMatcher().compare("data_analyst", "data_scientist")
    assert "SQL" in comparison["shared_skills"]
    assert comparison["first"]["title"] == "Data Analyst"
