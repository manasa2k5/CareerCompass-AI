"""Load and validate the local career knowledge base."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "careers.csv"
REQUIRED_COLUMNS = {
    "career_id",
    "title",
    "category",
    "description",
    "required_skills",
    "related_skills",
    "interests",
    "typical_tasks",
    "learning_topics",
    "project_ideas",
    "entry_level_guidance",
}
LIST_FIELDS = (
    "required_skills",
    "related_skills",
    "interests",
    "typical_tasks",
    "learning_topics",
    "project_ideas",
)


def _parse_list(value: Any) -> list[str]:
    if value is None or pd.isna(value):
        return []
    return [part.strip() for part in str(value).split(";") if part.strip()]


def load_careers(path: str | Path | None = None) -> list[dict[str, Any]]:
    """Load career rows, validating schema and normalizing list-like fields."""
    source = Path(path) if path is not None else DATA_PATH
    try:
        frame = pd.read_csv(source, dtype=str, keep_default_na=False)
    except (OSError, pd.errors.ParserError, UnicodeError) as exc:
        raise ValueError(f"Could not load career dataset at {source}: {exc}") from exc

    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Career dataset is missing required columns: {', '.join(sorted(missing))}")

    frame = frame.fillna("")
    frame["career_id"] = frame["career_id"].str.strip()
    frame = frame[frame["career_id"] != ""].drop_duplicates(subset=["career_id"], keep="first")
    if frame.empty:
        raise ValueError("Career dataset contains no usable career records.")

    records: list[dict[str, Any]] = []
    for row in frame.to_dict(orient="records"):
        career: dict[str, Any] = {key: str(value).strip() for key, value in row.items()}
        for field in LIST_FIELDS:
            career[field] = _parse_list(career.get(field))
        records.append(career)
    return records
